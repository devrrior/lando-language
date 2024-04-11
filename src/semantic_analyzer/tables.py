from enum import Enum


class Symbol:
    "Esta clase representa un simbolo dentro de nuestra tabla de simbolos"

    def __init__(self, id, valor):
        self.id = id
        self.valor = valor


class SymbolTable:
    "Esta clase representa la tabla de simbolos"

    def __init__(self, simbolos={}):
        self.simbolos = simbolos

    def agregar(self, simbolo):
        self.simbolos[simbolo.id] = simbolo

    def obtener(self, id):
        if not id in self.simbolos:
            raise Exception(f"Error: variable {id} no definida.")

        return self.simbolos[id]

    def clear(self):
        self.simbolos.clear()


class FunctionTable:
    "Esta clase representa la tabla de funciones"

    def __init__(self, funciones={}):
        self.funciones = funciones

    def agregar(self, funcion):
        self.funciones[funcion.nombre] = funcion

    def obtener(self, id):
        if not id in self.funciones:
            raise Exception(f"Error: función {id} no definida.")

        return self.funciones[id]

    def clear(self):
        self.funciones.clear()
