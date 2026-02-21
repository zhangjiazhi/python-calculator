#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Basic arithmetic operations module.
Provides fundamental mathematical operations with input validation.
"""


class BasicCalculator:
    """Static methods for basic arithmetic operations."""

    @staticmethod
    def add(a, b):
        """
        Add two numbers.

        Args:
            a: First operand
            b: Second operand

        Returns:
            Sum of a and b
        """
        return a + b

    @staticmethod
    def subtract(a, b):
        """
        Subtract b from a.

        Args:
            a: First operand
            b: Second operand

        Returns:
            Difference of a and b
        """
        return a - b

    @staticmethod
    def multiply(a, b):
        """
        Multiply two numbers.

        Args:
            a: First operand
            b: Second operand

        Returns:
            Product of a and b
        """
        return a * b

    @staticmethod
    def divide(a, b):
        """
        Divide a by b.

        Args:
            a: Numerator
            b: Denominator

        Returns:
            Quotient of a and b

        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b

    @staticmethod
    def modulo(a, b):
        """
        Calculate a modulo b.

        Args:
            a: First operand
            b: Modulus

        Returns:
            Remainder of a divided by b

        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Modulo by zero is not allowed")
        return a % b

    @staticmethod
    def power(a, b):
        """
        Raise a to the power of b.

        Args:
            a: Base
            b: Exponent

        Returns:
            a raised to the power b

        Raises:
            ValueError: If result would overflow
        """
        try:
            result = a ** b
            # Check for overflow
            if isinstance(result, float) and (result == float('inf') or result == float('-inf')):
                raise ValueError("Result overflow: number too large")
            return result
        except OverflowError:
            raise ValueError("Result overflow: number too large")
