import math
from collections.abc import Callable
from decimal import Decimal, InvalidOperation
from typing import NamedTuple

SPECIAL_TOKENS = ["(", ")"]
ALLOW_IDENTIFIERS = False

def is_valid_number(value: str) -> bool:
    return is_number(value) or value == "."

def tokenize(input: str)-> tuple[list[str] | None, str | None]:
    input = input.strip()
    if not input:
        return None, "The input expression is empty"

    buffer = ""
    tokens: list[str] = []

    for char in input:
        if char in OPERATORS or char in SPECIAL_TOKENS:
            if buffer:
                tokens.append(buffer)
            buffer = ""
            tokens.append(char)
            continue

        if not ALLOW_IDENTIFIERS:
            if char.isalpha(): return None, "Identifiers are not allowed in expressions"
            if char == "_": continue

        if is_valid_number(char):
            if is_valid_number(buffer):
                if "." in buffer and char == ".":
                    return None, "Multiple decimal points are not allowed"
                buffer += char
            else:
                if buffer:
                    tokens.append(buffer)
                buffer = char
            continue
        elif char.isalpha() or char == "_":
            if not is_valid_number(buffer):
                buffer += char
            else:
                if buffer:
                    tokens.append(buffer)
                buffer = char
            continue
        elif char == " ":
            continue
        else:
            return None, f"Unexpected token: {char}"

    if buffer:
        tokens.append(buffer)
    return tokens, None

class Operator(NamedTuple):
    precedence: int
    associativity: str # 'L' or 'R'
    func: Callable[[list[Decimal]], str | None]
    arity: int = 2  # 1 for unary, 2 for binary and so on

def add(stack: list[Decimal]) -> str | None:
    right = stack.pop()
    left = stack.pop()

    stack.append(left + right)
    return None

def sub(stack: list[Decimal]) -> str | None:
    right = stack.pop()
    left = stack.pop()

    stack.append(left - right)
    return None

def mul(stack: list[Decimal]) -> str | None:
    right = stack.pop()
    left = stack.pop()

    stack.append(left * right)
    return None

def div(stack: list[Decimal]) -> str | None:
    right = stack.pop()
    left = stack.pop()

    if right == 0: return "Cannot divide by zero"

    stack.append(left / right)
    return None

def mod(stack: list[Decimal]) -> str | None:
    right = stack.pop()
    left = stack.pop()

    if right == 0: return "Cannot divide by zero"

    stack.append(left % right)
    return None

def pow(stack: list[Decimal]) -> str | None:
    right = stack.pop()
    left = stack.pop()

    if left == 0 and right < 0: return "Zero raised a negative power is undefined behavior"
    if left == right and left == 0:
        stack.append(Decimal(1))
        return None

    stack.append(left ** right)
    return None

def fac(stack: list[Decimal]) -> str | None:
    value = stack.pop()

    stack.append(Decimal(math.gamma(value + 1)))
    return None

def neg(stack: list[Decimal]) -> str | None:
    value = stack.pop()

    stack.append(value * -1)
    return None

OPERATORS: dict[str, Operator] = {
    "+": Operator(precedence=1, associativity="L", func=add),
    "-": Operator(precedence=1, associativity="L", func=sub),
    "*": Operator(precedence=2, associativity="L", func=mul),
    "/": Operator(precedence=2, associativity="L", func=div),
    "%": Operator(precedence=2, associativity="L", func=mod),
    "^": Operator(precedence=3, associativity="R", func=pow),
    "!": Operator(precedence=4, associativity="L", func=fac, arity=1),
    "_neg": Operator(precedence=3, associativity="R", func=neg, arity=1)
}

def is_number(value: str) -> bool:
    try:
        _ = Decimal(value)
        return True
    except (InvalidOperation, TypeError):
        return False

def eval_expression(tokens: list[str]) -> tuple[Decimal | None, str | None]:
    out: list[Decimal] = []
    ops: list[str] = []

    if tokens.count("(") != tokens.count(")"):
        return None, "Mismatched parentheses: expected a matching parenthesis"

    if "-" in tokens:
        for index, token in enumerate(reversed(tokens)):
            if token == "-":
                if index == len(tokens) -1:
                    tokens[(len(tokens)-1)-index] = "_neg"
                    continue
                if tokens[len(tokens)-2-index] in OPERATORS or tokens[len(tokens)-2-index] == "(":
                    tokens[(len(tokens)-1)-index] = "_neg"

    if "+" in tokens:
        for index, token in enumerate(reversed(tokens)):
            if token == "+":
                if index == len(tokens) -1:
                    tokens[(len(tokens)-1)-index] = "_rem"
                    continue
                if tokens[len(tokens)-2-index] in OPERATORS or tokens[len(tokens)-2-index] == "(":
                    tokens[(len(tokens)-1)-index] = "_rem"
    tokens[:] = [token for token in tokens if token != "_rem"]

    for token in tokens:
        if is_number(token):
            out.append(Decimal(token))
            continue

        if token == "(": ops.append("(")
        if token == ")":
            for _ in range(len(ops)):
                op = ops.pop()
                if op == "(":
                    break
                err = OPERATORS[op].func(out)
                if err:
                    return None, err

        if token in OPERATORS:
            if len(ops) < 1 or ops[len(ops) - 1] == "(":
                ops.append(token)
                continue

            token_precedence = OPERATORS[token].precedence
            token_associativity = OPERATORS[token].associativity
            stack_precedence = OPERATORS[ops[len(ops) - 1]].precedence

            if (token_associativity == "L" and token_precedence > stack_precedence) or (token_associativity == "R" and token_precedence >= stack_precedence):
                ops.append(token)
                continue
            if len(out) < OPERATORS[ops[len(ops) - 1]].arity:
                return None, "Not a valid expression: too many operators or not enough numbers"
            err = OPERATORS[ops.pop()].func(out)
            if err:
                return None, err
            ops.append(token)

    for op in reversed(ops):
        if op == "(" or op == ")":
            return None, "Mismatched parentheses: expected a matching parenthesis"
        if len(out) < OPERATORS[ops[len(ops) - 1]].arity:
            return None, "Not a valid expression: too many operators or not enough numbers"
        err = OPERATORS[op].func(out)
        if err:
            return None, err
    if len(out) != 1: return None, "Failed to evaluate expression, less or more than one remaining result"
    return out[0], None

def solve_expression(expression: str) -> tuple[Decimal | None, str | None]:
    tokens, lex_error  = tokenize(expression)
    if not tokens:
        return None, lex_error
    result, eval_error = eval_expression(tokens)
    if result is None:
        return None, eval_error
    return result, None
