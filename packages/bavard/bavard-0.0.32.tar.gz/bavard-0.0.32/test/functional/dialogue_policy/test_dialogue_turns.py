from unittest import TestCase

from bavard.dialogue_policy.data.conversations.dialogue_turns import UserDialogueTurn, AgentDialogueTurn, DialogueState
from bavard.dialogue_policy.data.conversations.actions import UserAction, AgentAction, Tag, Actor
from test.functional.dialogue_policy.utils import (
    DummyContext, check_user_dialogue_turn_feature_vec, check_agent_action_feature_vec
)


class TestDialogueTurns(TestCase):

    def setUp(self):
        self.ctx = DummyContext()

    def test_user_dialogue_turn_serialization(self):
        turn = UserDialogueTurn(
            DialogueState({"slot3": "foo", "slot1": "bar"}),
            UserAction("intent2", "I utter.", [Tag("tagtype1", "value1")]),
            Actor.USER
        )
        self.assertEqual(turn, UserDialogueTurn.from_json(turn.to_json()))

    def test_user_dialogue_turn_encoding(self):
        turn = UserDialogueTurn.from_json({
            "actor": "USER",
            "userAction": {
                "intent": "intent2",
                "utterance": "This too is an utterance.",
                "tags": [{"tagType": "tagtype1", "value": "value1"}]
            },
            "state": {
                "slots": {
                    "slot3": "foo",
                    "slot1": "bar"
                }
            }
        })
        encoding = turn.encode(self.ctx.enc_context)

        check_user_dialogue_turn_feature_vec(
            encoding["feature_vec"], self.ctx, slots=("slot1", "slot3"), intent="intent2", tag_types=("tagtype1",)
        )

    def test_agent_dialogue_turn_serialization(self):
        turn = AgentDialogueTurn(
            DialogueState({"slot2": "foo"}),
            AgentAction("action2", "I utter also."),
            Actor.AGENT
        )
        self.assertEqual(turn, AgentDialogueTurn.from_json(turn.to_json()))

    def test_agent_dialogue_turn_encoding(self):
        turn = AgentDialogueTurn.from_json({
            "actor": "AGENT",
            "agentAction": {
                "name": "action3",
                "utterance": "This too is an utterance."
            },
            "state": {
                "slots": {
                    "slot2": "foo",
                    "slot3": "bar"
                }
            }
        })
        encoding = turn.encode(self.ctx.enc_context)
        check_agent_action_feature_vec(encoding, self.ctx, action="action3")
