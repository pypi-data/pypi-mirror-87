import datetime
import typing as t
from abc import ABC, abstractmethod

import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Activation, LSTM
import numpy as np
from bavard.common.serialization import Serializer
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, classification_report
from transformers import TFDistilBertModel
import kerastuner as kt

from bavard.dialogue_policy.constants import BASE_LANGUAGE_MODEL
from bavard.dialogue_policy.data.agent import AgentDataUtils


class NLUEmbedder(tf.keras.layers.Layer):
    def __init__(self, trainable: bool = False):
        super().__init__()
        self.trainable = trainable
        self.embed_dim = 768

    def build(self, input_shape):
        ids_shape, _ = input_shape
        self.seq_len = ids_shape[-1]  # the length of each text token sequence
        self.other_dims = [-1 if dim is None else dim for dim in ids_shape[:-1]]
        self.embed = TFDistilBertModel.from_pretrained(BASE_LANGUAGE_MODEL).distilbert
        self.embed.trainable = self.trainable

    def call(self, inputs) -> tf.Tensor:
        input_ids, input_mask = inputs

        input_ids_flat = tf.reshape(input_ids, (-1, self.seq_len))
        input_mask_flat = tf.reshape(input_mask, (-1, self.seq_len))

        token_embeddings = self.embed([input_ids_flat, input_mask_flat])[0]
        pooled_embeddings = token_embeddings[:, 0]

        unflattened = tf.reshape(pooled_embeddings, self.other_dims + [self.embed_dim])
        return unflattened

    def get_config(self) -> dict:
        return {"trainable": self.trainable}


class LSTMBlock(tf.keras.layers.Layer):
    """
    LSTM layer with dropout, batch norm, and l2 regularization included.
    """

    def __init__(
        self,
        units: int = 512,
        dropout: float = 0.0,
        l2: float = 0.0,
        return_sequences: bool = True,
    ):
        super().__init__()
        self.units = units
        self.dropout_rate = dropout
        self.l2_rate = l2
        self.return_sequences = return_sequences

    def build(self, input_shape):
        L2 = tf.keras.regularizers.l2(self.l2_rate) if self.l2_rate > 0 else None
        self.dropout = Dropout(rate=self.dropout_rate)
        self.lstm = LSTM(
            self.units, return_sequences=self.return_sequences, kernel_regularizer=L2
        )
        self.batch_norm = BatchNormalization()

    def call(self, inputs: tf.Tensor, training) -> tf.Tensor:
        X = self.dropout(inputs, training)
        X = self.lstm(X)
        X = self.batch_norm(X)
        return X

    def get_config(self) -> dict:
        return {
            "units": self.units,
            "dropout": self.dropout_rate,
            "l2": self.l2_rate,
            "return_sequences": self.return_sequences,
        }


class DenseBlock(tf.keras.layers.Layer):
    """
    Dense layer with dropout, batch norm, and l2 regularization included.
    """

    def __init__(
        self,
        units: int,
        activation: str = "relu",
        dropout: float = 0.0,
        l2: float = 0.0
    ):
        super().__init__()
        self.units = units
        self.activation = activation
        self.dropout_rate = dropout
        self.l2_rate = l2

    def build(self, input_shape):
        L2 = tf.keras.regularizers.l2(self.l2_rate) if self.l2_rate > 0 else None
        self.dropout = Dropout(rate=self.dropout_rate)
        self.dense = Dense(
            self.units, kernel_regularizer=L2
        )
        self.batch_norm = BatchNormalization()
        self.activate = Activation(self.activation)

    def call(self, inputs, training):
        X = self.dropout(inputs, training)
        X = self.dense(X)
        X = self.batch_norm(X)
        X = self.activate(X)
        return X

    def get_config(self) -> dict:
        return {
            "units": self.units,
            "activation": self.activation,
            "dropout": self.dropout_rate,
            "l2": self.l2_rate
        }


blocks = {
    "dense": DenseBlock,
    "lstm": LSTMBlock
}


class BaseModel(ABC):
    """
    Allows an inheriting dialogue policy base model to automatically
    inherit serialization and evaluation functionality. Also ensures the
    model has the correct fit and predict API (if the abstract methods are
    implemented in the way requested.)
    """

    serializer = Serializer()

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

    def to_dir(self, path: str) -> None:
        self.serializer.serialize(self, path)

    @classmethod
    def from_dir(cls, path: str, delete: bool = False) -> "BaseModel":
        return cls.serializer.deserialize(path, delete)

    def get_params(self) -> dict:
        return {name: getattr(self, name) for name in self.get_hp_spec(kt.HyperParameters())}

    def set_params(self, **params):
        param_names = self.get_params().keys()
        for k, v in params.items():
            if k not in param_names:
                raise ValueError(f"{k} is not a known hyperparameter")
            setattr(self, k, v)

    def evaluate(self, agent: dict, *, test_ratio: float, report: str = None) -> dict:
        """
        Evaluates the performance of the model on `agent`, using the
        f1 macro score over actions as the performance metric.
        """
        train_agent, test_agent = AgentDataUtils.split(agent, test_ratio)
        self.fit(train_agent)
        convs, next_actions = AgentDataUtils.make_validation_pairs(test_agent)
        predicted_actions = self.predict(convs)
        if report:
            with open(report, "w") as f:
                f.write("# Classification Report\n\n")
                f.write(classification_report(next_actions, predicted_actions))
                f.write("\n# Confusion Matrix\n\n")
                f.write("Columns are the predictions, rows are the true labels.\n\n")
                f.write(np.array2string(confusion_matrix(next_actions, predicted_actions)))
                f.write("\n")
        return {
            "test_f1_macro": f1_score(next_actions, predicted_actions, average="macro"),
            "test_accuracy": accuracy_score(next_actions, predicted_actions)
        }

    @classmethod
    def tune(
        cls,
        agent: dict,
        *,
        val_ratio: float,
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
        val_ratio : float
            The % of the agent's training conversations to use for the
            validation set (randomly selected).
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
        tuner.search(agent, test_ratio=val_ratio, callback=callback)

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

    def run_trial(self, trial, agent: dict, test_ratio: float, callback: t.Callable) -> None:
        """Each trial of the optimizer is a call to `BaseModel.evaluate`.
        """
        model = self.hypermodel.build(trial.hyperparameters)
        test_performance = model.evaluate(agent, test_ratio=test_ratio)
        if callback:
            callback(model, test_performance)
        tf.keras.backend.clear_session()
        del model
        self.oracle.update_trial(trial.trial_id, test_performance)
