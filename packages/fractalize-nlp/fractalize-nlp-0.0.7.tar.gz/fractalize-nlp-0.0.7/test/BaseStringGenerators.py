from fractalize_nlp.string_generators.BaseStringGenerator import *

class CorrectBaseStringGenerator(BaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)

class ContractedBaseStringGenerator(BaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)

class EmptyBaseStringGenerator(BaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)       

class ExtendedBaseStringGenerator(BaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)

class MismatchBaseStringGenerator(BaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)       

class MultipleBaseStringGenerator(BaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)

class NoDirBaseStringGenerator(BaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)    

class NonexistentBaseStringGenerator(BaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)

class NoStringBaseStringGenerator(BaseStringGenerator):
    def __init__(self, config):
        super().__init__(config)

    def sample(self,n=10):
        return super().sample(n)
  