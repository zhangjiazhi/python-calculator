# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python Calculator - A command-line calculator application with Phase 1 (Basic Calculator MVP) completed.

**Current Status**: Phase 1 implemented and tested (59/59 tests passing, 64% coverage)

## Project Structure

```
.
├── main.py                    # Application entry point
├── calculator/
│   ├── __init__.py
│   ├── basic.py              # Basic arithmetic operations (add, subtract, multiply, divide, modulo, power)
│   ├── parser.py             # Expression parser using Shunting Yard algorithm
│   └── history.py            # History management with timestamps
├── ui/
│   ├── __init__.py
│   └── cli.py                # Command-line REPL interface
├── tests/
│   ├── __init__.py
│   ├── test_basic.py         # Tests for basic operations
│   ├── test_parser.py        # Tests for expression parsing
│   └── test_history.py       # Tests for history management
├── requirements.txt           # pytest==7.4.3, pytest-cov==4.1.0
└── README.md
```

## Running the Project

**Interactive mode** (REPL):
```bash
python3 main.py
```

**Batch mode** (pipe input):
```bash
python3 main.py < /tmp/calculator_test_input.txt
```

## Testing

Run all tests:
```bash
pytest tests/ -v
```

Run specific test file:
```bash
pytest tests/test_parser.py -v
```

Run with coverage:
```bash
pytest tests/ --cov=calculator --cov=ui --cov-report=term-missing
```

## Architecture

### Expression Parsing
- Uses **Shunting Yard algorithm** to convert infix expressions to postfix
- Token-based parsing: NUMBER, OPERATOR, LPAREN, RPAREN
- Operator precedence: `**` (right-associative, precedence 3), `*/%` (left, 2), `+-` (left, 1)
- Handles negative numbers, decimals, multi-digit numbers, nested parentheses

### Error Handling
Three-layer strategy:
1. **Operation layer** (basic.py): Validates inputs, raises ValueError for domain errors
2. **Parser layer** (parser.py): Validates syntax, raises ValueError for invalid expressions
3. **UI layer** (cli.py): Catches all exceptions, displays user-friendly messages

### Commands
- `help` - Show available operations and commands
- `history` - Display calculation history with timestamps
- `clear` - Clear history
- `exit` / `quit` - Exit program

## Extension Points for Phase 2

The design supports future scientific calculator features:
- Token types can be extended (add FUNCTION type for sin/cos/tan)
- Parser can recognize function call syntax
- Can add CONSTANT type tokens (pi, e)
- HistoryManager can add save/load methods for persistence
