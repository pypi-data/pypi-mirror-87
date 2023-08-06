import typing as t
from itertools import chain
from collections import defaultdict, Counter

from sklearn.model_selection import train_test_split

from transformers import DistilBertTokenizerFast
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
import tensorflow as tf

from bavard.nlu.utils import (
    get_char_to_word_map,
    concat_tensor_dicts,
)
from bavard.common.utils import make_stratified_folds
from bavard.nlu.data_preprocessing.training_example import Example, Tag
from bavard.nlu import constants


class NLUDataPreprocessor:
    """
    Data preprocessing model that fits label encoders to the targets of an agent's
    NLU data and processes the raw NLU data into a tensorflow.data.Dataset instance
    ready for training.
    """

    lm_name = constants.BASE_LANGUAGE_MODEL

    def __init__(self, *, max_seq_len: int) -> None:
        self._fitted = False
        self.max_seq_len = max_seq_len

    def fit(self, nlu_data: dict) -> None:
        intents = nlu_data["intents"]
        tag_types = nlu_data["tagTypes"]

        # intents encoder
        self.intents_encoder = LabelEncoder()
        self.intents_encoder.fit(sorted(intents))

        # tags encoder
        tag_set = {"[CLS]", "[SEP]", "O"}
        for tag_type in sorted(tag_types):
            tag_set.add(f"B-{tag_type}")
            tag_set.add(f"I-{tag_type}")
        self.tag_encoder = LabelEncoder()
        self.tag_encoder.fit(list(tag_set))

        # tag and intent sizes
        self.n_tags = len(tag_set)
        self.n_intents = len(intents)

        # tokenizer
        self.tokenizer = DistilBertTokenizerFast.from_pretrained(self.lm_name)
        self._fitted = True

    def transform(self, nlu_data: dict) -> tf.data.Dataset:
        """
        Transform a whole training dataset of utterances and labels.
        """
        assert self._fitted
        examples = self._process_nlu_data(nlu_data)
        return self._examples_to_dataset(examples)

    def transform_utterance(self, utterance: str) -> dict:
        """
        Transform a single utterance with no labels.
        """
        tokens, word_start_mask, word_to_token_map = self._preprocess_text(utterance)

        tokens = ["[CLS]", *tokens, "[SEP]"]
        input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        input_mask = [1] * len(tokens)
        word_start_mask = [0, *word_start_mask, 0]

        while len(input_ids) < self.max_seq_len:
            input_ids.append(0)
            input_mask.append(0)
            word_start_mask.append(0)

        return {
            "input_ids": tf.convert_to_tensor([input_ids]),
            "input_mask": tf.convert_to_tensor([input_mask]),
            "word_start_mask": tf.convert_to_tensor([word_start_mask]),
        }

    def transform_utterances(self, utterances: t.List[str]) -> dict:
        """
        Transform a batch of utterances with no labels.
        """
        tensor_dicts = [self.transform_utterance(u) for u in utterances]
        return concat_tensor_dicts(tensor_dicts)

    def _process_nlu_data(self, nlu_data: dict) -> t.List[Example]:
        result_examples: t.List[Example] = []

        examples = nlu_data["examples"]

        for ex in examples:
            text = ex["text"]
            intent = ex["intent"]
            raw_tags = ex["tags"]

            (
                text_tokens,
                word_start_mask,
                word_to_token_map,
            ) = self._preprocess_text(text)

            char_to_word_map = get_char_to_word_map(text)

            result_tags: t.List[Tag] = []
            for tag in raw_tags:
                start = tag["start"]
                end = tag["end"]
                tag_type = tag["tagType"]

                start_word_idx = char_to_word_map[start]
                end_word_idx = char_to_word_map[end - 1]

                start_tok = word_to_token_map[start_word_idx]
                end_tok = word_to_token_map[end_word_idx]
                result_tags.append(
                    Tag(
                        tag_type=tag_type,
                        start=start,
                        end=end,
                        start_tok=start_tok,
                        end_tok=end_tok,
                    )
                )

            result_examples.append(
                Example(
                    text=text,
                    intent=intent,
                    tokens=text_tokens,
                    tags=result_tags,
                    word_start_mask=word_start_mask,
                    tokenizer=self.tokenizer,
                )
            )

        return result_examples

    def _preprocess_text(self, text: str):
        text = text.lower()
        text_words = text.split()
        text_tokens = []
        token_to_word_idx = []
        word_to_token_map = []
        word_start_mask = []
        for (wi, word) in enumerate(text_words):
            word_to_token_map.append(len(text_tokens))
            word_tokens = self.tokenizer.tokenize(word)
            for ti, token in enumerate(word_tokens):
                token_to_word_idx.append(wi)
                text_tokens.append(token)

                if ti == 0:
                    word_start_mask.append(1)
                else:
                    word_start_mask.append(0)

        return text_tokens, word_start_mask, word_to_token_map

    def _examples_to_dataset(self, examples: t.List[Example]) -> tf.data.Dataset:
        """
        Converts this instance's examples into a tensor dataset.
        """
        # Unpack each example's dictionary of tensors into a single dictionary
        # containing lists of tensors.
        data = defaultdict(list)
        tensor_dicts = [
            example.to_tensors(self.max_seq_len, self.tag_encoder, self.intents_encoder)
            for example in examples
        ]
        data = concat_tensor_dicts(tensor_dicts, new_axis=True)

        # Next, split them into X and Y.
        X = {k: data[k] for k in ["input_ids", "input_mask", "word_start_mask"]}
        Y = {k: data[k] for k in ["intent", "tags"]}

        return tf.data.Dataset.from_tensor_slices((X, Y))


