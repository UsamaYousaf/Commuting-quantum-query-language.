from sympy import simplify, lambdify, simplify_logic, symbols
from sympy.logic.boolalg import Or, And, Not, to_dnf
import sympy as sp


def remove_overlaps(e):
    # Step 1: Transform expression e into disjunctive normal form
    e = to_dnf(e)

    # Step 2: Simplify expression e by applying idempotence and invertibility rules
    e = simplify(e)

    # Step 3: Check for overlaps on an ordinal attribute among some conjunctions
    if isinstance(e, Or):
        # Get the arguments of the Or operation
        args = e.args

        # Check if there is an overlap
        for i in range(len(args)):
            for j in range(i + 1, len(args)):
                common_symbols = set(args[i].free_symbols) & set(args[j].free_symbols)
                if common_symbols:
                    # If there is an overlap, choose the first common symbol as 'o'
                    o = list(common_symbols)[0]

                    # Replace all conjunctions πi of e with (o∧πi) V (¬o∧πi)
                    new_args = [(And(o, arg) if o in arg.free_symbols else arg) for arg in args]
                    new_args += [(And(Not(o), arg) if o in arg.free_symbols else arg) for arg in args]

                    # Simplify e by applying idempotence, invertibility, and absorption
                    e = simplify(Or(*new_args))

                    # Continue with step (3) for e1 and e2
                    return remove_overlaps(e)

    # Step 4: Transform innermost disjunctions to conjunctions and negations by applying de Morgan law
    # This step is also specific to your use case and depends on the structure of your expressions.
    # You might need to implement a custom function to apply de Morgan's law to your expressions.

    return e

# Example usage
a, b, c, d, e = symbols('a b c d e')
expression = And(d, Or(And(c, a), And(Not(c), b)))
simplified_expression = remove_overlaps(expression)
print(simplified_expression)