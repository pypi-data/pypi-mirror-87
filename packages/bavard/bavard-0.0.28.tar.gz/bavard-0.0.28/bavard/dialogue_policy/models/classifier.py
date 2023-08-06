import typing as t

import tensorflow as tf
from tensorflow.keras.layers import Dense
import kerastuner as kt

from bavard.dialogue_policy.data.preprocessed_data import PreprocessedTrainingData
from bavard.dialogue_policy.models.base import BaseModel, NLUEmbedder, blocks
from bavard.dialogue_policy.constants import MAX_UTTERANCE_LEN


class Classifier(BaseModel):
    """
    Standard multinomial classifier predicting the next dialogue actions to take.
    """

    def __init__(
        self,
        *,
        units: int = 512,
        num_blocks: int = 2,
        block_type: str = "lstm",
        l2: float = 0.0,
        epochs: int = 100,
        learning_rate: float = 1e-4,
        fine_tune_nlu_embedder: bool = False,
        batch_size: float = 32,
        dropout: float = 0.0,
        use_utterances: bool = True,
        callbacks: list = None
    ) -> None:
        # Control parameters
        self._fitted = False
        self._preprocessor = None
        self._model = None
        self.callbacks = callbacks if callbacks else []

        # Tuning parameters
        self.units = units
        self.num_blocks = num_blocks
        assert block_type in blocks
        self.block_type = block_type
        self.l2 = l2
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.fine_tune_nlu_embedder = fine_tune_nlu_embedder
        self.batch_size = batch_size
        self.dropout = dropout
        self.use_utterances = use_utterances

    @staticmethod
    def get_hp_spec(hp: kt.HyperParameters) -> t.Dict[str, kt.engine.hyperparameters.HyperParameter]:
        return {
            "units": hp.Int("units", 32, 512, default=512),
            "num_blocks": hp.Int("num_blocks", 1, 4),
            "block_type": hp.Choice("block_type", list(blocks.keys())),
            "l2": hp.Float("l2", 1e-12, 0.1, sampling="log"),
            "epochs": hp.Int("epochs", 5, 200, step=5, default=100),
            "learning_rate": hp.Float("learning_rate", 1e-7, 0.1, sampling="log", default=5e-5),
            "fine_tune_nlu_embedder": hp.Boolean("fine_tune_nlu_embedder", default=False),
            "batch_size": hp.Choice("batch_size", [8, 16]),  # @TODO: Add larger sizes once memory issues are resolved.
            "dropout": hp.Float("dropout", 0.0, 0.6, default=0.1),
            "use_utterances": hp.Boolean("use_utterances", default=True),
        }

    def fit(self, agent: dict) -> None:
        """Fits the model on `agent`.

        Parameters
        ----------
        agent : dict
            An agent config JSON object.
        """
        # Preprocess the data.
        self._preprocessor = PreprocessedTrainingData(agent)

        # Define the model.
        feature_vec = tf.keras.Input((self._preprocessor.max_len, self._preprocessor.input_dim), name="feature_vec")
        utterance_ids = tf.keras.Input((self._preprocessor.max_len, MAX_UTTERANCE_LEN),
                                       name="utterance_ids", dtype=tf.int32)
        utterance_mask = tf.keras.Input((self._preprocessor.max_len, MAX_UTTERANCE_LEN),
                                        name="utterance_mask", dtype=tf.int32)
        conversation_mask = tf.keras.Input((self._preprocessor.max_len, 1), name="conversation_mask", dtype=tf.float32)

        # Embed utterances and concatenate to feature_vec.
        if self.use_utterances:
            utterance_emb = NLUEmbedder(self.fine_tune_nlu_embedder)([utterance_ids, utterance_mask])
            all_features = tf.concat([feature_vec, utterance_emb], axis=-1)
        else:
            all_features = feature_vec

        outputs = all_features
        for _ in range(self.num_blocks):
            outputs = blocks[self.block_type](
                self.units,
                dropout=self.dropout,
                l2=self.l2,
            )(outputs)

        outputs = Dense(self._preprocessor.num_actions, activation="softmax")(outputs)
        self._model = tf.keras.Model(inputs=[feature_vec, utterance_ids,
                                             utterance_mask, conversation_mask], outputs=outputs)

        # Build the model.
        self._model.compile(
            loss='sparse_categorical_crossentropy',
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate),
            metrics="accuracy",
        )

        # Fit the model.
        self._model.fit(self._preprocessor.to_classifier_dataset().batch(self.batch_size),
                        epochs=self.epochs,
                        callbacks=self.callbacks + [self.get_tensorboard_cb()])

        self._fitted = True

    def predict(self, conversations: t.List[dict]) -> t.List[str]:
        """Predict the next action to take on each conversation in `conversations`.

        Parameters
        ----------
        conversations : list of dict
            A list of conversations. Each is the current state of a JSON chatbot conversation.
        """
        assert self._fitted
        X = {k: v for k, v in self._preprocessor.encode_raw_conversations(conversations).items() if k != "action"}

        y_pred = self._model.predict(X, self.batch_size)
        return self._preprocessor.enc_context.inverse_transform("action", y_pred[:, -1, :])
