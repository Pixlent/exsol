from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from exsol import solve_expression

# A config of sorts
SOLVE_EXPRESSION = solve_expression
TEST_FILE = "tests.txt"
PERCENT_DECIMAL = 2
PRINT_SUCCESSFUL_TESTS = False

# A table of colors, usage: Use a pretty string (f"") and use {} with the property to insert it
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

# The unit for a test, contains a description of what the test is,
# the expression being tested and the correct answer
@dataclass
class Test:
    description: str
    expression: str
    answer: tuple[Decimal | None, str | None]

# Returns true if the string can be cast to the Decimal class
def is_number(value: str) -> bool:
    try:
        _ = Decimal(value)
        return True
    except (InvalidOperation, TypeError):
        return False

# Returns a parsed list of tests, loaded from a text file
def import_list() -> list[Test]:
    # Read the file
    with open(TEST_FILE, "r", encoding="utf-8") as file:
        # Initialize the array that contains the tests
        tests: list[Test] = []
        # An array of the lines in the file
        raw_tests = file.readlines()
        # The description of the current test being read
        description = "Blank"

        # Loop over all lines in the file
        for line in raw_tests:
            # Skip if the line doesn't contain an equal sign
            if not "=" in line:
                continue

            # Parse the description
            if line.startswith("[") and "]" in line:
                end_bracket = line.find("]")
                description = line[1:end_bracket]
                line = line[end_bracket + 1:].strip()

            # Extract the expression and the answer from the equation
            expression, answer_str = (part.strip() for part in line.rsplit("=", 1))

            # If the answer is a valid number, parse it
            if is_number(answer_str): answer = (Decimal(answer_str), None)
            else: answer = (None, answer_str)

            # Append the test
            tests.append(Test(description, expression, answer))
    return tests

# Parse the percent between two numbers and return it in a pretty manner
def pretty_percent(part: int, whole: int) -> str:
    part *= 100

    if part % whole != 0:
        return f"~{round(part / whole, PERCENT_DECIMAL)}"
    return f"{round(part / whole)}"

# Return a pretty index where we have enough space to so the indexes align when printed
def pretty_index(num: int, length: int) -> str:
    pretty = str(num)

    while len(pretty) != length:
        pretty = f" {pretty}"
    return pretty


# Returns true if the test passes, false otherwise. bool: true if the test passes, answer: the correct answer, err: the error encountered if it doesn't succeed
def check_answer(test: Test) -> tuple[bool, Decimal | None, str | None]:
    try:
        # Try to solve the expression using the solver provided
        result, err = SOLVE_EXPRESSION(test.expression)

        if err and err == test.answer[1]: return True, None, err # Passed, there is supposed to be an error, and they match
        if result == None: return False, None, err               # Not passed, there's no result, therefore an error
        return result == test.answer[0], result, None            # Passes if the result matches the key answer
    # Catch exceptions thrown by python: for instance if the program crashes
    except Exception as e:
        err = str(e)

        if err: return False, None, err
        else: return False, None, "Unknown exception"

# Runs the tests and print the results
def test():
    # Import the list of tests
    tests = import_list()

    # Calculate the total amount of tests
    total_tests = len(tests)
    # Keep count of how many tests pass
    tests_passed = 0

    # Loop over all tests
    for index, test in enumerate(tests):
        test_number = pretty_index(index + 1, len(str(total_tests)))
        passes, result, err = check_answer(test)

        # If the test passes, increment the counter and print the test if enabled
        if passes:
            tests_passed += 1
            if PRINT_SUCCESSFUL_TESTS:
                print(f"[{test_number}. Test passed] {TEXT_YELLOW}{test.expression}{RESET} = {TEXT_GREEN}{test.answer[0]}{RESET}")
        # If the test fails, print as much relevant information and possible
        else:
            print(f"{BACK_RED}[{test_number}. Test failed]{RESET}")
            print(f"expression . . . | {TEXT_YELLOW}{test.expression}{RESET} != {TEXT_YELLOW}{test.answer[0]}{RESET}")
            print(f"category . . . . | {test.description}")
            print(f"solver . . . . . | {TEXT_RED}{result}{RESET}")
            print(f"error  . . . . . | {TEXT_RED}{err}{RESET}")

    # Calculate the percent passed in a pretty manner
    percent_passed = pretty_percent(tests_passed, total_tests)

    # Print results to the console
    print()
    if total_tests == tests_passed:
        print(f"All tests passed {TEXT_GREEN}(100%)")
    else:
        print(f"{TEXT_YELLOW}{tests_passed} of {TEXT_YELLOW}{total_tests} tests passed {TEXT_RED}({percent_passed}%)")

# Run all the tests
test()
