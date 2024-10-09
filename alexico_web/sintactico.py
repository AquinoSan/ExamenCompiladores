import ply.yacc as yacc
from lexico import tokens

errors = []
variables_declaradas = set()

def p_funcion(p):
    '''funcion : PROGRAMA IDENTIFICADOR LPAREN RPAREN LBRACE estructura RBRACE'''
    if not errors:
        print("Ningún error sintáctico!")

def p_estructura(p):
    'estructura : variables entrada operacion impresion salida'
    pass

def p_variables(p):
    '''variables : INT IDENTIFICADOR COMA IDENTIFICADOR COMA IDENTIFICADOR SEMICOLON'''
    global variables_declaradas
    variables_declaradas.update([p[2], p[4], p[6]])
    print("Variables correctamente declaradas ", variables_declaradas)

def p_entrada(p):
    '''entrada : lectura lectura'''

def p_lectura(p):
    '''lectura : READ IDENTIFICADOR SEMICOLON'''
    if p[2] not in variables_declaradas:
        errors.append(f"Error: Variable '{p[2]}' no declarada en la línea {p.lineno(2)}")

def p_operacion(p):
    '''operacion : IDENTIFICADOR IGUAL IDENTIFICADOR ADICION IDENTIFICADOR SEMICOLON'''
    if p[1] not in variables_declaradas:
        errors.append(f"Error: Variable '{p[1]}' no declarada en la línea {p.lineno(1)}")
    if p[3] not in variables_declaradas:
        errors.append(f"Error: Variable '{p[3]}' no declarada en la línea {p.lineno(3)}")
    if p[5] not in variables_declaradas:
        errors.append(f"Error: Variable '{p[5]}' no declarada en la línea {p.lineno(5)}")

def p_impresion(p):
    '''impresion : PRINTF LPAREN CADENA RPAREN'''

def p_salida(p):
    '''salida : END SEMICOLON'''

def p_error(p):
    if p:
        errors.append(f"Error de sintaxis en la línea {p.lineno}")
    else:
        errors.append("Error de sintaxis al final del archivo")

parser = yacc.yacc()
# Función para realizar el análisis sintáctico
def realizar_analisis_sintactico(code, linea_param):
    global resultado_gramatica
    global lineas
    lineas = linea_param
    resultado_gramatica.clear()
    resultado_sintactico = parser.parse(code)
    if resultado_sintactico:
        resultado_gramatica.append(resultado_sintactico)
    return resultado_gramatica
