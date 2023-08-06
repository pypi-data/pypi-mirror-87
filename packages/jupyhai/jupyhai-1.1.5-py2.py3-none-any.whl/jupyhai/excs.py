class Problem(Exception):
    code = None
    status_code = 400

    def __init__(self, message, code=None, status_code=400):
        super(Problem, self).__init__(message)
        self.code = code
        self.status_code = status_code
