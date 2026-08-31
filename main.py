from decimal import Decimal
import math

def tokenize(input: str) -> list[str]:
    buffer = ""
    tokens: list[str] = []

    for char in input:
        if char.isdigit() or char == "." or (buffer == "" and char == "-"):
            buffer += char
        elif char == "-" and buffer == "-":
            buffer = ""
        elif char == "+" or char == "-" or char == "*" or char == "/" or char == "^" or char == "%" or char == "(" or char == ")":
            if buffer:
                tokens.append(buffer)
            buffer = ""
            tokens.append(char)
    if buffer:
        tokens.append(buffer)
    return tokens

def print_tokens(tokens: list[str]):
    print("\033[31m=\033[0m", end="")
    for token in tokens:
        print(f"\033[31m{token} \033[0m", end="")
    print()

def calculate(operator: str, left: Decimal, right: Decimal) -> tuple[Decimal | None, str | None]:
    if operator == "^": return left ** right, None
    if operator == "*": return left * right, None
    if operator == "+": return left + right, None
    if operator == "-": return left - right, None
    if operator == "%": return left % right, None
    if operator == "/" and right == 0: return None, "Can't divide by zero"
    if operator == "/": return left / right, None
    return None, "Error occured while calculating"

def reduce_operators(tokens: list[str], operators: list[str]) -> str | None:
    index = 0;
    while index < tokens.__len__():
        token = tokens[index]
        index += 1
        for operator in operators:
            if token == operator:
                index -= 1
                result, err = calculate(operator, Decimal(tokens[index-1]), Decimal(tokens[index+1]))
                if err:
                    return err
                tokens[index - 1] = str(result)
                del tokens[index:index+2]

def resolve_parentheses(tokens: list[str]) -> list[str]:
    if "(" in tokens:
        start = 0
        depth = 0
        index = 0
        while index < len(tokens):
            token = tokens[index]
            if token == "(":
                if depth == 0:
                    start = index
                    depth += 1
                else: depth += 1
            elif token == ")":
                if depth == 1:
                    result = evaluate_expression(tokens[start + 1:index])
                    del tokens[start:index + 1]
                    tokens[start:start] = result
                    index = start
                depth -= 1
            index += 1;

    return tokens

def evaluate_expression(tokens: list[str]) -> list[str]:
    tokens = resolve_parentheses(tokens)

    err1 = reduce_operators(tokens, ["^"])
    err2 = reduce_operators(tokens, ["*", "/", "%"])
    err3 = reduce_operators(tokens, ["+", "-"])

    if err1:
        return [err1]
    if err2:
        return [err2]
    if err3:
        return [err3]

    # temp fix
    if len(tokens) > 1:
        tokens[0] = str(math.prod([Decimal(x) for x in tokens]))
        del tokens[1:]

    return tokens

def solve_expression(expression: str) -> tuple[Decimal | None, str | None]:
    tokens = tokenize(expression)
    solved = evaluate_expression(tokens)

    return Decimal(solved[0]), None
