import tensorflow as tf
from tensorflow.keras.losses import sparse_categorical_crossentropy


@tf.function
def vwci(y: tf.Tensor, y_pred: tf.Tensor, e: float = 1e-10) -> tf.Tensor:
    """
    An implementation of Variance-Weighted Confidence-Integrated Loss (VWCI).

    Parameters
    ----------
    y : tf.Tensor
        The ground truth labels. Should be of dimension `(batch_size, dims-1)`
        (sparse labels).
    y_pred : tf.Tensor
        The predictions. Should be of dimension `(num_samples, batch_size, dims)`,
        where `num_samples` is the number of stochastic inferences the model did
        on its forward pass.
    e : float
        `epsilon`, the constant added to VWCI.
    """
    y_pred_shape = tf.cast(tf.shape(y_pred), tf.float32)
    num_labels = y_pred_shape[-1]
    num_samples = y_pred_shape[0]

    # In case each prediction vector doesn't sum to 1.
    y_pred_normalized = y_pred / tf.reduce_sum(y_pred, axis=-1, keepdims=True)

    # The average prediction vectors across the stochastic inferences.
    y_pred_avg = tf.math.reduce_mean(y_pred_normalized, axis=0)  # (batch_size, dims)
    # The deviation of each prediction vector from its mean prediction vector.
    bhatta_coeffs = bhattacharyya(y_pred_avg, y_pred_normalized)  # (num_samples, batch_size, dims)
    # `a` is then the empirical normalized variance of the predictions.
    a = tf.reduce_mean(bhatta_coeffs, axis=0)  # (batch_size, dims)

    # The loss between the predictions and the ground truth labels.
    broadcast_y_shape = tf.concat([[num_samples], tf.shape(y)], axis=0)
    L_GT = sparse_categorical_crossentropy(
        tf.broadcast_to(y, broadcast_y_shape),
        y_pred_normalized
    )  # (num_samples, batch_size, dims-1)

    # The loss between the predictions and the uniform distribution.
    u = tf.ones([num_labels]) / num_labels
    L_U = kl_divergence(u, y_pred_normalized)  # (num_samples, batch_size, dims-1)

    # A convex combination of the ground truth loss and uniform loss, weighted
    # by the model's predictive variance. When variance is high, train the model
    # to output the uniform distribution. When variance is low, the model is confident
    # so train it like normal (cross entropy).
    return tf.math.reduce_mean((1 - a) * L_GT + a * L_U + e, axis=0)  # (batch_size, dims-1)


@tf.function
def bhattacharyya(p: tf.Tensor, q: tf.Tensor) -> tf.Tensor:
    """
    Computes the Bhattacharyya coefficient between `p` and `q`. Note:
    the entries of `p` should all sum to 1. The same for `q`.
    For a description, see equation (1) in:
    http://www.cse.yorku.ca/~kosta/CompVis_Notes/bhattacharyya.pdf
    """
    return 1 - tf.math.reduce_sum(tf.math.sqrt(p * q), axis=-1)


@tf.function
def kl_divergence(y: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
    """
    Computes the KL Divergence between distributions `y` and `y_pred`.
    """
    return tf.math.reduce_sum(y * tf.math.log(y / y_pred), axis=-1)
