"""To test the function load_sources in utils.py.
Done via calling the classes in MockBaseStringGenerator.py, loaded with the test_strings_config.json file.
The attributes of the instances are checked against."""

import test.BaseStringGenerators as mbsg
from test.resources import MOCK_CONFIG
import pandas as pd
import pytest

def base_test(base_string_generator, config, state_field, string_field_present):
    """Checks if attributes of base_string_generator are correct."""

    attributes = vars(base_string_generator)
    state_file_string = [v for v in config[base_string_generator.__class__.__name__].values()][0]
    state_file = pd.read_csv(state_file_string).fillna('')

    if string_field_present:
        string_field = attributes["string_field"] == "String"
    else:
        string_field = "string_field" not in attributes

    return string_field and \
           attributes[state_field].equals(state_file) and \
           attributes["state_field"] == state_field

def test_cases():
    """
    Test cases:
        1. Tests when a typical correct state file is loaded.
        2. Tests when an empty state file with column headers is loaded.
        3. Tests when there is an additional column in the state file.
           The attribute, attribute_name, should still be identical to the state file.
        4. Tests when a state file without a 'String' column header is loaded.
        5. Tests when there is a single column in the state file, representing state only.
           The only attributes include state and state_field.
    """

    test_cases = [
        (mbsg.CorrectBaseStringGenerator(MOCK_CONFIG), MOCK_CONFIG, 'state', True),
        (mbsg.EmptyBaseStringGenerator(MOCK_CONFIG), MOCK_CONFIG, 'state', True),
        (mbsg.ExtendedBaseStringGenerator(MOCK_CONFIG), MOCK_CONFIG, 'state', True),
        (mbsg.NoStringBaseStringGenerator(MOCK_CONFIG), MOCK_CONFIG, 'state', False),
        (mbsg.ContractedBaseStringGenerator(MOCK_CONFIG), MOCK_CONFIG, 'state', False)
    ]

    return test_cases

@pytest.mark.parametrize("string_generator, config, state_field, string_field_present", test_cases())
def test_eval(string_generator, config, state_field, string_field_present):
    assert base_test(string_generator, config, state_field, string_field_present)

def exception_string(string_generator_name):
    """Generates the exception string when the state reflected in the config file 
    does not match that of the csv file."""
    
    entry = MOCK_CONFIG[string_generator_name]
    attribute_name = [k for k in entry.keys()][0]
    attribute_source_file = [v for v in entry.values()][0]
    exception_string = "Column {0} not found in {1}".format(attribute_name,
                                                            attribute_source_file)

    return exception_string

def test_multiple():
    """Tests when there are multiple files in test_strings_config.
    There will be multiple attribute_names and 
    state_field will consist of the attribute_name that appears last."""

    multiple = mbsg.MultipleBaseStringGenerator(MOCK_CONFIG)
    attributes = vars(multiple)
    
    state_file_strings = [v for v in MOCK_CONFIG[multiple.__class__.__name__].values()]
    state_files = {}

    for file_string in state_file_strings:
        state_df = pd.read_csv(file_string).fillna('')
        state_files[state_df.columns[0]] = state_df

    assert attributes["string_field"] == "String"
    assert attributes['state'].equals(state_files['state'])
    assert attributes['extra_state'].equals(state_files['extra_state'])
    assert attributes["state_field"] == 'extra_state'

def exception_cases():
    """
    Test cases:
        1. Tests when test_strings_config file has mismatching attribute_name and attribute_source_file.
           An exception should be raised, detailing that the states cannot be found in the csv file.
        2. Tests when test_string_config file contains a directory string pointing to a non-existent file.
           A FileNotFoundError should be raised.
        3. Tests when the name of the BaseStringGenerator instance is not reflected in the test_strings_config file.
           A KeyError should be raised.
    """

    exception_cases = [
        (mbsg.MismatchBaseStringGenerator, pytest.raises(Exception, 
                                                         match=exception_string("MismatchBaseStringGenerator"))),
        (mbsg.NoDirBaseStringGenerator, pytest.raises(FileNotFoundError)),
        (mbsg.NonexistentBaseStringGenerator, pytest.raises(KeyError, 
                                                            match="NonexistentBaseStringGenerator"))
    ]

    return exception_cases

@pytest.mark.parametrize("string_generator, exception", exception_cases())
def test_exceptions(string_generator, exception):
    with exception:
        assert string_generator(MOCK_CONFIG) is not None
    