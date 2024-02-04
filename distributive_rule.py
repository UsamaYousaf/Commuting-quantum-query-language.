from sympy.core import symbols
from sympy.logic.boolalg import BooleanFunction, And, Or, Not
from sympy import Symbol
from collections import defaultdict
from sympy import simplify
from find_overlaps import find_overlaps
from resolve_overlaps import resolve_overlaps


def factor_out_common_terms(expr, resolved_symbols=None):
    if not isinstance(expr, Or):
        return expr


    if resolved_symbols is None:
        resolved_symbols = set()

    # Separate terms with and without common symbols
    terms_with_common = []
    terms_without_common = []
    for term in expr.args:
        term_symbols = term.free_symbols
        has_common_symbol = any(symbol in term_symbols for symbol in resolved_symbols)
        # Check if the term contains any of the resolved symbols (not their negations)
        if has_common_symbol:
            # Split the term into parts that contain the resolved symbols and those that don't
            with_common = [arg for arg in term.args if arg in resolved_symbols]
            without_common = [arg for arg in term.args if arg not in resolved_symbols and not any(
                arg == Not(resolved_symbol) for resolved_symbol in resolved_symbols)]

            # If there are parts of the term that contain the resolved symbol, adjust the term accordingly
            if with_common:
                new_term = And(*without_common) if without_common else None
                if new_term is not None:
                    terms_with_common.append(new_term)
            else:
                # If the term does not contain the resolved symbol, add it to the without_common list
                terms_without_common.append(term)
        else:
            terms_without_common.append(term)

    # Combine terms with common symbols using Or
    if terms_with_common:
        combined_terms_with_common = And(
            *resolved_symbols, Or(*terms_with_common))
    else:
        combined_terms_with_common = None

    # Check overlap on combined terms
    if combined_terms_with_common:
        common_symbols_part = And(*resolved_symbols)
        other_part = Or(
            *[arg for arg in combined_terms_with_common.args if arg not in resolved_symbols])
        overlaps_with_other_parts = find_overlaps(other_part)
        if overlaps_with_other_parts:
            o = overlaps_with_other_parts.pop()
            other_part = resolve_overlaps(other_part, o)
            other_part = factor_out_common_terms(other_part, {o})

        combined_terms_with_common = And(common_symbols_part, other_part)

    # Construct the final expression
    if combined_terms_with_common and terms_without_common:
        final_expr = Or(combined_terms_with_common, *terms_without_common)
    elif combined_terms_with_common:
        final_expr = combined_terms_with_common
    else:
        final_expr = Or(*terms_without_common)
    return final_expr
