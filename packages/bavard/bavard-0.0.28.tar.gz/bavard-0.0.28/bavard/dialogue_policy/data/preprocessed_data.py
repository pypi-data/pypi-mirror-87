import typing as t

import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer

from bavard.dialogue_policy.data.conversations.conversation import Conversation
from bavard.dialogue_policy.data.utils import EncodingContext, LabelBinarizer, TextEncoder
from bavard.dialogue_policy.data.utils import concat_ndarray_dicts


class PreprocessedTrainingData:
    """
    Class for encoding the conversations of an agent's JSON data into ndarrays
    and tensorflow datasets.
    """

    def __init__(self, agent_data: dict):
        config = agent_data['config']
        self.intents = [d['name'] for d in config['intents']]
        self.tag_types = config['tagTypes']
        self.slots = config['slots']
        self.actions = [d['name'] for d in config['actions']]

        # Field encoders
        self.enc_context = EncodingContext(intent=LabelBinarizer(), action=LabelBinarizer(),
                                           tags=MultiLabelBinarizer(), slots=MultiLabelBinarizer(),
                                           action_index=LabelEncoder(), utterance=TextEncoder())

        self.enc_context.fit(intent=self.intents, action=self.actions, tags=[self.tag_types],
                             slots=[self.slots], action_index=self.actions)

        raw_convs = agent_data['trainingConversations']
        self.conversations = [Conversation.from_json(c) for c in raw_convs]

        encoded_convs, self.max_len = self._encode_conversations(self.conversations)
        self.encoded_convs = self._aggregate_encoded_convs(encoded_convs)
        self.input_dim = self.encoded_convs['feature_vec'].shape[-1]
        self.num_actions = len(self.actions)
        self.num_intents = len(self.intents)
        self.num_slots = len(self.slots)
        self.num_tag_types = len(self.tag_types)
        self.num_convs = len(self.conversations)

        print('Num actions:', self.num_actions)
        print('Num intents:', self.num_intents)
        print('Num tags:', self.num_tag_types)
        print('Num slots:', self.num_slots)
        print('Num encoded conversations:', self.num_convs)

    def encode_raw_conversations(self, conversations: t.List[dict]) -> t.Dict[str, np.ndarray]:
        """Encode raw conversation JSON data into a dictionary of numpy arrays ready to pass into a neural net.

        Parameters
        ----------
        conversations : t.List[dict]
            A list of raw JSON conversations.

        Returns
        -------
        t.Dict[str, np.ndarray]
            The dictionary of numpy arrays.
        """
        convs = [Conversation.from_json(c) for c in conversations]
        encoded_convs, _ = self._encode_conversations(convs)
        return self._aggregate_encoded_convs(encoded_convs)

    def _encode_conversations(self, conversations: t.List[Conversation]) \
            -> t.Tuple[t.List[t.Dict[str, np.ndarray]], int]:

        encoded_convs = []
        for conv in conversations:
            encoded_conv = conv.encode(enc_context=self.enc_context)
            encoded_convs.append(encoded_conv)

        max_conv_len = max([c['feature_vec'].shape[0] for c in encoded_convs])
        return encoded_convs, max_conv_len

    def _aggregate_encoded_convs(self, encoded_convs: t.List[t.Dict[str, np.ndarray]]) -> t.Dict[str, np.ndarray]:
        for conv in encoded_convs:
            conv_len = conv['feature_vec'].shape[0]
            for k, v in conv.items():
                # Pad the conversation feature v with zeros so that all features are the same length.
                pad_width = [(0, 0)] * v.ndim
                pad_width[0] = (self.max_len - v.shape[0], 0)  # pre padding along the conv turn dimension
                padded_v = np.pad(v, pad_width=pad_width, constant_values=0)
                conv[k] = padded_v

            # Compute a mask for conversation v so that padding is not factored into the loss function.
            mask = np.zeros((self.max_len, 1))
            mask[0:conv_len] = 1
            conv['conversation_mask'] = mask

        for conv in encoded_convs:
            for k, v in conv.items():
                assert v.shape[0] == self.max_len

        result = concat_ndarray_dicts(encoded_convs, new_axis=True)
        return result

    def to_classifier_dataset(self) -> tf.data.Dataset:
        """
        Makes a dataset with the next agent action indices as Y and all
        other features as X.
        """
        y_name = "action"
        X = {k: v for k, v in self.encoded_convs.items() if k != y_name}
        y = self.encoded_convs[y_name]
        return tf.data.Dataset.from_tensor_slices((X, y))
