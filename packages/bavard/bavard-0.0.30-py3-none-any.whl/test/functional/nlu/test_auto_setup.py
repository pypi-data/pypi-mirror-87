from unittest import TestCase

import tensorflow as tf

from bavard.nlu.auto_setup import AutoSetup


class TestAutoSetup(TestCase):

    def test_determine_batch_size(self):
        b = AutoSetup._determine_batch_size(AutoSetup.min_num_examples)
        self.assertEqual(b, AutoSetup.min_batch_size)

        b = AutoSetup._determine_batch_size(300)
        self.assertEqual(b, 8)

        b = AutoSetup._determine_batch_size(1e7)
        self.assertEqual(b, 64)

    def test_get_training_setup(self):

        # Test the `auto==False` case.
        hparams = {"batch_size": 5, "epochs": 12}
        expected_n = 11
        dataset = tf.data.Dataset.from_tensor_slices(list(range(expected_n)))
        train_data, val_data, hparams, _ = AutoSetup.get_training_setup(False, dataset, hparams)
        n = sum(1 for _ in train_data)

        self.assertEqual(n, expected_n, "dataset length not what expected")
        # Original hparams should be unchanged.
        self.assertEqual(hparams["batch_size"], 5, "batch size should not have changed")
        self.assertEqual(hparams["epochs"], 12, "epochs should not have changed")

        # Test the `auto==True` case without early stopping.

        hparams = {"batch_size": 5, "epochs": 1}
        expected_n = AutoSetup.min_train_size_for_validation - 1
        dataset = tf.data.Dataset.from_tensor_slices(list(range(expected_n)))
        train_data, val_data, hparams, _ = AutoSetup.get_training_setup(True, dataset, hparams)
        n = sum(1 for _ in train_data)

        self.assertEqual(n, expected_n, "dataset length not what expected")
        self.assertIsNone(val_data)
        self.assertEqual(hparams["batch_size"], AutoSetup._determine_batch_size(expected_n))

        # Test the `auto==True` case *with* early stopping.

        hparams = {"batch_size": 5, "epochs": 1}
        expected_n = AutoSetup.min_train_size_for_validation
        dataset = tf.data.Dataset.from_tensor_slices(list(range(expected_n)))
        train_data, val_data, hparams, _ = AutoSetup.get_training_setup(True, dataset, hparams)
        train_n = sum(1 for _ in train_data)

        self.assertIsNotNone(val_data)
        val_n = sum(1 for _ in val_data)

        # Train and validation sets should be the expected size.
        self.assertEqual(train_n, expected_n - AutoSetup._get_val_size(expected_n))
        self.assertEqual(val_n, AutoSetup._get_val_size(expected_n))

        self.assertEqual(hparams["batch_size"], AutoSetup._determine_batch_size(train_n))
