# C-Compiler-using-Python

This project implements a simplified **C language compiler and interpreter** in Python. It includes the full compilation pipeline:

- Lexical Analysis (Lexer)
- Syntax Analysis (Parser)
- Abstract Syntax Tree (AST)
- Semantic Analysis (Symbol Table)
- Interpreter (Execution Engine)

The compiler supports arithmetic operations, string handling, variable declarations, and includes basic error handling.

## Features

- Lexer for tokenizing C-like source code
- Recursive descent parser generating an Abstract Syntax Tree (AST)
- Symbol table management for variables
- Interpreter to execute the AST
- Error handling for syntax and semantic errors
- Example source file with arithmetic and string expressions

## Project Structure
c-compiler-python/
│
├── lexer.py # Lexical analyzer
├── parser.py # Syntax analyzer and AST builder
├── ast.py # AST node definitions
├── interpreter.py # AST evaluator
├── symbol_table.py # Symbol table for variable scoping
├── main.py # Entry point that integrates all components
├── README.md # Project documentation

How It Works
Lexer (lexer.py):

Reads raw source code.

Tokenizes keywords, identifiers, literals, symbols, and operators.

Parser (parser.py):

Consumes tokens from the lexer.

Builds an Abstract Syntax Tree (AST) representing the program structure.

AST Nodes (ast.py):

Contains classes like BinaryOp, Assignment, Print, Literal, etc.

Symbol Table (symbol_table.py):

Stores declared variables and their types/values.

Interpreter (interpreter.py):

Walks the AST and evaluates each node.

Prints output and raises errors if any semantic rules are violated.

Main Program (main.py):

Loads source from example_input.txt.

Runs the full pipeline: Lex → Parse → Interpret.
