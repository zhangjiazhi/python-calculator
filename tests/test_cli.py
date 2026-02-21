#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit tests for CLI interface.
"""

import pytest
from unittest.mock import patch
from ui.cli import CLI


class TestCLICommands:
    """Test suite for CLI command handling."""

    def test_help_command(self, capsys):
        """Test help command displays help message."""
        cli = CLI()
        cli.handle_command('help')
        captured = capsys.readouterr()
        assert "Available Commands:" in captured.out
        assert "Supported Operations:" in captured.out
        assert "Examples:" in captured.out

    def test_history_empty(self, capsys):
        """Test history command with no history."""
        cli = CLI()
        cli.handle_command('history')
        captured = capsys.readouterr()
        assert "No history available" in captured.out

    def test_history_with_entries(self, capsys):
        """Test history command with entries."""
        cli = CLI()
        cli.history.add("2+3", 5)
        cli.history.add("10*5", 50)
        cli.handle_command('history')
        captured = capsys.readouterr()
        assert "2+3 = 5" in captured.out
        assert "10*5 = 50" in captured.out
        assert "Total entries: 2" in captured.out

    def test_clear_command(self, capsys):
        """Test clear command."""
        cli = CLI()
        cli.history.add("2+3", 5)
        assert len(cli.history) == 1
        cli.handle_command('clear')
        captured = capsys.readouterr()
        assert "History cleared" in captured.out
        assert cli.history.is_empty()

    def test_exit_command(self):
        """Test exit command."""
        cli = CLI()
        assert cli.running is True
        cli.handle_command('exit')
        assert cli.running is False

    def test_quit_command(self, capsys):
        """Test quit command."""
        cli = CLI()
        assert cli.running is True
        cli.handle_command('quit')
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out
        assert cli.running is False


class TestCLIExpressions:
    """Test suite for expression evaluation in CLI."""

    def test_valid_expression(self, capsys):
        """Test valid expression evaluation."""
        cli = CLI()
        cli.evaluate_expression("2 + 3")
        captured = capsys.readouterr()
        assert "= 5" in captured.out
        assert len(cli.history) == 1

    def test_complex_expression(self, capsys):
        """Test complex expression."""
        cli = CLI()
        cli.evaluate_expression("(2 + 3) * 4")
        captured = capsys.readouterr()
        assert "= 20" in captured.out

    def test_invalid_expression(self, capsys):
        """Test invalid expression error handling."""
        cli = CLI()
        cli.evaluate_expression("2 + + 3")
        captured = capsys.readouterr()
        assert "Error:" in captured.out

    def test_division_by_zero(self, capsys):
        """Test division by zero error."""
        cli = CLI()
        cli.evaluate_expression("5 / 0")
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "zero" in captured.out.lower()

    def test_integer_result_formatting(self, capsys):
        """Test integer result formatting."""
        cli = CLI()
        cli.evaluate_expression("10.0 / 2.0")
        captured = capsys.readouterr()
        assert "= 5" in captured.out  # Not "= 5.0"

    def test_float_result_formatting(self, capsys):
        """Test float result formatting."""
        cli = CLI()
        cli.evaluate_expression("10 / 3")
        captured = capsys.readouterr()
        assert "= 3.33333" in captured.out

    def test_expression_too_long(self, capsys):
        """Test expression length limit in CLI."""
        cli = CLI()
        long_expr = "1+" * 600  # > 1000 characters
        cli.evaluate_expression(long_expr)
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "too long" in captured.out.lower()

    def test_complex_number_error(self, capsys):
        """Test complex number rejection."""
        cli = CLI()
        cli.evaluate_expression("(-1) ** 0.5")
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "complex" in captured.out.lower()

    def test_multiple_decimal_points_error(self, capsys):
        """Test multiple decimal points error."""
        cli = CLI()
        cli.evaluate_expression("1.2.3")
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "decimal" in captured.out.lower()


class TestCLIIntegration:
    """Integration tests for full CLI flow."""

    @patch('builtins.input', side_effect=['2+3', 'history', 'exit'])
    def test_full_session(self, mock_input, capsys):
        """Test complete CLI session."""
        cli = CLI()
        cli.run()
        captured = capsys.readouterr()

        # Welcome message
        assert "Python Calculator" in captured.out

        # Expression result
        assert "= 5" in captured.out

        # History display
        assert "2+3 = 5" in captured.out

        # Exit message
        assert "Goodbye!" in captured.out

    @patch('builtins.input', side_effect=['', 'exit'])
    def test_empty_input(self, mock_input, capsys):
        """Test empty input handling."""
        cli = CLI()
        cli.run()
        captured = capsys.readouterr()
        # Should not crash, just continue
        assert "Goodbye!" in captured.out

    @patch('builtins.input', side_effect=['help', 'exit'])
    def test_help_in_session(self, mock_input, capsys):
        """Test help command in session."""
        cli = CLI()
        cli.run()
        captured = capsys.readouterr()
        assert "Available Commands:" in captured.out
        assert "Goodbye!" in captured.out

    @patch('builtins.input', side_effect=['2+2', 'clear', 'history', 'exit'])
    def test_clear_in_session(self, mock_input, capsys):
        """Test clear command in session."""
        cli = CLI()
        cli.run()
        captured = capsys.readouterr()
        assert "= 4" in captured.out
        assert "History cleared" in captured.out
        assert "No history available" in captured.out

    @patch('builtins.input', side_effect=[KeyboardInterrupt(), 'exit'])
    def test_keyboard_interrupt(self, mock_input, capsys):
        """Test KeyboardInterrupt handling."""
        cli = CLI()
        cli.run()
        captured = capsys.readouterr()
        assert "Use 'exit' or 'quit'" in captured.out

    @patch('builtins.input', side_effect=EOFError())
    def test_eof_handling(self, mock_input, capsys):
        """Test EOF handling."""
        cli = CLI()
        cli.run()
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out


class TestCLIWelcome:
    """Test suite for welcome message."""

    def test_print_welcome(self, capsys):
        """Test welcome message display."""
        cli = CLI()
        cli.print_welcome()
        captured = capsys.readouterr()
        assert "Python Calculator" in captured.out
        assert "Type 'help'" in captured.out
