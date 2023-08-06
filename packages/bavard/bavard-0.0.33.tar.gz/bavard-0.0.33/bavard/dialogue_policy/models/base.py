import datetime
import typing as t
from abc import ABC, abstractmethod

import tensorflow as tf

from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, classification_report
import kerastuner as kt

from bavard.common.utils import leave_one_out, aggregate_dicts
from bavard.common.serialization import Persistent
from bavard.dialogue_policy.data.agent import AgentDataUtils


class BaseModel(ABC, Persistent):
    """
    Allows an inheriting dialogue policy base model to automatically
    inherit serialization and evaluation functionality. Also ensures the
    model has the correct fit and predict API (if the abstract methods are
    implemented in the way requested.)
    """

    @abstractmethod
    def fit(self, agent: dict) -> None:
        """Should fit on an agent's raw JSON data file.
        """
        pass

    @abstractmethod
    def predict(self, conversations: t.List[dict]) -> t.List[str]:
        """
        Should take in raw conversations and for each one output the name
        of the agent action that should be taken next.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_hp_spec(hp: kt.HyperParameters) -> t.Dict[str, kt.engine.hyperparameters.HyperParameter]:
        """
        In order to support hyperparameter tuning, this method should be implemented which
        accepts a kerastuner hyperparameter sampling argument `hp`, and returns a mapping
        of all hyperparameter names to their sampling specification. See
        https://keras-team.github.io/keras-tuner/documentation/hyperparameters/ for more
        info.
        """
        pass

    def get_params(self) -> dict:
        return {name: getattr(self, name) for name in self.get_hp_spec(kt.HyperParameters())}

    def set_params(self, **params):
        param_names = self.get_params().keys()
        for k, v in params.items():
            if k not in param_names:
                raise ValueError(f"{k} is not a known hyperparameter")
            setattr(self, k, v)

    def evaluate(self, agent: dict, *, test_ratio: float = None, nfolds: int = None) -> dict:
        """
        Performs cross validation to evaluate the model's training set performance
        and generalizable performance on `agent`.

        Parameters
        ----------
        agent : dict
            The agent to train and evaluate on.
        test_ratio : float
            If provided, a basic stratified train/test split will be used.
        nfolds : int
            If provided, stratified k-fold cross validation will be conducted with `k==nfolds`.
        """
        if test_ratio is not None and nfolds is not None:
            raise ValueError("please supply either test_ratio or nfolds, but not both")

        if test_ratio is not None:
            return self._evaluate_train_test(agent, test_ratio)
        elif nfolds is not None:
            return self._evaluate_kfold_cv(agent, nfolds)
        else:
            raise ValueError("please supply either test_ratio or nfolds")

    def _evaluate_train_test(self, agent: dict, test_ratio: float) -> dict:
        # Evaluate the model on a basic train/test split.
        train_agent, test_agent = AgentDataUtils.split(agent, test_ratio)
        return self._evaluate(train_agent, test_agent)

    def _evaluate_kfold_cv(self, agent: dict, nfolds: int) -> dict:
        # Evaluate the model using k-fold cross validation.
        folds = AgentDataUtils.to_folds(agent, nfolds)
        results = []
        for test_fold, train_folds in leave_one_out(folds):
            train_agent = AgentDataUtils.concat(*train_folds)
            results.append(self._evaluate(train_agent, test_fold))

        # Now average the k performance results.
        performance = aggregate_dicts(results, "mean")
        return performance

    def _evaluate(self, train_agent: dict, test_agent: dict) -> dict:
        self.fit(train_agent)
        scores = {}
        scores.update({f"train_{k}": v for k, v in self.score(train_agent).items()})
        scores.update({f"test_{k}": v for k, v in self.score(test_agent).items()})
        return scores

    def score(self, agent: dict) -> dict:
        convs, next_actions = AgentDataUtils.make_validation_pairs(agent)
        predicted_actions = [pred["value"] for pred in self.predict(convs)]
        return {
            "f1_macro": f1_score(next_actions, predicted_actions, average="macro"),
            "accuracy": accuracy_score(next_actions, predicted_actions),
            "classification_report": classification_report(next_actions, predicted_actions, output_dict=True),
            "confusion_matrix": confusion_matrix(next_actions, predicted_actions)
        }

    @classmethod
    def tune(
        cls,
        agent: dict,
        *,
        val_ratio: float = None,
        nfolds: int = None,
        strategy: str = "bayesian",
        max_trials: int = 100,
        callback: t.Callable = None
    ):
        """
        Performs hyperparameter optimization of the model over `agent`. Optimizes
        (maximizes) the validation set f1 macro score.

        Parameters
        ----------
        agent : dict
            The raw agent JSON to optimize over.
        val_ratio : float, optional
            The % of the agent's training conversations to use for the
            validation set (randomly selected).
        nfolds : int, optional
            The number of folds to do in k-fold cross validation.
        strategy : str, optional
            The optimization strategy to use.
        max_trials : int, optional
            The maximum number of optimization trials to run.
        callback : function, optional
            Optional callback function that will be invoked at the end of every
            tuning trial. Invoked with the parameters
            `callback(model: BaseModel, test_performance: dict)`, which
            yields the model from the completed trial, as well as that model's
            test set performance.
        """
        hypermodel = HyperModel(cls)
        tuner = ModelTuner(hypermodel, strategy, max_trials)
        tuner.search(agent, test_ratio=val_ratio, nfolds=nfolds, callback=callback)

        print("Tuning Results:")
        tuner.results_summary()

        best_hps, = tuner.get_best_hyperparameters()
        print("Best hyperparameters found:")
        print(best_hps.values)

    def get_tensorboard_cb(self) -> tf.keras.callbacks.TensorBoard:
        log_dir = f"logs/{self.__class__.__name__}/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        return tf.keras.callbacks.TensorBoard(log_dir=log_dir)


class HyperModel(kt.HyperModel):

    def __init__(self, ModelClass: t.Type[BaseModel]) -> None:
        super().__init__()
        self._ModelClass = ModelClass

    def build(self, hp: kt.HyperParameters) -> BaseModel:
        """
        Builds, compiles, and returns a new `self._ModelClass` instance. Uses
        `kerastuner` Hyperparameter objects as the model hyperparameters,
        so it can be searched via hyperparameter optimization.
        """
        return self._ModelClass(**self._ModelClass.get_hp_spec(hp))


class ModelTuner(kt.engine.base_tuner.BaseTuner):
    strategy_map = {
        "bayesian": kt.oracles.BayesianOptimization,
        "random": kt.oracles.RandomSearch
    }

    def __init__(
        self,
        hypermodel: HyperModel,
        strategy: str,
        max_trials: int,
    ) -> None:
        super().__init__(
            oracle=self.strategy_map[strategy](
                objective=kt.Objective("test_f1_macro", "max"), max_trials=max_trials
            ),
            hypermodel=hypermodel
        )

    def run_trial(self, trial, agent: dict, test_ratio: float, nfolds: int, callback: t.Callable) -> None:
        """Each trial of the optimizer is a call to `BaseModel.evaluate`.
        """
        model = self.hypermodel.build(trial.hyperparameters)
        performance = model.evaluate(agent, test_ratio=test_ratio, nfolds=nfolds)
        if callback:
            callback(model, performance)
        tf.keras.backend.clear_session()
        del model
        self.oracle.update_trial(trial.trial_id, {"test_f1_macro": performance["test_f1_macro"]})
