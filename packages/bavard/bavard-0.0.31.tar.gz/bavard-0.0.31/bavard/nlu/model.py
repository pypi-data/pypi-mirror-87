import logging
from datetime import datetime
import typing as t
from time import time

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, TimeDistributed, Dropout, Lambda, BatchNormalization, Activation, LSTM
from tensorflow.keras import regularizers, Model
from transformers import TFDistilBertModel
import tensorflow_probability as tfp
import uncertainty_metrics.tensorflow as um

from bavard.mlops.web_service import WebService, endpoint
from bavard.common.serialization import Persistent
from bavard.nlu.data_preprocessing.nlu_data import NLUDataPreprocessor, NLUDataUtils
from bavard.common.utils import leave_one_out, aggregate_dicts
from bavard.nlu.auto_setup import AutoSetup
from bavard.nlu import constants

logging.getLogger().setLevel(logging.DEBUG)


class NLUModel(WebService, Persistent):

    # Always predict on larger batches, for efficiency's sake,
    # since it doesn't affect the model's optimization.
    batch_size_predict = 64
    embedder_name = constants.BASE_LANGUAGE_MODEL
    hpnames = [
        "hidden_size",
        "dropout",
        "l2_regularization",
        "n_hidden_layers",
        "fine_tune_embedder",
        "learning_rate",
        "batch_size",
        "epochs",
        "intent_block_type",
        "balance_intent"
    ]

    def __init__(
        self,
        *,
        save_model_dir: t.Optional[str] = None,
        verbose: bool = False,
        max_seq_len: int = 120,
        auto: bool = False,
        hidden_size: int = 308,
        dropout: float = 0.0,
        l2_regularization: float = 1.899928623655182e-09,
        n_hidden_layers: int = 1,
        fine_tune_embedder: bool = False,
        learning_rate: float = 0.0015041607064607066,
        batch_size: int = 4,
        epochs: int = 60,
        intent_block_type: str = "dense",
        balance_intent: bool = False
    ):
        # Control parameters
        self.auto = auto
        self.save_model_dir = save_model_dir
        self.verbose = verbose
        self.max_seq_len = max_seq_len
        self._fitted = False

        # Hyperparameters
        self.hidden_size = hidden_size
        self.dropout = dropout
        self.l2_regularization = l2_regularization
        self.n_hidden_layers = n_hidden_layers
        self.fine_tune_embedder = fine_tune_embedder
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epochs = epochs
        self.intent_block_type = intent_block_type
        self.balance_intent = balance_intent

    @staticmethod
    def get_embedder(*, trainable: bool = False) -> tf.keras.Model:
        # TODO: Shouldn't have to access the underlying `.distilbert` layer once
        # https://github.com/huggingface/transformers/issues/3627 is resolved.
        embedder = TFDistilBertModel.from_pretrained(NLUModel.embedder_name).distilbert
        embedder.trainable = trainable
        return embedder

    def get_params(self) -> dict:
        """
        Get a copy of the model's hyperparameters as a dictionary.
        """
        return {name: getattr(self, name) for name in self.hpnames}

    def set_params(self, **params) -> None:
        """
        Sets the hyperparameters found in `**params`.
        """
        for name, value in params.items():
            if name in self.hpnames:
                setattr(self, name, value)
            else:
                raise ValueError(f"{name} is not a known hyperparameter")

    def add_model_block(
        self,
        block_input: tf.Tensor,
        *,
        block_type: str,
        is_time_distributed: bool,
        **layer_args
    ) -> tf.Tensor:
        """
        Uses the Keras functional API to add a neural network block
        to a Keras model. A block is a collection of `keras.layers.Layer`
        objects that together act like a single logical layer in a NN.

        Parameters
        ----------
        block_input : tensor
            A reference to the tensor the NN block should accept as input.

        Returns
        -------
        out : tensor
            A reference to the tensor returned by the NN block; the output
            of the block.
        """
        class_map = {"dense": Dense, "lstm": LSTM}
        assert block_type in class_map
        needs_activation = block_type == "dense"

        out = Dropout(rate=self.dropout)(block_input)

        layer = class_map[block_type](
            self.hidden_size,
            kernel_regularizer=regularizers.l2(self.l2_regularization),
            **layer_args
        )

        if is_time_distributed:
            out = TimeDistributed(layer)(out)
        else:
            out = layer(out)

        out = BatchNormalization()(out)
        if needs_activation:
            out = Activation("relu")(out)

        return out

    def _build_and_compile_model(self) -> None:
        embedder = self.get_embedder(trainable=self.fine_tune_embedder)

        in_id = Input(shape=(self.max_seq_len,), name='input_ids', dtype=tf.int32)
        in_mask = Input(shape=(self.max_seq_len,), name='input_mask', dtype=tf.int32)
        word_start_mask = Input(shape=(self.max_seq_len,), name='word_start_mask', dtype=tf.float32)
        embedder_inputs = [in_id, in_mask]
        all_inputs = [in_id, in_mask, word_start_mask]

        # The output of the pretrained base model.
        token_embeddings = embedder(embedder_inputs)[0]
        pooled_embedding = token_embeddings[:, 0]

        # A network for intent classification.

        if self.intent_block_type == "lstm":
            intent_out = token_embeddings
        else:
            intent_out = pooled_embedding

        for i in range(self.n_hidden_layers):
            if i < self.n_hidden_layers - 1 and self.intent_block_type == "lstm":
                layer_args = {"return_sequences": True}
            else:
                layer_args = {}
            intent_out = self.add_model_block(
                intent_out, block_type=self.intent_block_type, is_time_distributed=False, **layer_args
            )
        intent_out = Dense(self.preprocessor.n_intents, activation='sigmoid', name='intent')(intent_out)

        # Another network for NER.

        tags_out = token_embeddings
        for _ in range(self.n_hidden_layers):
            tags_out = self.add_model_block(
                tags_out, block_type="dense", is_time_distributed=True
            )

        tags_out = TimeDistributed(Dense(self.preprocessor.n_tags, activation='sigmoid'))(tags_out)
        tags_out = Lambda(lambda x: x, name='tags')(tags_out)
        # tags_out = Multiply(name='tagger')([tags_out, word_start_mask])

        self.model = Model(inputs=all_inputs, outputs=[intent_out, tags_out])
        self._compile_model()

    def _compile_model(self):
        optimizer = tf.keras.optimizers.Adam(self.learning_rate)
        losses = {
            'tags': 'binary_crossentropy',
            'intent': 'binary_crossentropy'
        }
        loss_weights = {'tags': 3.0, 'intent': 1.0}
        metrics = {'intent': 'acc', 'tags': 'acc'}
        self.model.compile(optimizer=optimizer, loss=losses, loss_weights=loss_weights, metrics=metrics)
        if self.verbose:
            self.model.summary()

    def get_tags_output_mask(self, word_start_mask):
        word_start_mask = np.expand_dims(word_start_mask, axis=2)  # n x seq_len x 1
        tags_output_mask = np.tile(word_start_mask, (1, 1, self.n_tags))  # n x seq_len x n_tags
        return tags_output_mask

    def train(self, nlu_data: dict) -> float:
        """Processes the agent's NLU data into training data, and trains the model.
        """
        start = time()

        if self.balance_intent:
            nlu_data = NLUDataUtils.balance_by_intent(nlu_data)
        self.preprocessor = NLUDataPreprocessor(max_seq_len=self.max_seq_len)
        self.preprocessor.fit(nlu_data)
        dataset = self.preprocessor.transform(nlu_data)

        train_data, val_data, hparams, callbacks = AutoSetup.get_training_setup(self.auto, dataset, self.get_params())
        self.set_params(**hparams)

        self._fit_tf_model(train_data, val_data, callbacks)

        self._fitted = True

        if self.save_model_dir is not None:
            # Save the model's state, so it can be deployed and used.
            self.to_dir(self.save_model_dir)

        train_time = time() - start
        if self.verbose:
            print(f"Total train time: {train_time:.6f} seconds.")

        return train_time

    def _fit_tf_model(
        self,
        train_data: tf.data.Dataset,
        val_data: tf.data.Dataset = None,
        callbacks: list = None,
        tensorboard: bool = True
    ) -> None:
        """
        Fits the model on `train_data`, using optional `val_data` for validation.
        `train_data` and `val_data` should be passed in unbatched.
        """
        if self.verbose:
            print("Fitting model using hyperparameters:")
            print(self.get_params())

        self._build_and_compile_model()

        if callbacks is None:
            callbacks = []

        if val_data:
            val_data = val_data.batch(self.batch_size)

        if tensorboard:
            logdir = "logs/" + datetime.now().strftime("%Y%m%d-%H%M%S")
            callbacks.append(tf.keras.callbacks.TensorBoard(log_dir=logdir))

        n_train = sum(1 for _ in train_data)

        self.model.fit(
            train_data.batch(self.batch_size),
            epochs=self.epochs,
            steps_per_epoch=AutoSetup.get_steps_per_epoch(n_train, self.batch_size),
            validation_data=val_data,
            use_multiprocessing=True,
            callbacks=callbacks
        )

    def evaluate(
        self,
        nlu_data: dict,
        *,
        test_ratio: float = None,
        nfolds: int = None,
        repeat: int = 0,
        do_error_analysis: bool = False
    ) -> tuple:
        """
        Performs cross validation to evaluate the model's training set performance
        and generalizable performance on `nlu_data`.

        Parameters
        ----------
        nlu_data : dict
            An agent's NLU data to train and evaluate on.
        test_ratio : float
            If provided, a basic stratified train/test split will be used.
        nfolds : int
            If provided, stratified k-fold cross validation will be conducted with `k==nfolds`.
        repeat : int
            If > 0, the evaluation will be performed `repeat` times and results will be
            averaged. This is useful when you want to average out the variance caused by
            random weight initialization, etc.
        do_error_analysis : bool
            Possible only when doing k-fold CV with no repeats. Performs on error analysis on
            all the hold-out folds.

        Returns
        -------
        training_performance : dict
            The metrics from evaluating the fitted model on the training set.
        test_performance : dict
            The metrics from evaluating the fitted model on the test set.
        """
        if test_ratio is not None and nfolds is not None:
            raise ValueError("please supply either test_ratio or nfolds, but not both")
        if do_error_analysis and repeat > 0:
            raise ValueError("an error analysis can only be done when there are no repeats")
        if do_error_analysis and nfolds is None:
            raise ValueError("an error analysis can only be done with k-fold CV")

        if test_ratio is not None:
            eval_fn = lambda: self._evaluate_train_test(nlu_data, test_ratio)
        elif nfolds is not None:
            eval_fn = lambda: self._evaluate_kfold_cv(nlu_data, nfolds, do_error_analysis)
        else:
            raise ValueError("please supply either test_ratio or nfolds")

        if repeat > 0:
            results = [eval_fn() for _ in range(repeat)]
            return tuple(aggregate_dicts(dicts, "mean") for dicts in zip(*results))
        else:
            return eval_fn()

    def error_analysis(self, nlu_data: dict) -> list:
        """Predicts on `nlu_data`, then determines which misclassifications were made.

        Parameters
        ----------
        nlu_data : dict
            The agent's NLU data to predict on.

        Returns
        -------
        list
            A list of instance error analyses. Each entry contains data about
            what the ground truth was, what the predictions were, and whether the
            model got the predictions correct or not.
        """
        preds = self.predict([instance["text"] for instance in nlu_data["examples"]])
        return [
            {
                "prediction": pred,
                "instance": instance,
                "correct": {
                    "intent": pred["intent"]["value"] == instance["intent"],
                    # @TODO: This tags comparison will need to be more granular
                    # once we care more about tags.
                    "tags": set(
                        tag["tagType"] for tag in pred["tags"]
                    ) == set(
                        tag["tagType"] for tag in instance["tags"]
                    )
                }
            } for pred, instance in zip(preds["predictions"], nlu_data["examples"])
        ]

    def _evaluate_train_test(self, nlu_data: dict, test_ratio: float) -> tuple:
        # Evaluate the model on a basic train/test split.
        train_nlu_data, test_nlu_data = NLUDataUtils.split(nlu_data, test_ratio)
        return self._evaluate(train_nlu_data, test_nlu_data)

    def _evaluate_kfold_cv(self, nlu_data: dict, nfolds: int, do_error_analysis: bool = False) -> tuple:
        # Evaluate the model using k-fold cross validation.
        folds = NLUDataUtils.to_folds(nlu_data, nfolds)
        results = []
        error_analysis = []
        for test_fold, train_folds in leave_one_out(folds):
            train_nlu_data = NLUDataUtils.concat(*train_folds)
            results.append(self._evaluate(train_nlu_data, test_fold))
            if do_error_analysis:
                error_analysis += self.error_analysis(test_fold)

        # Now average the k performance results.
        train_performance, test_performance = tuple(aggregate_dicts(dicts, "mean") for dicts in zip(*results))
        if do_error_analysis:
            test_performance["error_analysis"] = error_analysis

        return train_performance, test_performance

    def _evaluate(self, train_nlu_data: dict, test_nlu_data: dict) -> tuple:
        train_time = self.train(train_nlu_data)

        train_performance = self.score(train_nlu_data)
        train_performance["train_time"] = train_time

        test_performance = self.score(test_nlu_data)

        # Get ECE
        ece_quantiles = self.bayesian_ece_for_obj(
            test_nlu_data,
            "intent",
            quantiles=[10, 50, 90],
            is_sparse=False
        )
        for quantile, value in ece_quantiles.items():
            test_performance[f"intent_test_ece_q{quantile}"] = value

        return train_performance, test_performance

    def score(self, nlu_data: dict) -> dict:
        """
        Predict the fitted model on `nlu_data`, returning its performance on it.
        """
        assert self._fitted
        dataset = self.preprocessor.transform(nlu_data)
        return self.model.evaluate(dataset.batch(self.batch_size_predict), return_dict=True)

    @endpoint
    def predict(self, instances: t.List[str]) -> dict:
        """
        @TODO: Upon error, raise an HTTP exception with the signature `{"error": "..."}`, so GCP
        can intercept it if they want. See https://fastapi.tiangolo.com/tutorial/handling-errors/.
        This is just a nice-to-have.
        """
        assert self._fitted

        X = self.preprocessor.transform_utterances(instances)
        raw_intent_preds, raw_tags_preds = self.model.predict(X)

        predictions = []
        for i, (raw_intent_pred, raw_tags_pred, text) in enumerate(zip(raw_intent_preds, raw_tags_preds, instances)):
            word_start_mask_i = X["word_start_mask"][i, :].numpy()  # word start mask for ith instance
            intent_dict = self._decode_intent(raw_intent_pred)
            tags = self._decode_tags(raw_tags_pred, text, word_start_mask_i)

            predictions.append({
                "intent": intent_dict,
                "tags": tags,
            })

        return {"predictions": predictions}

    def _decode_intent(self, raw_intent_prediction: np.ndarray) -> dict:
        intent_max = np.argmax(raw_intent_prediction)
        confidence = np.max(raw_intent_prediction).item()
        decoded_intent = self.preprocessor.intents_encoder.inverse_transform([intent_max])[0]
        return {"value": decoded_intent, "confidence": confidence}

    def _decode_tags(self, raw_tag_predictions: np.ndarray, text: str, word_start_mask: np.ndarray):
        raw_tag_predictions = np.squeeze(raw_tag_predictions)
        assert raw_tag_predictions.shape[0] == len(word_start_mask)
        decoded_tags = []
        for i, e in enumerate(word_start_mask):
            if e == 1:
                predicted_tag_idx = np.argmax(raw_tag_predictions[i])
                predicted_tag = self.preprocessor.tag_encoder.inverse_transform([predicted_tag_idx])[0]
                decoded_tags.append(predicted_tag)

        words = text.split()

        result = []
        current_tag_words = []
        current_tag_type = None
        for i, tag in enumerate(decoded_tags):
            if tag == 'O':
                if current_tag_words and current_tag_type:
                    result.append({
                        'tag_type': current_tag_type,
                        'value': ' '.join(current_tag_words),
                    })

                current_tag_type = None
                current_tag_words = []
                continue

            if tag.startswith('B-'):
                if current_tag_words and current_tag_type:
                    result.append({
                        'tag_type': current_tag_type,
                        'value': ' '.join(current_tag_words),
                    })

                current_tag_words = [words[i]]
                current_tag_type = tag[2:]
            elif tag.startswith('I-'):
                current_tag_words.append(words[i])

        if current_tag_words and current_tag_type:
            result.append({
                'tag_type': current_tag_type,
                'value': ' '.join(current_tag_words),
            })

        return result

    def bayesian_ece_for_obj(
        self,
        nlu_data: dict,
        obj: str,
        *,
        quantiles: t.Sequence = [10, 50, 90],
        bins: int = 15,
        is_sparse: bool = True
    ) -> t.Dict[int, float]:
        """
        Computes the Bayesian Expected Calibration Error (ECE) for `data` (ubatched)
        with respect to a single objective of the model (denoted by `obj`). Returns
        the quantiles denoted by `quantiles` of the approximated posterier bayesian
        distribution over ECE. If the labels in `data` are sparse, `is_sparse` should be
        `True`.
        """
        assert self._fitted
        dataset = self.preprocessor.transform(nlu_data)
        y_pred = self.model.predict(dataset.batch(self.batch_size_predict), verbose=1)

        # Isolate the labels and predictions for the objective in question.
        y_obj = tf.stack([y[obj] for _, y in dataset])
        if not is_sparse:
            # The ECE equation expects sparse labels.
            y_obj = tf.argmax(y_obj, axis=-1)

        obj_i = self.model.output_names.index(obj)
        y_pred_obj = tf.convert_to_tensor(y_pred[obj_i], tf.float32)

        ece_samples = um.bayesian_expected_calibration_error(
            bins,
            probabilities=y_pred_obj,
            labels_true=tf.cast(y_obj, tf.int32)
        )
        ece_quantiles = tfp.stats.percentile(ece_samples, quantiles)
        return {quantile: float(value) for quantile, value in zip(quantiles, ece_quantiles)}
