from unittest import TestCase
import typing as t

from bavard.dialogue_policy.models import Classifier
from bavard.dialogue_policy.data.agent import AgentDataUtils
from test.utils import load_json_file


class TestModel(TestCase):

    def setUp(self) -> None:
        self.agent = load_json_file("test/data/dialogue_policy/agents/bavard-dialogue.json")

    def test_can_fit_and_predict(self) -> None:
        convs, _ = AgentDataUtils.make_validation_pairs(self.agent)

        model = Classifier(epochs=1)
        model.fit(self.agent)

        # Predicted actions should be valid actions
        self._assert_can_predict(model, convs)

        # Model should be able to be serialized and deserialized and still work.
        model.to_dir("temp-model")
        loaded_model = Classifier.from_dir("temp-model", True)
        self._assert_can_predict(loaded_model, convs)

    def _assert_can_predict(self, model: Classifier, convs: t.List[dict]):
        preds = model.predict(convs)
        # Predicted actions should be valid actions
        for pred in preds:
            self.assertIn(pred["value"], model._preprocessor.enc_context.classes_("action"))
