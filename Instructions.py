from enum import Enum


class ARITMETIC_OPERATION(Enum):
    SUMA = 1
    RESTA = 2
    MULT = 3
    DIV = 4
    MOD = 5
    NEG = 6
    ABS = 7


class LOGIC_OPERATION(Enum):
    NOT = 1
    AND = 2
    OR = 3
    XOR = 4


class RELATIONAL_OPERATION(Enum):
    ES_IGUAL = 1
    NO_IGUAL = 2
    MAYOR_IGUAL = 3
    MENOR_IGUAL = 4
    MAYOR = 5
    MENOR = 6
    

class BITXBIT_OPERATION(Enum):
    BIT_NOT = 1
    BIT_AND = 2
    BIT_OR = 3
    BIT_XOR = 4
    SHIFT_IZQ = 5
    SHIFT_DER = 6


class REGISTER(Enum):
    TEMPORAL = 1
    PARAM = 2
    DEVUELTO = 3
    RETURNED = 4
    PILA = 5
    PUNTERO = 6

class DATA_TYPE(Enum):
    INTEGER = 1
    FLOAT = 2
    CHARACTER = 3



class Program:

    def __init__(self, blocks = []):
        self.main = blocks[0]
        blocks.pop(0)
        self.labels = blocks


class Instruction:

    '''Esto no hace nada'''


class Block:

    '''Esto es un bloque'''


class Expression:

    '''Esto es una expresion'''


class Main(Block):

    def __init__(self, instructions = []):
        self.name = 'main'
        self.instructions = instructions


class Label(Block):

    def __init__(self, name, instructions = []):
        self.name = name
        self.instructions = instructions


class Set(Instruction):

    def __init__(self, register, data):
        self.register = register
        self.data = data

class If(Instruction): 

    def __init__(self, condition, goto):
        self.condition = condition
        self.goto = goto

class ArrayDeclaration(Instruction):

    def __init__(self):
        '''sin parametros'''

class Goto(Instruction):

    def __init__(self, label):
        self.label = label


class Unset(Instruction):

    def __init__(self, register):
        self.register = register


class Print(Instruction):

    def __init__(self, register):
        self.register = register


class Register(Expression):

    def __init__(self, name, type_, position):
        self.name = name
        self.type_ = type_
        self.position = position


class Array(Expression):

    def __init__(self, name, type_, position, indexs = []):
        self.name = name
        self.type_ = type_
        self.position = position
        self.indexs = indexs


class Read(Instruction):

    def __init__(self):

        '''sin parametros'''


class Index(Expression):

    def __init__(self, index):
        self.index = index


class Primary(Expression):

    def __init__(self, type_, data):
        self.type_ = type_
        self.data = data

class Pointer(Instruction):

    def __init__(self, register):
        self.register = register

class Exit(Instruction):

    def __init__(self):
        '''sin parametros'''


class Cast(Instruction):

    def __init__(self, casting, data):
        self.casting = casting
        self.data = data


class AritmeticOperation(Expression):

    def __init__(self, operator, expression1, expression2):
        self.operator = operator
        self.expression1 = expression1
        self.expression2 = expression2


class BitxbitOperation(Expression):

    def __init__(self, operator, expression1, expression2):
        self.operator = operator
        self.expression1 = expression1
        self.expression2 = expression2


class LogicOperation(Expression):

    def __init__(self, operator, expression1, expression2):
        self.operator = operator
        self.expression1 = expression1
        self.expression2 = expression2


class RelationalOperation(Expression):

    def __init__(self, operator, expression1, expression2):
        self.operator = operator
        self.expression1 = expression1
        self.expression2 = expression2



