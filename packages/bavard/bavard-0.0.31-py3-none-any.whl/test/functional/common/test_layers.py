from unittest import TestCase
import typing as t
import shutil

import tensorflow as tf
from sklearn.datasets import make_classification

from bavard.common.layers import LSTMBlocks, DenseBlocks, Encoder


ModelBody = t.Union[DenseBlocks, LSTMBlocks, Encoder]


class TestLayers(TestCase):
    def setUp(self):
        self.n = 30  # number of samples used on test models
        self.p = 4  # number of features used on test models
        self.seq_len = 3  # length of each feature sequence used on test models
        self.k = 2  # number of classes used on test models
        self.save_path = "temp-model"

    def test_dense_blocks(self):
        self._test_body(
            DenseBlocks(num_blocks=1, units=1, dropout=0.0),
            is_sequence_problem=False
        )
        self._test_body(
            DenseBlocks(num_blocks=1, units=1, dropout=0.0),
            is_sequence_problem=True
        )

    def test_lstm_blocks(self):
        self._test_body(
            LSTMBlocks(num_blocks=1, units=1, dropout=0.0, return_sequences=True),
            is_sequence_problem=True
        )

    def test_encoder(self):
        self._test_body(
            Encoder(num_blocks=1, embed_dim=4, num_heads=2, units=1, dropout=0.0, causal=True),
            is_sequence_problem=True
        )

    def _make_model(self, body: ModelBody, is_sequence_problem: bool) -> tf.keras.Model:
        if is_sequence_problem:
            inputs = tf.keras.Input((self.seq_len, self.p))
        else:
            inputs = tf.keras.Input((self.p,))
        outputs = body(inputs)
        outputs = tf.keras.layers.Dense(self.k, activation="softmax")(outputs)
        model = tf.keras.Model(inputs, outputs)
        model.compile("adam", "sparse_categorical_crossentropy", "accuracy")
        return model

    def _make_dataset(self, is_sequence_problem: bool) -> tuple:
        X, y = make_classification(n_samples=self.n, n_features=self.p, n_classes=self.k)
        if not is_sequence_problem:
            return X, y
        X = X.reshape((-1, self.seq_len, self.p))
        y = y.reshape((-1, self.seq_len))
        return X, y

    def _test_body(self, body: ModelBody, is_sequence_problem: bool):
        # Body should be able to work in a model.
        model = self._make_model(body, is_sequence_problem)
        X, y = self._make_dataset(is_sequence_problem)
        model.fit(X, y, batch_size=self.n, verbose=0)
        acc = model.evaluate(X, y, verbose=0, return_dict=True)["accuracy"]

        # Should be able to persist and load.
        model.save(self.save_path)
        loaded_model = tf.keras.models.load_model(self.save_path)
        shutil.rmtree(self.save_path)
        # Loaded model should be able to predict and get the same accuracy.
        loaded_acc = loaded_model.evaluate(X, y, verbose=0, return_dict=True)["accuracy"]

        self.assertEqual(acc, loaded_acc)