class NLUDataUtils:
    """
    Utilities for interacting with an agent's NLU data.
    """

    @staticmethod
    def split(
        nlu_data: dict, split_ratio: float, shuffle: bool = True, seed: int = 0
    ) -> tuple:
        """
        Splits `nlu_data` into two different training sets, stratified by their intent labels.
        """
        examples = nlu_data["examples"]
        intent_labels = [ex["intent"] for ex in examples]
        examples_a, examples_b = train_test_split(
            examples,
            test_size=split_ratio,
            random_state=seed,
            shuffle=shuffle,
            stratify=intent_labels,
        )
        return (
            NLUDataUtils.build_from_examples(examples_a),
            NLUDataUtils.build_from_examples(examples_b),
        )

    @staticmethod
    def to_folds(
        nlu_data: dict, nfolds: int, shuffle: bool = True, seed: int = 0
    ) -> tuple:
        """
        Splits `nlu_data` into `nfolds` random subsets, stratified by intent label.
        """
        examples = nlu_data["examples"]
        intent_labels = [ex["intent"] for ex in examples]
        folds = make_stratified_folds(examples, intent_labels, nfolds, shuffle, seed)
        return tuple(NLUDataUtils.build_from_examples(examples) for examples in folds)

    @staticmethod
    def build_from_examples(examples: list) -> dict:
        """
        Builds an `nluData` object from examples.
        """
        return {
            "examples": examples,
            "intents": NLUDataUtils.get_intents(examples),
            "tagTypes": NLUDataUtils.get_tag_types(examples),
        }

    @staticmethod
    def get_intents(examples: list) -> list:
        return list(set(ex["intent"] for ex in examples))

    @staticmethod
    def get_tag_types(examples: list) -> list:
        return list(set(tag["tagType"] for ex in examples for tag in ex["tags"]))

    @staticmethod
    def concat(*nlu_datas: tuple) -> dict:
        """
        Takes the concatenation of multiple nluData objects, returning a single nluData
        object with all the examples from `nlu_datas`.
        """
        examples = list(
            chain.from_iterable(nlu_data["examples"] for nlu_data in nlu_datas)
        )
        return {
            "examples": examples,
            "intents": NLUDataUtils.get_intents(examples),
            "tagTypes": NLUDataUtils.get_tag_types(examples),
        }

    @staticmethod
    def balance_by_intent(nlu_data: dict, seed: int = 0) -> dict:
        """
        Makes a new version of `nlu_data`, where the minority classes
        are upsampled to have the same number examples as the majority class.
        """
        examples_by_intent = defaultdict(list)
        for ex in nlu_data["examples"]:
            examples_by_intent[ex["intent"]].append(ex)
        n_majority_intent = max(len(examples) for examples in examples_by_intent.values())
        upsampled = list(
            chain.from_iterable(
                resample(examples, replace=True, n_samples=n_majority_intent, random_state=seed)
                for examples in examples_by_intent.values()
            )
        )
        return NLUDataUtils.build_from_examples(upsampled)

    @staticmethod
    def get_intent_distribution(nlu_data: dict) -> Counter:
        """
        Counts the number of each type of intent present in `nlu_data`.
        The returned `Counter` object can be treated as a dictionary e.g.
        `my_intent_count = counter["my_intent"]`.
        """
        return Counter([ex["intent"] for ex in nlu_data["examples"]])
