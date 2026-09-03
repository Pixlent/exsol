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
A function called "solve_expression" that returns an answer or an error detailing what went wrong. Optionally show how it solved it (what order and so on)
We first tokenize the input string to make it easier to operate on. Here we also convert aliases, strip spaces and so on
We then convert the list of tokens into reverse polish notation
We then take the stack and evaluate it, solving the equation

Test archetecture:
We have a list of groups of tests. A group is a category of tests that gets executed.
When a test spans more than a single line, add ":" for every line.

Replace * and / with × and ÷ when showing.

Passed all test cases!

Reverse polish notation is an alternative to the infix notation we are used to. It doesn't require brackets and doesn't need to look ahead. It's sequential, making it easy for computers.

The Single-Pop Precedence Bug is present (use a while loop, instead of if).

Look at Djikstra's Two-stack algo and compare

Rebuild the tokenizer, to be even dumber and include identifiers and such (for functions and variables.)

Intended behavior for tokenizer:
If operator, append operator and buffer
If number and buffer is number, add number to buffer
If number and buffer is identifier, append buffer and start a new buffer with that number
If identifier and buffer is identifier, add identifier to buffer
If identifier and buffer is identifier, append buffer and start a new buffer with that identifier
If space, skip
Otherwise error.

(100 - 50) / (2 + 3) = 10

OUT: 
OPS: 

1. + -
2. * /
3. ^

+5    = 5
+
5

-(-5) = 5
-
(
-
5
)

(5 * (2 + 3)) - 10 = 15

(
5
*
(
2
+
3
)
)
-
10

Sources:
https://switzerb.github.io/imposter/algorithms/2021/01/12/dijkstra-two-stack.html
