from enum import Enum
from Instructions import REGISTER

class TIPO_RELATIVO(Enum):
    PARAMETRO = 1
    TEMPORAL = 2
    DEVUELTO = 3
    RETORNADO = 4
    PILA = 5
    PUNTERO = 6
    LABEL = 7
    ARREGLO = 8


class TIPO_ESPECIFICO(Enum):
    ENTERO = 1
    DECIMAL = 2
    CARACTER = 3
    CADENA = 4
    ARRAY = 5
    PUNTERO = 6
    FUNCION = 7
    PROCEDIMIENTO = 8
    CONTROL = 9
    MAIN = 10

class Simbolo():

    def __init__(self, nombre, identificador, tipo_relativo, tipo_especifico, valor):
        self.nombre = nombre
        self.identificador = identificador
        self.tipo_relativo = tipo_relativo
        self.tipo_especifico = tipo_especifico
        self.valor = valor


class TablaSimbolos():

    def __init__(self):
        self.simbolos = {}

    def agregar(self, nombre, identificador, tipo_relativo, tipo_especifico, valor):
        simbolo = Simbolo(nombre, identificador, tipo_relativo, tipo_especifico, valor)
        self.simbolos[nombre] = simbolo
    
    def obtener(self, nombre):
        if nombre in self.simbolos:
            if self.simbolos[nombre].tipo_especifico == TIPO_ESPECIFICO.PUNTERO:
                return self.obtener(self.simbolos[nombre].valor)
            else:
                return self.simbolos[nombre]
        else:
            nombreDes = nombre.split('#')
            if nombreDes[0] in self.simbolos:
                if self.simbolos[nombreDes[0]].tipo_especifico == TIPO_ESPECIFICO.CADENA:
                    if nombreDes[1].isnumeric():
                        if int(nombreDes[1])<len(self.simbolos[nombreDes[0]].valor):
                            ret = self.simbolos[nombreDes[0]]
                            ret.valor = self.simbolos[nombreDes[0]].valor[int(nombreDes[1])]
                            return ret
        return None

    def eliminar(self, nombre):
        if nombre in self.simbolos:
            self.simbolos[nombre] = None
            return True
        return False
            
    def asignarLabelType(self, nombre, tipo):
        self.simbolos[nombre].tipo_especifico = tipo
    
    def graph(self, consola):
        simbo = ''
        for simb in self.simbolos:
            simbo += '--------------------------------------------------------------------------------------------------------------------------\n'
            if self.simbolos[simb].tipo_relativo == TIPO_RELATIVO.ARREGLO:
                simbo += 'Nombre: ' + str(self.simbolos[simb].nombre).replace('#', ' -> ') + '\n'
            else:
                simbo += 'Nombre: ' + str(self.simbolos[simb].nombre) + '\n'
            simbo += 'Tipo registro: ' + str(self.simbolos[simb].tipo_relativo) + '\n'
            simbo += 'Tipo almacenado: ' + str(self.simbolos[simb].tipo_especifico) + '\n'
            if self.simbolos[simb].tipo_especifico == TIPO_ESPECIFICO.ARRAY:
                simbo += 'Valor: Arreglo \n'
            elif self.simbolos[simb].tipo_relativo == TIPO_RELATIVO.LABEL:
                simbo += 'Valor: Instrucciones\n'
            else:
                simbo += 'Valor: ' + str(self.simbolos[simb].valor) + '\n'
            simbo += '--------------------------------------------------------------------------------------------------------------------------\n'

        consola.setText(simbo)