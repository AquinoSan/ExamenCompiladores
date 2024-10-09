import ply.lex as lex
import ply.yacc as yacc
from flask import Flask, render_template, request

app = Flask(__name__)

# Lista de tokens
tokens = ['USING', 'NAMESPACE', 'CLASS', 'STATIC', 'VOID', 'MAIN', 'STRING', 
          'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN', 'SEMICOLON', 
          'CONSOLE', 'WRITELINE', 'CADENA', 'IDENTIFICADOR', 'DOT', 'LBRACKET', 'RBRACKET', 'ERROR']

reservada = {
    'using': 'USING',
    'namespace': 'NAMESPACE',
    'class': 'CLASS',
    'static': 'STATIC',
    'void': 'VOID',
    'Main': 'MAIN',
    'string': 'STRING',
    'Console': 'CONSOLE',
    'WriteLine': 'WRITELINE'
}

# Definir símbolos
simbolo = {
    '{': 'LBRACE',
    '}': 'RBRACE',
    '(': 'LPAREN',
    ')': 'RPAREN',
    '[': 'LBRACKET',
    ']': 'RBRACKET',
    ';': 'SEMICOLON',
    '.': 'DOT'
}

# Reglas de expresión regular para los tokens simples
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_DOT = r'\.'

# Reglas de expresiones regulares para palabras reservadas y otros tokens
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

# Ignorar espacios y tabs
t_ignore = ' \t'

# Manejo de errores léxicos
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.type = 'ERROR'
    t.lexer.skip(1)
    return t

lexer = lex.lex()

# Definición del parser (sintaxis)
errors = []

def p_programa(p):
    '''programa : using_decl namespace_decl'''
    if not errors:
        print("¡Análisis sintáctico sin errores!")

def p_using_decl(p):
    '''using_decl : USING IDENTIFICADOR SEMICOLON'''

def p_namespace_decl(p):
    '''namespace_decl : NAMESPACE IDENTIFICADOR LBRACE class_decl RBRACE'''

def p_class_decl(p):
    '''class_decl : CLASS IDENTIFICADOR LBRACE method_decl RBRACE'''

def p_method_decl(p):
    '''method_decl : STATIC VOID MAIN LPAREN STRING LBRACKET RBRACKET IDENTIFICADOR RPAREN LBRACE statement RBRACE'''

def p_statement(p):
    '''statement : CONSOLE DOT WRITELINE LPAREN CADENA RPAREN SEMICOLON'''

def p_error(p):
    if p:
        errors.append(f"Error de sintaxis en la línea {p.lineno}")
    else:
        errors.append("Error de sintaxis al final del archivo")

parser = yacc.yacc()

# Función para analizar el código
def analyze_code(code):
    global errors
    errors = []  # Reiniciar lista de errores
    tokens_list = []
    lexer.lineno = 1  # Reiniciar el contador de líneas
    lexer.input(code)

    # Recopilar todos los tokens léxicos
    for token in lexer:
        tokens_list.append({"token": token.type, "lexema": str(token.value), "linea": token.lineno})

    syntax_error = None
    try:
        parser.parse(code, lexer=lexer)
    except SyntaxError as e:
        syntax_error = str(e)

    if errors:
        syntax_error = "\n".join(errors)

    return tokens_list, syntax_error

# Rutas del servidor Flask
@app.route('/', methods=['GET', 'POST'])
def index():
    tokens = []
    error = None

    if request.method == 'POST':
        code = request.form['code']
        tokens, error = analyze_code(code)

    return render_template('index.html', tokens=tokens, error=error)

if __name__ == '__main__':
    app.run(debug=True)
