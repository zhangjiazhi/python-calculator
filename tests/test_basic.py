#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit tests for basic calculator operations.
"""

import pytest
from calculator.basic import BasicCalculator


class TestBasicCalculator:
    """Test suite for BasicCalculator class."""

    def test_add_positive_numbers(self):
        """Test addition of positive numbers."""
        assert BasicCalculator.add(2, 3) == 5
        assert BasicCalculator.add(10, 20) == 30
        assert BasicCalculator.add(0, 5) == 5

    def test_add_negative_numbers(self):
        """Test addition with negative numbers."""
        assert BasicCalculator.add(-5, 3) == -2
        assert BasicCalculator.add(-5, -3) == -8
        assert BasicCalculator.add(5, -3) == 2

    def test_add_floats(self):
        """Test addition of floating-point numbers."""
        assert BasicCalculator.add(2.5, 3.5) == 6.0
        assert BasicCalculator.add(0.1, 0.2) == pytest.approx(0.3)

    def test_subtract(self):
        """Test subtraction."""
        assert BasicCalculator.subtract(5, 3) == 2
        assert BasicCalculator.subtract(3, 5) == -2
        assert BasicCalculator.subtract(-5, -3) == -2
        assert BasicCalculator.subtract(10.5, 5.5) == 5.0

    def test_multiply(self):
        """Test multiplication."""
        assert BasicCalculator.multiply(2, 3) == 6
        assert BasicCalculator.multiply(-2, 3) == -6
        assert BasicCalculator.multiply(-2, -3) == 6
        assert BasicCalculator.multiply(2.5, 4) == 10.0
        assert BasicCalculator.multiply(0, 100) == 0

    def test_divide(self):
        """Test division."""
        assert BasicCalculator.divide(6, 3) == 2
        assert BasicCalculator.divide(7, 2) == 3.5
        assert BasicCalculator.divide(-6, 3) == -2
        assert BasicCalculator.divide(10, 4) == 2.5

    def test_divide_by_zero(self):
        """Test division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Division by zero"):
            BasicCalculator.divide(5, 0)

    def test_modulo(self):
        """Test modulo operation."""
        assert BasicCalculator.modulo(10, 3) == 1
        assert BasicCalculator.modulo(20, 7) == 6
        assert BasicCalculator.modulo(15, 5) == 0
        assert BasicCalculator.modulo(-10, 3) == 2

    def test_modulo_by_zero(self):
        """Test modulo by zero raises ValueError."""
        with pytest.raises(ValueError, match="Modulo by zero"):
            BasicCalculator.modulo(5, 0)

    def test_power(self):
        """Test power operation."""
        assert BasicCalculator.power(2, 3) == 8
        assert BasicCalculator.power(5, 2) == 25
        assert BasicCalculator.power(2, 0) == 1
        assert BasicCalculator.power(10, -1) == 0.1
        assert BasicCalculator.power(4, 0.5) == 2.0

    def test_power_negative_base(self):
        """Test power with negative base."""
        assert BasicCalculator.power(-2, 3) == -8
        assert BasicCalculator.power(-2, 2) == 4

    def test_power_overflow(self):
        """Test power overflow handling."""
        # Test with float that causes overflow to infinity
        with pytest.raises(ValueError, match="overflow"):
            BasicCalculator.power(10.0, 10000)

    def test_power_complex_number_rejection(self):
        """Test that negative base with fractional exponent is rejected."""
        with pytest.raises(ValueError, match="complex number"):
            BasicCalculator.power(-1, 0.5)

        with pytest.raises(ValueError, match="complex number"):
            BasicCalculator.power(-4, 0.5)

        with pytest.raises(ValueError, match="complex number"):
            BasicCalculator.power(-2, 1.5)

    def test_power_negative_base_integer_exponent(self):
        """Test negative base with integer exponent still works."""
        # These should work fine (no complex numbers)
        assert BasicCalculator.power(-2, 2) == 4
        assert BasicCalculator.power(-2, 3) == -8
        assert BasicCalculator.power(-1, 2) == 1
