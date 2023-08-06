import typing as t
from dataclasses import dataclass, field
from enum import Enum

import numpy as np

from bavard.dialogue_policy.constants import MAX_UTTERANCE_LEN
from bavard.dialogue_policy.data.utils import Encodable, Jsonable, EncodingContext


class Actor(Enum):
    USER = 'USER'
    AGENT = 'AGENT'


@dataclass
class Tag(Jsonable):
    tagType: str
    value: str

    @classmethod
    def from_json(cls, data: dict) -> "Tag":
        return Tag(data["tagType"], data["value"])


@dataclass
class UserAction(Encodable, Jsonable):
    intent: str
    utterance: str = ''
    tags: t.List[Tag] = field(default_factory=list)
    actor = Actor.USER

    def encode(self, enc_context: EncodingContext) -> t.Dict[str, np.ndarray]:

        # feature vec
        encoded_intent = enc_context.transform("intent", [self.intent])
        encoded_tags = enc_context.transform("tags", [[tag.tagType for tag in self.tags]])
        feature_vec = np.concatenate([encoded_intent, encoded_tags], axis=1)
        utterance_encoding = enc_context.transform("utterance", self.utterance)

        return {
            "feature_vec": feature_vec,
            "utterance_ids": utterance_encoding["input_ids"],
            "utterance_mask": utterance_encoding["input_mask"],
        }

    @classmethod
    def get_encoding_shape(cls, enc_context: EncodingContext) -> t.Dict[str, t.Tuple[int, int]]:
        return {
            "feature_vec": (1, enc_context.get_size("intent") + enc_context.get_size("tags")),
            "utterance_ids": (1, MAX_UTTERANCE_LEN),
            "utterance_mask": (1, MAX_UTTERANCE_LEN),
        }

    def to_json(self) -> dict:
        return {
            "intent": self.intent,
            "utterance": self.utterance,
            "tags": [tag.to_json() for tag in self.tags]
        }

    @classmethod
    def from_json(cls, data: dict) -> "UserAction":
        return cls(data["intent"], data.get("utterance"), [Tag.from_json(tag) for tag in data.get("tags", [])])

    @classmethod
    def encode_null(cls, enc_context: EncodingContext, dtype: t.Type = np.int32) \
            -> t.Dict[str, np.ndarray]:
        return {
            'feature_vec': np.zeros(cls.get_encoding_shape(enc_context), dtype=dtype),
            'utterance_ids': np.zeros((1, MAX_UTTERANCE_LEN)),
            'utterance_mask': np.zeros((1, MAX_UTTERANCE_LEN)),
        }


@dataclass
class AgentAction(Encodable, Jsonable):
    action_name: str
    utterance: str = ''
    actor = Actor.AGENT

    def encode(self, enc_context: EncodingContext):
        # TODO: include utternance encoding
        return enc_context.transform("action", [self.action_name])

    def encode_index(self, enc_context: EncodingContext) -> int:
        return enc_context.transform("action_index", [self.action_name])[0]

    @classmethod
    def encode_null(cls, enc_context: EncodingContext, dtype: t.Type = np.int32) -> np.ndarray:
        return np.zeros(cls.get_encoding_shape(enc_context), dtype=dtype)

    @classmethod
    def get_encoding_shape(cls, enc_context: EncodingContext) -> t.Tuple[int, int]:
        return 1, enc_context.get_size("action")

    def to_json(self) -> dict:
        return {
            "name": self.action_name,
            "utterance": self.utterance
        }

    @classmethod
    def from_json(cls, data: dict) -> "AgentAction":
        return cls(data["name"], data.get("utterance"))
