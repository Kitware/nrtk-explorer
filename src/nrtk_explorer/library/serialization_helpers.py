import numpy as np


def np_array_to_string(array):
    return np.array2string(array, separator=", ")


def string_to_np_array(input):
    return np.fromstring(input.strip("[]"), sep=",")
