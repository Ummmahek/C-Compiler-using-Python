import sys
from Lexer import Lexer
from Parser import Parser
from SymbolTable import SymbolTable
from Interpreter import Interpreter

def main():
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <source_file>")
        sys.exit(1)
    
    try:
        with open(sys.argv[1], 'r') as file:
            source = file.read()
    except FileNotFoundError:
        print("Error: Could not open file.")
        sys.exit(1)
    
    lexer = Lexer(source)
    parser = Parser(lexer)
    symbol_table = SymbolTable()
    interpreter = Interpreter(symbol_table)
    
    try:
        ast = parser.parse()
        for node in ast:
            interpreter.execute(node)
    except Exception as e:
        if isinstance(e, SyntaxError):
            print(f"Syntax Error: {e}")
        else:
            print(f"Execution Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()