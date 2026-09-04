
# Exsol.py

An **Ex**pression **sol**ver that takes PEMDAS and parentheses into account and includes the following operators with more to come: addition, subtraction, multiplication, division, modulo, exponentiation, factorial and negation. It has passed all 191 tests I've written for it, and is quite stable, however I do miss implicit multiplication that I haven't implemented yet.
## Usage/Examples
Below is the "example.py" file attached to the repo that showcases how you can utilize the library. You can simply copy the "exsol.py" file into your project and import it. 
```python
from exsol import solve_expression

while True:
    # Take input from the user
    user_input = input("Please write an expression: \033[31m")
    # Call the library to solve the expression
    answer, err = solve_expression(user_input)

    # If the expression failed to solve, print the error
    if err: print(err)
    # Else, print the answer
    else: print(f"= {answer}")
```
To execute the example file, download it, have python installed, open a terminal and write the following:
```bash
$ py example.py
Please write an expression: -5 * (5/2)
= -12.5
Please write an expression: (3+7) * (2-8)
= -60
```
## Running Tests

To run tests, clone the repo, have python installed, open a terminal and run
```bash
$ py test.py
```
To add to the tests list, locate the `tests.txt` file and add an entry using this format:
- Each line should be one test
- The expression is one the left of the equals sign, while the answer should be on the right
- To make a new category, write the category name in brackets, then have a test follow, like so:
    ```
    [Standard Arithmetic] 1 + 1 = 2
    ```
- All following tests will be in the last defined category
