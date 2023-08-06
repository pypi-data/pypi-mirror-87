import tensorflow as tf


def similarity_loss(y_true, y_pred):
    # mask = tf.cast(tf.not_equal(y_true, 0), tf.float32)

    action_similarities = y_pred  # (n, seq_len, n_actions)
    n_actions = tf.shape(action_similarities)[-1]

    y_true = tf.cast(y_true, tf.int32)
    y_neg = tf.cast(1 - tf.one_hot(indices=y_true, depth=n_actions), tf.float32)

    neg_sim = action_similarities * y_neg
    neg_sim = tf.reduce_sum(neg_sim, axis=-1) / tf.cast(n_actions - 1, tf.float32)

    true_sim = action_similarities * tf.cast(tf.one_hot(indices=y_true, depth=n_actions), tf.float32)
    true_sim = tf.reduce_sum(true_sim, axis=-1)

    tf.assert_equal(tf.shape(y_true), tf.shape(true_sim))
    tf.assert_equal(tf.shape(true_sim), tf.shape(neg_sim))

    loss = -true_sim + neg_sim
    loss = loss
    return tf.reduce_sum(loss)
