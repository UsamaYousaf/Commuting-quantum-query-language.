from sympy import simplify, symbols, lambdify, simplify_logic, sympify
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
    # Ask the user for a logical expression
    expr_str = input("Please input a logical expression: ")
    expr = sympify(expr_str)

    # Extract variables from the expression
    variables = expr.free_symbols

    # Map variables to weight symbols
    weights = symbols(' '.join([f'w_{var}' for var in variables]))
    weight_map = dict(zip(variables, weights))

    # Get values
    var_values = {}
    # Get the values for the variables from the user
    for var in variables:
        value = float(
            input(f"Please enter a value for {var} (between [0,1]): "))
        var_values[var] = value
    # Get values for weights
    weight_values = {}
    for weight in weights:
        value = float(
            input(f"Please enter a value for {weight} (between [0,1]): "))
        weight_values[weight] = value

    return expr_str, var_values, weight_values, weight_map


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
    # Example usage
    expr, var_values, weight_values, weight_map = user_input()

    print("Weight map here", weight_map)
    exper = apply_weights(sympify(expr), weight_map)

    print("Experession from schmitt weighting:", exper)
    # exper = apply_weights(input_expr1, weight_map)a
    # print("Experession with weights added:", exper)
    # Step 1: Transform to disjunctive normal form
    dnf_expr = disjunctive_normal_form(exper)
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
