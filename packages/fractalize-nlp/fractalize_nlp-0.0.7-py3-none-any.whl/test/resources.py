"""Contains all test_resources required."""

import json
import pandas as pd

"""config files"""

with open('./test/test_resources/test_strings_config.json', 'r') as f:
    MOCK_CONFIG = json.load(f)

"""state files"""

CORRECT_STATE = pd.read_csv('./test/test_resources/states/correct_state.csv').fillna('')
CONTRACTED_STATE = pd.read_csv('./test/test_resources/states/contracted_state.csv').fillna('')
EMPTY_STATE = pd.read_csv('./test/test_resources/states/empty_state.csv').fillna('')
EXTENDED_STATE = pd.read_csv('./test/test_resources/states/extended_state.csv').fillna('')
SINGLE_STATE = pd.read_csv('./test/test_resources/states/single_state.csv').fillna('')

"""sample files"""

CORRECT_SAMPLE = pd.read_csv('./test/test_resources/samples/correct_sample.csv').fillna('')
EMPTY_SAMPLE = pd.read_csv('./test/test_resources/samples/empty_sample.csv').fillna('')
EXTENDED_SAMPLE = pd.read_csv('./test/test_resources/samples/extended_sample.csv').fillna('')
MATCHING_SAMPLE = pd.read_csv('./test/test_resources/samples/matching_sample.csv').fillna('')
SINGLE_SAMPLE = pd.read_csv('./test/test_resources/samples/single_sample.csv').fillna('')
STRING_COLUMN_SAMPLE = pd.read_csv('./test/test_resources/samples/string_column_sample.csv').fillna('')

"""state_domains, for testing of generate_string_for_state"""

CORRECT_STATE_DOMAIN = pd.read_csv('./test/test_resources/state_domains/correct_state_domain.csv').fillna('')
EMPTY_STATE_DOMAIN = pd.read_csv('./test/test_resources/state_domains/empty_state_domain.csv').fillna('')
EXTENDED_STATE_DOMAIN = pd.read_csv('./test/test_resources/state_domains/extended_state_domain.csv').fillna('')
SINGLE_STATE_DOMAIN = pd.read_csv('./test/test_resources/state_domains/single_state_domain.csv').fillna('')

"""output of the state_outcomes, for testing of select_state_domain_for_state"""

OUTPUT_FIRSTSTATE_OUTCOME = pd.read_csv('./test/test_resources/state_outcomes/output_firststate_outcome.csv').fillna('')
OUTPUT_LASTSTATE_OUTCOME = pd.read_csv('./test/test_resources/state_outcomes/output_laststate_outcome.csv').fillna('')
OUTPUT_FIRSTSTATE_OUTCOME_FALSE = pd.read_csv('./test/test_resources/state_outcomes/output_firststate_outcome_false.csv').fillna('')
OUTPUT_LASTSTATE_OUTCOME_FALSE = pd.read_csv('./test/test_resources/state_outcomes/output_laststate_outcome_false.csv').fillna('')
OUTPUT_EXTENDED_STATE_OUTCOME = pd.read_csv('./test/test_resources/state_outcomes/output_extended_state_outcome.csv').fillna('')
