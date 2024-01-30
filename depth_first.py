from sympy import And, Or, Not, Symbol

def print_depth_first(expr, depth=0):
    if isinstance(expr, (And, Or, Not)):
        # For each argument in the expression, go deeper first
        for arg in expr.args:
            print_depth_first(arg, depth + 1)
        # Print the current expression after printing deeper levels
        print(" " * depth * 2 + str(expr))
    elif isinstance(expr, Symbol):
        # Base case: just print the symbol
        print(" " * depth * 2 + str(expr))

# Example usage
A, B, C, D = Symbol('A'), Symbol('B'), Symbol('C'), Symbol('D')
expression = Or(And(Or(A, B),C)), D
print_depth_first(expression)