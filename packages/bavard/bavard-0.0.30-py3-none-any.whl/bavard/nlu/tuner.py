"""
@TODO: Test the classes in this module.
"""
import kerastuner as kt
import tensorflow as tf

from bavard.nlu.model import NLUModel
from bavard.nlu.auto_setup import AutoSetup


class HyperNLUModelFactory(kt.HyperModel):

    def __init__(self, *args, **kwargs) -> None:
        # These will be forwarded on to the `NLUModel` constructor
        # when it is called by `build`.
        self.args = args
        self.kwargs = kwargs

    def build(self, params: kt.HyperParameters) -> NLUModel:
        """
        Builds, compiles, and returns a new `NLUModel` instance. Uses
        `kerastuner` Hyperparameter objects as the model hyperparameters,
        so it can be searched via hyperparameter optimization.
        """
        nlu_params = {
            "hidden_size": params.Int("hidden_size", 32, 512, default=256),
            "dropout": params.Float("dropout", 0.0, 0.6, default=0.1),
            "l2_regularization": params.Float("l2_regularization", 1e-12, 0.1, sampling="log"),
            "n_hidden_layers": params.Int("n_hidden_layers", 1, 5),
            "fine_tune_embedder": params.Boolean("fine_tune_embedder", default=True),
            "learning_rate": params.Float("learning_rate", 1e-7, 0.1, sampling="log", default=5e-5),
            "epochs": params.Int("epochs", 5, 200, step=5, default=AutoSetup.default_num_epochs),
            "intent_block_type": params.Choice("intent_block_type", ["dense", "lstm"]),
            "balance_intent": params.Boolean("balance_intent", default=False),
            "batch_size": params.Choice("batch_size", [2**2, 2**3, 2**4, 2**5, 2**6])
        }
        kwargs = {k: v for k, v in self.kwargs.items()}
        kwargs.update(nlu_params)
        model = NLUModel(*self.args, **kwargs)
        return model


class NLUModelTuner(kt.engine.base_tuner.BaseTuner):
    strategy_map = {
        "bayesian": kt.oracles.BayesianOptimization,
        "random": kt.oracles.RandomSearch
    }

    def __init__(self, hypermodel: kt.HyperModel, strategy: str, max_trials: int, project_name: str = None) -> None:
        super().__init__(
            oracle=self.strategy_map[strategy](
                objective=kt.Objective("intent_acc", "max"), max_trials=max_trials
            ),
            hypermodel=hypermodel,
            project_name=project_name
        )

    def run_trial(self, trial, nlu_data: dict, test_ratio: float, nfolds: int, repeat: int) -> None:
        """
        Each trial of the optimizer is a call to `NLUModel.evaluate`.
        """
        model = self.hypermodel.build(trial.hyperparameters)
        _, test_performance = model.evaluate(nlu_data, test_ratio=test_ratio, nfolds=nfolds, repeat=repeat)
        tf.keras.backend.clear_session()
        del model
        self.oracle.update_trial(trial.trial_id, test_performance)
