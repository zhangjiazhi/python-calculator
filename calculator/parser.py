#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Expression parser using Shunting Yard algorithm.
Converts infix notation to postfix and evaluates mathematical expressions.
"""

from enum import Enum
from typing import List, Union
from .basic import BasicCalculator

# Maximum allowed expression length to prevent DoS attacks
MAX_EXPRESSION_LENGTH = 1000

Number = Union[int, float]


class TokenType(Enum):
    """Token types for expression parsing."""
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"


class Token:
    """Represents a token in the expression."""

    def __init__(self, token_type: TokenType, value: Union[Number, str]):
        """
        Initialize a token.

        Args:
            token_type: TokenType enum value
            value: The actual value (number or operator string)
        """
        self.type: TokenType = token_type
        self.value: Union[Number, str] = value

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class ExpressionParser:
    """Parser for mathematical expressions using Shunting Yard algorithm."""

    # Operator precedence and associativity
    OPERATORS = {
        '+': {'precedence': 1, 'associativity': 'left'},
        '-': {'precedence': 1, 'associativity': 'left'},
        '*': {'precedence': 2, 'associativity': 'left'},
        '/': {'precedence': 2, 'associativity': 'left'},
        '%': {'precedence': 2, 'associativity': 'left'},
        '**': {'precedence': 3, 'associativity': 'right'},
    }

    @staticmethod
    def tokenize(expression: str) -> List[Token]:
        """
        Convert expression string to list of tokens.

        Args:
            expression: String expression to tokenize

        Returns:
            List of Token objects

        Raises:
            ValueError: If expression contains invalid characters
        """
        tokens: List[Token] = []
        i = 0
        expression = expression.replace(' ', '')  # Remove whitespace

        while i < len(expression):
            char = expression[i]

            # Handle numbers (including decimals and negatives)
            if char.isdigit() or char == '.':
                num_str = ''
                decimal_count = 0

                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        decimal_count += 1
                        if decimal_count > 1:
                            raise ValueError(f"Invalid number format: multiple decimal points in number")
                    num_str += expression[i]
                    i += 1

                # Validate not a standalone decimal point
                if num_str == '.':
                    raise ValueError("Invalid number: standalone decimal point")

                try:
                    value = float(num_str) if '.' in num_str else int(num_str)
                    tokens.append(Token(TokenType.NUMBER, value))
                except ValueError:
                    raise ValueError(f"Invalid number format: {num_str}")
                continue

            # Handle operators
            elif char in '+-*/%':
                # Check for ** (power operator)
                if char == '*' and i + 1 < len(expression) and expression[i + 1] == '*':
                    tokens.append(Token(TokenType.OPERATOR, '**'))
                    i += 2
                    continue

                # Handle unary minus
                if char == '-':
                    # It's unary if it's at the start or after an operator or left paren
                    if (not tokens or
                        tokens[-1].type in [TokenType.OPERATOR, TokenType.LPAREN]):
                        # Look ahead to get the number
                        i += 1
                        if i >= len(expression):
                            raise ValueError("Invalid expression: operator at end")

                        # Skip whitespace
                        while i < len(expression) and expression[i] == ' ':
                            i += 1

                        if i >= len(expression):
                            raise ValueError("Invalid expression: operator at end")

                        # Check if next is a number or parenthesis
                        if expression[i].isdigit() or expression[i] == '.':
                            num_str = '-'
                            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                                num_str += expression[i]
                                i += 1
                            try:
                                value = float(num_str) if '.' in num_str else int(num_str)
                                tokens.append(Token(TokenType.NUMBER, value))
                            except ValueError:
                                raise ValueError(f"Invalid number: {num_str}")
                            continue
                        elif expression[i] == '(':
                            # Unary minus with parenthesis: treat as -1 * (...)
                            tokens.append(Token(TokenType.NUMBER, -1))
                            tokens.append(Token(TokenType.OPERATOR, '*'))
                            continue

                tokens.append(Token(TokenType.OPERATOR, char))
                i += 1

            # Handle parentheses
            elif char == '(':
                tokens.append(Token(TokenType.LPAREN, char))
                i += 1

            elif char == ')':
                tokens.append(Token(TokenType.RPAREN, char))
                i += 1

            else:
                raise ValueError(f"Invalid character in expression: {char}")

        return tokens

    @staticmethod
    def infix_to_postfix(tokens: List[Token]) -> List[Token]:
        """
        Convert infix token list to postfix using Shunting Yard algorithm.

        Args:
            tokens: List of Token objects in infix notation

        Returns:
            List of Token objects in postfix notation

        Raises:
            ValueError: If parentheses are mismatched
        """
        output: List[Token] = []
        operator_stack: List[Token] = []

        for token in tokens:
            if token.type == TokenType.NUMBER:
                output.append(token)

            elif token.type == TokenType.OPERATOR:
                op1 = token.value
                while operator_stack:
                    top = operator_stack[-1]
                    if top.type != TokenType.OPERATOR:
                        break

                    op2 = top.value
                    op1_prec = ExpressionParser.OPERATORS[op1]['precedence']
                    op2_prec = ExpressionParser.OPERATORS[op2]['precedence']
                    op1_assoc = ExpressionParser.OPERATORS[op1]['associativity']

                    if (op2_prec > op1_prec or
                        (op2_prec == op1_prec and op1_assoc == 'left')):
                        output.append(operator_stack.pop())
                    else:
                        break

                operator_stack.append(token)

            elif token.type == TokenType.LPAREN:
                operator_stack.append(token)

            elif token.type == TokenType.RPAREN:
                # Pop operators until we find the matching left paren
                found_lparen = False
                while operator_stack:
                    top = operator_stack.pop()
                    if top.type == TokenType.LPAREN:
                        found_lparen = True
                        break
                    output.append(top)

                if not found_lparen:
                    raise ValueError("Mismatched parentheses: missing opening parenthesis")

        # Pop remaining operators
        while operator_stack:
            top = operator_stack.pop()
            if top.type == TokenType.LPAREN:
                raise ValueError("Mismatched parentheses: missing closing parenthesis")
            output.append(top)

        return output

    @staticmethod
    def evaluate_postfix(postfix_tokens: List[Token]) -> Number:
        """
        Evaluate postfix expression.

        Args:
            postfix_tokens: List of Token objects in postfix notation

        Returns:
            Numerical result of evaluation

        Raises:
            ValueError: If expression is invalid or operations fail
        """
        stack: List[Number] = []

        for token in postfix_tokens:
            if token.type == TokenType.NUMBER:
                stack.append(token.value)

            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: insufficient operands")

                b = stack.pop()
                a = stack.pop()

                operator = token.value
                try:
                    if operator == '+':
                        result = BasicCalculator.add(a, b)
                    elif operator == '-':
                        result = BasicCalculator.subtract(a, b)
                    elif operator == '*':
                        result = BasicCalculator.multiply(a, b)
                    elif operator == '/':
                        result = BasicCalculator.divide(a, b)
                    elif operator == '%':
                        result = BasicCalculator.modulo(a, b)
                    elif operator == '**':
                        result = BasicCalculator.power(a, b)
                    else:
                        raise ValueError(f"Unknown operator: {operator}")

                    stack.append(result)
                except ValueError as e:
                    raise ValueError(f"Operation error: {e}")

        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands")

        return stack[0]

    @staticmethod
    def parse(expression: str) -> Number:
        """
        Parse and evaluate a mathematical expression.

        Args:
            expression: String expression to evaluate

        Returns:
            Numerical result

        Raises:
            ValueError: If expression is invalid or evaluation fails
        """
        if not expression or not expression.strip():
            raise ValueError("Empty expression")

        # Check expression length to prevent DoS attacks
        if len(expression) > MAX_EXPRESSION_LENGTH:
            raise ValueError(
                f"Expression too long: {len(expression)} characters "
                f"(maximum {MAX_EXPRESSION_LENGTH})"
            )

        tokens = ExpressionParser.tokenize(expression)
        if not tokens:
            raise ValueError("No valid tokens in expression")

        postfix = ExpressionParser.infix_to_postfix(tokens)
        result = ExpressionParser.evaluate_postfix(postfix)

        return result
