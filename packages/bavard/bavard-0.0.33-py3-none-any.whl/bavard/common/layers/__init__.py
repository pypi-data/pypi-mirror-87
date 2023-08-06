from bavard.common.layers.dense import DenseBlocks
from bavard.common.layers.lstm import LSTMBlocks
from bavard.common.layers.text_embedder import TextEmbedder  # noqa F401
from bavard.common.layers.transformer import Encoder

model_bodies = {
    "dense": DenseBlocks,
    "lstm": LSTMBlocks,
    "encoder": Encoder
}
