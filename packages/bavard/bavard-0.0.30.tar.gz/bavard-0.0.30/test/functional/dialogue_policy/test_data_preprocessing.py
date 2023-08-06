from unittest import TestCase

from bavard.dialogue_policy.data.conversations.conversation import Actor, Conversation
from bavard.dialogue_policy.data.preprocessed_data import PreprocessedTrainingData
from test.utils import load_json_file


class TestDataPreprocessing(TestCase):
    def setUp(self) -> None:
        self.agent = load_json_file("test/data/dialogue_policy/agents/mwoz2_2_hotel_dialogs.json")
        self.conv_last_turn_user = load_json_file("test/data/dialogue_policy/conversations/last-turn-user.json")
        self.conv_single_turn = load_json_file("test/data/dialogue_policy/conversations/length-one.json")

    def test_preprocessor(self) -> None:
        # Should process all conversations
        preprocessor = PreprocessedTrainingData(self.agent)
        self.assertEqual(len(preprocessor.conversations), len(self.agent["trainingConversations"]))

        # Should encode actions (y) correctly.
        for i, conv in enumerate(preprocessor.conversations):
            y = preprocessor.encoded_convs['action'][i][-conv.num_agent_turns:]  # account for padding
            agent_actions = [turn.action.action_name for turn in conv.turns if turn.actor == Actor.AGENT]
            deprocessed_agent_actions = preprocessor.enc_context.inverse_transform("action_index", y)
            self.assertTrue(agent_actions, deprocessed_agent_actions)

        # Should encode X properly.
        for i, conv in enumerate(preprocessor.conversations):
            X = preprocessor.encoded_convs['feature_vec'][i][-conv.num_agent_turns:]  # account for padding
            # X should have one row for every agent turn.
            self.assertEqual(X.shape[0], conv.num_agent_turns)
            # X should have correct number of columns
            self.assertEqual(X.shape[1], Conversation.get_encoding_shape(preprocessor.enc_context)['feature_vec'][1])

    def test_preprocessor_inference_time(self) -> None:
        # Should be an extra row during inference time when a user action was last.
        # (The extra row is for that last user action.)
        preprocessor = PreprocessedTrainingData(self.agent)
        Conversation.from_json(self.conv_last_turn_user)

        encoded_conv = preprocessor.encode_raw_conversations([self.conv_last_turn_user])
        self.assertEqual(
            encoded_conv['feature_vec'].shape[-1],
            Conversation.get_encoding_shape(preprocessor.enc_context)['feature_vec'][-1]
        )

        # Should be able to handle single turn conversations.
        X = preprocessor.encode_raw_conversations([self.conv_single_turn])
        self.assertEqual(X['feature_vec'].shape[0], 1)
