from graphviz import Digraph
from Instructions import *

index = 0
dot = None

def inc():
    global index
    index += 1
    return index

def GraphAST(AST, consola):
    global dot
    dot = Digraph()
    dot.attr(splines = 'false')
    programIndex = inc()
    dot.node(str(index), 'PROGRAM')
    inc()
    program = AST

    if program.main != None:
        labels = [program.main] + program.labels
        for label in labels:
            AST_Label(programIndex, label)

    try:
        dot.view()
    except:
        consola.setText('ERROR: No fue posible realizar el reporte AST por algun error desconocido.')


                    
def AST_Label(father, label):
    labelIndex = inc()
    dot.node(str(labelIndex), label.name)
    dot.edge(str(father), str(labelIndex))
    
    for instruction in label.instructions:
        if isinstance(instruction, Unset): AST_Unset(labelIndex, instruction)
        elif isinstance(instruction, Set): AST_Set(labelIndex, instruction)
        elif isinstance(instruction, Goto): AST_Goto(labelIndex, instruction)
        elif isinstance(instruction, If): AST_If(labelIndex, instruction)
        elif isinstance(instruction, Print): AST_Print(labelIndex, instruction)
        elif isinstance(instruction, Exit): AST_Exit(labelIndex, instruction)


def AST_Unset(father, instruction):
    unsetIndex = inc()
    dot.node(str(unsetIndex), 'UNSET')
    dot.edge(str(father), str(unsetIndex))
    if isinstance(instruction.register, Register): AST_Register(unsetIndex, instruction.register)
    elif isinstance(instruction.register, Array): AST_Array(unsetIndex, instruction.register)

def AST_Print(father, instruction):
    printIndex = inc()
    dot.node(str(printIndex), 'PRINT')
    dot.edge(str(father), str(printIndex))
    if isinstance(instruction.register, Register): AST_Register(printIndex, instruction.register)
    elif isinstance(instruction.register, Array): AST_Array(printIndex, instruction.register)

def AST_Goto(father, instruction):
    gotoIndex = inc()
    dot.node(str(gotoIndex), 'GOTO')
    dot.edge(str(father), str(gotoIndex))
    son = inc()
    dot.node(str(son), instruction.label)
    dot.edge(str(gotoIndex), str(son))

def AST_If(father, instruction):
    ifIndex = inc()
    dot.node(str(ifIndex), 'IF')
    dot.edge(str(father), str(ifIndex))

    if isinstance(instruction.condition, Register): AST_Register(ifIndex, instruction.condition)
    elif isinstance(instruction.condition, Array): AST_Array(ifIndex, instruction.condition)
    elif isinstance(instruction.condition, AritmeticOperation): AST_Operation(ifIndex, instruction.condition, 'ARITMETIC')
    elif isinstance(instruction.condition, BitxbitOperation): AST_Operation(ifIndex, instruction.condition, 'BIT X BIT')
    elif isinstance(instruction.condition, LogicOperation): AST_Operation(ifIndex, instruction.condition, 'LOGIC')
    elif isinstance(instruction.condition, RelationalOperation): AST_Operation(ifIndex, instruction.condition, 'RELATIONAL')
    AST_Goto(ifIndex, instruction.goto)

def AST_Set(father, instruction):
    setIndex = inc()
    dot.node(str(setIndex), 'SET')
    dot.edge(str(father), str(setIndex))

    son = inc()
    dot.node(str(son), '=')
    dot.edge(str(setIndex), str(son))

    if isinstance(instruction.register, Register): AST_Register(son, instruction.register)
    elif isinstance(instruction.register, Array): AST_Array(son, instruction.register)

    if isinstance(instruction.data, Register): AST_Register(son, instruction.data)
    elif isinstance(instruction.data, Array): AST_Array(son, instruction.data)
    elif isinstance(instruction.data, AritmeticOperation): AST_Operation(son, instruction.data, 'ARITMETIC')
    elif isinstance(instruction.data, BitxbitOperation): AST_Operation(son, instruction.data, 'BIT X BIT')
    elif isinstance(instruction.data, LogicOperation): AST_Operation(son, instruction.data, 'LOGIC')
    elif isinstance(instruction.data, RelationalOperation): AST_Operation(son, instruction.data, 'RELATIONAL')
    elif isinstance(instruction.data, ArrayDeclaration): AST_ArrayDeclaration(son, instruction.data)
    elif isinstance(instruction.data, Read): AST_Read(son, instruction.data)
    elif isinstance(instruction.data, Cast): AST_Cast(son, instruction.data)
    elif isinstance(instruction.data, Primary): AST_Primary(son, instruction.data)
    elif isinstance(instruction.data, Pointer): AST_Pointer(son, instruction.data)

def AST_Register(father, expression):
    registerIndex = inc()
    dot.node(str(registerIndex), 'REGISTER')
    dot.edge(str(father), str(registerIndex))
    regType = ''
    if expression.type_ == REGISTER.TEMPORAL: regType = 'TEMPORAL'
    elif expression.type_ == REGISTER.PARAM: regType = 'PARAMETRO'
    elif expression.type_ == REGISTER.PILA: regType = 'PILA'
    elif expression.type_ == REGISTER.DEVUELTO: regType = 'RETORNO'
    elif expression.type_ == REGISTER.RETURNED: regType = 'RECURSIVIDAD'
    elif expression.type_ == REGISTER.PUNTERO: regType = 'PUNTERO PILA'
    son = inc()
    dot.node(str(son), regType)
    dot.edge(str(registerIndex), str(son))
    son = inc()
    dot.node(str(son), str(expression.position))
    dot.edge(str(registerIndex), str(son))

