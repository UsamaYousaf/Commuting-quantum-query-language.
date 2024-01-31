from sympy import simplify,symbols, lambdify, simplify_logic
from sympy.logic.boolalg import Or, And, Not, to_dnf
from schmitt_weighting import apply_weights
from find_overlaps import find_overlaps
from distributive_rule import factor_out_common_terms
from resolve_overlaps import resolve_overlaps

# Define variables and weights
variables = symbols('a b c d e')
weights = symbols('w_a w_b w_c w_d w_e')
weight_map = dict(zip(variables, weights))
def user_input():
    # Create dictionaries to store the values of the variables and weights
    var_values = {}
    weight_values = {}

    # Get the values for the variables from the user
    for var in variables:
        value = float(input(f"Please enter a value for {var} (between [0,1]): "))
        var_values[var] = value

    # Get the values of weights for the variables from the user
    for weight in weights[:3]:
        value = float(input(f"Please enter a value for {weight} (between [0,1]): "))
        weight_values[weight] = value

    # Ask the user if they want to input more weights (maximum: 5 weights)
    """
    This implementation will be expected at least three weight's input from the user
    .If type "yes", user will input more weights manually, otherwise assign the weights to 1 automatically.
    """

    for weight in weights[3:]:
        answer = input(f"Do you want to input the {weight}? (yes/no): ")
        if answer.lower() == "yes":
            value = float(input(f"Please enter a value for {weight} (between [0,1]): "))
            weight_values[weight] = value
        else:
            weight_values[weight] = 1

    # Get the logical expression from the user
    expr_str = input("Please input a logical expression: ")
    return expr_str
def disjunctive_normal_form(expr):
    return to_dnf(expr)

def simplify_expression(expr):
    return simplify_logic(expr, form="dnf")

def eliminate_overlaps(expr):
  while True:
    common_attributes = find_overlaps(expr)
    if common_attributes:
        o = common_attributes.pop()
        expr = resolve_overlaps(expr, o)
        expr = factor_out_common_terms(expr)

    else:
        break
  return expr


if __name__ == "__main__":
    #input_expr = user_input()
    #print("Original Expression:", input_expr)
    input_expr1 = Or(And(variables[0], variables[1]), And(variables[0], variables[2]), And(variables[1], variables[2]))

    print("Original Expression is:", input_expr1)
    #exper = apply_weights(input_expr1, weight_map)
    #print("Experession with weights added:", exper)
    # Step 1: Transform to disjunctive normal form
    dnf_expr = disjunctive_normal_form(input_expr1)
    print("Disjunctive Normal Form:", dnf_expr)

    # Step 2: Simplify expression
    simplified_expr = simplify_expression(dnf_expr)
    print("Simplified Expression:", simplified_expr)

    # Find an overlaps
    overlaps = find_overlaps(simplified_expr)
    print("The first overlap of this expression is:", overlaps)

    # Step 3: Eliminate overlaps
    expr_without_overlaps = eliminate_overlaps(simplified_expr)
    print("Expression without Overlaps:", expr_without_overlaps)



