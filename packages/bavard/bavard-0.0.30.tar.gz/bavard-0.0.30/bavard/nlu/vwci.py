import tensorflow as tf

from bavard.nlu.metrics import vwci


class VWCIModel(tf.keras.Model):
    """
    Subclass of `tf.keras.Model` which implements a custom training
    step, using the "Variance-Weighted Confidence-Integrated Loss" (VWCI)
    to encourage the neural network to have better calibration. VWCI was
    introduced in the paper "Learning for Single-Shot Confidence
    Calibration in Deep Neural Networks through Stochastic Inferences"
    by Seo et al. in 2019.
    """

    def __init__(
        self,
        *args,
        vwci_ratio: float,
        n_vwci_inferences: int,
        loss_weights: dict,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.loss_trackers = [tf.keras.metrics.Mean(name=name + "_loss")
                              for name in self.output_names]  # pylint: disable=not-an-iterable
        self.loss_trackers.append(tf.keras.metrics.Mean(name="loss"))  # to track total loss

        self.vwci_ratio = vwci_ratio
        assert n_vwci_inferences > 1
        self.n_vwci_inferences = n_vwci_inferences
        self.loss_weights = loss_weights

    @tf.function
    def _get_cross_entropy_losses(self, x, y) -> tuple:
        # Train with normal cross entropy.
        y_pred = self(x, training=True)  # forward pass
        losses = [tf.keras.losses.sparse_categorical_crossentropy(_y, _y_pred) for _y, _y_pred in zip(y, y_pred)]
        return losses, y_pred

    @tf.function
    def _get_vwci_losses(self, x, y) -> tuple:
        # Train with VWCI. First, make multiple stochastic inferences.
        y_pred = [self(x, training=True) for _ in range(self.n_vwci_inferences)]  # multiple forward passes
        y_pred_by_objective = zip(*y_pred)
        losses = [vwci(_y, tf.stack(_y_pred)) for _y, _y_pred in zip(y, y_pred_by_objective)]
        return losses, y_pred[0]

    @tf.function
    def train_step(self, data: tuple) -> dict:
        """
        A custom train step function that `tf.keras.Model` will call
        in its `fit` method. Supports multi-objective optimization.
        Source: https://keras.io/guides/customizing_what_happens_in_fit/
        """
        # Preprocess data.
        x, y = data  # comes pre-batched
        if isinstance(y, dict):
            # Switch to a list of y values, since y_pred is always a list.
            y = [y[name] for name in self.output_names]  # pylint: disable=not-an-iterable
        loss_weight_vec = [self.loss_weights[name] for name in self.output_names]  # pylint: disable=not-an-iterable

        # Compute the loss. Use VWCI part of the time.
        with tf.GradientTape() as tape:
            dice_roll = tf.random.uniform([1])  # pylint: disable=no-value-for-parameter
            losses, y_pred = tf.cond(
                dice_roll < self.vwci_ratio,
                lambda: self._get_vwci_losses(x, y),
                lambda: self._get_cross_entropy_losses(x, y)
            )

            # Apply loss weights and sum to get the final loss.
            loss = sum(tf.reduce_mean(_loss) * weight for _loss, weight in zip(losses, loss_weight_vec))
            # Add regularization losses from the model's layers
            loss += sum(self.losses)

        # Compute gradients
        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)

        # Update weights
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))

        # Update metrics and losses
        self.compiled_metrics.update_state(y, y_pred)
        for loss_tracker, loss in zip(self.loss_trackers, losses + [loss]):
            loss_tracker.update_state(loss)

        # Return a dict mapping metric names to current value
        return {m.name: m.result() for m in self.metrics}

    @property
    def metrics(self):
        # We list our `Metric` objects here so that `reset_states()` can be
        # called automatically at the start of each epoch
        # or at the start of `evaluate()`.
        # If you don't implement this property, you have to call
        # `reset_states()` yourself at the time of your choosing.
        return super().metrics + self.loss_trackers
