#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit tests for expression parser.
"""

import pytest
from calculator.parser import ExpressionParser, Token, TokenType


class TestTokenize:
    """Test suite for tokenization."""

    def test_tokenize_simple_numbers(self):
        """Test tokenizing simple numbers."""
        tokens = ExpressionParser.tokenize("42")
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 42

    def test_tokenize_decimal_numbers(self):
        """Test tokenizing decimal numbers."""
        tokens = ExpressionParser.tokenize("3.14")
        assert len(tokens) == 1
        assert tokens[0].value == 3.14

    def test_tokenize_simple_expression(self):
        """Test tokenizing a simple expression."""
        tokens = ExpressionParser.tokenize("2 + 3")
        assert len(tokens) == 3
        assert tokens[0].value == 2
        assert tokens[1].value == '+'
        assert tokens[2].value == 3

    def test_tokenize_complex_expression(self):
        """Test tokenizing a complex expression."""
        tokens = ExpressionParser.tokenize("10 * (5 - 2)")
        assert len(tokens) == 7
        assert tokens[0].value == 10
        assert tokens[1].value == '*'
        assert tokens[2].type == TokenType.LPAREN
        assert tokens[3].value == 5
        assert tokens[4].value == '-'
        assert tokens[5].value == 2
        assert tokens[6].type == TokenType.RPAREN

    def test_tokenize_power_operator(self):
        """Test tokenizing power operator."""
        tokens = ExpressionParser.tokenize("2 ** 8")
        assert len(tokens) == 3
        assert tokens[1].value == '**'

    def test_tokenize_negative_number(self):
        """Test tokenizing negative numbers."""
        tokens = ExpressionParser.tokenize("-5")
        assert len(tokens) == 1
        assert tokens[0].value == -5

    def test_tokenize_negative_in_expression(self):
        """Test tokenizing negative numbers in expressions."""
        tokens = ExpressionParser.tokenize("-5 + 3")
        assert tokens[0].value == -5
        assert tokens[1].value == '+'
        assert tokens[2].value == 3

    def test_tokenize_negative_after_operator(self):
        """Test tokenizing negative after operator."""
        tokens = ExpressionParser.tokenize("5 * -3")
        assert len(tokens) == 3
        assert tokens[0].value == 5
        assert tokens[1].value == '*'
        assert tokens[2].value == -3

    def test_tokenize_no_spaces(self):
        """Test tokenizing without spaces."""
        tokens = ExpressionParser.tokenize("2+3*4")
        assert len(tokens) == 5

    def test_tokenize_invalid_character(self):
        """Test tokenizing with invalid character."""
        with pytest.raises(ValueError, match="Invalid character"):
            ExpressionParser.tokenize("2 + abc")


class TestInfixToPostfix:
    """Test suite for infix to postfix conversion."""

    def test_simple_addition(self):
        """Test simple addition conversion."""
        tokens = ExpressionParser.tokenize("2 + 3")
        postfix = ExpressionParser.infix_to_postfix(tokens)
        assert postfix[0].value == 2
        assert postfix[1].value == 3
        assert postfix[2].value == '+'

    def test_operator_precedence(self):
        """Test operator precedence handling."""
        tokens = ExpressionParser.tokenize("2 + 3 * 4")
        postfix = ExpressionParser.infix_to_postfix(tokens)
        # Should be: 2 3 4 * +
        assert postfix[0].value == 2
        assert postfix[1].value == 3
        assert postfix[2].value == 4
        assert postfix[3].value == '*'
        assert postfix[4].value == '+'

    def test_parentheses(self):
        """Test parentheses handling."""
        tokens = ExpressionParser.tokenize("(2 + 3) * 4")
        postfix = ExpressionParser.infix_to_postfix(tokens)
        # Should be: 2 3 + 4 *
        assert postfix[0].value == 2
        assert postfix[1].value == 3
        assert postfix[2].value == '+'
        assert postfix[3].value == 4
        assert postfix[4].value == '*'

    def test_power_operator_precedence(self):
        """Test power operator has highest precedence."""
        tokens = ExpressionParser.tokenize("2 + 3 ** 2")
        postfix = ExpressionParser.infix_to_postfix(tokens)
        # Should be: 2 3 2 ** +
        assert postfix[0].value == 2
        assert postfix[1].value == 3
        assert postfix[2].value == 2
        assert postfix[3].value == '**'
        assert postfix[4].value == '+'

    def test_power_right_associative(self):
        """Test power operator right associativity."""
        tokens = ExpressionParser.tokenize("2 ** 3 ** 2")
        postfix = ExpressionParser.infix_to_postfix(tokens)
        # Should be: 2 3 2 ** ** (right associative)
        assert postfix[0].value == 2
        assert postfix[1].value == 3
        assert postfix[2].value == 2
        assert postfix[3].value == '**'
        assert postfix[4].value == '**'

    def test_mismatched_parentheses_missing_close(self):
        """Test error on missing closing parenthesis."""
        tokens = ExpressionParser.tokenize("(2 + 3")
        with pytest.raises(ValueError, match="missing closing parenthesis"):
            ExpressionParser.infix_to_postfix(tokens)

    def test_mismatched_parentheses_missing_open(self):
        """Test error on missing opening parenthesis."""
        tokens = ExpressionParser.tokenize("2 + 3)")
        with pytest.raises(ValueError, match="missing opening parenthesis"):
            ExpressionParser.infix_to_postfix(tokens)


class TestEvaluatePostfix:
    """Test suite for postfix evaluation."""

    def test_simple_evaluation(self):
        """Test simple postfix evaluation."""
        tokens = [
            Token(TokenType.NUMBER, 2),
            Token(TokenType.NUMBER, 3),
            Token(TokenType.OPERATOR, '+')
        ]
        result = ExpressionParser.evaluate_postfix(tokens)
        assert result == 5

    def test_complex_evaluation(self):
        """Test complex postfix evaluation."""
        # 2 3 4 * + = 2 + (3 * 4) = 14
        tokens = [
            Token(TokenType.NUMBER, 2),
            Token(TokenType.NUMBER, 3),
            Token(TokenType.NUMBER, 4),
            Token(TokenType.OPERATOR, '*'),
            Token(TokenType.OPERATOR, '+')
        ]
        result = ExpressionParser.evaluate_postfix(tokens)
        assert result == 14

    def test_division_by_zero(self):
        """Test division by zero error."""
        tokens = [
            Token(TokenType.NUMBER, 5),
            Token(TokenType.NUMBER, 0),
            Token(TokenType.OPERATOR, '/')
        ]
        with pytest.raises(ValueError, match="Operation error"):
            ExpressionParser.evaluate_postfix(tokens)


class TestParse:
    """Test suite for full expression parsing."""

    def test_simple_expressions(self):
        """Test simple expression parsing."""
        assert ExpressionParser.parse("2 + 3") == 5
        assert ExpressionParser.parse("10 - 5") == 5
        assert ExpressionParser.parse("4 * 5") == 20
        assert ExpressionParser.parse("15 / 3") == 5

    def test_operator_precedence(self):
        """Test operator precedence in parsing."""
        assert ExpressionParser.parse("2 + 3 * 4") == 14
        assert ExpressionParser.parse("10 - 2 * 3") == 4
        assert ExpressionParser.parse("20 / 4 + 5") == 10

    def test_parentheses(self):
        """Test parentheses in parsing."""
        assert ExpressionParser.parse("(2 + 3) * 4") == 20
        assert ExpressionParser.parse("10 * (5 - 2)") == 30
        assert ExpressionParser.parse("((2 + 3) * 4) / 2") == 10

    def test_power_operator(self):
        """Test power operator parsing."""
        assert ExpressionParser.parse("2 ** 3") == 8
        assert ExpressionParser.parse("2 ** 8") == 256
        assert ExpressionParser.parse("5 ** 2") == 25

    def test_negative_numbers(self):
        """Test negative number parsing."""
        assert ExpressionParser.parse("-5") == -5
        assert ExpressionParser.parse("-5 + 3") == -2
        assert ExpressionParser.parse("5 * -3") == -15
        assert ExpressionParser.parse("(-2) * 3") == -6

    def test_decimal_numbers(self):
        """Test decimal number parsing."""
        assert ExpressionParser.parse("3.14 + 2.86") == 6.0
        assert ExpressionParser.parse("10.5 * 2") == 21.0

    def test_modulo(self):
        """Test modulo operator."""
        assert ExpressionParser.parse("10 % 3") == 1
        assert ExpressionParser.parse("20 % 7") == 6

    def test_complex_expressions(self):
        """Test complex expressions."""
        assert ExpressionParser.parse("2 + 3 * 4 - 5") == 9
        assert ExpressionParser.parse("(2 + 3) * (4 - 1)") == 15
        assert ExpressionParser.parse("2 ** 3 + 4 * 5") == 28

    def test_empty_expression(self):
        """Test empty expression error."""
        with pytest.raises(ValueError, match="Empty expression"):
            ExpressionParser.parse("")

    def test_whitespace_only(self):
        """Test whitespace-only expression error."""
        with pytest.raises(ValueError, match="Empty expression"):
            ExpressionParser.parse("   ")

    def test_division_by_zero_error(self):
        """Test division by zero error message."""
        with pytest.raises(ValueError, match="Operation error"):
            ExpressionParser.parse("5 / 0")

    def test_invalid_expression(self):
        """Test invalid expression error."""
        with pytest.raises(ValueError):
            ExpressionParser.parse("2 + + 3")
