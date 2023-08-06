import json
import os

from bavard.nlu.model import NLUModel
from bavard.nlu.tuner import NLUModelTuner, HyperNLUModelFactory


class NLUModelCLI:
    """Tools useful for local development and ad-hoc architecture search of NLU models.
    """

    @staticmethod
    def train(*, agent_data_file: str, **nlu_model_args):
        """
        Parameters
        ----------
        agent_data_file : str
            Path to the agent data file to train on.
        **nlu_model_args : optional
            Any control parameters or hyperparameters to pass to NLUModel
            constructor. If `auto==True`, some of these values may be
            overridden.
        """
        with open(agent_data_file) as f:
            nlu_data = json.load(f)["nluData"]

        model = NLUModel(**nlu_model_args)
        model.train(nlu_data)

    @staticmethod
    def evaluate(
        *,
        agent_data_file: str,
        test_ratio: float = None,
        nfolds: int = None,
        repeat: int = 0,
        do_error_analysis: bool = False,
        write_path: str = None,
        **nlu_model_args
    ):
        """
        Parameters
        ----------
        agent_data_file : str
            Path to the agent data file to evaluate on.
        test_ratio : float, optional
            The percentage of the dataset to use as a test set, if evaluating
            via a train/test split.
        nfolds : int, optional
            The number of folds to do, if evaluating via k-fold cross validation.
        repeat : int, optional
            If > 0, the evaluation will be performed `repeat` times and results will be
            averaged. This is useful when you want to average out the variance caused by
            random weight initialization, etc.
        do_error_analysis : bool, optional
            Possible only when doing k-fold CV with no repeats. Performs on error analysis on
            all the hold-out folds.
        write_path : str, optional
            If supplied, the results will be written out to the `write_path` directory.
        **nlu_model_args : optional
            Any control parameters or hyperparameters to pass to NLUModel
            constructor. If `auto==True`, some of these values may be
            overridden.
        """
        with open(agent_data_file) as f:
            nlu_data = json.load(f)["nluData"]

        model = NLUModel(**nlu_model_args)
        train_performance, test_performance = model.evaluate(
            nlu_data, test_ratio=test_ratio, nfolds=nfolds, repeat=repeat,
            do_error_analysis=do_error_analysis
        )
        print("train performance:", train_performance)
        print("test performance:", test_performance)
        if write_path:
            with open(os.path.join(write_path, "train-performance.json"), "w") as f:
                json.dump(train_performance, f)
            with open(os.path.join(write_path, "test-performance.json"), "w") as f:
                json.dump(test_performance, f)

    @staticmethod
    def predict(
        *,
        model_path: str,
        batch_file: str = None,
        interactive: bool = False
    ):
        """
        Parameters
        ----------
        model_path : str
            Path to the saved model that will be loaded.
        batch_file : str, optional
            Pass this file path to predict on a file of text; one prediction per line.
        interactive : bool, optional
            If supplied, interact with the model, providing inputs for prediction via CLI.
        """
        model = NLUModel.from_dir(model_path)
        if batch_file:
            with open(batch_file) as f:
                utterances = [utterance.replace("\n", "") for utterance in f]
            print(model.predict(utterances))

        if interactive:
            quits = {"q", "quit", "exit"}
            utterance = ""
            while True:
                utterance = input("\nEnter your utterance ('q' to quit) >>> ")
                if utterance in quits:
                    break
                print(model.predict([utterance]))

    @staticmethod
    def tune(
        *,
        agent_data_file: str,
        max_trials: int,
        strategy: str = "bayesian",
        test_ratio: float = None,
        nfolds: int = None,
        repeat: int = 0,
        project_name: str = None,
        **nlu_model_args
    ):
        """
        Parameters
        ----------
        agent_data_file : str
            Path to the agent data file to evaluate on.
        max_trials : int
            The maximum number of trials to run the hyperparameter optimization for.
        strategy : str, optional.
            The hyperparameter tuning strategy to use. One of `{"random", "bayesian"}`.
        test_ratio : float, optional
            The percentage of the dataset to use as a test set, if evaluating
            via a train/test split.
        nfolds : int, optional
            The number of folds to do, if evaluating via k-fold cross validation.
        repeat : int, optional
            If > 0, the evaluation will be performed `repeat` times and results will be
            averaged. This is useful when you want to average out the variance caused by
            random weight initialization, etc.
        project_name : str, optional
            If provided, the results from each trial will be saved under a directory by
            this name. If not provided, a default is used.
        **nlu_model_args : optional
            Any control parameters or hyperparameters to pass to NLUModel
            constructor. If `auto==True`, some of these values may be overridden.
        """
        with open(agent_data_file) as f:
            nlu_data = json.load(f)["nluData"]

        hypermodel = HyperNLUModelFactory(**nlu_model_args)
        tuner = NLUModelTuner(hypermodel, strategy, max_trials=max_trials, project_name=project_name)
        tuner.search(nlu_data=nlu_data, test_ratio=test_ratio, nfolds=nfolds, repeat=repeat)

        print("Tuning Results:")
        tuner.results_summary()

        best_hps, = tuner.get_best_hyperparameters()
        print("Best hyperparameters found:")
        print(best_hps.values)
