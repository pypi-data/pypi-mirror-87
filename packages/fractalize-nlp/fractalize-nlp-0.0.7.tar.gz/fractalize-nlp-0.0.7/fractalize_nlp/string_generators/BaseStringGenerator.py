from fractalize_nlp.string_generators.utils import *

class BaseStringGenerator():

    def __init__(self, config):
        load_sources(self,config)

    def generate_sample_for_state(self, state, other_sample, other_state_field):
        return generate_sample_for_state(self,
                                         state,
                                         other_sample,
                                         "_"+self.state_field,
                                         "_"+other_state_field)

    def generate_sample_for_all_states(self, other_sample, other_state_field):
        return generate_sample_for_all_states(self,
                                              other_sample,
                                              "_"+self.state_field,
                                              "_"+other_state_field)
    def sample(self,n=10):
        return sample(self.__dict__[self.state_field],
                      self.state_field,
                      n)
