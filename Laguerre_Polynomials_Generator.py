from sympy import symbols, summation, binomial, sympify, expand, factorial, latex

x = symbols('x')
k= symbols('k', integer = True, nonnegative = True)
flag = ''

print("Startup...")
while flag != "E":
    n = int(input("Please Enter n, Integer Only: "))
    l = int(input("Pleas Enter l, Integer Only: "))
    L_x = summation((-1) ** k * binomial(n + l, n - k) * x** k / (factorial(k)), (k, 0, n))
    print(latex(L_x))
    flag = str(input("Enter E for exit. Enter any key for continue generating:"))

print("Exit Successfully.")