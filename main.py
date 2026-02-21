#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main entry point for Python Calculator
"""

from ui.cli import CLI


def main():
    """Main entry point - start the calculator CLI."""
    calculator = CLI()
    calculator.run()


if __name__ == "__main__":
    main()
