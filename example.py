from exsol import solve_expression

while True:
    # Take input from the user
    user_input = input("Please write an expression: \033[31m")
    # Call the library to solve the expression
    answer, err = solve_expression(user_input)

    # If the expression failed to solve, print the error
    if err: print(f"{err}\033[0m")
    # Else, print the answer
    else: print(f"= {answer}\033[0m")
