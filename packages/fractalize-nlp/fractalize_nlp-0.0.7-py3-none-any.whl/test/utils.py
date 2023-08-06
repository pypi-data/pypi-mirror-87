import collections
from functools import reduce

def check_format(df, dimension, expected_headers):
    """Checks if a given dataframe has the required dimensions and column names."""

    return df.shape == dimension and df.columns.tolist() == expected_headers.tolist()

def check_preserved(df, df_contains):
    """Checks if all the values of df are present in df_contains."""

    return reduce(lambda prev, col: prev and df[col].tolist() == df_contains[col].tolist(),
                  df.columns,
                  True)

def states_presence(state, sample):
    """Checks if states are all represented in a sample."""

    all_states = state[state.columns[0]].unique()
    sample_states = sample[sample.columns[0]].unique()

    return collections.Counter(all_states) == collections.Counter(sample_states)

def string_states_presence(state, sample):
    """Checks if string states are all represented in a sample."""

    all_string_states = state[state.columns[1]].unique()
    sample_string_states = sample[sample.columns[1]].unique()

    return collections.Counter(all_string_states) == collections.Counter(sample_string_states)
    