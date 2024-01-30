from sympy import symbols, Or, And, Not

# Define the variables and weights
variables = symbols('a b c d e')
weights = symbols('w_a w_b w_c w_d w_e')
weight_map = dict(zip(variables, weights))

# Function to apply weights to a logical expression
def apply_weights(expr, weight_map):
    print(f"Applying weights to: {expr}")

    if isinstance(expr, And):

        transformed = And(*(Or(Not(weight_map.get(arg, 1)), arg) for arg in expr.args))
        print(f"Transformed And: {transformed}")
        return transformed
    elif isinstance(expr, Or):
        transformed = Or(*(And(weight_map.get(arg, 1), arg) for arg in expr.args))
        print(f"Transformed Or: {transformed}")
        return transformed
    elif isinstance(expr, Not):
        transformed = Not(apply_weights(expr.args[0], weight_map))
        print(f"Transformed Not: {transformed}")
        return transformed
    else:
        print(f"No transformation needed for: {expr}")
        return expr
    
# Example usage
#input_expr = Or(variables[0], variables[1])
#Or(a, And(b,c))
input_expr= And(variables[1],variables[2])

print("Original expression is:", input_expr)

weighted_expr = apply_weights(input_expr, weight_map)
print("Weighted expression is:", weighted_expr)
