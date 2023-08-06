import logging
import math

import tensorflow as tf

from bavard.nlu.utils import assert_all_not_none


class AutoSetup:
    """
    Class of static methods useful for automatically determining the hyperparameter
    setup for a NLUModel, and other methods for aiding in setting up a model's
    training configuration.
    """

    max_val_size = 10000
    default_val_ratio = 0.2
    min_train_size_for_validation = 250
    default_num_epochs = 60  # used when no early stopping takes place
    max_epochs = 1000
    min_batch_size = 4
    min_num_examples = 5
    # Format: `(min_examples, batch_size)`.
    # Based on the function `(n/50)+4`
    batch_size_lower_bounds = [
        (min_num_examples, min_batch_size),
        (200, 8),
        (600, 16),
        (1400, 32),
        (3000, 64)
    ]

    @staticmethod
    def get_training_setup(auto: bool, dataset: tf.data.Dataset, hparams: dict) -> tuple:
        """
        Determines and creates the training set up to use, including hyperparameter
        settings and train/validation splits. Supports `auto` mode and non-auto mode.

        Parameters
        ----------
        auto : bool
            If `True`, hyperparameters and splits are determined automatically. If `False`,
            the hyperparameters present in `hparams` will be used, and no split will occur.
        dataset : tf.data.Dataset
            The full training dataset used to create the train/validatino split.
        hparams : dict
            The hyperparameter values passed in by the user.

        Returns
        -------
        train_data : tf.data.Dataset
            The training portion of the dataset split.
        val_data : tf.data.Dataset
            The validatin portion of the dataset split. Set to `None` if
            there is no validation data.
        hparams : dict
            The updated hyperparameter settings to use when training.
        callbacks : list
            Any callback functions the model should be sure to use when
            fitting.
        """
        n = sum(1 for _ in dataset)
        AutoSetup._assert_min_dataset_size(n)
        dataset = dataset.shuffle(buffer_size=1000, seed=0)

        if not auto:
            # Use the user-provided settings.

            # Values must be passed in for the hyperparameters when auto mode is off.
            assert_all_not_none(**hparams)
            logging.info(f'Training example count: {n}')
            return dataset, None, hparams, []

        # Automatically determine the training set up using some
        # heuristics.

        if n < AutoSetup.min_train_size_for_validation:
            # No validation set will be used -- the dataset is too small.

            hparams["batch_size"] = AutoSetup._determine_batch_size(n)
            hparams["epochs"] = AutoSetup.default_num_epochs
            logging.info(f'Training example count: {n}')
            return dataset, None, hparams, []

        # A validation set and early stopping will be used.

        n_val = AutoSetup._get_val_size(n)
        n_train = n - n_val

        hparams["batch_size"] = AutoSetup._determine_batch_size(n_train)
        # Since we're using early stopping, the `epochs` hparam essentially becomes a
        # max epochs hparam.
        hparams["epochs"] = AutoSetup.max_epochs

        val_data = dataset.take(n_val)
        train_data = dataset.skip(n_val)

        # Use early stopping.
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor="val_loss",
                min_delta=1e-5,
                patience=3
            )
        ]

        logging.info(f'Training example count: {n_train}')
        logging.info(f'Validation example count: {n_val}')
        return train_data, val_data, hparams, callbacks

    @staticmethod
    def get_steps_per_epoch(n: int, b: int) -> int:
        """
        Returns the number of steps per epoch a model should take
        while training, given `n`, the number of examples in the training set,
        and `b`, the batch size.
        """
        return math.ceil(n / b)

    @staticmethod
    def _determine_batch_size(n: int) -> int:
        """
        Uses a heuristic to determine a good batch size to use,
        given dataset size `n` (uses a linear function of `n`, rounding
        to a power of 2).
        """
        AutoSetup._assert_min_dataset_size(n)
        batch_size = AutoSetup.min_batch_size
        for lower_bound, b in AutoSetup.batch_size_lower_bounds:
            if n >= lower_bound:
                batch_size = b
        return batch_size

    @staticmethod
    def _assert_min_dataset_size(n: int) -> None:
        if n < AutoSetup.min_num_examples:
            raise Exception(
                f"Too few examples to train, must be at least {AutoSetup.min_num_examples}"
            )

    @staticmethod
    def _get_val_size(n: int, val_ratio: float = None) -> int:
        if val_ratio is None:
            val_ratio = AutoSetup.default_val_ratio
        return min(int(n * AutoSetup.default_val_ratio), AutoSetup.max_val_size)
