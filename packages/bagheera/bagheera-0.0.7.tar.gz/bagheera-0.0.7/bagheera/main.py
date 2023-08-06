"""
Main module used as entry point for the console executable "bagheera"
"""
import os
from bagheera.parser.parser import parser
import pyparsing

"""
Entry point for the parser.
"""
def parse(file):
    try:
        return parser(file).parseFile(file)
    except pyparsing.ParseException as e:
        print(e.line)
        print(" " * (e.column - 1) + "^")
        print(e)
        raise e