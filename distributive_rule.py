from sympy.core import symbols
from sympy.logic.boolalg import BooleanFunction, And, Or, Not
from collections import defaultdict
from sympy import simplify
from find_overlaps import find_overlaps
from resolve_overlaps import resolve_overlaps

def factor_out_common_terms(expr):
    if not isinstance(expr, Or):
        return expr

    # Identify common attributes
    sets = [set(arg.free_symbols) for arg in expr.args if
            isinstance(arg, And) and not any(isinstance(a, Not) for a in arg.args)]
    if sets:
        common_symbols = set.intersection(*sets)
    else:
        common_symbols = set()

    # Separate terms with and without common symbols
    terms_with_common = []
    terms_without_common = []
    for term in expr.args:
        if isinstance(term, And) and all(symbol in term.free_symbols for symbol in common_symbols) and not any(
                isinstance(a, Not) for a in term.args):
            # Removing common symbols from the term
            terms_with_common.append(And(*[arg for arg in term.args if arg not in common_symbols]))
        else:
            terms_without_common.append(term)

    # Combine terms with common symbols using Or
    if terms_with_common:
        combined_terms_with_common = And(*common_symbols, Or(*terms_with_common))
    else:
        combined_terms_with_common = None

    # Check overlap on combined terms
    if combined_terms_with_common:
        common_symbols_part = And(*common_symbols)
        other_part = Or(*[arg for arg in combined_terms_with_common.args if arg not in common_symbols])

        overlaps_with_other_parts = find_overlaps(other_part)
        if overlaps_with_other_parts:
            o = overlaps_with_other_parts.pop()
            other_part = resolve_overlaps(other_part, o)
            other_part = factor_out_common_terms(other_part)

        combined_terms_with_common = And(common_symbols_part, other_part)

    # Construct the final expression
    if combined_terms_with_common and terms_without_common:
        final_expr = Or(combined_terms_with_common, *terms_without_common)
    elif combined_terms_with_common:
        final_expr = combined_terms_with_common
    else:
        final_expr = Or(*terms_without_common)
    return final_expr
