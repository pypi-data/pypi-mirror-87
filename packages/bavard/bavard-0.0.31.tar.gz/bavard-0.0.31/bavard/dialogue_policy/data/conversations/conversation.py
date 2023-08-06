import typing as t
from dataclasses import dataclass
from typing import Union, List, Tuple, Dict

import numpy as np

from bavard.dialogue_policy.constants import MAX_UTTERANCE_LEN
from bavard.dialogue_policy.data.conversations.actions import AgentAction, Actor
from bavard.dialogue_policy.data.conversations.dialogue_turns import UserDialogueTurn, AgentDialogueTurn
from bavard.dialogue_policy.data.utils import EncodingContext, Jsonable, Encodable
from bavard.dialogue_policy.data.utils import concat_ndarray_dicts


@dataclass
class Conversation(Encodable, Jsonable):
    def __init__(self, turns: List[Union[AgentDialogueTurn, UserDialogueTurn]]):
        self.turns = turns
        self.num_agent_turns = sum(1 for turn in self.turns if turn.actor == Actor.AGENT)
        self.is_last_turn_user = False if len(self.turns) == 0 else self.turns[-1].actor == Actor.USER

    def encode(self, enc_context: EncodingContext) \
            -> Dict[str, np.ndarray]:
        """
        Encodes the conversation into a 2D matrix, wich includes binarized encodings
        of the user and agent actions taken at each turn. Axis 0 is the time dimension;
        one row for each agent action taken. Also encodes a Y matrix; a one hot representation
        of the agent action taken at each timestep. The whole matrix can be treated as a training
        example for a sequence-based neural network, with each row being a time step in the
        sequence.
        """

        last_user_turn: t.Optional[UserDialogueTurn] = None
        last_agent_turn: t.Optional[AgentDialogueTurn] = None

        def encode_last_user_turn() -> t.Dict[str, np.ndarray]:
            if last_user_turn:
                return last_user_turn.encode(enc_context=enc_context)
            else:
                return UserDialogueTurn.encode_null(enc_context)

        def encode_last_agent_turn() -> np.ndarray:
            if last_agent_turn:
                return last_agent_turn.encode(enc_context=enc_context)
            else:
                return AgentDialogueTurn.encode_null(enc_context)

        def encode_agent_output_action(action: AgentAction) -> int:
            assert action.actor == Actor.AGENT
            return action.encode_index(enc_context)

        encoded_turns: List[Dict[str, np.ndarray]] = []

        def get_encoded_turn(next_turn):
            user_turn_features = encode_last_user_turn()
            agent_feature_vec = encode_last_agent_turn()

            feature_vec = np.concatenate([
                user_turn_features['feature_vec'],
                agent_feature_vec
            ], axis=-1)

            action = None
            if next_turn.actor == Actor.AGENT:
                # next action
                action = np.expand_dims(encode_agent_output_action(next_turn.action), axis=-1)

            return {
                'feature_vec': feature_vec,
                'utterance_ids': user_turn_features['utterance_ids'],
                'utterance_mask': user_turn_features['utterance_mask'],
                'action': action
            }

        for i, turn in enumerate(self.turns):
            if turn.actor == Actor.USER:
                last_user_turn = turn

                # If conversation ends with a user turn.
                if i == len(self.turns) - 1:
                    encoded_turns.append(get_encoded_turn(turn))
            else:
                encoded_turns.append(get_encoded_turn(turn))
                last_agent_turn = turn

        result = concat_ndarray_dicts(encoded_turns)
        return result

    @classmethod
    def encode_null(cls, enc_context: EncodingContext):
        raise NotImplementedError()

    def make_validation_pairs(self) -> Tuple[List["Conversation"], List[str]]:
        """
        Expands this conversation into as many conversations as possible,
        under the constraint that each conversation end with a user action
        and have an agent action following it.
        """
        cls = self.__class__
        val_convs = []
        next_actions = []
        for conv in self.expand():
            val_convs.append(cls(conv.turns[:-1]))
            next_actions.append(conv.turns[-1].action.action_name)
        return val_convs, next_actions

    def expand(self) -> List["Conversation"]:
        cls = self.__class__
        convs = []
        for i in range(len(self)):
            if i > 0 and self.turns[i].actor == Actor.AGENT:
                convs.append(cls(self.turns[:i + 1]))
        return convs

    @classmethod
    def from_json(cls, data: dict) -> "Conversation":
        turns = []
        for turn in data['turns']:
            if Actor(turn['actor']) == Actor.USER:
                turns.append(UserDialogueTurn.from_json(turn))
            else:
                assert Actor(turn['actor']) == Actor.AGENT
                turns.append(AgentDialogueTurn.from_json(turn))

        return cls(turns)

    def to_json(self):
        return {
            'turns': [x.to_json() for x in self.turns]
        }

    @staticmethod
    def get_encoding_shape(enc_context: EncodingContext) -> t.Dict[str, t.Tuple[int, int]]:
        """Returns the encoding dimensionality of one row of `X`.
        """
        n_features = AgentDialogueTurn.get_encoding_shape(enc_context)[1] \
            + UserDialogueTurn.get_encoding_shape(enc_context)['feature_vec'][1]
        return {
            'feature_vec': (1, n_features),
            'utterance_ids': (1, MAX_UTTERANCE_LEN),
            'utterance_mask': (1, MAX_UTTERANCE_LEN),
            'action': (1, enc_context.get_size('action'))
        }

    def __len__(self):
        return len(self.turns)
