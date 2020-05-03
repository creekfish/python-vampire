class Result:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ResultSuccess(Result):
    pass


class ResultFailure(Result):
    pass
