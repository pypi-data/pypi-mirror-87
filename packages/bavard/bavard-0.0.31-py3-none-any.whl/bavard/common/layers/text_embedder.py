import tensorflow as tf
from tensorflow.python.keras.engine.base_layer import Layer
from transformers import TFDistilBertModel

from bavard.dialogue_policy.constants import BASE_LANGUAGE_MODEL


class TextEmbedder(Layer):
    def __init__(self, trainable: bool = False):
        super().__init__()
        self.trainable = trainable
        self.embed_dim = 768

    def build(self, input_shape):
        ids_shape, _ = input_shape
        self.seq_len = ids_shape[-1]  # the length of each text token sequence
        self.other_dims = [-1 if dim is None else dim for dim in ids_shape[:-1]]
        self.embed = TFDistilBertModel.from_pretrained(BASE_LANGUAGE_MODEL).distilbert
        self.embed.trainable = self.trainable

    def call(self, inputs) -> tf.Tensor:
        input_ids, input_mask = inputs

        input_ids_flat = tf.reshape(input_ids, (-1, self.seq_len))
        input_mask_flat = tf.reshape(input_mask, (-1, self.seq_len))

        token_embeddings = self.embed([input_ids_flat, input_mask_flat])[0]
        pooled_embeddings = token_embeddings[:, 0]

        unflattened = tf.reshape(pooled_embeddings, self.other_dims + [self.embed_dim])
        return unflattened

    def get_config(self) -> dict:
        return {"trainable": self.trainable}
