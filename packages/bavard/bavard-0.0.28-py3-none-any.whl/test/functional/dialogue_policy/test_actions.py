from unittest import TestCase

from bavard.dialogue_policy.data.conversations.actions import UserAction, AgentAction, Tag
from test.functional.dialogue_policy.utils import DummyContext, check_agent_action_feature_vec


class TestActions(TestCase):

    def setUp(self):
        self.ctx = DummyContext()

    def test_user_action_serialization(self):
        user_action = UserAction("intent1", "I am uttering.", [Tag("tagtype1", "tagvalue")])
        self.assertEqual(user_action, UserAction.from_json(user_action.to_json()))

    def test_user_action_encoding(self):
        user_action = UserAction(
            "intent1", "I am uttering.", [Tag("tagtype1", "tagvalue"), Tag("tagtype3", "othervalue")]
        )
        encoding = user_action.encode(enc_context=self.ctx.enc_context)
        # Shape should be correct
        self.assertEqual(encoding['feature_vec'].shape,
                         (1, len(self.ctx.intents)
                          + len(self.ctx.tag_types)))
        # Content should be correct
        enc_intent = encoding["feature_vec"][:, :len(self.ctx.intents)]
        self.assertEqual(self.ctx.enc_context.inverse_transform("intent", enc_intent)[0], "intent1")
        tags_enc = encoding["feature_vec"][:, -len(self.ctx.tag_types):]
        self.assertEqual(self.ctx.enc_context.inverse_transform("tags", tags_enc)[0], ("tagtype1", "tagtype3"))

    def test_agent_action_serialization(self):
        agent_action = AgentAction("action2", "I am uttering also.")
        self.assertEqual(agent_action, AgentAction.from_json(agent_action.to_json()))

    def test_agent_action_encoding(self):
        agent_action = AgentAction("action2", "I am uttering also.")
        encoding = agent_action.encode(enc_context=self.ctx.enc_context)
        check_agent_action_feature_vec(encoding, self.ctx, action="action2")
