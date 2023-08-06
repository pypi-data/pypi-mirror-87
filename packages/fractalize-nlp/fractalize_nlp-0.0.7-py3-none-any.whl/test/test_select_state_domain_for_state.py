"""To test the function select_state_domain_for_state in utils.py."""

from fractalize_nlp.string_generators.utils import select_state_domain_for_state
from test.resources import (
    CORRECT_STATE,
    CONTRACTED_STATE,
    EMPTY_STATE,
    EXTENDED_STATE,
    OUTPUT_FIRSTSTATE_OUTCOME,
    OUTPUT_LASTSTATE_OUTCOME,
    OUTPUT_FIRSTSTATE_OUTCOME_FALSE,
    OUTPUT_LASTSTATE_OUTCOME_FALSE,
    OUTPUT_EXTENDED_STATE_OUTCOME
)
import pytest

def base_test(state_outcome, state, selected, expected):
    """To test if running `selected` is equal to `expected`.
    `expected` is first re-indexed."""

    occurences = state_outcome[state_outcome['state'] == state].shape[0]
    start_index = (state_outcome['state'] == state).idxmax()
    expected.index = [i for i in range(start_index , start_index + occurences)]

    return selected.equals(expected)

def test_cases():
    """
    Test cases:
        1. Tests when the first cell is selected as the state_domain.
        2. Tests when the last cell of the state column is selected as the state_domain.
        3. Tests when the first cell is selected as the state_domain 
           and filter_state_field is set to False.
        4. Tests when the last cell of the state column is selected as the state_domain
           and filter_state_field is set to False.
        5. Tests when the state file has an additional column.
           The function should still return a dataframe object with the first column filtered against.
    """

    test_cases = [
        (CORRECT_STATE, 1, True, OUTPUT_FIRSTSTATE_OUTCOME),
        (CORRECT_STATE, 3, True, OUTPUT_LASTSTATE_OUTCOME),
        (CORRECT_STATE, 1, False, OUTPUT_FIRSTSTATE_OUTCOME_FALSE),
        (CORRECT_STATE, 3, False, OUTPUT_LASTSTATE_OUTCOME_FALSE),
        (EXTENDED_STATE, 1, True, OUTPUT_EXTENDED_STATE_OUTCOME)
    ]

    return test_cases

@pytest.mark.parametrize("state_outcome, state, filter_state_field, expected", test_cases())
def test_eval(state_outcome, state, filter_state_field, expected):
    selected = select_state_domain_for_state(state_outcome, 
                                             state, 
                                             'state',
                                             filter_state_field)
    assert base_test(state_outcome, state, selected, expected)

def test_contracted():
    """Tests when the state file has a single column of state only.
    The function should return an empty dataframe object with matching number of rows."""

    state = CONTRACTED_STATE['state'].iloc[0]
    selected = select_state_domain_for_state(CONTRACTED_STATE, 
                                             state,
                                             'state')

    occurences = CONTRACTED_STATE[CONTRACTED_STATE['state'] == state].shape[0]

    assert selected.empty
    assert selected.shape[0] == occurences

def test_empty():
    """Tests when the state file is blank and only has column headers.
    The function should return an empty dataframe object 
    with a column name matching 'String'."""

    selected = select_state_domain_for_state(EMPTY_STATE, 
                                             "EMPTY_STATE", 
                                             'state')

    assert selected.empty
    assert selected.columns[0] == 'String'