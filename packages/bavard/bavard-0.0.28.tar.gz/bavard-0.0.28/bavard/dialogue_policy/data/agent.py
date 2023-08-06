import typing as t
from collections import defaultdict

from sklearn.model_selection import train_test_split

from bavard.dialogue_policy.data.conversations.conversation import Conversation
from bavard.dialogue_policy.data.conversations.actions import Actor


class AgentDataUtils:

    """Utilities for interacting with the training conversations of an agent."""

    @staticmethod
    def split(
        agent: dict, split_ratio: float, shuffle: bool = True, seed: int = 0
    ) -> tuple:
        """Splits `agent` into two different training/test conversation sets."""
        convs = agent["trainingConversations"]
        convs_a, convs_b = train_test_split(
            convs,
            test_size=split_ratio,
            random_state=seed,
            shuffle=shuffle,
        )
        return (
            AgentDataUtils.build_from_convs(convs_a),
            AgentDataUtils.build_from_convs(convs_b),
        )

    @staticmethod
    def make_validation_pairs(agent: dict) -> t.Tuple[list, list]:
        """
        Takes all the conversations in `agent` and expands them into
        many conversations, with all conversations ending with a user
        action.

        Returns
        -------
        tuple of lists
            The first list is the list of raw conversations. The second
            is the list of the names of the next actions that should
            be taken, given the conversations; one action per conversation.
        """
        all_convs = []
        all_next_actions = []
        for conv in agent["trainingConversations"]:
            convs, next_actions = Conversation.from_json(conv).make_validation_pairs()
            all_convs += [c.to_json() for c in convs]
            all_next_actions += next_actions
        return all_convs, all_next_actions

    @staticmethod
    def build_from_convs(conversations: t.List[dict]) -> dict:
        """Builds an agent JSON from raw conversations only."""

        actions = set()
        intents = set()
        tag_types = set()
        slot_names = set()

        for conv in conversations:
            for turn in conv['turns']:
                if turn['actor'] == 'AGENT':
                    actions.add(turn['agentAction']['name'])
                else:
                    action_body = turn['userAction']
                    intents.add(action_body['intent'])
                    tag_types.update(tag['tagType'] for tag in action_body['tags'])
                    slot_names.update(turn['state']['slots'].keys())

        return {
            'config': {
                'actions': [{"name": action} for action in actions],
                'intents': [{"name": intent} for intent in intents],
                'tagTypes': list(tag_types),
                'slots': list(slot_names),
            },
            'trainingConversations': conversations
        }

    @staticmethod
    def get_action_distribution(agent: dict) -> dict:
        """
        Counts the number of each type of action present in `agent`'s training
        conversations.
        """
        counts = defaultdict(int)
        for conv in agent["trainingConversations"]:
            for turn in conv["turns"]:
                if Actor(turn["actor"]) == Actor.AGENT:
                    counts[turn["agentAction"]["name"]] += 1
        return counts
