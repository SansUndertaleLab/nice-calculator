from fraction import Fraction

pi = 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679
gr = 1.6180339887498948482045868343656381177203091798057628621354486227052604628189024497072072041893911374

def factorial(x):
    if x < 2:
        return 1
    return x * factorial(x - 1)

def sin(x):
    v = Fraction(x % (pi * 2))
    taylor_series = Fraction(0)
    for n in range(85):
        n = Fraction(n)
        current = (((Fraction(-1)) ** n) / factorial((Fraction(2) * n) + 1)) * (v ** ((Fraction(2) * n) + 1))
        taylor_series += current
    return taylor_series

def cos(x):
    return sin(x - ((pi * 3) / 2))

def tan(x):
    return sin(x) / cos(x)
