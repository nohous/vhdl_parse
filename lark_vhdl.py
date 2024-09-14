from pprint import pprint
from lark import Lark


with open("vhdl.lark") as f:
    vhdl_grammar = f.read()

#pprint(vhdl_grammar)

parser = Lark(vhdl_grammar)