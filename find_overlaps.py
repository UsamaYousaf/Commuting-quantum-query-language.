from sympy import simplify,symbols, lambdify, simplify_logic
from sympy.logic.boolalg import Or, And, Not, to_dnf
from sympy import Symbol
def find_overlaps(expr):

    common_attributes = set()


    for i, conj in enumerate(expr.args):
        if isinstance(conj, Symbol):
            literals = [conj]
        else:
            literals = conj.args
        for j, other_conj in enumerate(expr.args[i+1:], i+1):
            if isinstance(other_conj, Symbol):
                other_literals = [other_conj]
            else:
                other_literals = other_conj.args
            common_attributes |= set(literal for literal in literals if literal in other_literals)

            attribute_with_nega = set()
            for attr in common_attributes.copy():
                for conj_inner in expr.args:
                    if (Not(attr) in conj_inner.args) or (isinstance(attr, Not) and attr.args[0] in conj_inner.args):
                        attribute_with_nega.add(attr)
                        break

            common_attributes -= attribute_with_nega

            if common_attributes:
                return common_attributes
    return set()