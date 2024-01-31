from sympy import simplify,symbols, lambdify, simplify_logic
from sympy.logic.boolalg import Or, And, Not, to_dnf

def resolve_overlaps(expr, o):
  disjunctions = expr.args if isinstance(expr, Or) else expr

  new_dnf = []
  for conj in disjunctions:
    if o in conj.free_symbols:
      new_dnf.append(conj)
    else:
      new_dnf.append(And(o, conj))
      new_dnf.append(And(Not(o), conj))

  # Create a new Or object directly using the *args syntax
  expr = Or(*new_dnf)

  return expr