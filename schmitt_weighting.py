from sympy import symbols, And, Or, Not

# Define the variables and weights
variables = symbols('a b c d')
weights = symbols('w_a w_b w_c w_d')

weight_map = dict(zip(variables, weights))

# Function to apply weights to a logical expression
def apply_weights(expr, weight_map):
    if isinstance(expr, And):
        # Apply w⊤ formula for And operation
        return And(*(Or(Not(weight_map.get(arg, 1)), apply_weights(arg, weight_map)) for arg in expr.args))
    elif isinstance(expr, Or):
        # Apply w⊥ formula for Or operation
        return Or(*(And(weight_map.get(arg, 1), apply_weights(arg, weight_map)) for arg in expr.args))
    elif isinstance(expr, Not):
        return Not(apply_weights(expr.args[0], weight_map))
    else:
        return expr

# Test the function with the expression
input_expr = Or(variables[0], And(variables[1], variables[2]))
weighted_expr = apply_weights(input_expr, weight_map)
print("Weighted expression is:", weighted_expr)
