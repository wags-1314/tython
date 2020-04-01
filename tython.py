from parser import parse
from printer import print_forms
from tython_types import Environment, Symbol, List, Procedure
from standard_env import std_env
import sys


def is_macro_call(expr, env):
    if type(expr) == List and type(expr[0]) == Symbol:
        f = env.get(expr[0])
        return type(f) == Procedure and f.is_macro
    return False

def macroexpand(expr, env):
    while is_macro_call(expr, env):
        mac = env.get(expr[0])
        expr = mac(*expr[1:])
    return expr


def READ(source):
    return parse(source)


def EVAL(expr, env):
    while True:
        expr = macroexpand(expr, env)
        if type(expr) in (int, bool, str):
            return expr
        elif type(expr) == Symbol:
            return env.get(expr)
        elif expr[0] == "define":
            if type(expr[1]) != List:
                symbol = Symbol(expr[1])
                body = List(expr[2:])
                body.insert(0, "do")
                value = EVAL(body, env)
                env.set(symbol, value)
                return symbol
            else:
                name, *params = expr[1]
                symbol = Symbol(name)
                body = List(expr[2:])
                body.insert(0, Symbol("do"))
                env.set(symbol, Procedure(params, body, env, EVAL))
                return symbol
        elif expr[0] == "macro":
            name, *params = expr[1]
            symbol = Symbol(name)
            body = List(expr[2:])
            body.insert(0, Symbol("do"))
            proc = Procedure(params, body, env, EVAL)
            proc.is_macro = True
            env.set(symbol, proc)
            return symbol
        elif expr[0] == "lambda":
            params = expr[1]
            body = List(expr[2:])
            body.insert(0, Symbol("do"))
            print(body)
            return Procedure(params, body, env, EVAL)
        elif expr[0] == "let":
            bindings = expr[1]
            body = List(expr[2:])
            body.insert(0, Symbol("do"))
            local_env = Environment(env)

            for binding in bindings:
                param = binding[0]
                expr = binding[1]
                local_env.set(Symbol(param), EVAL(expr, env))

            expr = body
            env = local_env
            continue

            return EVAL(body, local_env)
        elif expr[0] == "if":
            if EVAL(expr[1], env):
                expr = expr[2]
                continue
            else:
                if len(expr) > 3:
                    expr = expr[3]
                    continue
                else:
                    return None
        elif expr[0] == "do":
            body = expr[1:]
            [EVAL(e, env) for e in body[:-1]]
            expr = body[-1]
            continue
        elif expr[0] == "quote":
            return expr[1]
        else:
            symbol, *arguments = expr
            function = EVAL(symbol, env)
            arguments = [EVAL(argument, env) for argument in arguments]

            if type(function) == Procedure:
                expr = function.body
                local_env = Environment(env)
                local_env.bind(function.params, arguments)
                env = local_env
                continue
            else:
                return function(*arguments)


def PRINT(expr):
    return print_forms(expr)


def slurp(file_name):
    string = ""
    with open(file_name) as file:
        string = file.read()

    return string


std_env.set(Symbol("eval"), lambda a: EVAL(a, std_env))
std_env.set(Symbol("slurp"), slurp)
std_env.set(Symbol("parse"), parse)
print(EVAL(READ("(define (load-file file-name) (eval (parse (slurp file-name))))"), std_env))


if __name__ == "__main__":
    line_count = 1
    while True:
        source = input(f"[{line_count}] ty> ")
        parse_tree = READ(source)
        print("\n", PRINT(EVAL(parse_tree, std_env)), sep="")
        line_count += 1