def AST_Array(father, expression):
    arrayIndex = inc()
    dot.node(str(arrayIndex), 'ARRAY')
    dot.edge(str(father), str(arrayIndex))
    regType = ''
    if expression.type_ == REGISTER.TEMPORAL: regType = 'TEMPORAL'
    elif expression.type_ == REGISTER.PARAM: regType = 'PARAMETRO'
    elif expression.type_ == REGISTER.PILA: regType = 'PILA'
    elif expression.type_ == REGISTER.DEVUELTO: regType = 'RETORNO'
    elif expression.type_ == REGISTER.RETURNED: regType = 'RECURSIVIDAD'
    elif expression.type_ == REGISTER.PUNTERO: regType = 'PUNTERO PILA'
    son = inc()
    dot.node(str(son), regType)
    dot.edge(str(arrayIndex), str(son))
    son = inc()
    dot.node(str(son), str(expression.position))
    dot.edge(str(arrayIndex), str(son))
    count = 1
    for index_ in expression.indexs:
        AST_Position(arrayIndex, index_, 'INDICE '+ str(count))
        count += 1

def AST_Position(father, expression, count):
    positionIndex = inc()
    dot.node(str(positionIndex), count)
    dot.edge(str(father), str(positionIndex))
    if isinstance(expression.index, Register): AST_Register(positionIndex, expression.index)
    elif isinstance(expression.index, Primary): AST_Primary(positionIndex, expression.index)

def AST_Primary(father, expression):
    primaryIndex = inc()
    dot.node(str(primaryIndex), str(expression.data))
    dot.edge(str(father), str(primaryIndex))

def AST_Read(father, instruction):
    readIndex = inc()
    dot.node(str(readIndex), 'READ')
    dot.edge(str(father), str(readIndex))

def AST_ArrayDeclaration(father, instruction):
    arrayDeclarationIndex = inc()
    dot.node(str(arrayDeclarationIndex), 'ARRAY')
    dot.edge(str(father), str(arrayDeclarationIndex))


def AST_Cast(father, instruction):
    castIndex = inc()
    dot.node(str(castIndex), 'CASTING')
    dot.edge(str(father), str(castIndex))
    cast = ''
    if instruction.casting == DATA_TYPE.CHARACTER: cast = 'CHAR'
    elif instruction.casting == DATA_TYPE.INTEGER: cast = 'INT'
    elif instruction.casting == DATA_TYPE.FLOAT: cast = 'FLOAT'
    son = inc()
    dot.node(str(son), cast)
    dot.edge(str(castIndex), str(son))
    if isinstance(instruction.data, Register): AST_Register(castIndex, instruction.data)
    elif isinstance(instruction.data, Array): AST_Array(castIndex, instruction.data)

def AST_Pointer(father, instruction):
    pointerIndex = inc()
    dot.node(str(pointerIndex), 'POINTER')
    dot.edge(str(father), str(pointerIndex))
    if isinstance(instruction.register, Register): AST_Register(pointerIndex, instruction.register)
    elif isinstance(instruction.register, Array): AST_Array(pointerIndex, instruction.register)

def AST_Exit(father, instruction):
    exitIndex = inc()
    dot.node(str(exitIndex), 'EXIT')
    dot.edge(str(father), str(exitIndex))

def AST_Operation(father, expression, tipo):
    operationIndex = inc()
    dot.node(str(operationIndex), tipo)
    dot.edge(str(father), str(operationIndex))
    simbol = ''
    if expression.operator == ARITMETIC_OPERATION.NEG: simbol = '-'
    elif expression.operator == ARITMETIC_OPERATION.SUMA: simbol = '+'
    elif expression.operator == ARITMETIC_OPERATION.RESTA: simbol = '-'
    elif expression.operator == ARITMETIC_OPERATION.MULT: simbol = '*'
    elif expression.operator == ARITMETIC_OPERATION.DIV: simbol = '/'
    elif expression.operator == ARITMETIC_OPERATION.MOD: simbol = '%'
    elif expression.operator == ARITMETIC_OPERATION.ABS: simbol = 'ABSOLUT'
    elif expression.operator == LOGIC_OPERATION.AND: simbol = '&&'
    elif expression.operator == LOGIC_OPERATION.OR: simbol = '||'
    elif expression.operator == LOGIC_OPERATION.NOT: simbol = '!'
    elif expression.operator == RELATIONAL_OPERATION.ES_IGUAL: simbol = '=='
    elif expression.operator == RELATIONAL_OPERATION.NO_IGUAL: simbol = '!='
    elif expression.operator == RELATIONAL_OPERATION.MAYOR: simbol = '>'
    elif expression.operator == RELATIONAL_OPERATION.MENOR: simbol = '<'
    elif expression.operator == RELATIONAL_OPERATION.MAYOR_IGUAL: simbol = '>='
    elif expression.operator == RELATIONAL_OPERATION.MENOR_IGUAL: simbol = '<='    

    son = inc()
    dot.node(str(son), simbol)
    dot.edge(str(operationIndex), str(son))

    if isinstance(expression.expression1, Register): AST_Register(son, expression.expression1)
    elif isinstance(expression.expression1, Array): AST_Array(son, expression.expression1)
    elif isinstance(expression.expression1, Primary): AST_Primary(son, expression.expression1)

    if isinstance(expression.expression2, Register): AST_Register(son, expression.expression2)
    elif isinstance(expression.expression2, Array): AST_Array(son, expression.expression2)
    elif isinstance(expression.expression2, Primary): AST_Primary(son, expression.expression2)
    












    
                            


            
