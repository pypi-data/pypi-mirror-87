"""To test the function generate_order_choice_string in utils.py."""

from fractalize_nlp.string_generators.utils import generate_order_choice_string
import copy
import pandas as pd
import pytest

def base():
    return pd.read_csv("./test/test_resources/order_choice/values.csv", 
                       index_col='key', 
                       squeeze=True).to_dict()

def add_order_choice(dictionary, choice_list):
    temp_dict = copy.deepcopy(dictionary)
    temp_dict["Order_Choice"] = choice_list

    return pd.Series(temp_dict)

def test_cases():
    base_dict = base()

    order_choices = pd.read_csv("./test/test_resources/order_choice/order_choices.csv",
                                index_col='Order_Choice',
                                squeeze=True).fillna('').to_dict()

    test_cases = []

    for choice in order_choices:

        if choice == 'EMPTY':
            choice_list = []
        else:
            choice_list = choice.split(';')

        row = add_order_choice(base_dict, choice_list)
        test_cases.append((row, order_choices[choice]))

    return test_cases

@pytest.mark.parametrize("test_input, expected", test_cases())
def test_eval(test_input, expected):
    assert generate_order_choice_string(test_input) == expected

def exception_cases():
    base_dict = base()

    unindexable_case = add_order_choice(base_dict, "unindexable case")
    absent_order_choice_case = copy.deepcopy(base_dict)
    nonexistent_choice_case = add_order_choice(base_dict, ['nonexistent choice'])
    wrong_indexable_case = add_order_choice(base_dict, 12345)

    exception_cases = [
        (unindexable_case, pytest.raises(KeyError)),
        (absent_order_choice_case, pytest.raises(KeyError)),
        (nonexistent_choice_case, pytest.raises(KeyError)),
        (wrong_indexable_case, pytest.raises(IndexError))
    ]

    return exception_cases

@pytest.mark.parametrize("test_input, exception", exception_cases())
def test_exceptions(test_input, exception):
    with exception:
        assert generate_order_choice_string(test_input) is not None