from calculator import *

while True:
    expression = input(" > ")

    ast = parse_expr(tokenize(expression))

    print(ast.evaluate().as_representation())