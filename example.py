from main import solve_expression

user_input = input("Please write an equation: \033[31m")
answer, err = solve_expression(user_input)

print(f"= {answer}")
