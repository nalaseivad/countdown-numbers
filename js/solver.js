const swapArgs = (a, b) => [b, a];
const args = (a, b) => [a, b];

//
// A map to contain info about possible operators
//
const operators = {
  'ADD': ['+', (a, b) => a + b, args],
  'SUB': ['-', (a, b) => a - b, args],
  'SUB2': ['-', (a, b) => b - a, swapArgs],   // Subtraction with the args swapped
  'MUL': ['*', (a, b) => a * b, args],
  'DIV': ['/', (a, b) => a / b, args],
  'DIV2': ['/', (a, b) => b / a, swapArgs],   // Division with the args swapped
};


//
// Check if a given operation is valid according to our use case
//
const isValidOperation = (opKey, lhs, rhs) => {
  // Skip division by zero or any division that results in a remainder
  if (opKey == 'DIV' && (rhs == 0 || lhs % rhs != 0)) return 0
  if (opKey == 'DIV2' && (lhs == 0 || rhs % lhs != 0)) return 0

  // Skip any subtraction that results in a negative number
  if (opKey == 'SUB' && rhs > lhs) return 0
  if (opKey == 'SUB2' && lhs > rhs) return 0

  return true;
};


//
// Perform an operation, if valid. Returns a boolean and a tuple containing (result, op, lhs, rhs)
//
const doOperation = (opKey, lhs, rhs) => {
  const lhsValue = getExpressionValue(lhs);
  const rhsValue = getExpressionValue(rhs);
  if (!isValidOperation(opKey, lhsValue, rhsValue)) return [false, null];

  const [opSymbol, opFn, argsFn] = operators[opKey];
  const result = opFn(lhsValue, rhsValue);
  [lhs, rhs] = argsFn(lhs, rhs);                    // Potentially swap the args, for DIV2 and SUB2
  return [true, [result, opSymbol, lhs, rhs]];      // Return the result as a tuple of the form (result, op, lhs, rhs)
};


//
// Create a new list of expressions from the old one, a new expression, and the indexes of the args to that new
// expression
//
const newExpressionList = (expressions, newExpression, i, j) => {
  // Replace the element at position i with the new expression and exclude the element at position j
  let result = [...expressions.slice(0, i), newExpression, ...expressions.slice(i + 1, j)];
  // Concatenate any elements after position j
  if (j < expressions.length)
    result = result.concat(expressions.slice(j + 1));
  return result;
};


//
// Get the value from an expression tuple of the form (value, op, lhs, rhs)
//
const getExpressionValue = (expression) => Array.isArray(expression) ? expression[0] : expression;


//
// The main recursive routine to search the space of possible expressions and find those that evaluate to the target
//
const findExpressionsForTarget = (expressions, target, foundFn) => {
  for (const expression of expressions) {
    if (getExpressionValue(expression) === target)
      if (foundFn(expression))
        return true;
  }
  
  for (let i = 0; i < expressions.length - 1; i++) {
    const ei = expressions[i];
    for (let j = i + 1; j < expressions.length; j++) {
      const ej = expressions[j];
      for (const opKey of Object.keys(operators)) {
        const [valid, newExpression] = doOperation(opKey, ei, ej);
        if (!valid) continue;
        const newExpressions = newExpressionList(expressions, newExpression, i, j);
        if (findExpressionsForTarget(newExpressions, target, foundFn))
          return true;
      }
    }
  }
  return false;
};


//
// Exports
//
export { findExpressionsForTarget };
