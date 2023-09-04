from fraction import Fraction
from smsin import sin, cos, tan, pi, gr

class Token:
    def __init__(self, lexeme, value):
        self.lexeme = lexeme
        self.value = value

def tokenize(expression):
    expression = cleanup(expression)
    NUMBER = "1234567890."
    NAME = "abcdefghijklmnopqrstuvwxyz"
    NEGATE = "|"
    POWER = "^"
    DIVIDE = "/"
    MULTIPLY = "*"
    MINUS = "-"
    PLUS = "+"
    OPEN_PARAN = "("
    CLOSE_PARAN = ")"

    cval = ""
    
    token_list = []

    index = 0

    expression = expression.replace(" ", "")

    while index < len(expression):
        if expression[index] in NUMBER:
            while index < len(expression) and expression[index] in NUMBER:
                cval += expression[index]
                index += 1
            token_list.append(Token("NUMBER", cval))
            cval = ""
            index -= 1
        elif expression[index] in NAME:
            while index < len(expression) and expression[index] in NAME:
                cval += expression[index]
                index += 1
            token_list.append(Token("NAME", cval))
            cval = ""
            index -= 1
        elif expression[index] in NEGATE:
            token_list.append(Token("NEGATE", "-"))
        elif expression[index] in POWER:
            token_list.append(Token("POWER", POWER))
        elif expression[index] in DIVIDE:
            token_list.append(Token("DIVIDE", DIVIDE))
        elif expression[index] in MULTIPLY:
            token_list.append(Token("MULTIPLY", MULTIPLY))
        elif expression[index] in MINUS:
            token_list.append(Token("MINUS", MINUS))
        elif expression[index] in PLUS:
            token_list.append(Token("PLUS", PLUS))
        elif expression[index] in OPEN_PARAN:
            token_list.append(Token("OPEN_PARAN", OPEN_PARAN))
        elif expression[index] in CLOSE_PARAN:
            token_list.append(Token("CLOSE_PARAN", CLOSE_PARAN))

        index += 1

    return token_list

class Node:
    def __init__(self, own, left_child, right_child):
        self.own = own
        self.left_child = left_child
        self.right_child = right_child

    def print_connected_nodes(self, level = 0):
        indent = "    " * level
        print(indent + "[" + self.own.lexeme, self.own.value + "]", end = "", flush = True)

        print(" {") if self.left_child or self.right_child else None

        if self.left_child:
            self.left_child.print_connected_nodes(level + 1)

        if self.right_child:
            self.right_child.print_connected_nodes(level + 1)
        print(indent + "}") if self.left_child or self.right_child else print()

    def evaluate(self):
        if self.own.lexeme == "NUMBER":
            return Fraction(self.own.value)
        elif self.own.lexeme == "PLUS":
            return ((Fraction(self.left_child.evaluate())) + (Fraction(self.right_child.evaluate())))
        elif self.own.lexeme == "MINUS":
            return ((Fraction(self.left_child.evaluate())) - (Fraction(self.right_child.evaluate())))
        elif self.own.lexeme == "MULTIPLY":
            return ((Fraction(self.left_child.evaluate())) * (Fraction(self.right_child.evaluate())))
        elif self.own.lexeme == "DIVIDE":
            return ((Fraction(self.left_child.evaluate())) / (Fraction(self.right_child.evaluate())))
        elif self.own.lexeme == "POWER":
            return ((Fraction(self.left_child.evaluate())) ** (Fraction(self.right_child.evaluate())))
        elif self.own.lexeme == "NEGATE":
            return (Fraction(self.left_child.evaluate() * -1))
        elif self.own.lexeme == "NAME":
            values = {"pi": pi, "gr": gr}
            functions = {"sin": sin, "cos": cos, "tan": tan}
            if self.own.value in values:
                return Fraction(values[self.own.value])
            return Fraction(functions[self.own.value](self.left_child.evaluate().as_representation()))
        
def find_lowest_pv_index(token_list, PV):
    lowest_pv = float("inf")
    index = 0

    depth = 0

    for i, v in enumerate(token_list):
        if v.lexeme in PV:
            if depth == 0:
                if PV[v.lexeme] < lowest_pv:
                        lowest_pv = PV[v.lexeme]
                        index = i
                elif PV[v.lexeme] == lowest_pv:
                    index = i
        elif v.lexeme == "OPEN_PARAN":
            depth += 1
        elif v.lexeme == "CLOSE_PARAN":
            depth -= 1
    return index

def allow_negative(expr):
    expr = expr.replace(" ", "")
    if expr[0] == "-":
        expr = "|" + expr[1:]
    return expr.replace("+-", "+|").replace("--", "-|").replace("*-", "*|").replace("/-", "/|").replace("^-", "^|")

def cleanup(expr):
    for i in "1234567890)":
        expr = expr.replace(i + "(", i + "* (")
    for i in "1234567890)":
        for j in "abcdefghijklmnopqrstuvwxyz":
            expr = expr.replace(i + j, i + "* " + j)
    expr = expr.replace("(-", "(|")
    return allow_negative(expr)

def split_iterable(iterable, index):
    if index == 0:
        return (iterable[0], iterable[1:], [])
    return (iterable[index], iterable[:index], iterable[index + 1:])
        
def parse_expr(token_list):
    PRECEDENCE_VALUE = {"NAME": 5, "NEGATE": 4, "POWER": 3, "DIVIDE": 2, "MULTIPLY": 2, "MINUS": 1, "PLUS": 1}
    
    if len(token_list) == 0:
        return None
    
    if len(token_list) == 1:
        return Node(token_list[0], None, None)
    
    if token_list[0].lexeme == "OPEN_PARAN" and token_list[-1].lexeme == "CLOSE_PARAN":
        depth = 1
        for i in range(1, len(token_list) - 1):
            if token_list[i].lexeme == "OPEN_PARAN":
                depth += 1
            elif token_list[i].lexeme == "CLOSE_PARAN":
                depth -= 1
                if depth == 0:
                    break
        else:
            token_list = token_list[1:-1]

    index = find_lowest_pv_index(token_list, PRECEDENCE_VALUE)
    own, left, right = split_iterable(token_list, index)

    return Node(own, parse_expr(left), parse_expr(right))

def isolate_deepest_paranthesis(expression):
    if not "(" in expression:
        return (0, len(expression))
    depth = 1
    deepest = -1
    location = 0
    end_location = 0
    setdeepest = False
    for i, v in enumerate(expression):
        if v == "(":
            depth += 1
            if deepest < depth:
                deepest = depth
                location = i
                setdeepest = True
        elif v == ")":
            depth -= 1
            if setdeepest:
                setdeepest = False
                end_location = i
    return (location + 1, end_location)

def calculate(expression):
    tokens = tokenize(expression)
    ast = parse_expr(tokens)
    return ast.evaluate().as_representation()