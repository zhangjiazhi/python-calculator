#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Command-line interface for the calculator.
Provides REPL loop with expression evaluation and command handling.
"""

from calculator.parser import ExpressionParser
from calculator.history import HistoryManager

# Maximum input length (same as parser limit)
MAX_INPUT_LENGTH = 1000


class CLI:
    """Command-line interface for the calculator."""

    def __init__(self):
        """Initialize the CLI with history manager."""
        self.history = HistoryManager()
        self.parser = ExpressionParser()
        self.running = True

    def run(self):
        """Main REPL loop."""
        self.print_welcome()

        while self.running:
            try:
                user_input = input("calc> ").strip()

                if not user_input:
                    continue

                # Check if it's a command
                if user_input.lower() in ['help', 'history', 'clear', 'exit', 'quit']:
                    self.handle_command(user_input.lower())
                else:
                    # Try to evaluate as expression
                    self.evaluate_expression(user_input)

            except KeyboardInterrupt:
                print("\nUse 'exit' or 'quit' to leave the calculator.")
            except EOFError:
                print("\nGoodbye!")
                break

    def print_welcome(self):
        """Print welcome message."""
        print("=" * 60)
        print("Python Calculator - Phase 1")
        print("=" * 60)
        print("Type 'help' for available commands")
        print("Enter mathematical expressions to calculate")
        print("=" * 60)

    def handle_command(self, command: str):
        """
        Handle special commands.

        Args:
            command: The command string (help, history, clear, exit, quit)
        """
        if command == 'help':
            self.show_help()

        elif command == 'history':
            self.show_history()

        elif command == 'clear':
            self.clear_history()

        elif command in ['exit', 'quit']:
            print("Goodbye!")
            self.running = False

    def show_help(self):
        """Display help information."""
        print("\nAvailable Commands:")
        print("  help     - Show this help message")
        print("  history  - Display calculation history")
        print("  clear    - Clear calculation history")
        print("  exit     - Exit the calculator")
        print("  quit     - Exit the calculator")
        print("\nSupported Operations:")
        print("  +   - Addition")
        print("  -   - Subtraction")
        print("  *   - Multiplication")
        print("  /   - Division")
        print("  %   - Modulo")
        print("  **  - Power (exponentiation)")
        print("  ()  - Parentheses for grouping")
        print("\nExamples:")
        print("  2 + 3")
        print("  10 * (5 - 2)")
        print("  2 ** 8")
        print("  -5 + 3")
        print("  (-2) * 3")
        print()

    def show_history(self):
        """Display calculation history."""
        if self.history.is_empty():
            print("No history available.")
            return

        print("\nCalculation History:")
        print("-" * 60)
        for entry in self.history.get_all():
            print(entry)
        print("-" * 60)
        print(f"Total entries: {len(self.history)}")
        print()

    def clear_history(self):
        """Clear calculation history."""
        self.history.clear()
        print("History cleared.")

    def evaluate_expression(self, expression: str):
        """
        Evaluate a mathematical expression.

        Args:
            expression: The expression string to evaluate
        """
        # Check input length for user-friendly error message
        if len(expression) > MAX_INPUT_LENGTH:
            print(f"Error: Expression too long ({len(expression)} characters). "
                  f"Maximum allowed: {MAX_INPUT_LENGTH}")
            return

        try:
            result = self.parser.parse(expression)

            # Format the result nicely
            if isinstance(result, float):
                # Remove trailing zeros for cleaner display
                if result.is_integer():
                    result = int(result)
                else:
                    # Format to reasonable precision
                    result = round(result, 10)

            print(f"= {result}")

            # Add to history
            self.history.add(expression, result)

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
