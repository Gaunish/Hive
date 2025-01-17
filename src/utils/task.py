
class Task:
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        result = self.func(*self.args, **self.kwargs)
        return result