# Python Calculator

Command-line calculator with expression parsing and history management.

## Features

- Basic arithmetic operations (+, -, *, /, %, **)
- Expression parsing with Shunting Yard algorithm
- Parentheses and operator precedence
- Calculation history with timestamps
- Interactive REPL interface

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py
```

## Testing

```bash
pytest tests/ -v
--cov=calculator --cov=ui --cov-report=term-missing
```