from sympy import sympify, And, Or, Not

def transform_cqql(expr_str):
    # Parse the string into a symbolic expression
    expr = sympify(expr_str)

    # Define the transformation rules
    def transform(expr):
        if isinstance(expr, And):
            # Replace And with multiplication
            return '*'.join(str(arg) for arg in expr.args)
        elif isinstance(expr, Or):
            # Replace Or with addition and subtraction
            terms = [transform(arg) for arg in expr.args]
            return '+'.join(terms) + '-' + '*'.join(terms)
        elif isinstance(expr, Not):
            # Negation stays the same in this context
            return f'1-{transform(expr.args[0])}'
        else:
            # If it's a variable or a constant, return as is
            return str(expr)

    # Apply the transformation
    return transform(expr)


