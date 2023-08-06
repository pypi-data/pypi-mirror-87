from pyparsing import Word, nums, alphas, Combine, Optional, oneOf,Group,delimitedList, Keyword, Suppress, pyparsing_common, printables, Forward, ZeroOrMore
import bagheera.parser.errors as e

def parser(filename=None):
    module_name = Group(delimitedList(Word(alphas.upper(),alphas.lower()),"."))("Module Name")
    module_imports = Keyword("..") | Group(delimitedList(Word(printables, excludeChars=',)')))("Module Imports")
    module_declaration = Group(Suppress("module").setFailAction(e.ModuleDeclarationMissingException(filename)) + module_name + Suppress("exposing") + Suppress("(")+ module_imports+Suppress(")"))("Module Declaration")

    LPAR,RPAR = map(Suppress, '()')
    integer = Word(nums)
    real = Optional(Word(nums)) + '.' + Word(nums)
    expr = Forward()
    operand = Optional("-") + (real | integer)
    factor = operand | Group(LPAR + expr + RPAR)
    term = factor + ZeroOrMore( oneOf('* /') + factor )
    expr <<= term + ZeroOrMore( oneOf('+ -') + term )

    function_name = Word(alphas.lower())
    function_parameter = Word(alphas.upper()+alphas.lower())
    function_parameters = ZeroOrMore(function_parameter)("Function Parameter")
    function_body = expr
    function_declaration = Group(function_name + function_parameters + Suppress("=") + function_body)("Function Declaration")

    return module_declaration + ZeroOrMore(function_declaration)

def ast_print(item, ident=0):
    try:
        for key, value in item.items():
            print("\t"*ident, key,"->", value)
            ast_print(value, ident + 1)
    except Exception:
        print("\t"*ident,item, "bla")

if __name__ == "__main__":
    res = parser().parseString("module Header exposing (..)")
    print(res.dump())