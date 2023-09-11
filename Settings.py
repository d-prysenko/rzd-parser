import json, os

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Settings(metaclass=Singleton):
    data = {}
    cwd = ''

    def __init__(self):
        self.cwd = os.path.dirname(__file__)

        with open(self.cwd + '/parameters.json', 'r') as params_file:
            self.data = json.load(params_file)

    def get(self, key):
        return self.data[key]