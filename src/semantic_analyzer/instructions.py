class Instruccion:
    """This is an abstract class"""


class Imprimir(Instruccion):
    """
    Esta clase representa la instrucción imprimir.
    La instrucción imprimir únicamente tiene como parámetro una cadena
    """

    def __init__(self, cad):
        self.cad = cad


class Mientras(Instruccion):
    """
    Esta clase representa la instrucción mientras.
    La instrucción mientras recibe como parámetro una expresión lógica y la lista
    de instrucciones a ejecutar si la expresión lógica es verdadera.
    """

    def __init__(self, expLogica, instrucciones=[]):
        self.expLogica = expLogica
        self.instrucciones = instrucciones


class Asignacion(Instruccion):
    """
    Esta clase representa la instrucción de asignación de variables
    Recibe como parámetro el identificador a asignar y el valor que será asignado.
    """

    def __init__(self, id, expNumerica):
        self.id = id
        self.expNumerica = expNumerica


class If(Instruccion):
    """
    Esta clase representa la instrucción if.
    La instrucción if recibe como parámetro una expresión lógica y la lista
    de instrucciones a ejecutar si la expresión lógica es verdadera.
    """

    def __init__(self, expLogica, instrucciones=[]):
        self.expLogica = expLogica
        self.instrucciones = instrucciones


class IfElse(Instruccion):
    """
    Esta clase representa la instrucción if-else.
    La instrucción if-else recibe como parámetro una expresión lógica y la lista
    de instrucciones a ejecutar si la expresión lógica es verdadera y otro lista de instrucciones
    a ejecutar si la expresión lógica es falsa.
    """

    def __init__(self, expLogica, instrIfVerdadero=[], instrIfFalso=[]):
        self.expLogica = expLogica
        self.instrIfVerdadero = instrIfVerdadero
        self.instrIfFalso = instrIfFalso


class Funcion(Instruccion):
    """
    Esta clase representa la instrucción de una función.
    La instrucción de una función recibe como parámetro el nombre de la función, los parámetros
    de la función y la lista de instrucciones que se ejecutarán al llamar a la función.
    """

    def __init__(self, nombre, parametros, instrucciones):
        self.nombre = nombre
        self.parametros = parametros
        self.instrucciones = instrucciones

    def __str__(self):
        return f"Funcion: {self.nombre}, Parametros: {self.parametros}, Instrucciones: {self.instrucciones}"


class LlamadaFuncion(Instruccion):
    """
    Esta clase representa la instrucción de llamada a una función.
    La instrucción de llamada a una función recibe como parámetro el nombre de la función
    y los parámetros que se le pasarán a la función.
    """

    def __init__(self, nombre, parametros):
        self.nombre = nombre
        self.parametros = parametros


from enum import Enum


class TipoParametro(Enum):
    """
    Esta clase representa los tipos de parámetros que puede tener una función.
    """

    ENTERO = "entero"
    DECIMAL = "decimal"
    CADENA = "cadena"
    BOOLEANO = "booleano"
    VARIABLE = "variable"


class Parametro(Instruccion):
    """
    Esta clase representa un parámetro de una función.
    Un parámetro de una función recibe como parámetro el nombre del parámetro.
    """

    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor


class Incremento(Instruccion):
    """
    Esta clase representa la instrucción de incremento.
    La instrucción de incremento recibe como parámetro el identificador de la variable
    que se incrementará.
    """

    def __init__(self, id):
        self.id = id


class Decremento(Instruccion):
    """
    Esta clase representa la instrucción de decremento.
    La instrucción de decremento recibe como parámetro el identificador de la variable
    que se decrementará.
    """

    def __init__(self, id):
        self.id = id


class FuncionMain(Instruccion):
    """
    Esta clase representa la instrucción de la función main.
    La instrucción de la función main recibe como parámetro la lista de instrucciones
    que se ejecutarán al llamar a la función main.
    """

    def __init__(self, instrucciones=[]):
        self.instrucciones = instrucciones
