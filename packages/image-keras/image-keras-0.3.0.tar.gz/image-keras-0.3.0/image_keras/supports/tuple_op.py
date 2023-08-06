from typing import Tuple


def tuple_element_wise_add(a: Tuple, b: Tuple):
    return tuple(map(lambda el_1, el_2: el_1 + el_2, a, b))


def tuple_element_wise_subtract(a: Tuple, b: Tuple):
    return tuple(map(lambda el_1, el_2: el_1 - el_2, a, b))


def tuple_element_wise_multiply(a: Tuple, b: Tuple):
    return tuple(map(lambda el_1, el_2: el_1 * el_2, a, b))


def tuple_element_wise_divide(a: Tuple, b: Tuple):
    return tuple(map(lambda el_1, el_2: el_1 / el_2, a, b))


def tuple_element_wise_divide_int(a: Tuple, b: Tuple):
    return tuple(map(lambda el_1, el_2: el_1 // el_2, a, b))


def tuple_add(a: Tuple, b: int):
    return tuple(map(lambda el: el + b, a))


def tuple_subtract(a: Tuple, b: int):
    return tuple(map(lambda el: el - b, a))


def tuple_multiply(a: Tuple, b: int):
    return tuple(map(lambda el: el * b, a))


def tuple_divide(a: Tuple, b: int):
    return tuple(map(lambda el: el / b, a))


def tuple_divide_int(a: Tuple, b: int):
    return tuple(map(lambda el: el // b, a))
