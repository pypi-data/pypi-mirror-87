import numpy as np
import pandas as pd


def load_sources(instance, config):
    """The constructor method for a BaseStringGenerator.

    Parameters
    ----------
    instance : StringGenerator
        The equivalent of self in a constructor method.
    config : dict
        The valid_strings_config.json file.

    Attributes
    ----------
    string_field : str, optional
        An optional attribute of 'String', if there exists a column named 'String'
        in the corresponging csv file in `config`.
    attribute_name : pandas.DataFrame
        Read in from the corresponding csv file in `config`.
    state_field : str
        The state read in from `config`.
        If there are multiple state files, the name is set in accordance to the last state file.

    Raises
    ------
    Exception
        If the state in `attribute_name` is not found in the `config` file.

    """

    for attribute_name, attribute_source_file in config[instance.__class__.__name__].items():
        attribute_source = pd.read_csv(attribute_source_file,
                                       encoding='utf-8')
        if attribute_name not in attribute_source.columns:
            raise Exception("Column {0} not found in {1}".format(attribute_name,
                                                                 attribute_source_file))
        if 'String' in attribute_source.columns:
            attribute_source['String'].fillna("",
                                              inplace=True)
            instance.__setattr__('string_field',
                                 'String')
        instance.__setattr__(attribute_name,
                             attribute_source)
        instance.__setattr__('state_field',
                             attribute_name)
    # TODO: ensure this is included in test cases
    if all([x in instance.__dict__
            for x in ['string_field',
                      'state_field']]):
        instance.__setattr__('joint_string_field',
                             "_".join([instance.string_field,
                                       instance.state_field]))

def generate_string_for_state(state_domain_df, sample_for_state):
    """Joins a sample of state_domain_df onto sample_for_state.

    Parameters
    ----------
    state_domain_df : pandas.DataFrame
        Dataframe consisting of the state domain of a pre-selected state.
    sample_for_state : pandas.DataFrame
        Dataframe consisting of the sample to be joined onto.

    Returns
    -------
    pandas.DataFrame
        The combined dataframe of `state_domain_df` and `sample_for_state`.
        `sample_for_state` will be placed on the left of `state_domain_df`.

    """

    sample_to_join = state_domain_df.sample(sample_for_state.shape[0],
                                            replace=True)
    joint_sample = sample_for_state.reset_index(drop=True).join(sample_to_join.reset_index(drop=True))
    return joint_sample

def select_state_domain_for_state(state_outcomes_denormalized,
                                  state,
                                  state_field,
                                  filter_state_field=True):
    """Returns the subset of state_outcome_denormalized where state_field == state.
    However, removes the state_field column before returning the result.

    Parameters
    ----------
    state_outcome_denormalized : pandas.DataFrame
        Dataframe that contains one row per outcome associated with `state_field`=`state`.
    state : int
        The particular state that we are selecting for.
    state_field : str
        Name of the column in state_outcomes_denormalized that represents the value state.
    filter_state_field : bool, optional
        If True, the resulting subset will not include the state field.

    Returns
    -------
    pandas.DataFrame
        Contains the subset where state_field == state.
        The index starts with the row number of the first occurence of `state` in `state_outcomes_denormalized`.

    """
    if filter_state_field:
        selected_columns = [x
                            for x in state_outcomes_denormalized.columns
                            if x!= state_field]
    else:
        selected_columns = state_outcomes_denormalized.columns
    return state_outcomes_denormalized.loc[state_outcomes_denormalized[state_field] == state][selected_columns]

def sample(state_outcomes_denormalized,
           state_field,
           n=10):
    # TODO: Refactor so that it can be invoked with an instance of a string generator instead of directly using
    # state_outcomes_denormalized and state_field.
    """Generates a DataFrame of `n` rows, by uniformly distributing all the states in `state_outcomes_denormalized`.

    Parameters
    ----------
    state_outcomes_denormalized : pandas.DataFrame
        DataFrame that contains one row per outcome associated with state_field=state.
    state_field : str
        Name of the column in state_outcomes_denormalized that represents the value state.
    n : int, optional
        Number of rows to be generated.

    Returns
    -------
    pandas.DataFrame
        Contains `n` rows with uniformly distributed state and sub-states.
        Any sub-states within a state is also uniformly distributed within itself.

    """

    state_sample = np.random.choice(state_outcomes_denormalized[state_field].unique(),
                                    n,
                                    replace=True)
    state_sample = pd.DataFrame({state_field: state_sample})
    states_and_samples = [(state,
                           select_state_domain_for_state(state_outcomes_denormalized,
                                                         state,
                                                         state_field),
                           sample_for_state)
                          for state, sample_for_state in state_sample.groupby(state_field)]
    sample = pd.concat([generate_string_for_state(state_domain_df,
                                                  sample_for_state)
                        for _, state_domain_df, sample_for_state in states_and_samples])
    sample.reset_index(inplace=True,
                       drop=True)
    # TODO: This rename was introduced to account for cases where a single sample is generated without being joined
    # into a pre-existing sample. This needs to be tested and may cause a bug in some string generators where the
    # suffix gets added inappropriately, leading to some unknown dependency getting affected. We need to test this thoroughly
    # and come up with a more elegant solution for this. (Specific case of StartString and EndString Generators)
    sample.rename(columns={"String": "String_" + state_field},
                  inplace=True)
    # Added to ensure String fields are always strings
    # sample['String_'+state_field] = sample['String_'+state_field].apply(str)
    return sample

