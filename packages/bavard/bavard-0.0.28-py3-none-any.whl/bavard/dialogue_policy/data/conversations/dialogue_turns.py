import typing as t
from dataclasses import dataclass, field

import numpy as np

from bavard.dialogue_policy.constants import MAX_UTTERANCE_LEN
from bavard.dialogue_policy.data.conversations.actions import Actor, AgentAction, UserAction
from bavard.dialogue_policy.data.utils import Encodable, Jsonable, EncodingContext


@dataclass
class DialogueState(Encodable, Jsonable):
    slots: t.Dict[str, str] = field(default_factory=dict)

    def encode(self, enc_context: EncodingContext) -> np.ndarray:
        # Encodes the names of the slots that are filled.
        encoded_slots = enc_context.transform("slots", [list(self.slots.keys())])
        return encoded_slots

    @classmethod
    def encode_null(cls, enc_context: EncodingContext) -> np.ndarray:
        raise NotImplementedError()

    @classmethod
    def from_json(cls, data: dict) -> "DialogueState":
        return cls(data["slots"])

    @staticmethod
    def get_encoding_shape(enc_context: EncodingContext) -> t.Tuple[int, int]:
        return 1, enc_context.get_size("slots")


@dataclass
class DialogueTurn:
    state: DialogueState
    action: t.Union[UserAction, AgentAction]
    actor: Actor


@dataclass
class UserDialogueTurn(DialogueTurn, Jsonable, Encodable):
    action: UserAction
    actor = Actor.USER

    def encode(self, enc_context: EncodingContext) -> t.Dict[str, np.ndarray]:
        encoded_state = self.state.encode(enc_context)
        encoded_action = self.action.encode(enc_context=enc_context)
        feature_vec = np.concatenate([encoded_state, encoded_action['feature_vec']], axis=-1)
        return {
            'feature_vec': feature_vec,
            'utterance_ids': encoded_action['utterance_ids'],
            'utterance_mask': encoded_action['utterance_mask'],
        }

    @classmethod
    def encode_null(cls, enc_context: EncodingContext) -> t.Dict[str, np.ndarray]:
        return {k: np.zeros(v) for k, v in cls.get_encoding_shape(enc_context).items()}

    @staticmethod
    def get_encoding_shape(enc_context: EncodingContext) -> t.Dict[str, t.Tuple[int, int]]:
        feature_vec_shape = (
            1, DialogueState.get_encoding_shape(enc_context)[1]
            + UserAction.get_encoding_shape(enc_context)['feature_vec'][1]
        )
        return {
            'feature_vec': feature_vec_shape,
            'utterance_ids': (1, MAX_UTTERANCE_LEN),
            'utterance_mask': (1, MAX_UTTERANCE_LEN),
        }

    @classmethod
    def from_json(cls, data: dict) -> "UserDialogueTurn":
        return cls(DialogueState.from_json(data["state"]),
                   UserAction.from_json(data["userAction"]),
                   Actor(data["actor"]))

    def to_json(self) -> dict:
        return {
            "actor": self.actor.value,
            "userAction": self.action.to_json(),
            "state": self.state.to_json()
        }


@dataclass
class AgentDialogueTurn(DialogueTurn, Jsonable, Encodable):
    action: AgentAction
    actor = Actor.AGENT

    def encode(self, enc_context: EncodingContext) -> np.ndarray:
        return self.action.encode(enc_context)

    @classmethod
    def encode_null(cls, enc_context: EncodingContext) -> np.ndarray:
        return np.zeros(AgentAction.get_encoding_shape(enc_context))

    @staticmethod
    def get_encoding_shape(enc_context: EncodingContext) -> t.Tuple[int, int]:
        return 1, AgentAction.get_encoding_shape(enc_context)[1]

    def to_json(self):
        return {
            "actor": self.actor.value,
            "agentAction": self.action.to_json(),
            "state": self.state.to_json()
        }

    @classmethod
    def from_json(cls, data) -> "AgentDialogueTurn":
        return cls(DialogueState.from_json(data["state"]),
                   AgentAction.from_json(data["agentAction"]),
                   Actor[data["actor"]])
