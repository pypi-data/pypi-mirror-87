import tensorflow as tf
from tensorflow.python.keras.engine.base_layer import Layer
from tensorflow.python.keras.layers import Dropout, Dense, BatchNormalization, Activation


class DenseBlock(Layer):
    """Dense layer with dropout, batch norm, and l2 regularization included.
    """

    def __init__(
        self,
        units: int,
        activation: str = "relu",
        dropout: float = 0.0,
        l2: float = 0.0
    ):
        super().__init__()
        self.units = units
        self.activation = activation
        self.dropout_rate = dropout
        self.l2_rate = l2

        L2 = tf.keras.regularizers.l2(self.l2_rate) if self.l2_rate > 0 else None
        self.dropout = Dropout(rate=self.dropout_rate)
        self.dense = Dense(
            self.units, kernel_regularizer=L2
        )
        self.batch_norm = BatchNormalization(renorm=True)
        self.activate = Activation(self.activation)

    def call(self, inputs, training):
        X = self.dropout(inputs, training)
        X = self.dense(X)
        X = self.batch_norm(X)
        X = self.activate(X)
        return X

    def get_config(self) -> dict:
        return {
            "units": self.units,
            "activation": self.activation,
            "dropout": self.dropout_rate,
            "l2": self.l2_rate
        }


class DenseBlocks(Layer):
    """Wrapper layer for calling multiple `DenseBlock`s at once.
    """
    def __init__(
        self,
        num_blocks: int,
        units: int,
        activation: str = "relu",
        dropout: float = 0.0,
        l2: float = 0.0
    ):
        super().__init__()
        self.num_blocks = num_blocks
        self.units = units
        self.activation = activation
        self.dropout_rate = dropout
        self.l2_rate = l2

        self.blocks = tf.keras.Sequential([DenseBlock(units, activation, dropout, l2) for _ in range(num_blocks)])

    def call(self, inputs, training):
        return self.blocks(inputs, training)

    def get_config(self) -> dict:
        return {
            "num_blocks": self.num_blocks,
            "units": self.units,
            "activation": self.activation,
            "dropout": self.dropout_rate,
            "l2": self.l2_rate
        }
