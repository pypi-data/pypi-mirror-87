from typing import List, Dict

import numpy as np
import tensorflow as tf
from transformers import DistilBertTokenizerFast
from sklearn.preprocessing import LabelEncoder


class Tag:
    def __init__(self, tag_type: str, start: int, end: int, start_tok: int, end_tok: int):
        self.tag_type = tag_type
        self.start = start
        self.end = end
        self.start_tok = start_tok
        self.end_tok = end_tok


class Example:
    def __init__(self,
                 text: str,
                 intent: str,
                 tokens: List[str],
                 tags: List[Tag],
                 word_start_mask: List[int],
                 tokenizer: DistilBertTokenizerFast):
        self.text = text.lower()
        self.intent = intent
        self.tokens = tokens
        self.tags = tags
        self.word_start_mask = word_start_mask
        self.token_tags: List[str] = ['O'] * len(tokens)

        for tag in self.tags:
            for i in range(tag.start_tok, tag.end_tok + 1):
                if i == tag.start_tok:
                    self.token_tags[i] = f'B-{tag.tag_type}'
                else:
                    self.token_tags[i] = f'I-{tag.tag_type}'

        self.tokens = ['[CLS]', *self.tokens, '[SEP]']
        self.token_tags = ['[CLS]', *self.token_tags, '[SEP]']
        self.word_start_mask = [0, *self.word_start_mask, 0]

        self.input_ids = tokenizer.convert_tokens_to_ids(self.tokens)
        self.input_mask = [1] * len(self.tokens)

    def to_tensors(self,
                   max_seq_len: int,
                   tag_encoder: LabelEncoder,
                   intent_encoder: LabelEncoder) -> Dict[str, tf.Tensor]:
        n_tags = len(tag_encoder.classes_)
        n_intents = len(intent_encoder.classes_)

        input_ids = self.input_ids.copy()
        input_mask = self.input_mask.copy()
        word_start_mask = self.word_start_mask.copy()
        token_tags = self.token_tags.copy()
        intent = intent_encoder.transform([self.intent])

        assert len(input_ids) == len(input_mask) == len(token_tags) == len(word_start_mask)

        while len(input_ids) < max_seq_len:
            input_ids.append(0)
            input_mask.append(0)
            word_start_mask.append(0)
            token_tags.append('O')

        token_tags = tag_encoder.transform(token_tags).astype(np.int32)

        tensors = {
            "input_ids": tf.convert_to_tensor(input_ids),
            "input_mask": tf.convert_to_tensor(input_mask),
            "word_start_mask": tf.convert_to_tensor(word_start_mask),
            "intent": tf.squeeze(tf.one_hot(intent, n_intents)),
            "tags": tf.squeeze(tf.one_hot(token_tags, n_tags))
        }

        return tensors
