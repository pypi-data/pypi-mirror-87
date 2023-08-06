import tensorflow as tf


def create_padding_mask(seq):
    seq = tf.cast(tf.math.equal(seq, -1), tf.float32)
    return seq  # (batch_size, 1, 1, seq_len)


def create_look_ahead_mask(seq_len: int):
    mask = 1 - tf.linalg.band_part(tf.ones((seq_len, seq_len)), -1, 0)
    return mask  # (seq_len, seq_len)
