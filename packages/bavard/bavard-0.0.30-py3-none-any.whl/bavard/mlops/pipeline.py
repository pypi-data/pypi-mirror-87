import typing as t

from bavard.dialogue_policy.models.classifier import Classifier
from bavard.nlu.model import NLUModel
from bavard.dialogue_policy.data.conversations.actions import Actor
from bavard.mlops.web_service import WebService, endpoint
from bavard.common.serialization import Persistent


class ChatbotPipeline(WebService, Persistent):
    """
    A machine learning pipeline for chatbots that handles NLU parsing
    and dialogue policy prediction.
    """

    def __init__(self, config: dict = None):
        if config is None:
            config = {}
        self._fitted = False
        self._do_dp = False
        self._nlu_model = NLUModel(**config.get("nlu", {}))
        self._dp_model = Classifier(**config.get("dp", {}))

    def fit(self, agent: dict):
        self._nlu_model.train(agent["nluData"])
        if len(agent["trainingConversations"]) > 0:
            self._dp_model.fit(agent)
            self._do_dp = True
        else:
            self._do_dp = False
        self._fitted = True

    @endpoint
    def predict(self, instances: t.List[dict]) -> dict:
        """
        Takes `instances` (a list of conversations) and parses the intent of the final user
        utterance on each of them. Also, predicts the next agent action to take for
        each one.

        Returns
        -------
        dict
            An object with key `predictions` mapping to a list of NLU and DP
            predictions, one for each conversation. Has the form:
            ```json
            {
                "predictions": [
                    {
                        "nlu": {
                            "intent": {
                                "value": <intent_name>,
                                "confidence": <float>
                            },
                            "tags": [
                                {
                                    "tag_type": <tag_name>,
                                    "value": <tag_value>
                                }
                            ]
                        },
                        "dp": {
                            "value": <action_name>,
                            "confidence": <float>
                        }
                    }
                ]
            }
            ```
            If the agent the pipeline was trained on had no training conversations, the pipeline will
            not use a dialogue policy model and the `"dp"` entry for each prediction will be `None`.
        """
        assert self._fitted
        predictions = [{"nlu": None, "dp": None}] * len(instances)

        # Parse the user utterances.
        utterances = [self._get_final_user_utterance(conv) for conv in instances]
        nlu_preds = self._nlu_model.predict(utterances)["predictions"]
        for conv, utterance, pred, nlu_pred in zip(instances, utterances, predictions, nlu_preds):
            # If there is no utterance then the prediction for it won't make sense.
            if utterance:
                pred["nlu"] = nlu_pred
                # The DP model will need to have the NLU intent prediction to make its own
                # action prediction.
                conv["turns"][-1]["userAction"]["intent"] = nlu_pred["intent"]["value"]

        if self._do_dp:
            # Predict the next agent action to take.
            dp_preds = self._dp_model.predict(instances)
            for pred, dp_pred in zip(predictions, dp_preds):
                pred["dp"] = dp_pred
                # We convert from numpy float to python float so it can be JSON serializable
                # (this method is a web service endpoint).
                pred["dp"]["confidence"] = pred["dp"]["confidence"].item()

        return {"predictions": predictions}

    @staticmethod
    def _get_final_user_utterance(conv: dict) -> str:
        """
        Retrieves the user utterance from the most recent
        turn of the conversation. If the most recent turn is not
        a user turn or doesn't have an utterance, returns the empty string.
        """
        if len(conv["turns"]) > 0:
            last_turn = conv["turns"][-1]
            if Actor(last_turn["actor"]) == Actor.USER and last_turn["userAction"]["type"] == "UTTERANCE_ACTION":
                return last_turn["userAction"]["utterance"]
        return ""
