class APIInvalidError(Exception):
    def __init__(self):
        super().__init__('API key is invalid, Please check the API key again on http://digo.ai')

class NotFoundCore(Exception):
    def __init__(self):
        super().__init__('Digo Core is Not Found')

class FailExperiment(Exception):
    def __init__(self):
        super().__init__('Fail Experiment')

class InvalidType(Exception):
    def __init__(self):
        super().__init__('Invalid Input Type')