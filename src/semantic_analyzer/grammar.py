from ply import yacc
from ply import lex
from semantic_analyzer.expresions import *
from semantic_analyzer.instructions import *


reservadas = {
    "print": "IMPRIMIR",
    "while": "WHILE",
    "if": "IF",
    "do": "DO",
    "func": "FUNC",
    "true": "TRUE",
    "false": "FALSE",
    "args": "ARGS",
    "main": "MAIN",
}

tokens = [
    "PTCOMA",
    "LLAVIZQ",
    "LLAVDER",
    "PARIZQ",
    "PARDER",
    "MENQUE",
    "MAYQUE",
    "IGUALQUE",
    "NIGUALQUE",
    "DECIMAL",
    "ENTERO",
    "CADENA",
    "ID",
    "ASSIGN",
    "COMA",
    "INCREMENTO",
    "DECREMENTO",
] + list(reservadas.values())

# Tokens
t_PTCOMA = r";"
t_LLAVIZQ = r"{"
t_LLAVDER = r"}"
t_PARIZQ = r"\("
t_PARDER = r"\)"
t_MENQUE = r"<"
t_MAYQUE = r">"
t_IGUALQUE = r"=="
t_NIGUALQUE = r"!="
t_ASSIGN = r":="
t_COMA = r","
t_INCREMENTO = r"\+\+"
t_DECREMENTO = r"--"


def t_DECIMAL(t):
    r"\d+\.\d+"
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t


def t_ENTERO(t):
    r"\d+"
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reservadas.get(t.value.lower(), "ID")  # Check for reserved words
    return t


def t_CADENA(t):
    r"\".*?\" "
    t.value = t.value[1:-1]  # remuevo las comillas
    return t


# Caracteres ignorados
t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def p_init(t):
    "init            : instrucciones"
    t[0] = t[1]


def p_instrucciones_lista(t):
    "instrucciones    : instrucciones instruccion"
    t[1].append(t[2])
    t[0] = t[1]


def p_instrucciones_instruccion(t):
    "instrucciones    : instruccion"
    t[0] = [t[1]]


def p_instruccion(t):
    """instruccion      : imprimir_instr
    | asignacion_instr
    | mientras_instr
    | if_instr
    | funcion
    | llamada_funcion
    | incremento
    | decremento"""
    t[0] = t[1]


def p_instruccion_imprimir(t):
    "imprimir_instr     : IMPRIMIR PARIZQ expresion_cadena PARDER PTCOMA"
    t[0] = Imprimir(t[3])


def p_asignacion_instr(t):
    "asignacion_instr   : ID ASSIGN expresion_numerica PTCOMA"
    t[0] = Asignacion(t[1], t[3])


def p_mientras_instr(t):
    "mientras_instr     : WHILE PARIZQ expresion_logica PARDER DO LLAVIZQ instrucciones LLAVDER PTCOMA"
    t[0] = Mientras(t[3], t[7])


def p_if_instr(t):
    "if_instr           : IF PARIZQ expresion_logica PARDER DO LLAVIZQ instrucciones LLAVDER PTCOMA"
    t[0] = If(t[3], t[7])


def p_parametros_funcion_lista(t):
    "parametros_funcion : parametros_funcion COMA ID"
    t[0] = t[1]
    t[0].append(t[3])

def p_parametros_funcion(t):
    "parametros_funcion : ID"
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1]
        t[0].append(t[3])

def p_parametro_funcion_skip(t):
    "parametros_funcion : skip"
    t[0] = []


def p_parametro_variable(t):
    """parametro_funcion : ID"""
    t[0] = Parametro(TipoParametro.VARIABLE, t[1])


def p_parametro_entero(t):
    """parametro_funcion : ENTERO"""
    t[0] = Parametro(TipoParametro.ENTERO, t[1])


def p_parametro_decimal(t):
    """parametro_funcion : DECIMAL"""
    t[0] = Parametro(TipoParametro.DECIMAL, t[1])


def p_parametro_cadena(t):
    """parametro_funcion : CADENA"""
    t[0] = Parametro(TipoParametro.CADENA, t[1])


def p_parametro_booleano(t):
    """parametro_funcion : TRUE
    | FALSE"""
    t[0] = Parametro(TipoParametro.BOOLEANO, t[1])


def p_skip(t):
    "skip :"
    pass


def p_parametros_funcion_recibe_lista(t):
    "parametros_funcion_recibe : parametros_funcion_recibe COMA parametro_funcion"
    t[0] = t[1]
    t[0].append(t[3])


def p_parametros_funcion_recibe(t):
    "parametros_funcion_recibe : parametro_funcion"
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1]
        t[0].append(t[3])


def p_parametros_funcion_recibe_skip(t):
    "parametros_funcion_recibe : skip"
    t[0] = []


def p_instrucciones_funcion_lista(t):
    "instrucciones_funcion : instrucciones_funcion instruccion"
    t[1].append(t[2])
    t[0] = t[1]


def p_instrucciones_funcion_instruccion(t):
    "instrucciones_funcion : instruccion"
    t[0] = [t[1]]


def p_instrucciones_funcion_skip(t):
    "instrucciones_funcion : skip"
    t[0] = []


def p_funcion(t):
    "funcion : FUNC ID PARIZQ parametros_funcion PARDER LLAVIZQ instrucciones_funcion LLAVDER PTCOMA"
    t[0] = Funcion(t[2], t[4], t[7])


def p_llamada_funcion(t):
    "llamada_funcion : ID PARIZQ parametros_funcion_recibe PARDER PTCOMA"
    t[0] = LlamadaFuncion(t[1], t[3])


def p_incremento(t):
    "incremento : ID INCREMENTO PTCOMA"
    t[0] = Incremento(t[1])


def p_decremento(t):
    "decremento : ID DECREMENTO PTCOMA"
    t[0] = Decremento(t[1])


def p_funcion_main(t):
    "funcion : FUNC MAIN PARIZQ ARGS PARDER LLAVIZQ instrucciones_funcion LLAVDER PTCOMA"
    t[0] = Funcion("main", [], t[6])


def p_expresion_number(t):
    """expresion_numerica : ENTERO
    | DECIMAL"""
    t[0] = ExpresionNumero(t[1])


def p_expresion_id(t):
    "expresion_numerica   : ID"
    t[0] = ExpresionIdentificador(t[1])

def p_expresion_booleano(t):
    """expresion_numerica : TRUE
    | FALSE"""
    t[0] = ExpresionBooleano(t[1])


def p_expresion_cadena(t):
    "expresion_cadena     : CADENA"
    t[0] = ExpresionDobleComilla(t[1])


def p_expresion_cadena_numerico(t):
    "expresion_cadena     : expresion_numerica"
    t[0] = ExpresionCadenaNumerico(t[1])


def p_expresion_logica(t):
    """expresion_logica : expresion_numerica MAYQUE expresion_numerica
    | expresion_numerica MENQUE expresion_numerica
    | expresion_numerica IGUALQUE expresion_numerica
    | expresion_numerica NIGUALQUE expresion_numerica"""
    if t[2] == ">":
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MAYOR_QUE)
    elif t[2] == "<":
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.MENOR_QUE)
    elif t[2] == "==":
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.IGUAL)
    elif t[2] == "!=":
        t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.DIFERENTE)


def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)


parser = yacc.yacc()


def parse(input):
    return parser.parse(input)
