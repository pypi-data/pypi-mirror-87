"""To test the uniform distribution of samples generated from the function sample in utils.py.
The chisquare test is conducted to check for uniform distribution of states and string states.
A critical value of 0.05 and a sample size of 10000 is used."""

from fractalize_nlp.string_generators.utils import sample
from test.resources import CORRECT_STATE, SINGLE_STATE
import pytest
from scipy.stats import chisquare

def test_single():
    """Tests when there is only 1 state. All states and String_states in the sample should be equal."""

    state_field = 'state'
    state = [1]
    string_state = ['sample_state_1']
    sampled_state = sample(SINGLE_STATE, state_field, 10000)

    assert state == sampled_state[state_field].unique()
    assert string_state == sampled_state["String_" + state_field].unique()

def states_distribution(sample_output, state_field, critical_value):
    """Chisquare test for the uniform distribution of states."""

    states = sample_output[state_field].value_counts().to_numpy()
    n = states.size
    f_exp = [(states.sum() / n) for i in range(n)]

    return chisquare(states, f_exp=f_exp).pvalue > critical_value

def string_states_distribution(sample_output, state_field, critical_value):
    """Chisquare test for the uniform distribution of string_states within its parent state."""

    sample_states = sample_output[state_field].unique()

    for state in sample_states: 
        sample_string_values = sample_output[sample_output[state_field] == state]['String_'+state_field].value_counts().to_numpy()
        n = sample_string_values.size
        f_exp = [(sample_string_values.sum() / n) for i in range(n)]

        if chisquare(sample_string_values, f_exp=f_exp).pvalue <= critical_value:
            return False

    return True

def repeat(chisquare_test, sample_output, state, critical_value):
    """Repeats the given chisquare test 10 times, and returns False 
    when the chisquare_test returns False at least two times."""

    false_counter = 0
    for i in range(10):
        if not chisquare_test(sample_output, state, critical_value):
            false_counter += 1

        if false_counter > 2:
            return False
    
    return True

def test_cases():
    """
    Test cases:
        1. Tests for the uniform distribution of states in the sample.
        2. Tests for the uniform distribution of string_states within its parent state.
    """

    test_cases = [
        (states_distribution, CORRECT_STATE, 'state'),
        (string_states_distribution, CORRECT_STATE, 'state')
    ]

    return test_cases

@pytest.mark.parametrize("chisquare_test, state_file, state_field", test_cases())
def test_eval(chisquare_test, state_file, state_field):

    critical_value = 0.05
    sample_size = 10000
    sample_output = sample(state_file, state_field, sample_size)

    assert repeat(chisquare_test, sample_output, state_field, critical_value)
