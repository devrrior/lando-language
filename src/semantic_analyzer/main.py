import semantic_analyzer.tables as TS
from semantic_analyzer.grammar import parser as g
from semantic_analyzer.expresions import *
from semantic_analyzer.instructions import *

output_list = []
ts_global = TS.SymbolTable()
tf_global = TS.FunctionTable()


def procesar_imprimir(instr, ts):
    return resolver_cadena(instr.cad, ts)


def procesar_asignacion(instr, ts):
    val = resolver_expresion_aritmetica(instr.expNumerica, ts)
    simbolo = TS.Symbol(instr.id, val)
    ts.agregar(simbolo)


def procesar_mientras(instr, ts, tf):
    while resolver_expreision_logica(instr.expLogica, ts):
        ts_local = TS.SymbolTable(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local, tf)


def procesar_if(instr, ts, tf):
    val = resolver_expreision_logica(instr.expLogica, ts)
    if val:
        ts_local = TS.SymbolTable(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local, tf)


def resolver_cadena(expCad, ts):
    if isinstance(expCad, ExpresionDobleComilla):
        return expCad.val
    elif isinstance(expCad, ExpresionCadenaNumerico):
        return str(resolver_expresion_aritmetica(expCad.exp, ts))
    else:
        print("Error: Expresión cadena no válida")


def resolver_expreision_logica(expLog, ts):
    exp1 = resolver_expresion_aritmetica(expLog.exp1, ts)
    exp2 = resolver_expresion_aritmetica(expLog.exp2, ts)

    if expLog.operador == OPERACION_LOGICA.MAYOR_QUE:
        if isinstance(exp1, str) or isinstance(exp2, str):
            raise Exception("Error: tipos de datos no válidos")

        return exp1 > exp2
    if expLog.operador == OPERACION_LOGICA.MENOR_QUE:
        if isinstance(exp1, str) or isinstance(exp2, str):
            raise Exception("Error: tipos de datos no válidos")

        return exp1 < exp2
    if expLog.operador == OPERACION_LOGICA.IGUAL:
        return exp1 == exp2
    if expLog.operador == OPERACION_LOGICA.DIFERENTE:
        return exp1 != exp2


def resolver_expresion_aritmetica(expNum, ts):
    if isinstance(expNum, ExpresionNumero):
        return expNum.val
    elif isinstance(expNum, ExpresionIdentificador):
        return ts.obtener(expNum.id).valor


def procesar_funcion(instr, tf):
    tf.agregar(instr)


def procesar_llamada_funcion(instr, ts, tf):

    funcion = tf.obtener(instr.nombre)
    ts_local = TS.SymbolTable(ts.simbolos)

    # verificar si el numero de parametros es igual al numero de argumentos
    if len(instr.parametros) != len(funcion.parametros):
        raise Exception(
            "Error: número de argumentos no coincide con el número de parámetros"
        )

    for parametro_definido, parametro_dado in zip(funcion.parametros, instr.parametros):
        if parametro_dado.tipo != TipoParametro.VARIABLE:
            simbolo = TS.Symbol(parametro_definido, parametro_dado.valor)
            ts_local.agregar(simbolo)

    procesar_instrucciones(funcion.instrucciones, ts_local, tf)

def procesar_incremento(instr, ts):
    # checar si existe la variable
    simbolo = ts.obtener(instr.id)

    if simbolo is None:
        raise Exception(f"Error: variable {instr.id} no definida")

    # checar si la variable es de tipo entero
    if not isinstance(simbolo.valor, int):
        raise Exception(f"Error: variable {instr.id} no es de tipo entero")

    simbolo.valor += 1

def procesar_decremento(instr, ts):
    # checar si existe la variable
    simbolo = ts.obtener(instr.id)

    if simbolo is None:
        raise Exception(f"Error: variable {instr.id} no definida")

    # checar si la variable es de tipo entero
    if not isinstance(simbolo.valor, int):
        raise Exception(f"Error: variable {instr.id} no es de tipo entero")

    simbolo.valor -= 1

def procesar_funcion_main(instr, ts, tf):
    ts_local = TS.SymbolTable(ts.simbolos)
    procesar_instrucciones(instr.instrucciones, ts_local, tf)


def procesar_instrucciones(instrucciones, ts, tf):
    for instr in instrucciones:
        if isinstance(instr, Imprimir):
            output_list.append(procesar_imprimir(instr, ts))
        elif isinstance(instr, Asignacion):
            procesar_asignacion(instr, ts)
        elif isinstance(instr, Mientras):
            procesar_mientras(instr, ts, tf)
        elif isinstance(instr, If):
            procesar_if(instr, ts, tf)
        elif isinstance(instr, Funcion):
            procesar_funcion(instr, tf)
        elif isinstance(instr, LlamadaFuncion):
            procesar_llamada_funcion(instr, ts, tf)
        elif isinstance(instr, Incremento):
            procesar_incremento(instr, ts)
        elif isinstance(instr, Decremento):
            procesar_decremento(instr, ts)
        elif isinstance(instr, FuncionMain):
            procesar_funcion_main(instr, ts, tf)
        else:
            print("Error: instrucción no válida")


def semantic_analyzer(input):
    output_list.clear()
    ts_global.clear()
    tf_global.clear()
    instrucciones = g.parse(input)

    procesar_instrucciones(instrucciones, ts_global, tf_global)
    return output_list