def generate_sample_for_state(instance,
                              state,
                              state_sample,
                              lsuffix,
                              rsuffix):
    """For an instance of a string generator, it generates a sample of same size as `state_sample` from the instances
    state_field dataframe and joins it onto `state_sample` with `lsuffix` and `rsuffix` for overlapping rows.

    Parameters
    ----------
    instance : StringGenerator
        The equivalent of self in a class method.
    state : int
        The state that is to be sampled for.
    state_sample : pandas.DataFrame
        A Dataframe object that is to be joined onto.
    lsuffix : str
        To be concatenated to the columns in `state_sample`.
    rsuffix : str
        To be concatenated to the columns the sample generated from `instance`, if there are overlaps.

    Returns
    -------
    pandas.DataFrame
        The state_sample DataFrame that is joined onto by a sample of `instance` from `state`.

    Notes
    -----
    This method does not perform any checks on state_sample to ensure that it contains that
    right rows to be joint onto. This responsibility is with the client.

    """
    state_domain_df = select_state_domain_for_state(instance.__dict__[instance.state_field],
                                                    state,
                                                    instance.state_field,
                                                    filter_state_field=False)
    sample_to_join = state_domain_df.sample(state_sample.shape[0],
                                            replace=True)
    if instance.string_field in state_sample.columns:
        state_sample.rename(columns={instance.string_field: instance.string_field+rsuffix},
                            inplace=True)
    if instance.string_field in sample_to_join.columns:
        sample_to_join.rename(columns={instance.string_field: instance.string_field+lsuffix},
                            inplace=True)
    joint_sample = state_sample.reset_index(drop=True).join(sample_to_join.reset_index(drop=True),
                                                            lsuffix = rsuffix,
                                                            rsuffix = lsuffix)
    if instance.string_field in joint_sample.columns:
        joint_sample.rename(columns={instance.string_field: instance.string_field+lsuffix},
                            inplace=True)
    return joint_sample

def generate_sample_for_all_states(instance,
                              state_sample,
                              lsuffix,
                              rsuffix):
    """For an instance of a string generator, it generates a sample of same size as `state_sample` from the instances
    state_field DataFrame and joins it onto state_sample with `lsuffix` and `rsuffix` for overlapping rows.

    Parameters
    ----------
    instance : StringGenerator
        The equivalent of self in a class method.
    state_sample : pandas.DataFrame
        A Dataframe object that is to be joined onto.
    lsuffix : str
        To be concatenated to the columns in `state_sample`, if there are overlaps.
    rsuffix : str
        To be concatenated to the columns in the sample generated from `instance`, if there are overlaps.

    Returns
    -------
    pandas.DataFrame
        The state_sample DataFrame that is joined onto by a sample of `instance`.

    Notes
    -----
    This method does not perform any checks on state_sample to ensure that it contains that
    right rows to be joint onto. This responsibility is with the client.

    """
    #This rename was added to accoint for cases where instance.string_field exists as a column
    #in state_sample. In this case, because instance.sample() appends instance.state_field to
    #the instance.string_field column, the join function does not apply suffixes (as there is no
    #overlap).
    if instance.string_field in state_sample.columns:
        state_sample.rename(columns={instance.string_field: instance.string_field+rsuffix},
                            inplace=True)

    sample_to_join = instance.sample(state_sample.shape[0])
    joint_sample = state_sample.reset_index(drop=True).join(sample_to_join.reset_index(drop=True),
                                                            lsuffix = rsuffix,
                                                            rsuffix = lsuffix)
    if instance.string_field in joint_sample.columns:
        joint_sample.rename(columns={instance.string_field: instance.string_field+lsuffix},
                            inplace=True)
    return joint_sample

def generate_order_choice_string(row):
    """Generates a str of values determined by its presence and ordering in Order_Choice.

    Parameters
    ----------
    row : pandas.Series
        A Series object containing a dictionary. It contains Order_Choice as a key.

    Returns
    -------
    str
        The values determined by Order_Choice. Each value is separated by a whitespace.

    """

    return " ".join([x for x in row[row['Order_Choice']].values if x!=''])