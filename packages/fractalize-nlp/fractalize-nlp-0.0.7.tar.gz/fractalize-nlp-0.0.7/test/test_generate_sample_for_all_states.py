"""To test the function generate_sample_for_all_states in utils.py.
Done via invoking classes in MockBaseStringGenerator.py, loaded with test_strings_config.json file.
As this is a non-deterministic function, the format of the returned dataframe is checked against."""

from fractalize_nlp.string_generators.utils import generate_sample_for_all_states
import test.BaseStringGenerators as mbsg
from test.resources import (
    MOCK_CONFIG,
    CORRECT_SAMPLE,
    EMPTY_SAMPLE,
    EXTENDED_SAMPLE,
    MATCHING_SAMPLE,
    STRING_COLUMN_SAMPLE
)
from test.utils import check_format, check_preserved
import pytest

def base_test(generated, expected_df_format, sample):
    """Tests if format of generated output matches the required dimensions and column names.
    Also tests if the sample is identical to that in the generated output."""

    expected_columns = sample.columns.append(expected_df_format.columns)
    row_count = sample.shape[0]
    column_count = sample.shape[1] + expected_df_format.shape[1]

    print(generated)
    print(sample)
    print(expected_df_format)

    format = check_format(generated, (row_count, column_count), expected_columns)
    preserved = check_preserved(sample, generated)

    print(format)
    print(preserved)

    return format and preserved


def get_expected_df_format(string_generator):
    """Appends '_' + state_field to the pre-existing 'String' column in the string_generator DataFrame."""

    expected_df_format = vars(string_generator)[string_generator.state_field]
    state_field = string_generator.state_field
    expected_df_format = expected_df_format.rename(columns={'String': 'String_' + state_field})

    return expected_df_format

def test_cases():
    """
    Test cases:
        1. Tests simple case of a BaseStringGenerator instance combined with a sample of 2 columns.
        2. Tests when a BaseStringGenerator instance is combined with a sample of multiple columns.
        3. Tests when a BaseStringGenerator instance reads in an extended state file.
        4. Tests when a BaseStringGenerator instance reads in multiple state files.
    """

    test_cases = [
        (mbsg.CorrectBaseStringGenerator(MOCK_CONFIG), CORRECT_SAMPLE, "_l_suffix", "_r_suffix"),
        (mbsg.CorrectBaseStringGenerator(MOCK_CONFIG), EXTENDED_SAMPLE, "_l_suffix", "_r_suffix"),
        (mbsg.ExtendedBaseStringGenerator(MOCK_CONFIG), CORRECT_SAMPLE, "_l_suffix", "_r_suffix"),
        (mbsg.MultipleBaseStringGenerator(MOCK_CONFIG), CORRECT_SAMPLE, "_l_suffix", "_r_suffix"),
    ]

    return test_cases

@pytest.mark.parametrize("string_generator, sample, l_suffix, r_suffix", test_cases())
def test_eval(string_generator, sample, l_suffix, r_suffix):
    generated = string_generator.generate_sample_for_all_states(sample, r_suffix)
    expected_df_format = get_expected_df_format(string_generator)

    assert base_test(generated, expected_df_format, sample)

def test_suffix():
    """Tests when there are overlaps in the rows and the suffixes are provided appropriately."""

    correct_sg = mbsg.CorrectBaseStringGenerator(MOCK_CONFIG)
    l_suffix = "_l_suffix"
    r_suffix = "_r_suffix"
    generated = generate_sample_for_all_states(correct_sg, MATCHING_SAMPLE, l_suffix, r_suffix)

    expected_df_format = get_expected_df_format(correct_sg)
    expected_df_format = expected_df_format.add_suffix(l_suffix)
    matching_sample = MATCHING_SAMPLE.add_suffix(r_suffix)

    assert base_test(generated, expected_df_format, matching_sample)

    generated = correct_sg.generate_sample_for_all_states(MATCHING_SAMPLE, "r_suffix")

    expected_df_format = get_expected_df_format(correct_sg)
    expected_df_format = expected_df_format.add_suffix("_"+correct_sg.state_field)
    matching_sample = MATCHING_SAMPLE.add_suffix(r_suffix)

    assert base_test(generated, expected_df_format, matching_sample)

def test_string_column():
    """Tests when the sample has a column named as String.
    The header of this String column will be concatenated with the l_suffix."""

    correct_sg = mbsg.CorrectBaseStringGenerator(MOCK_CONFIG)
    l_suffix = "_l_suffix"
    generated = generate_sample_for_all_states(correct_sg, STRING_COLUMN_SAMPLE, l_suffix, "_r_suffix")

    expected_df_format = get_expected_df_format(correct_sg)
    string_column_sample = STRING_COLUMN_SAMPLE.rename(columns={'String': 'String' + l_suffix})

    assert base_test(generated, expected_df_format, string_column_sample)

    generated = correct_sg.generate_sample_for_all_states(STRING_COLUMN_SAMPLE, "_r_suffix")

    expected_df_format = get_expected_df_format(correct_sg)
    string_column_sample = STRING_COLUMN_SAMPLE.rename(columns={'String': 'String' + "_r_suffix"})
    assert base_test(generated, expected_df_format, string_column_sample)

def exception_cases():
    """
    Test cases:
        1. Tests when there are overlaps in the rows and the suffixes are not provided appropriately.
           A ValueError should be raised.
        2. Tests when a BaseStringGenerator instance is combined with an empty sample, with only column headers.
           A ValueError should be raised.
        3. Tests when a BaseStringGenerator instance with no string_field (no 'String' column)
            is combined with a correct sample. An AttributeError should be raised.
        4. Tests when a BaseStringGenerator instance that reads in an empty file, with only column headers,
           is combined with a correct sample. A ValueError should be raised.
    """

    exception_cases = [
        (mbsg.CorrectBaseStringGenerator(MOCK_CONFIG), MATCHING_SAMPLE, '', '', pytest.raises(ValueError)),
        (mbsg.CorrectBaseStringGenerator(MOCK_CONFIG), EMPTY_SAMPLE, '', '', pytest.raises(ValueError)),
        (mbsg.ContractedBaseStringGenerator(MOCK_CONFIG), CORRECT_SAMPLE, '', '', pytest.raises(AttributeError)),
        (mbsg.EmptyBaseStringGenerator(MOCK_CONFIG), CORRECT_SAMPLE, '', '', pytest.raises(ValueError)),
    ]

    return exception_cases

@pytest.mark.parametrize("string_generator, sample, l_suffix, r_suffix, exception", exception_cases())
def test_exceptions(string_generator, sample, l_suffix, r_suffix, exception):
    with exception:
        assert generate_sample_for_all_states(string_generator, sample, l_suffix, r_suffix) is not None
        assert string_generator.generate_sample_for_all_states(sample, l_suffix, r_suffix) is not None
