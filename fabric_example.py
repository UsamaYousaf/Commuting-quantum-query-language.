from sympy import symbols, And, Or, Not

# Define the attributes and weights
color, texture, quality = symbols('color texture quality')
weights = symbols('w_color w_texture w_quality')

# Assign weights according to the problem statement
weight_map = {color: 2, texture: 1, quality: 1/3}

# Constructing the query expression
# Assuming 'And' represents the need for high quality and 'Or' represents the similarity based on color and texture
query_expr = And(Or(color, texture), quality)

# Update the apply_weights function to handle weights as numbers
def apply_weights(expr, weight_map):
    if isinstance(expr, And):
        return And(*(Or(Not(weight_map.get(arg, 1)), arg) if weight_map.get(arg, 1) != 1 else arg for arg in expr.args))
    elif isinstance(expr, Or):
        return Or(*(And(weight_map.get(arg, 1), arg) if weight_map.get(arg, 1) != 1 else arg for arg in expr.args))
    elif isinstance(expr, Not):
        return Not(apply_weights(expr.args[0], weight_map))
    else:
        return expr

# Applying weights to the query
weighted_query = apply_weights(query_expr, weight_map)

print("Weighted Query:", weighted_query)
