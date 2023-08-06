"""To test the function generate_string_for_state in utils.py. 
As the function is not deterministic, only the format(number of rows, column headers, etc.) 
of the returned dataframe is checked against."""

from fractalize_nlp.string_generators.utils import generate_string_for_state
from test.resources import (
    CORRECT_SAMPLE,
    SINGLE_SAMPLE,
    EMPTY_SAMPLE,
    EXTENDED_SAMPLE,
    CORRECT_STATE_DOMAIN,
    EMPTY_STATE_DOMAIN,
    EXTENDED_STATE_DOMAIN,
    SINGLE_STATE_DOMAIN
)
from test.utils import check_format, check_preserved
import pytest

def base_test(generated, sample, domain):
    """Tests if format of `generated` matches the required dimensions and column names.
    Also tests if `sample` is present and equivelent in the leftmost columns of `generated`."""

    expected_columns = sample.columns.append(domain.columns)
    row_count = sample.shape[0]
    column_count = sample.shape[1] + domain.shape[1]

    return check_format(generated, (row_count, column_count), expected_columns) and \
           check_preserved(sample, generated)

def test_cases():
    """
    Test cases:
        1. Typical test case of a sample with multiple states 
           and a state_domain with multiple state strings.
        2. Tests when there is only a single row in the sample.
        3. Tests when the given sample is empty and only has column headers.
        4. Tests when the sample has multiple columns.
        5. Tests when there is an additional column in the state_domain file. 
           The function should return the processed additional column.
    """

    test_cases = [
        (CORRECT_STATE_DOMAIN, CORRECT_SAMPLE),
        (CORRECT_STATE_DOMAIN, SINGLE_SAMPLE),
        (CORRECT_STATE_DOMAIN, EMPTY_SAMPLE),
        (CORRECT_STATE_DOMAIN, EXTENDED_SAMPLE),
        (EXTENDED_STATE_DOMAIN, CORRECT_SAMPLE)
    ]

    return test_cases

@pytest.mark.parametrize("state_domain, sample", test_cases())
def test_eval(state_domain, sample):
    generated = generate_string_for_state(state_domain, sample)
    assert base_test(generated, sample, state_domain)

def test_single_state_domain():
    """Tests when there is only a single row in the state_domain.
    Performs additional check: if state and String in domain is equal throughout in `generated`."""

    generated = generate_string_for_state(SINGLE_STATE_DOMAIN, CORRECT_SAMPLE)
    assert base_test(generated, CORRECT_SAMPLE, SINGLE_STATE_DOMAIN)

    domain_values = generated['state_domain'].to_numpy()
    string_values = generated['String'].to_numpy()

    assert (domain_values[0] == domain_values[1:]).all()
    assert domain_values[0] == SINGLE_STATE_DOMAIN['state_domain'][0]
    assert (string_values[0] == string_values[1:]).all()
    assert string_values[0] == SINGLE_STATE_DOMAIN['String'][0]

def exception_cases():
    """
    Test cases:
        1. Tests when the state_domain is empty and only has column headers.
           The function should not be able to return a dataframe.
    """

    exception_cases = [
        (EMPTY_STATE_DOMAIN, CORRECT_SAMPLE, pytest.raises(ValueError))
    ]

    return exception_cases

@pytest.mark.parametrize("state_domain, sample, exception", exception_cases())
def test_exceptions(state_domain, sample, exception):
    with exception:
        assert generate_string_for_state(state_domain, sample) is not None
