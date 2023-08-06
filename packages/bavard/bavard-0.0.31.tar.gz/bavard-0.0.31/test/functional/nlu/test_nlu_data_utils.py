from unittest import TestCase
import json

from bavard.nlu.data_preprocessing.nlu_data import NLUDataUtils


class TestNLUDataUtils(TestCase):
    def setUp(self) -> None:
        with open("test/data/nlu/bavard.json") as f:
            self.nlu_data = json.load(f)["nluData"]

    def test_balance_by_intent(self) -> None:

        intent_distribution = NLUDataUtils.get_intent_distribution(self.nlu_data)
        majority_class_n = intent_distribution.most_common(1)[0][1]

        balanced = NLUDataUtils.balance_by_intent(self.nlu_data)
        balanced_intents = NLUDataUtils.get_intents(balanced["examples"])

        # The intents should still be the same
        self.assertSetEqual(set(self.nlu_data["intents"]), set(balanced_intents))
        # Each intent's examples should have been upsampled.
        balanced_intent_distribution = NLUDataUtils.get_intent_distribution(balanced)
        for intent in self.nlu_data["intents"]:
            self.assertEqual(balanced_intent_distribution[intent], majority_class_n)
