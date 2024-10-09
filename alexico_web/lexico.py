import ply.lex as lex

# Lista de tokens
tokens = ['PROGRAMA', 'INT', 'READ', 'PRINTF', 'END', 'SUMA', 'LPAREN', 
          'RPAREN', 'LBRACE', 'RBRACE', 'COMA', 'SEMICOLON', 'ADICION', 
          'IGUAL', 'IDENTIFICADOR', 'VARIABLE', 'CADENA']

reservada = {
    "programa": "PROGRAMA",
    "int": "INT",
    "read": "READ",
    "printf": "PRINTF",
    "end": "END"
}

simbolo = {
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE", 
    "}": "RBRACE",
    ",": "COMA",
    ";": "SEMICOLON",
    "+": "ADICION",
    "=": "IGUAL"
}

# Reglas de expresión regular para los tokens simples
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMA = r'\,'
t_SEMICOLON = r';'
t_ADICION = r'\+'
t_IGUAL = r'='

# Definición de palabras clave y variables
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservada.get(t.value, 'IDENTIFICADOR')
    return t

def t_CADENA(t):
    r'"[^"]*"'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
