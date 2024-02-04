from sympy import sympify, And, Or, Not
from sympy import Symbol

def transform_cqql(expr_str):
    # Parse the string into a symbolic expression
    expr = sympify(expr_str, evaluate=False)

    # Define the transformation rules
    def transform(expr):
        if isinstance(expr, And):
            # Replace And with multiplication
            return '(' + '*'.join(transform(arg) for arg in expr.args) + ')'
        elif isinstance(expr, Or):
            # Replace Or with addition and subtraction
            if all(isinstance(arg, Symbol) for arg in expr.args):
                terms = [transform(arg) for arg in expr.args]
                return '(' + '+'.join(terms) + ')'
            else:
                terms = [transform(arg) for arg in expr.args]
                return '(' + ' + '.join(terms) + ' - ' + '*'.join(terms) + ')'
        elif isinstance(expr, Not):
            # Negation is transformed as 1 minus the argument
            return f'(1-{transform(expr.args[0])})'
        else:
            # If it's a variable or a constant, return as is
            return str(expr)

    # Apply the transformation
    return transform(expr)


