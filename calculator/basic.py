#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Basic arithmetic operations module.
Provides fundamental mathematical operations with input validation.
"""

from typing import Union

Number = Union[int, float]


class BasicCalculator:
    """Static methods for basic arithmetic operations."""

    @staticmethod
    def add(a: Number, b: Number) -> Number:
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
    def subtract(a: Number, b: Number) -> Number:
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
    def multiply(a: Number, b: Number) -> Number:
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
    def divide(a: Number, b: Number) -> float:
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
    def modulo(a: Number, b: Number) -> Number:
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
    def power(a: Number, b: Number) -> Number:
        """
        Raise a to the power of b.

        Args:
            a: Base
            b: Exponent

        Returns:
            a raised to the power b

        Raises:
            ValueError: If result would overflow or produce complex number
        """
        # Check for operations that would produce complex numbers
        if a < 0 and isinstance(b, float) and not b.is_integer():
            raise ValueError(
                f"Cannot raise negative number to fractional power: "
                f"{a} ** {b} would produce complex number"
            )

        try:
            result = a ** b

            # Check if result is complex (additional safety check)
            if isinstance(result, complex):
                raise ValueError(
                    f"Operation produced complex number: {a} ** {b}"
                )

            # Check for overflow
            if isinstance(result, float) and (result == float('inf') or result == float('-inf')):
                raise ValueError("Result overflow: number too large")
            return result
        except OverflowError:
            raise ValueError("Result overflow: number too large")
