import math
from collections.abc import Callable
from decimal import Decimal, InvalidOperation
from typing import NamedTuple

# A python script that solves expressions. Based on dijkstra-two-stack algorhitm

# A config of sorts
SPECIAL_TOKENS = ["(", ")"]
ALLOW_IDENTIFIERS = False

# Returns true if the string can be interpretet as a number
def is_valid_number(value: str) -> bool:
    return is_number(value) or value == "."

# Takes an expression as an input and tokenizes it into a list of tokens, returns an error otherwise
# An example is "-5 * ( 5 + 5 )" into ["-", "5", "*", "(", "5", "+", "5", ")"]
def tokenize(input: str)-> tuple[list[str] | None, str | None]:
    # Remove all leading and trailing whitespace
    input = input.strip()
    # Error if the string is empty
    if not input:
        return None, "The input expression is empty"

    # A buffer used to store numbers, and optionally identifiers
    buffer = ""
    # This will eventually be the list of tokens
    tokens: list[str] = []

    # Loop over all characters in the expression
    for char in input:
        # If the character is an operator or parentheses, append it to the list
        if char in OPERATORS or char in SPECIAL_TOKENS:
            if buffer:
                tokens.append(buffer)
            buffer = ""
            tokens.append(char)
            continue

        # If we disallow identifiers, return an error if found
        if not ALLOW_IDENTIFIERS:
            if char.isalpha(): return None, "Identifiers are not allowed in expressions"
            if char == "_": continue

        # Check if the character is a number, if so attempt to add it to the buffer
        # If we can't append the current character to the buffer (it isn't a number), append the buffer to the list
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
        # If identifiers are allowed, we would handle them similar to numbers where they can span multiple characters
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

    # If the buffer isn't empty, append it to the list
    if buffer:
        tokens.append(buffer)
    # Return the list
    return tokens, None

# The base class for all operands, like addition or multiplication
class Operator(NamedTuple):
    precedence: int                             # The priority of the operator, according to PEMDAS
    associativity: str                          # 'L' or 'R'
    func: Callable[[list[Decimal]], str | None] # The function called that does the operation. Returns an error if something failed.
    arity: int = 2                              # 1 for unary, 2 for binary and so on

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

# Negation operator, like in -1
def neg(stack: list[Decimal]) -> str | None:
    value = stack.pop()

    stack.append(value * -1)
    return None

# The list of all operators, their priority (according to pemdas), whether or not they're left or right associated,
# The function that actually applies the operation to the stack and optionally how many numbers the operation takes.
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

# Returns true if the string can be cast into the Decimal class (a number)
def is_number(value: str) -> bool:
    try:
        _ = Decimal(value)
        return True
    except (InvalidOperation, TypeError):
        return False

# Takes in a list of tokens, for instance: ["-", "5", "*","(", "5", "+", "5", ")"]
# And tries to evaluate it into a single number.
# Returns the number if successful and an error otherwise.
def eval_expression(tokens: list[str]) -> tuple[Decimal | None, str | None]:
    # The value stack
    out: list[Decimal] = []
    # The operator stack
    ops: list[str] = []

    if tokens.count("(") != tokens.count(")"):
        return None, "Mismatched parentheses: expected a matching parenthesis"

    # If the expression contains a minus, check for the negation operator
    if "-" in tokens:
        for index, token in enumerate(reversed(tokens)):
            if token == "-":
                if index == len(tokens) -1:
                    tokens[(len(tokens)-1)-index] = "_neg"
                    continue
                if tokens[len(tokens)-2-index] in OPERATORS or tokens[len(tokens)-2-index] == "(":
                    tokens[(len(tokens)-1)-index] = "_neg"

    # If the expression contains a plus, mark it for removal
    if "+" in tokens:
        for index, token in enumerate(reversed(tokens)):
            if token == "+":
                if index == len(tokens) -1:
                    tokens[(len(tokens)-1)-index] = "_rem"
                    continue
                if tokens[len(tokens)-2-index] in OPERATORS or tokens[len(tokens)-2-index] == "(":
                    tokens[(len(tokens)-1)-index] = "_rem"
    # Remove everything marked for removal
    tokens[:] = [token for token in tokens if token != "_rem"]

    # Solve the expression using dijkstra-two-stack algorhitm, start by looping over all tokens
    for token in tokens:
        # If the token is a number, push it to the number stack
        if is_number(token):
            out.append(Decimal(token))
            continue

        # If the token is a open parentheses, push it to the operator stack
        if token == "(": ops.append("(")
        # If the token is a closing parentheses, loop over the operator stack until we find a open parentheses
        if token == ")":
            for _ in range(len(ops)):
                op = ops.pop()
                # If we find a open parentheses, exit
                if op == "(":
                    break
                # Pop the operator and run it
                err = OPERATORS[op].func(out)
                if err:
                    return None, err

        # Do the following logic if the token is an operator
        if token in OPERATORS:
            # If the operator is an open parentheses, add it to the operator stack
            if len(ops) < 1 or ops[len(ops) - 1] == "(":
                ops.append(token)
                continue

            token_precedence = OPERATORS[token].precedence
            token_associativity = OPERATORS[token].associativity
            stack_precedence = OPERATORS[ops[len(ops) - 1]].precedence

            # If the operator is left associated and has higher precedence than the first operator on the operator stack, append it
            # If the operator is right associated and has a higher or equal precedence than the first operator on the operator stack, append it
            if (token_associativity == "L" and token_precedence > stack_precedence) or (token_associativity == "R" and token_precedence >= stack_precedence):
                ops.append(token)
                continue
            if len(out) < OPERATORS[ops[len(ops) - 1]].arity:
                return None, "Not a valid expression: too many operators or not enough numbers"
            # Pop the operator and execute it
            err = OPERATORS[ops.pop()].func(out)
            if err:
                return None, err
            # Append the operator
            ops.append(token)

    # Loop over the remaining operators from left to right and pop them
    for op in reversed(ops):
        if op == "(" or op == ")":
            return None, "Mismatched parentheses: expected a matching parenthesis"
        if len(out) < OPERATORS[ops[len(ops) - 1]].arity:
            return None, "Not a valid expression: too many operators or not enough numbers"
        err = OPERATORS[op].func(out)
        if err:
            return None, err
    if len(out) != 1: return None, "Failed to evaluate expression, less or more than one remaining result"
    # Return the number
    return out[0], None

def solve_expression(expression: str) -> tuple[Decimal | None, str | None]:
    # Attempt to tokenize the string, exit early if we encounter problems
    tokens, lex_error  = tokenize(expression)
    if not tokens:
        return None, lex_error
    # Attempt to solve the expression, exit early if we encounter problems
    result, eval_error = eval_expression(tokens)
    if result is None:
        return None, eval_error
    # Return the result if everything went accordingly
    return result, None
