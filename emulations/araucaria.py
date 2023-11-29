import ply.lex as lex

# List of token names.   This is always required
tokens = (
   'LCOLCH',
   'RCOLCH',
   'LPAREN',
   'RPAREN',
   'LBRACKET',
   'RBRACKET',
   'COMMA',
   'NAME',
)

# Regular expression rules for simple tokens
t_LCOLCH   = r'\['
t_RCOLCH  = r'\]'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

lexer = lex.lex()

name = ' '

def p_intent(t):
    'intent : operation NAME LBRACKET predicates RBRACKET'
    name = t[1]

def p_operation(t):
    