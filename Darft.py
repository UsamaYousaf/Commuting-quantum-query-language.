from sympy import simplify, sympify, symbols, lambdify, simplify_logic
from sympy.logic.boolalg import Or, And, Not, to_dnf
from schmitt_weighting import apply_weights


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
        break
    return expr


def find_overlaps(expr):

    common_attributes = set()

    # for i in range(len(disjunctions)):
    #     for j in range(i+1, len(disjunctions)):
    #         common_attributes |= set(disjunctions[i].atoms()) & set(disjunctions[j].atoms())
    for i, conj in enumerate(expr.args):
        for j, other_conj in enumerate(expr.args[i+1:], i+1):
            common_attributes |= set(
                literal for literal in conj.args if literal in other_conj.args)

    return common_attributes


def resolve_overlaps(expr, o):
    disjunctions = expr.args if isinstance(expr, Or) else expr
    print(f"disjunctions: {disjunctions}")

    new_dnf = []
    for conj in disjunctions:
        print(f"Processing conjunction: {conj}")
        if o in conj.free_symbols:
            print(f"Conjunctions {conj} contains {o}")
            new_dnf.append(conj)
        else:
            print(f"Conjunctions {conj} does not contain {o}")
            new_dnf.append(And(o, conj))
            new_dnf.append(And(Not(o), conj))

    print(f"New DNF: {new_dnf}")

    # Create a new Or object directly using the *args syntax
    expr = Or(*new_dnf)

    return expr


if __name__ == "__main__":
    # Example usage
    expr, var_values, weight_values, weight_map = user_input()
    # weight_map = {symbols(var): weight for var,
    #               weight in weight_values.items()}

    print("Weight map here", weight_map)
    exper = apply_weights(sympify(expr), weight_map)

    print("Experession from schmitt weighting:", exper)
    # Step 1: Transform to disjunctive normal form
    dnf_expr = disjunctive_normal_form(exper)
    print("Disjunctive Normal Form:", dnf_expr)

    # Step 2: Simplify expression
    simplified_expr = simplify_expression(dnf_expr)
    print("Simplified Expression:", simplified_expr)

    # Find an overlaps
    overlaps = find_overlaps(simplified_expr)
    print("An overlap of this logical expression is:", overlaps)

    # Step 3: Eliminate overlaps
    expr_without_overlaps = eliminate_overlaps(simplified_expr)
    print("Expression without Overlaps:", expr_without_overlaps)

    # Step 4: Transform innermost disjunctions to conjunctions and negations
    final_result = expr_without_overlaps.to_anf()
    print("Final Result after applying de Morgan law:", final_result)
