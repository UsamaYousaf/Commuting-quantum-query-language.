from sympy import simplify,symbols, lambdify, simplify_logic
from sympy.logic.boolalg import Or, And, Not, to_dnf
from schmitt_weighting import apply_weights

# Define variables and weights
variables = symbols('a b c d')
weights = symbols('w_a w_b w_c w_d')
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
    break
  return expr

def find_overlaps(expr):

    common_attributes = set()

    # for i in range(len(disjunctions)):
    #     for j in range(i+1, len(disjunctions)):
    #         common_attributes |= set(disjunctions[i].atoms()) & set(disjunctions[j].atoms())
    for i, conj in enumerate(expr.args):
        for j, other_conj in enumerate(expr.args[i+1:], i+1):
            common_attributes |= set(literal for literal in conj.args if literal in other_conj.args)


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
    #input_expr = user_input()
    #print("Original Expression:", input_expr)
    input_expr1 = Or(variables[0], And(variables[1], variables[2]))
    exper= apply_weights(input_expr1,weight_map)
    print("Exper from schmitt weighting:", exper)
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