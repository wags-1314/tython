from tython_types import Environment, List, Symbol
import parser


def cons(a, b):
    if type(b) == List:
        return List([a] + b)
    else:
        return List([a, b])


std_env = Environment(None)
std_env.set(Symbol("+"), lambda a, b: a + b)
std_env.set(Symbol("-"), lambda a, b: a - b)
std_env.set(Symbol("*"), lambda a, b: a * b)
std_env.set(Symbol("quotient"), lambda a, b: a // b)
std_env.set(Symbol("remainder"), lambda a, b: a % b)
std_env.set(Symbol("pow"), lambda a, b: a ** b)
std_env.set(Symbol("exit"), lambda: sys.exit())
std_env.set(Symbol("="), lambda a, b: a == b)
std_env.set(Symbol("!="), lambda a, b: a != b)
std_env.set(Symbol(">"), lambda a, b: a > b)
std_env.set(Symbol(">="), lambda a, b: a >= b)
std_env.set(Symbol("<"), lambda a, b: a < b)
std_env.set(Symbol("<="), lambda a, b: a <= b)
std_env.set(Symbol("and"), lambda a, b: a and b)
std_env.set(Symbol("or"), lambda a, b: a or b)
std_env.set(Symbol("not"), lambda a: not a)
std_env.set(Symbol("print"), lambda a: print(a, end=""))
std_env.set(Symbol("println"), lambda a: print(a))
std_env.set(Symbol("quote"), lambda a: a)
std_env.set(Symbol("::"), cons)
std_env.set(Symbol("and"), lambda a, b: a + b)
std_env.set(Symbol("head"), lambda a: a[0])
std_env.set(Symbol("tail"), lambda a: List(a[1:]))
std_env.set(Symbol("empty?"), lambda a: True if len(a) == 0 else False)
std_env.set(Symbol("list"), lambda *a: List(a))
std_env.set(Symbol("list?"), lambda a: type(a) == List)
std_env.set(Symbol("count"), lambda a: len(a))
std_env.set(Symbol("symbol?"), lambda a: type(a) == Symbol)
std_env.set(Symbol("number?"), lambda a: type(a) == int)
std_env.set(Symbol("eq?"), lambda a, b: a == b)
std_env.set(Symbol("nth"), lambda a, b: a[b])
