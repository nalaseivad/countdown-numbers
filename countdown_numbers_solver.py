def _swap_args(a, b):
  return b, a


def _args(a, b):
  return a, b

#
# A hash to contain info about possible operators
#
_operators = {
  'ADD' : ['+', lambda a, b: a + b, _args],
  'SUB' : ['-', lambda a, b: a - b, _args],
  'SUB2' : ['-', lambda a, b: b - a, _swap_args],    # Subtraction with the args swapped
  'MUL' : ['*', lambda a, b: a * b, _args],
  'DIV' : ['/', lambda a, b: a / b, _args],
  'DIV2' : ['/', lambda a, b: b / a, _swap_args],    # Division with the args swapped
}


#
# Is a given operation valid according to our use case?
#
def _is_valid_operation(op_key, lhs, rhs):
  # Skip division by zero or any division that results in a remainder
  if(op_key == 'DIV' and (rhs == 0 or lhs % rhs != 0)): return 0
  if(op_key == 'DIV2' and (lhs == 0 or rhs % lhs != 0)): return 0

  # Skip any subtraction that results in a negative number
  if(op_key == 'SUB' and rhs > lhs): return 0
  if(op_key == 'SUB2' and lhs > rhs): return 0

  # It's a legit operation
  return 1


#
# Perform an operation, if valid.  Returns a bool (indicating whether the expression was valid) and a tuple containing
# (result, op, lhs, rhs).
#
def _do_operation(op_key, lhs, rhs):
  lhs_value = _get_expression_value(lhs)
  rhs_value = _get_expression_value(rhs)
  if not _is_valid_operation(op_key, lhs_value, rhs_value):
    return 0, None
  op_symbol, op_fn, args_fn = _operators[op_key]
  result = op_fn(lhs_value, rhs_value)
  lhs, rhs = args_fn(lhs, rhs)                 # Potentially swap the args, for DIV2 and SUB2
  return 1, (result, op_symbol, lhs, rhs)      # Return the result as a tuple of the form (result, op, lhs, rhs)


#
# Create a new list of expressions from the old one, a new expression and the indexes of the args to that new expression
#
def _new_expression_list(expressions, new_expression, i, j):
  # Replace the element at position i with the new expression and exclude the element at position j
  result = expressions[0:i] + [new_expression] + expressions[i + 1:j]
  # Concatenate any elements after position j
  if j < len(expressions):
    result += expressions[j + 1:]
  return result


#
# Get the value from an expression tuple of the form (value, op, lhs, rhs)
#
def _get_expression_value(expression):
  return expression[0] if type(expression) is tuple else expression


#
# The main recursive routine to search the space of possible expressions and find those that evaluate to the target
#
def _find_expressions_for_target(expressions, target, found_fn):
  first_expression = expressions[0]
  if _get_expression_value(first_expression) == target:
    if found_fn(first_expression):
      return 1
    
  for i in range(len(expressions) - 1):
    ei = expressions[i]
    for j in range(i + 1, len(expressions)):
      ej = expressions[j]
      for op_key in _operators.keys():
        valid, new_expression = _do_operation(op_key, ei, ej)
        if not valid: continue
        new_expressions = _new_expression_list(expressions, new_expression, i, j)
        if _find_expressions_for_target(new_expressions, target, found_fn):
          return 1
        

########################################################################################################################


#
# The public solver function
#
def find_expressions_for_target(numbers, target, found_fn):
  # Test for a trivial solution, i.e. one of the numbers is equal to the target
  for number in numbers:
    if number == target:
      if found_fn(number):
        return
  # Call the recursive finder
  _find_expressions_for_target(numbers, target, found_fn)
