
import ply.lex as lex
import ply.yacc as yacc

# List of token names
tokens = [
    'IDENTIFIER',
    'COLON',
    'SEMICOLON',
    'COMMA',
    'SIGNAL',
    'PORT',
    'IN',
    'OUT',
    'INOUT',
    'TYPE'
]

# Regular expression rules for simple tokens
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_ignore = ' 	\n'

# Keywords
keywords = {
    'signal': 'SIGNAL',
    'port': 'PORT',
    'in': 'IN',
    'out': 'OUT',
    'inout': 'INOUT'
}

# A regular expression rule with some action code
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')  # Check for keywords
    return t

def t_TYPE(t):
    r'bit|std_logic|std_logic_vector|integer'
    return t

# Error handling rule
def t_error(t):
    print(f"Illegal character '{{t.value[0]}}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# List to hold the ports and signals
ports = []
signals = []

# Grammar rules and actions
def p_design_entity(p):
    '''design_entity : port_clause
                     | signal_clause'''
    p[0] = p[1]

def p_port_clause(p):
    '''port_clause : PORT '(' port_list ')' ';' '''
    p[0] = p[3]

def p_port_list(p):
    '''port_list : port_list_item
                 | port_list_item COMMA port_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_port_list_item(p):
    '''port_list_item : IDENTIFIER COLON direction TYPE'''
    ports.append((p[1], p[4]))

def p_direction(p):
    '''direction : IN
                 | OUT
                 | INOUT'''
    p[0] = p[1]

def p_signal_clause(p):
    '''signal_clause : SIGNAL signal_list ';' '''
    p[0] = p[2]

def p_signal_list(p):
    '''signal_list : signal_item
                   | signal_item COMMA signal_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_signal_item(p):
    '''signal_item : IDENTIFIER COLON TYPE'''
    signals.append((p[1], p[3]))

def p_error(p):
    print(f"Syntax error at '{{p.value}}'")

# Build the parser
parser = yacc.yacc()

# Testing the parser
vhdl_code = """
signal clk : std_logic;
signal rst : std_logic;
port(
    a : in std_logic;
    b : out std_logic_vector;
    c : inout std_logic
);
"""

# Parse the VHDL code
parser.parse(vhdl_code)

# Output the extracted ports and signals
print("Ports:", ports)
print("Signals:", signals)
