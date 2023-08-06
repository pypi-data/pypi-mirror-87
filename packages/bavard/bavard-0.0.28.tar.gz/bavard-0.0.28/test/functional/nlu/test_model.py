import json
from unittest import TestCase
from pathlib import Path

from fastapi.testclient import TestClient

from bavard.nlu.model import NLUModel


class TestModel(TestCase):
    def setUp(self):
        super().setUp()
        self.model_save_dir = "test-model"
        self.max_model_size_in_gigabytes = 2
        # Translations of the same utterance
        self.prediction_inputs = {
            "eng": "how much is a flight from washington to boston",
            "chi": "从华盛顿飞往波士顿多少钱",
            "rus": "сколько стоит перелет из вашингтона в бостон",
            "spa": "¿Cuánto cuesta un vuelo de Washington a Boston?",
            "fre": "Combien est un vol de Washington à Boston",
        }
        with open("test/data/nlu/test-agent.json") as f:
            self.nlu_data = json.load(f)["nluData"]

        with open("test/data/nlu/bavard.json") as f:
            self.bavard_nlu_data = json.load(f)["nluData"]

    def test_train_and_predict(self):
        # Check that model can build and train without failing.
        model = NLUModel(save_model_dir=self.model_save_dir)
        model.set_params(batch_size=1, epochs=1)
        model.train(self.nlu_data)

        # Check that the saved model is small enough
        saved_model_size = self._get_dir_size(self.model_save_dir, "GB")
        self.assertLessEqual(saved_model_size, self.max_model_size_in_gigabytes)

        # Check that model can handle multiple languages without breaking.
        self._assert_model_can_predict(model)

        # Check that the model can be successfully loaded
        loaded_model = NLUModel.from_dir(self.model_save_dir, delete=True)
        self._assert_model_can_predict(loaded_model)

        # Check that the model can be used as a web service.
        app = loaded_model.to_app()
        client = TestClient(app)

        res = client.get("/")
        self.assertEqual(res.status_code, 200)

        res = client.post(
            "/predict", json={"instances": list(self.prediction_inputs.values())}
        )
        self.assertEqual(res.status_code, 200)
        predictions = res.json()
        self.assertEqual(len(predictions["predictions"]), len(self.prediction_inputs))
        self._assert_predictions_are_valid(predictions)

    def test_evaluate(self):
        # Check that model can evaluate without failing.
        model = NLUModel()
        model.set_params(batch_size=4, epochs=1)
        model.evaluate(self.bavard_nlu_data, test_ratio=0.2)

    def _assert_model_can_predict(self, model: NLUModel) -> None:
        predictions = model.predict(self.prediction_inputs.values())
        self._assert_predictions_are_valid(predictions)

    def _assert_predictions_are_valid(self, predictions: dict) -> None:
        for prediction in predictions["predictions"]:
            self.assertIn(prediction["intent"]["value"], self.nlu_data["intents"])
            for tag in prediction["tags"]:
                self.assertIn(tag["tag_type"], self.nlu_data["tagTypes"])

    def _get_dir_size(self, dir: str, units: str = "GB") -> int:
        """
        Gets the size of the directory at `path`.
        Source: https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
        """
        units_map = {"KB": 1e-3, "MB": 1e-6, "GB": 1e-9}
        path = Path(dir)
        total_bytes = sum(f.stat().st_size for f in path.glob("**/*") if f.is_file())
        return total_bytes * units_map[units]
