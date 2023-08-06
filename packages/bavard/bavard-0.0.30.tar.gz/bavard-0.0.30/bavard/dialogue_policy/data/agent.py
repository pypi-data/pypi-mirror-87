import typing as t
from collections import defaultdict
from itertools import chain

from sklearn.model_selection import train_test_split
from sklearn.utils import resample

from bavard.dialogue_policy.data.conversations.conversation import Conversation
from bavard.dialogue_policy.data.conversations.actions import Actor
from bavard.common.utils import make_stratified_folds


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
    def expand(agent: dict, *, balance: bool = False, seed: int = 0) -> dict:
        """
        Takes `agent` and makes a new agent with all the old agent's training conversations
        expanded into more conversations. Makes as many conversations as possible under the
        constraints that each conversation have the full dialogue from the beginning of the
        conversation forward, and that each conversation end with an agent action, making the
        resulting conversation useful for training dialogue models to decide which agent action
        to take, given a conversation history.
        """
        all_convs: t.List[Conversation] = []
        for raw_conv in agent["trainingConversations"]:
            all_convs += Conversation.from_json(raw_conv).expand()

        if balance:
            # Partition the conversations by their final agent action,
            # then upsample till each action has equal representation.
            convs_by_action = defaultdict(list)
            for conv in all_convs:
                convs_by_action[conv.turns[-1].action.action_name].append(conv)
            n_majority = max(len(examples) for examples in convs_by_action.values())
            all_convs = list(
                chain.from_iterable(
                    resample(convs, replace=True, n_samples=n_majority, random_state=seed)
                    for convs in convs_by_action.values()
                )
            )

        return AgentDataUtils.build_from_convs([c.to_json() for c in all_convs])

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
                    tag_types.update(tag['tagType'] for tag in action_body.get('tags', []))
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

    @staticmethod
    def concat(*agents: t.Tuple[dict]) -> dict:
        """
        Takes the concatenation of multiple agent objects, returning a single agent
        object with all the training conversations included.
        """
        convs = list(chain.from_iterable(agent["trainingConversations"] for agent in agents))
        return AgentDataUtils.build_from_convs(convs)

    @staticmethod
    def to_folds(agent: dict, nfolds: int, *, shuffle: bool = True, seed: int = 0) -> tuple:
        """
        Splits an expanded version of `agent` into `nfolds` random subsets, stratified by action label.
        The stratification will only be accurate when the agents returned by this method are consumed in
        `predict_single` mode.
        """
        convs = AgentDataUtils.expand(agent, balance=False)["trainingConversations"]
        action_labels = [c["turns"][-1]["agentAction"]["name"] for c in convs]
        folds = make_stratified_folds(convs, action_labels, nfolds, shuffle, seed)
        return tuple(AgentDataUtils.build_from_convs(convs) for convs in folds)
