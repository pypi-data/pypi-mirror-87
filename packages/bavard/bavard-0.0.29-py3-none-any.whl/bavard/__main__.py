"""A CLI for interacting with NLU and dialogue policy models.
"""

from fire import Fire

from bavard.nlu.cli import NLUModelCLI
from bavard.dialogue_policy.cli import DialoguePolicyModelCLI


def main():
    Fire({"nlu": NLUModelCLI, "dialogue_policy": DialoguePolicyModelCLI})


if __name__ == "__main__":
    main()
