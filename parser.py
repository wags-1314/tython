from tython_types import List, Symbol, Boolean
import re


def tokenize(string):
    tre = re.compile(
        r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)"""
    )
    return [token for token in re.findall(tre, string) if token[0] != ";"]


def peek(lst, index):
    if index >= len(lst):
        return None
    else:
        return lst[index]


def parse_forms(tokens):
    token = tokens[0]

    if token == "(":
        return parse_list(tokens)
    elif token == ")":
        raise Exception("Unexpected ')")
    elif token == "'":
        tokens.pop(0)
        return List([Symbol("quote"), parse_forms(tokens)])
    else:
        return parse_selfeval(tokens)


def parse_list(tokens):
    tokens.pop(0)  # remove '('
    lst = []

    while peek(tokens, 0) != ")":
        if len(tokens) == 0:
            raise Exception("Expecting a ')'")

        lst.append(parse_forms(tokens))

    tokens.pop(0)  # remove '('

    return List(lst)


def parse_selfeval(tokens):
    token = tokens.pop(0)
    if re.match(r"^[-+]?\d+$", token):
        return int(token)
    elif re.match(r'"(?:[^"\\]|\\.)*"', token):
        return str(token)[1:-1]
    elif token == "#t":
        return True
    elif token == "#f":
        return False
    return Symbol(token)


def parse(source):
    return parse_forms(tokenize(source))
