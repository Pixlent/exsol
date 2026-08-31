# TODO:
- Make aliases work for operators (:, / and ÷ all work for division)
- Proper error handling (like giving error messages, showing to where the fail is, coming up with suggestions, etc)
- Decouple code for easier modification and easier reading
- Remove the ability to return multiple answers
- Implicit multiplication with parentheses
- Functions, like sqr(), sin(), cos()
- Ability to set and use variables, including default ones like pi
- Add the factorial operator
- Variable precision by digit count

Archetecture:
A function called "evaluate_expression" that returns an answer or an error detailing what went wrong. Optionally show how it solved it (what order and so on)

Test archetecture:
We have a list of groups of tests. A group is a category of tests that gets executed.
When a test spans more than a single line, add ":" for every line.

Replace * and / with × and ÷ when showing.

Passed all test cases!
