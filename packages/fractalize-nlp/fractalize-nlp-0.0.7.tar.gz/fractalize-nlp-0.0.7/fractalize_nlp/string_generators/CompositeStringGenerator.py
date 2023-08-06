from fractalize_nlp.string_generators.BaseStringGenerator import BaseStringGenerator
from itertools import accumulate
import pandas as pd
import numpy as np
from functools import partial

def transform_row(joint_string_field,row):
    strings = row[row.OrderChoiceStrings.ComponentString]
    lengths = map(len, strings)
    start_offsets = []
    end_offsets = []
    final_string = ''
    for idx, (string, l) in enumerate(zip(strings, lengths)):
        cursor = len(final_string)
        if l > 0:
            if final_string!= '':
                final_string+= " "+string
                cursor+=1
            else:
                final_string = string
        next_cursor = len(final_string)
        start_offsets.append(cursor)
        end_offsets.append(next_cursor)

    offsets_df = pd.DataFrame({'StartOffset':start_offsets,
                                  'EndOffset':end_offsets},
                              index = row['OrderChoiceStrings'].index)
    s1 = pd.concat([offsets_df,
                    row['OrderChoiceStrings']],
                  axis=1)
    s2 = pd.Series([s1,final_string],
                   index=['OrderChoiceStrings',joint_string_field])
    return s2


def transform_order_choice_df(order_choice_df,component_code_df):
    order_choice_df['OrderChoiceIndices'] = [list(map(int,
                                                 x.split("|")))
                                             for x in order_choice_df.OrderChoice]
    order_choice_df['OrderChoiceStrings'] = [component_code_df.loc[x].copy(deep=True)
                                             for x in order_choice_df.OrderChoiceIndices]


class CompositeStringGenerator(BaseStringGenerator):

    def __init__(self,
                 config):
        super().__init__(config)
        self.state_field = "OrderChoiceCode"
        self.component_code_field = "ComponentStringCode"
        self.string_field = "String"
        self.joint_string_field = "_".join([self.string_field,
                                            self.state_field])
        self.transform_function = partial(transform_row,self.joint_string_field)
        self.validate_dataframes()
        transform_order_choice_df(self.__dict__[self.state_field],
                                  self.__dict__[self.component_code_field])

    def validate_dataframes(self):
        fields_status = [(x, x in self.__dict__)
                         for x in [self.state_field,
                                   self.component_code_field]]
        for nfd,status in [x for x in fields_status if not x[1]]:
            raise (Exception("DataFrame not found for required field {0}".format(nfd)))

        for fd,status in [x for x in fields_status if x[1]]:
            if fd not in self.__dict__[fd].columns:
                raise (Exception("Dataframe for required field {0} does not contain field column".format(fd)))

        return True

    def generate_sample_for_state(self, state, other_sample, other_state_field):
        joint_sample = super().generate_sample_for_state(state,
                                                   other_sample,
                                                   other_state_field)

        joint_sample[['OrderChoiceStrings',
                      self.joint_string_field]] = joint_sample.apply(self.transform_function,
                                                                                                 axis=1)

        return joint_sample

    def generate_sample_for_all_states(self, other_sample, other_state_field):
        '''Pseudocode to test:
        for idx,row in joint_sample.iterrows():
            if len(row[self.joint_string_field])>0:
                if len(row[self.joint_string_field])!=row['Premium.OrderChoiceStrings']['EndOffset'].max():
                    print('break')
                    break
            for ii,rr in row['OrderChoiceStrings'].iterrows():
                if row[self.joint_string_field][rr['StartOffset']:rr['EndOffset']]!= row[rr['ComponentString']]:
                    print('break1')
                    break'''
        joint_sample = super().generate_sample_for_all_states(other_sample,
                                                              other_state_field)

        joint_sample[['OrderChoiceStrings',
                      self.joint_string_field]] = joint_sample.apply(self.transform_function,
                                                                           axis=1)

        return joint_sample
