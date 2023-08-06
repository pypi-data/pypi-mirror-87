import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np


def get_angles(pos, i, dim):
    """Source: https://www.tensorflow.org/tutorials/text/transformer
    """
    angle_rates = 1 / np.power(10000, (2 * (i // 2)) / np.float32(dim))
    return pos * angle_rates


def positional_encoding(seq_len: int, dim: int):
    """Source: https://www.tensorflow.org/tutorials/text/transformer
    """
    angle_rads = get_angles(
        np.arange(seq_len)[:, np.newaxis],
        np.arange(dim)[np.newaxis, :],
        dim
    )

    # apply sin to even indices in the array; 2i
    angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])

    # apply cos to odd indices in the array; 2i+1
    angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])

    pos_encoding = angle_rads[np.newaxis, ...]

    return tf.cast(pos_encoding, dtype=tf.float32)


class MultiHeadSelfAttention(layers.Layer):
    """Source: https://keras.io/examples/nlp/text_classification_with_transformer/
    """
    def __init__(self, embed_dim: int, num_heads: int = 8, causal: bool = False):
        """
        Parameters
        ----------
        embed_dim : int
            The representation width to use for the key, value, query vectors
        num_heads : int, optional
            The number of heads to split the key, value, and query vectors into
            for performing multiple attention.
        causal : book, optional
            If `True`, adds a mask such that position i cannot attend to positions j > i.
            This prevents the flow of information from the future towards the past.
        """
        super().__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.causal = causal  # performs look-ahead masking if True
        if embed_dim % num_heads != 0:
            raise ValueError(
                f"embedding dimension = {embed_dim} should be divisible by number of heads = {num_heads}"
            )
        self.projection_dim = embed_dim // num_heads
        self.query_dense = layers.Dense(embed_dim)
        self.key_dense = layers.Dense(embed_dim)
        self.value_dense = layers.Dense(embed_dim)
        self.combine_heads = layers.Dense(embed_dim)

    def attention(self, query, key, value):
        score = tf.matmul(query, key, transpose_b=True)
        dim_key = tf.cast(tf.shape(key)[-1], tf.float32)
        seq_len = tf.shape(key)[-2]
        scaled_score = score / tf.math.sqrt(dim_key)
        if self.causal:
            # Source: https://www.tensorflow.org/tutorials/text/transformer
            mask = 1 - tf.linalg.band_part(tf.ones((seq_len, seq_len)), -1, 0)
            scaled_score += (mask * -1e9)
        weights = tf.nn.softmax(scaled_score, axis=-1)
        output = tf.matmul(weights, value)
        return output, weights

    def separate_heads(self, x, batch_size):
        x = tf.reshape(x, (batch_size, -1, self.num_heads, self.projection_dim))
        x = tf.transpose(x, perm=[0, 2, 1, 3])
        return x

    def call(self, inputs):
        # x.shape = [batch_size, seq_len, embedding_dim]
        batch_size = tf.shape(inputs)[0]
        query = self.query_dense(inputs)  # (batch_size, seq_len, embed_dim)
        key = self.key_dense(inputs)  # (batch_size, seq_len, embed_dim)
        value = self.value_dense(inputs)  # (batch_size, seq_len, embed_dim)
        query = self.separate_heads(
            query, batch_size
        )  # (batch_size, num_heads, seq_len, projection_dim)
        key = self.separate_heads(
            key, batch_size
        )  # (batch_size, num_heads, seq_len, projection_dim)
        value = self.separate_heads(
            value, batch_size
        )  # (batch_size, num_heads, seq_len, projection_dim)
        attention, weights = self.attention(query, key, value)
        attention = tf.transpose(
            attention, perm=[0, 2, 1, 3]
        )  # (batch_size, seq_len, num_heads, projection_dim)
        concat_attention = tf.reshape(
            attention, (batch_size, -1, self.embed_dim)
        )  # (batch_size, seq_len, embed_dim)
        output = self.combine_heads(
            concat_attention
        )  # (batch_size, seq_len, embed_dim)
        return output

    def get_config(self):
        return {
            "embed_dim": self.embed_dim,
            "num_heads": self.num_heads,
            "causal": self.causal
        }


class TransformerBlock(layers.Layer):
    """Source: https://keras.io/examples/nlp/text_classification_with_transformer/
    """
    def __init__(self, embed_dim: int, num_heads: int, ff_dim: int, causal: bool, rate: float):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.causal = causal
        self.rate = rate

        self.att = MultiHeadSelfAttention(embed_dim, num_heads, causal)
        self.ffn = keras.Sequential(
            [layers.Dense(ff_dim, activation="relu"), layers.Dense(embed_dim)]
        )
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, inputs, training):
        attn_output = self.att(inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)

    def get_config(self):
        return {
            "embed_dim": self.embed_dim,
            "num_heads": self.num_heads,
            "ff_dim": self.ff_dim,
            "causal": self.causal,
            "rate": self.rate,
        }


class Encoder(layers.Layer):
    def __init__(
        self,
        num_blocks: int,
        embed_dim: int = 64,
        num_heads: int = 8,
        units: int = 512,
        dropout: float = 0.1,
        causal: bool = True,
        **kwargs
    ):
        super().__init__()
        self.num_blocks = num_blocks
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.units = units
        self.dropout = dropout
        self.causal = causal

        self.dense = layers.Dense(embed_dim)
        self.blocks = tf.keras.Sequential(
            [TransformerBlock(embed_dim, num_heads, units, causal, dropout) for _ in range(num_blocks)]
        )

    def build(self, input_shape):
        self.pos_encoding = positional_encoding(input_shape[-2], input_shape[-1])

    def call(self, inputs, training):
        x = inputs + self.pos_encoding
        x = self.dense(x)
        return self.blocks(x, training)

    def get_config(self):
        return {
            "num_blocks": self.num_blocks,
            "embed_dim": self.embed_dim,
            "num_heads": self.num_heads,
            "units": self.units,
            "dropout": self.dropout,
            "causal": self.causal,
        }
