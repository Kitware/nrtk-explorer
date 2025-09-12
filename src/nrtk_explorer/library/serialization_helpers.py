import numpy as np
from ast import literal_eval


def np_array_to_string(array):
    return np.array2string(array, separator=", ")


def string_to_np_array(input):
    return np.fromstring(input.strip("[]"), sep=",")


def string_to_literal(input):
    return literal_eval(input)


def literal_to_string(input):
    return str(input)
