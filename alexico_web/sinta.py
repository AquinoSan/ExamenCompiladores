from flask import Flask, render_template, request
from lexico import lexer
from sintactico import parser, errors, variables_declaradas

app = Flask(__name__)

# Función para analizar el código
def analyze_code(code):
    global variables_declaradas, errors
    variables_declaradas = set()  # Reiniciar variables declaradas
    errors = []  # Reiniciar lista de errores
    tokens_list = []
    sintactic_list = []
    lexer.lineno = 1  # Reiniciar el contador de líneas
    lexer.input(code)

    # Diccionario para contar tokens por tipo
    token_count = {
        'PROGRAMA': 0,
        'INT': 0,
        'READ': 0,
        'PRINTF': 0,
        'END': 0,
        'IDENTIFICADOR': 0,
        'CADENA': 0,
        'SÍMBOLOS': 0  # Para símbolos como +, =, etc.
    }

    # Recopilar todos los tokens léxicos
    for token in lexer:
        tokens_list.append({"token": token.type, "lexema": str(token.value), "linea": token.lineno})

        # Identificar el tipo de token para el análisis sintáctico
        token_type = {
            'PR': 'X' if token.type in ['PROGRAMA', 'INT', 'READ', 'PRINTF', 'END'] else '',
            'ID': 'X' if token.type == 'IDENTIFICADOR' else '',
            'SÍM': 'X' if token.type in ['IGUAL', 'ADICION', 'SEMICOLON', 'COMA', 'RBRACE', 'LBRACE', 'RPAREN', 'LPAREN'] else '',
            'CAD': 'X' if token.type == 'CADENA' else '',
            'TIPO': ''  
        }

        # Contar tokens por tipo
        if token.type in ['PROGRAMA', 'INT', 'READ', 'PRINTF', 'END']:
            token_count[token.type] += 1
        elif token.type == 'IDENTIFICADOR':
            token_count['IDENTIFICADOR'] += 1
        elif token.type == 'CADENA':
            token_count['CADENA'] += 1
        else:
            token_count['SÍMBOLOS'] += 1

        sintactic_list.append({
            "token": token.type,
            "lexema": str(token.value),
            **token_type
        })

    syntax_error = None
    try:
        parser.parse(code, lexer=lexer)
    except SyntaxError as e:
        syntax_error = str(e)

    if errors:
        syntax_error = "\n".join(errors)

    return tokens_list, sintactic_list, token_count, syntax_error

# Rutas del servidor Flask
@app.route('/', methods=['GET', 'POST'])
def index():
    tokens = []
    sintactic_tokens = []
    token_count = None
    error = None

    if request.method == 'POST':
        code = request.form['code']
        tokens, sintactic_tokens, token_count, error = analyze_code(code)

    return render_template('index.html', tokens=tokens, sintactic_tokens=sintactic_tokens, token_count=token_count, error=error)

if __name__ == '__main__':
    app.run(debug=True)
