import tensorflow as tf
from tensorflow.python.keras.engine.base_layer import Layer
from tensorflow.python.keras.layers import Dropout, LSTM, BatchNormalization


class LSTMBlock(Layer):
    """LSTM layer with dropout, batch norm, and l2 regularization included.
    """

    def __init__(
        self,
        units: int = 512,
        dropout: float = 0.0,
        l2: float = 0.0,
        return_sequences: bool = True,
    ):
        super().__init__()
        self.units = units
        self.dropout_rate = dropout
        self.l2_rate = l2
        self.return_sequences = return_sequences

        L2 = tf.keras.regularizers.l2(self.l2_rate) if self.l2_rate > 0 else None
        self.dropout = Dropout(rate=self.dropout_rate)
        self.lstm = LSTM(
            self.units, return_sequences=self.return_sequences, kernel_regularizer=L2
        )
        self.batch_norm = BatchNormalization(renorm=True)

    def call(self, inputs: tf.Tensor, training) -> tf.Tensor:
        X = self.dropout(inputs, training)
        X = self.lstm(X)
        X = self.batch_norm(X)
        return X

    def get_config(self) -> dict:
        return {
            "units": self.units,
            "dropout": self.dropout_rate,
            "l2": self.l2_rate,
            "return_sequences": self.return_sequences,
        }


class LSTMBlocks(Layer):
    """Wrapper layer for calling multiple `LSTMBlock`s at once.
    """

    def __init__(
        self,
        num_blocks: int,
        units: int = 512,
        dropout: float = 0.0,
        l2: float = 0.0,
        return_sequences: bool = True,
    ):
        super().__init__()
        self.num_blocks = num_blocks
        self.units = units
        self.dropout_rate = dropout
        self.l2_rate = l2
        self.return_sequences = return_sequences

        self.blocks = tf.keras.Sequential([
            LSTMBlock(units, dropout, l2, return_sequences) for _ in range(num_blocks)
        ])

    def call(self, inputs, training):
        return self.blocks(inputs, training)

    def get_config(self) -> dict:
        return {
            "num_blocks": self.num_blocks,
            "units": self.units,
            "dropout": self.dropout_rate,
            "l2": self.l2_rate,
            "return_sequences": self.return_sequences
        }
