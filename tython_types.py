from typing import Union, Any


class List(list):
    pass


class Symbol(str):
    pass


class Boolean:
    def __init__(self, boolean):
        self.data = boolean

    def __bool__(self):
        return self.data

    def __repr__(self):
        if self.data:
            return "#t"
        else:
            return "#f"

    def __str__(self):
        return self.__repr__()


class Procedure:
    def __init__(self, params, body, env, eval_function):
        self.params = params
        self.body = body
        self.env = env
        self.EVAL = eval_function
        self.is_macro = False

    def __call__(self, *arguments):
        local_env = Environment(self.env)
        local_env.bind(self.params, arguments)
        return self.EVAL(self.body, local_env)

    def __repr__(self):
        return '#procedure'


class LispException(Exception):
    pass


class Environment:
    def __init__(self, environment):
        self.top_env = environment
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def _get_env(self, key):
        env = self
        while True:
            if key in env.data.keys():
                return env
            elif env.top_env is not None:
                env = env.top_env
            else:
                return None

    def get(self, key):
        env = self._get_env(key)
        if env is not None:
            return env.data[key]
        else:
            return None

    def bind(self, params, arguments):
        """for i, param in enumerate(params):
            self.data[param] = arguments[i]"""
        n = len(params)
        i = 0
        while i < n:
            if params[i] == "*":
                self.data[params[i + 1]] = List(arguments[i:])
                i += 1
            else:
                self.data[params[i]] = arguments[i]

            i += 1

    def __repr__(self):
        return str(self.data)


def is_list(expr):
    return type(expr) == List


def is_symbol(expr):
    return type(expr) == Symbol
