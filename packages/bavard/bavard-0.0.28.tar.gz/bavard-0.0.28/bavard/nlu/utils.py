import unicodedata
from typing import List, Sequence
import typing as t
from statistics import mean, stdev, median
from collections import defaultdict

from sklearn.model_selection import StratifiedKFold
from sklearn.utils import shuffle as do_shuffle
import tensorflow as tf


def is_whitespace(char: str):
    """Checks whether `char` is a whitespace character."""
    if char == " " or char == "\t" or char == "\n" or char == "\r":
        return True
    cat = unicodedata.category(char)
    if cat == "Zs":
        return True
    return False


def get_char_to_word_map(text: str) -> List[int]:
    words = []
    char_to_word_idx = []
    prev_is_whitespace = True

    for char in text:
        if is_whitespace(char):
            prev_is_whitespace = True
            char_to_word_idx.append(len(words))

        else:
            if prev_is_whitespace:
                words.append(char)
            else:
                words[-1] += char
            prev_is_whitespace = False
            char_to_word_idx.append(len(words) - 1)
    return char_to_word_idx


def assert_all_not_none(**items) -> None:
    """
    Asserts every value in `items` is not `None`.
    The keys in `items` should be the names of the items.
    """
    for name, val in items.items():
        if val is None:
            raise AssertionError(f"{name} cannot be None")


def concat_tensor_dicts(
    dicts: t.Sequence[t.Dict[str, tf.Tensor]], axis: int = 0, new_axis: bool = False
) -> t.Dict[str, tf.Tensor]:
    """
    Concatenates all the tensors in `dicts` by dictionary key.
    """
    # Unpack each dictionary of tensors into a single dictionary
    # containing lists of tensors.
    data = defaultdict(list)
    for d in dicts:
        for key in d:
            data[key].append(d[key])

    # Now convert those lists to tensors
    for key in data:
        if new_axis:
            data[key] = tf.stack(data[key])
        else:
            data[key] = tf.concat(data[key], axis)

    return dict(data)


def aggregate_dicts(dicts: list, agg: str) -> dict:
    """
    Aggregates a list of dictionaries all having the same keys.
    All values for a given key are aggregated into a single value
    using `agg`. Returns a single dictionary with the aggregated values
    """
    aggs = {
        "mean": mean,
        "stdev": stdev,
        "sum": sum,
        "median": median,
        "min": min,
        "max": max,
    }
    assert len(dicts) > 0
    keys = dicts[0].keys()
    result = {}
    for key in keys:
        result[key] = aggs[agg]([d[key] for d in dicts])
    return result


def make_stratified_folds(
    data: Sequence, labels: Sequence, nfolds: int, shuffle: bool = True, seed: int = 0
) -> tuple:
    """
    Takes `data`, a list, and breaks it into `nfolds` chunks. Each chunk is stratified
    by `labels`.
    """
    skf = StratifiedKFold(n_splits=nfolds, shuffle=shuffle, random_state=seed)
    fold_indices = [indices for _, indices in skf.split(data, labels)]
    folds = [[data[i] for i in indices] for indices in fold_indices]
    if shuffle:
        folds = [do_shuffle(fold, random_state=seed) for fold in folds]
    return folds


def leave_one_out(items: Sequence):
    """
    Cycles through `items`. On each ith item `item_i`, it yields
    `item_i`, as well as all items in `items` except `item_i` as a list.
    So given `items==[1,2,3,4]`, the first iteration will yield
    `1, [2,3,4]`, the second will yield `2, [1,3,4]`, and so on.
    """
    for i, item in enumerate(items):
        yield item, items[:i] + items[i + 1 :]
