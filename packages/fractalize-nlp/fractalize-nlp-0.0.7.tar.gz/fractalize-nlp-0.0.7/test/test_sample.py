"""To test the function sample in utils.py. 
As the function is not deterministic, only the format(number of rows, column headers, etc.) 
of the returned dataframe is checked against here. 
The test of uniform distribution will be done in test_uniform_distribution.py"""

from fractalize_nlp.string_generators.utils import sample
from test.resources import (
    CORRECT_STATE,
    CONTRACTED_STATE,
    EMPTY_STATE,
    EXTENDED_STATE
)
from test.utils import check_format, states_presence, string_states_presence
import pandas as pd
import pytest

def base_test(state_file, state_field, sampled_state, n=None):
    """Checks if the format of the sample is correct"""

    state_shape = state_file.shape

    if n is None:
        expected_shape = (10, state_shape[1])
    else:
        expected_shape = (n, state_shape[1])

    expected_headers = pd.Index([state_field, "String_" + state_field])
    return check_format(sampled_state, expected_shape, expected_headers)

def test_cases():
    """
    Test cases:
        1. Tests when number of rows is not passed into sample.
           Number of rows should correspond to the default value of 10.
        2. Tests when number of rows, n = 5, is passed into sample.
           Number of rows should correspond to n.
    """

    test_cases = [
        (CORRECT_STATE, 'state', None),
        (CORRECT_STATE, 'state', 5),
    ]

    return test_cases

@pytest.mark.parametrize("state_file, state_field, n", test_cases())
def test_eval(state_file, state_field, n):

    if n is None:
        sampled_state = sample(state_file, state_field)
    else:
        sampled_state = sample(state_file, state_field, n)
    
    assert base_test(state_file, state_field, sampled_state, n)

def test_big_n():
    """Tests when number of rows, n, is passed into sample, where n >> total number of rows in state file.
    Number of rows should correspond to n. All states and String_states should also be represented."""

    state_field = 'state'
    correct_state_shape = CORRECT_STATE.shape
    n = 100 * correct_state_shape[0]
    sampled_state = sample(CORRECT_STATE, state_field, n)

    assert base_test(CORRECT_STATE, state_field, sampled_state, n)
    assert states_presence(CORRECT_STATE, sampled_state)
    assert string_states_presence(CORRECT_STATE, sampled_state)

def test_extended():
    """Tests when an extended state is passed into sample.
    The function should return a dataframe, with matching column headers.
    The last column should have a 'String_' prefix."""

    state_columns = EXTENDED_STATE.columns
    sampled_state = sample(EXTENDED_STATE, 'state')
    expected_columns = EXTENDED_STATE.columns.tolist()
    # changes 'String' column header to 'String_state'
    expected_columns[-1] = 'String_state'

    assert expected_columns == sampled_state.columns.tolist()

def test_contracted():
    """Tests when a contracted state is passed into sample.
    The function should return a dataframe, with a matching column header."""

    sampled_state = sample(CONTRACTED_STATE, 'state')
    assert CONTRACTED_STATE.columns == sampled_state.columns

def exception_cases():
    """
    Test cases:
        1. Tests when an empty state is passed into sample.
           The function should not be able to return a dataframe and raises a ValueError.
    """

    exception_cases = [
        (EMPTY_STATE, 'state', 10, pytest.raises(ValueError)),
        (CORRECT_STATE, 'state', 0, pytest.raises(ValueError))
    ]

    return exception_cases

@pytest.mark.parametrize("state_file, state_field, n, exception", exception_cases())
def test_exceptions(state_file, state_field, n, exception):
    with exception:
        assert sample(state_file, state_field, n) is not None
