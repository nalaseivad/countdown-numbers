import { findExpressionsForTarget } from './solver.js';

let _solutions = new Set()

function _foundExpression(expression, onlyOne) {
  let infixExpression = _formatExpressionInfix(expression);
  if (!(infixExpression in _solutions))
    _solutions.add(infixExpression)
  return onlyOne;
}

function _parseInt(s) {
  if (!/^\d+$/.test(s)) return -1
  return parseFloat(s);
}

function _expressionIsNumber(expression) {
  return Array.isArray(expression) ? 0 : 1;
}

function _formatExpressionInfix(expression) {
  if (_expressionIsNumber(expression))
    return expression;
  let opSymbol = expression[1];
  let lhs = _formatExpressionInfix(expression[2]);
  let rhs = _formatExpressionInfix(expression[3]);
  return `(${lhs} ${opSymbol} ${rhs})`;
}

function _clearSolutions(results, s) {
  document.getElementById('solutions-list').innerHTML = "";
}

function _renderSolution(solutionText) {
  var solutions = document.getElementById('solutions-list');
  var solution = document.createElement('div');
  solution.textContent = solutionText;
  solution.className = "solutions-list-item";
  solutions.appendChild(solution);
}

function _showError(msg) {
  _renderSolution(msg);
}

function solve() {
  _solutions = new Set();
  _clearSolutions();

  let targetText = document.getElementById("target").value;
  let target = _parseInt(targetText, 10);
  if (target <= 0) {
    _showError("Target must be a positive integer")
    return;
  }

  let numbersText = document.getElementById("numbers").value.trim();
  let stringNumbers = numbersText.split(' ');
  let numbers = [];
  for (const sn of stringNumbers) {
    let number = _parseInt(sn, 10);
    if (number <= 0) {
      _showError("Numbers must all be positive integers");
      return;
    }
    numbers.push(number)
  }
  if (numbers.length > 6) {
    _showError("There can be no more than 6 numbers");
    return;
  }

  findExpressionsForTarget(numbers, target, expression => _foundExpression(expression, false));

  if (_solutions.size == 0) {
    _renderSolution('No solutions');
    return;
  }

  for (const solution of _solutions)
    _renderSolution(`${target} = ${solution}`);
};

document.addEventListener('DOMContentLoaded', (event) => {
  document.getElementById('solveButton').addEventListener('click', solve);
});
