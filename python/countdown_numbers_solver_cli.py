import countdown_numbers_solver as solver
import sys
import sympy
import os


#
# My solver may find expressions whose infix representations are visually different but that are structurally the same,
# according to the rules of arithmetic (associativity, commutability, etc.).  In order to remove such duplicates we can
# take advantage of a community Python library for symbolic math called sympy (https://sympy.org).  This exposes
# functionality to parse expression strings into a standard expression tree form and also to format those trees in
# various ways.  We can use this to create a canonical representatiion for each solution expression that can be used as
# the key in a map to remove duplicates.
#
# Note: users will need to 'pip install sympy'.
#
def _found_expression(expression, only_one):
  infix_expression = _format_expression_infix(expression)
  key = sympy.srepr(sympy.sympify(infix_expression, evaluate = False))
  if not key in _solutions:
    _solutions[key] = infix_expression
  return only_one


def _is_number(expression):
  return 0 if type(expression) is tuple else 1


def _format_expression_infix(expression):
  if _is_number(expression):
    return expression 
  op_symbol = expression[1]
  lhs = _format_expression_infix(expression[2])
  rhs = _format_expression_infix(expression[3])
  return f'({lhs} {op_symbol} {rhs})'


def _print_usage():
  python_name = os.path.basename(sys.executable)
  script_file_name = os.path.basename(__file__)
  text = f"""
A Countdown Numbers Game Solver

USAGE: {python_name} ./{script_file_name} <target> <numbers> [-all]
  <target>    The target number
  <numbers>   A space delimited list of numbers (must be +ve integers)
  -all        [Optional] Find all solutions.  Default behavior is to find just the first.

E.g. {python_name} ./{script_file_name} 952 3 6 25 50 75 100
"""
  print(text)


_solutions = {}    # A dict to eliminate duplicate solution expressions


def main():
  if len(sys.argv) < 3:
    _print_usage()
    return 1
  
  target = int(sys.argv[1])
  numbers = [int(s) for s in sys.argv[2:] if s[0] != '-']
  only_one = 0 if '-all' in sys.argv[2:] else 1

  numbers.sort()    # Don't have to do this but let's be tidy shall we?

  print(f'target = {target}, numbers = {numbers}')

  solver.find_expressions_for_target(numbers, target, lambda e: _found_expression(e, only_one))

  for solution in _solutions.values():
    print(f'{target} = {solution}')
  return 0


if __name__ == "__main__":
  exit(main())
