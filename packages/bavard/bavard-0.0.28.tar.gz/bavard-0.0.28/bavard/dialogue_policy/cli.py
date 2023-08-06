import json
from glob import glob
from pprint import pprint

from bavard.dialogue_policy.models import Classifier
from bavard.dialogue_policy.models.base import BaseModel


class WandbClient:
    """Client for logging model evaluation results to a Weights and Biases project.
    """
    def __init__(self, project: str):
        import wandb
        self._project = project
        self._wandb = wandb

    def log_model(self, model: BaseModel, test_performance: dict, **other_config_values):
        with self._wandb.init(project=self._project, reinit=True) as run:
            # Log the hyperparameter values
            run.config.update(model.get_params())
            # Log the model's performance and other config
            run.config.update(other_config_values)
            run.summary.update(test_performance)


class DialoguePolicyModelCLI:
    """
    Tools useful for local development and ad-hoc architecture search of
    dialogue policy models.
    """

    @staticmethod
    def train(agent_data_file: str, save_path: str = None, **modelparams) -> None:
        """Train a model on an agent's training conversations, then optionally save it.

        Parameters
        ----------
        agent_data_file : str
            The path to an agent's JSON data.
        save_path : str, optional
            If provided, the fitted model will be serialized to this path, by default None
        **modelparams : dict
            Any additional control or hyper parameters to pass to the model.
        """
        with open(agent_data_file) as f:
            agent = json.load(f)

        model = Classifier(**modelparams)
        model.fit(agent)
        if save_path:
            model.to_dir(save_path)

    @staticmethod
    def predict(save_path: str, conversations_path: str) -> None:
        """Loads a trained model and predicts next actions on conversations.

        Parameters
        ----------
        save_path : str
            The path to load a serialized model from.
        conversations_path : str
            The path to a JSON file of conversations to predict on.
        """
        with open(conversations_path) as f:
            convs = json.load(f)
        model = Classifier.from_dir(save_path)
        print(model.predict(convs))

    @staticmethod
    def evaluate(
            agent_data_file: str,
            test_ratio: float,
            report: str = None,
            wandb_project: str = None,
            **modelparams
    ) -> None:
        """Evaluates a model on an agent's training conversations.

        Parameters
        ----------
        agent_data_file : str
            The path to an agent's JSON data.
        test_ratio : float
            The ratio of the agent's training conversations to use as the test set.
        report : str, optional
            If provided, a classification report will be created and written to this path.
        wandb_project : str, optional
            If provided, the model's training info and metrics will be logged to this
            Weights & Biases project name.
        **modelparams : dict
            Any additional control or hyper parameters to pass to the model.
        """
        with open(agent_data_file) as f:
            agent = json.load(f)

        if wandb_project:
            # Log all results to the Weights and Biases project
            wb = WandbClient(wandb_project)
            model = Classifier(**modelparams)
            test_performance = model.evaluate(agent, test_ratio=test_ratio, report=report)
            wb.log_model(model, test_performance, test_ratio=test_ratio)
        else:
            # Just evaluate the model and print the results.
            model = Classifier(**modelparams)
            test_performance = model.evaluate(agent, test_ratio=test_ratio, report=report)
            print(f"Test Performance: {test_performance}")

    @staticmethod
    def tune(
        agent_data_file: str,
        val_ratio: float,
        wandb_project: str = None,
        strategy: str = "bayesian",
        max_trials: int = 100
    ) -> None:
        with open(agent_data_file) as f:
            agent = json.load(f)
        if wandb_project:
            wb = WandbClient(wandb_project)
            Classifier.tune(agent, val_ratio=val_ratio, strategy=strategy, max_trials=max_trials, callback=wb.log_model)
        else:
            Classifier.tune(agent, val_ratio=val_ratio, strategy=strategy, max_trials=max_trials)

    @staticmethod
    def aggregate(project_dir: str, topn: int = 5) -> None:
        """
        Aggregate the results of a hyperparameter tuning session, to see which
        hyperparameter configurations resulted in the best scores.

        Parameters
        ----------
        project_dir : str
            The path to the directory containing all the hyperparameter
            optimization trial results.
        topn : int
            The number of top experiments to show.
        """
        files = glob(f"{project_dir}/*/trial.json")
        results = []
        for fname in files:
            with open(fname) as f:
                data = json.load(f)
            if data["status"] == "COMPLETED":
                results.append({
                    "score": data["score"],
                    "hyperparameters": data["hyperparameters"]["values"]
                })

        results.sort(reverse=True, key=lambda r: r["score"])
        for result in results[:topn]:
            pprint(result)
