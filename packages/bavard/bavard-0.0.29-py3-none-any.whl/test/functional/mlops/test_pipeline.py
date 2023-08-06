from unittest import TestCase

from fastapi.testclient import TestClient

from bavard.mlops.pipeline import ChatbotPipeline
from test.utils import load_json_file


class TestChatbotPipeline(TestCase):
    def setUp(self) -> None:
        self.agent_with_convs = load_json_file("test/data/dialogue_policy/agents/bavard-dialogue.json")
        self.agent_no_convs = load_json_file("test/data/nlu/bavard.json")
        self.save_path = "test-model"
        self.test_conv = {
            "turns": [
                {
                    "actor": "USER",
                    "state": {
                        "slots": {}
                    },
                    "userAction": {
                        "type": "UTTERANCE_ACTION",
                        "utterance": "Good morning.",
                        "intent": ""
                    }
                }
            ]
        }

    def test_can_fit_predict(self):
        pipe = ChatbotPipeline({"nlu": {"epochs": 1}, "dp": {"epochs": 1}})
        pipe.fit(self.agent_with_convs)

        # Predictions should be valid values.
        preds = pipe.predict([self.test_conv])
        self._assert_predictions_are_valid(self.agent_with_convs, preds, True)

        # Model should be able to be persisted, loaded, and still work.
        pipe.to_dir(self.save_path)
        loaded_pipe = ChatbotPipeline.from_dir(self.save_path, delete=True)
        preds = loaded_pipe.predict([self.test_conv])
        self._assert_predictions_are_valid(self.agent_with_convs, preds, True)

        # Model should be able to work as a web service.
        app = pipe.to_app()
        client = TestClient(app)

        res = client.get("/")
        self.assertEqual(res.status_code, 200)

        res = client.post(
            "/predict", json={"instances": [self.test_conv]}
        )
        self.assertEqual(res.status_code, 200)
        predictions = res.json()
        self._assert_predictions_are_valid(self.agent_with_convs, predictions, True)

    def test_can_fit_predict_no_convs(self):
        pipe = ChatbotPipeline({"nlu": {"epochs": 1}, "dp": {"epochs": 1}})
        pipe.fit(self.agent_no_convs)

        # Predictions should be valid values.
        preds = pipe.predict([self.test_conv])
        self._assert_predictions_are_valid(self.agent_no_convs, preds, False)

    def _assert_predictions_are_valid(self, agent: dict, preds: dict, has_dp: bool):
        intents = agent["nluData"]["intents"]
        actions = {action["name"] for action in agent["config"]["actions"]}
        for pred in preds["predictions"]:
            self.assertIn(pred["nlu"]["intent"]["value"], intents)
            if has_dp:
                self.assertIn(pred["dp"]["value"], actions)
            else:
                self.assertIsNone(pred["dp"])
