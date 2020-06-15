"""Custom Exception classes"""


class MissingParams(Exception):
    def __init__(self, params):
        self.message = "Missing params: {}".format(params)
        super(MissingParams, self).__init__(self.message)

