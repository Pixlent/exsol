from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from exsol import solve_expression

SOLVE_EXPRESSION = solve_expression
TEST_FILE = "tests.txt"
PERCENT_DECIMAL = 2

RESET        = "\033[0m"
BOLD         = "\033[1m"

TEXT_RED     = "\033[31m"
TEXT_GREEN   = "\033[32m"
TEXT_YELLOW  = "\033[33m"
TEXT_BLUE    = "\033[34m"
TEXT_MAGENTA = "\033[35m"
TEXT_CYAN    = "\033[36m"

BACK_RED     = "\033[41m"
BACK_GREEN   = "\033[42m"
BACK_YELLOW  = "\033[43m"
BACK_BLUE    = "\033[44m"
BACK_MAGENTA = "\033[45m"
BACK_CYAN    = "\033[46m"

@dataclass
class Test:
    description: str
    expression: str
    answer: tuple[Decimal | None, str | None]

def is_number(value: str) -> bool:
    try:
        _ = Decimal(value)
        return True
    except (InvalidOperation, TypeError):
        return False

def import_list() -> list[Test]:
    with open(TEST_FILE, "r", encoding="utf-8") as file:
        tests: list[Test] = []
        raw_tests = file.readlines()
        description = "Blank"

        for line in raw_tests:
            if not "=" in line:
                continue

            if line.startswith("[") and "]" in line:
                end_bracket = line.find("]")
                description = line[1:end_bracket]
                line = line[end_bracket + 1:].strip()

            expression, answer_str = (part.strip() for part in line.rsplit("=", 1))

            if is_number(answer_str): answer = (Decimal(answer_str), None)
            else: answer = (None, answer_str)

            tests.append(Test(description, expression, answer))
    return tests

def pretty_percent(part: int, whole: int) -> str:
    part *= 100

    if part % whole != 0:
        return f"~{round(part / whole, PERCENT_DECIMAL)}"
    return f"{round(part / whole)}"

def pretty_index(num: int, length: int):
    pretty = str(num)

    while len(pretty) != length:
        pretty = f" {pretty}"
    return pretty


# Returns true if the check passes, false otherwise. bool, answer, err
def check_answer(test: Test) -> tuple[bool, Decimal | None, str | None]:
    try:
        result, err = SOLVE_EXPRESSION(test.expression)

        if err and err == test.answer[1]: return True, None, err # Passed, there is supposed to be an error, and they match
        if result == None: return False, None, err                   # Not passed, there's no result, therefore an error
        return result == test.answer[0], result, None            # Passes if the result matches the key answer
    except Exception as e:
        err = str(e)

        if err: return False, None, err
        else: return False, None, "Unknown exception"

def test():
    tests = import_list()

    total_tests = len(tests)
    tests_passed = 0

    for index, test in enumerate(tests):
        test_number = pretty_index(index + 1, len(str(total_tests)))
        passes, result, err = check_answer(test)

        if passes:
            tests_passed += 1
            print(f"[{test_number}. Test passed] {TEXT_YELLOW}{test.expression}{RESET} = {TEXT_GREEN}{test.answer[0]}{RESET}")
        else:
            print(f"{BACK_RED}[{test_number}. Test failed]{RESET} Category: {test.description}{RESET}")
            print(f"|   {TEXT_YELLOW}{test.expression} != {TEXT_RED}{test.answer[0]} {TEXT_RED}{RESET}")
            print(f"|   {TEXT_RED}{result} is not correct, error: {err}{RESET}")

    percent_passed = pretty_percent(tests_passed, total_tests)

    print()
    if total_tests == tests_passed:
        print(f"All tests passed {TEXT_GREEN}(100%)")
    else:
        print(f"{TEXT_YELLOW}{tests_passed} of {TEXT_YELLOW}{total_tests} tests passed {TEXT_RED}({percent_passed}%)")

test()
