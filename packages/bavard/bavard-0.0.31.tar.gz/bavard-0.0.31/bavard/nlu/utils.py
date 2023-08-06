import unicodedata
from typing import List
import typing as t
from collections import defaultdict

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
