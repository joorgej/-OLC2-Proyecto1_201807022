from PyQt5 import QtWidgets
from PyQt5 import QtCore
from Instructions import * 
from TablaSimbolos import *


ts = TablaSimbolos()
flag = True 
errores = ''

def parar():
    global flag
    flag = False

def continuar():
    global flag 
    flag = True

def addError(texto, consola):
    global errores
    prints = consola.toPlainText()[len(errores):]
    errores += texto
    consola.setText(errores + prints)

def interpretar(AST, consola, salidaSimbolos):
    global ts
    ts = None
    ts = TablaSimbolos()
    global errores
    errores = consola.toPlainText()

    if AST.main != None: 
        ts.agregar(AST.main.name, AST.main.name, TIPO_RELATIVO.LABEL, TIPO_ESPECIFICO.MAIN, AST.main.instructions)

    for label in AST.labels:
        ts.agregar(label.name, label.name, TIPO_RELATIVO.LABEL, None,  label.instructions)
    
    flag1 = False
    flag2 = False
    labeles = [AST.main] + AST.labels
    for label in labeles:
        for instruction in label.instructions:
            if isinstance(instruction, Set):
                if instruction.register.type_ == REGISTER.PARAM:
                    flag1 = True
            elif isinstance(instruction, Goto):
                goto = ts.obtener(instruction.label)
                if goto != None:
                    if goto.tipo_especifico == None:
                        for instr in goto.valor:
                            if isinstance(instr, Set):
                                if instr.register.type_ == REGISTER.DEVUELTO:
                                    flag2 = True

                        if flag2:
                            ts.asignarLabelType(instruction.label, TIPO_ESPECIFICO.FUNCION)
                        elif flag1:
                            ts.asignarLabelType(instruction.label, TIPO_ESPECIFICO.PROCEDIMIENTO)
                        else:
                            ts.asignarLabelType(instruction.label, TIPO_ESPECIFICO.CONTROL)

                        flag1 = False
                        flag2 = False
            elif isinstance(instruction, If):
                gotoIf = instruction.goto
                goto = ts.obtener(gotoIf.label)
                if goto != None:
                    if goto.tipo_especifico == None:
                        for instr in goto.valor:
                            if isinstance(instr, Set):
                                if instr.register.type_ == REGISTER.DEVUELTO:
                                    flag2 = True

                        if flag2:
                            ts.asignarLabelType(gotoIf.label, TIPO_ESPECIFICO.FUNCION)
                        elif flag1:
                            ts.asignarLabelType(gotoIf.label, TIPO_ESPECIFICO.PROCEDIMIENTO)
                        else:
                            ts.asignarLabelType(gotoIf.label, TIPO_ESPECIFICO.CONTROL)

                        flag1 = False
                        flag2 = False
    


    i_main(AST.main, consola)
    ts.graph(salidaSimbolos)
    


def i_main(main, consola):
    for instruction in main.instructions:
        if isinstance(instruction, Unset): i_unset(instruction, consola)
        elif isinstance(instruction, Set): i_set(instruction, consola)
        elif isinstance(instruction, Goto): 
            gotoL = i_goto(instruction, consola)
            if gotoL != None:
                gotoL = i_label(gotoL, consola)
                print(gotoL)
                while True:
                    if gotoL == None:
                        break
                    gotoL = i_label(gotoL, consola)
            return
        elif isinstance(instruction, If): 
            iflag = i_if(instruction, consola)
            if iflag[0] == True:
                gotoL = i_goto(instruction, consola)
                if gotoL != None:
                    gotoL = i_label(gotoL, consola)
                    print(gotoL)
                    while True:
                        if gotoL == None:
                            break
                        gotoL = i_label(gotoL, consola)
                return
        elif isinstance(instruction, Print): i_print(instruction, consola)
        elif isinstance(instruction, Exit): 
            parar() 
            return

def i_label(instructions, consola):
    for instruction in instructions:
        if isinstance(instruction, Unset): i_unset(instruction, consola)
        elif isinstance(instruction, Set): i_set(instruction, consola)
        elif isinstance(instruction, Goto): 
            gotoL = i_goto(instruction, consola)
            if gotoL != None:
                return gotoL
            return None
            
        elif isinstance(instruction, If): 
            iflag = i_if(instruction, consola)
            if iflag[0] == True:
                gotoL = i_goto(iflag[1], consola)
                if gotoL != None:
                    return gotoL
                
        elif isinstance(instruction, Print): i_print(instruction, consola)
        elif isinstance(instruction, Exit): 
            parar()
            return
        
    return None

def i_unset(instruction, consola):
    if not ts.eliminar(instruction.register.name):
        addError('ERROR SEMANTICO: No es posible eliminar el registro "'+str(instruction.register.name)+'", porque no ha sido declarado. \n', consola)

def i_print(instruction, consola):
    printed = ''
    if isinstance(instruction.register, Register):
        printed = ts.obtener(instruction.register.name)
    elif isinstance(instruction.register, Array):
        printed = ts.obtener(get_array_name(instruction.register, consola))

    if printed == None:
        addError('ERROR SEMANTICO: Se intento imprimir un registro no declarado. \n', consola)
    else:
        printed = printed.valor
        consola.setText(consola.toPlainText() + '>> ' +str(printed) + '\n')
        
    

def i_goto(instruction, consola):
    goto = ts.obtener(instruction.label)
    if goto != None:
        return goto.valor
    else: 
        addError('ERROR SEMANTICO: El label que se intentaba ejecutar no a sido declarado.\n', consola)
        return None

def i_if(instruction, consola):
    valor = [None, None]

    if isinstance(instruction.condition, Register) or isinstance(instruction.condition, Array) or isinstance(instruction.condition, Primary):
        tempo = i_get_data(instruction.condition, consola)
        valor = tempo[0]
    elif isinstance(instruction.condition, AritmeticOperation):
        tempo = i_aritmetic_operation(instruction.condition, consola)
        valor = tempo[0]
    elif isinstance(instruction.condition, RelationalOperation):
        tempo = i_relational_operation(instruction.condition, consola)
        valor = tempo[0]
    elif isinstance(instruction.condition, LogicOperation):
        tempo = i_logic_operation(instruction.condition, consola)
        valor = tempo[0]
    elif isinstance(instruction.condition, BitxbitOperation):
        tempo = i_bitxbit_operation(instruction.condition, consola)
        valor = tempo[0]
    elif isinstance(instruction.condition, Cast):
        tempo = i_cast(instruction.condition, consola)
        valor = tempo[0]

    if valor == 0:
        return [False, None]
    elif valor == 1:
        return [True, instruction.goto]
    else:
        addError('ERROR SEMANTICO: El valor obtenido en la condicion de la instruccion if, no es un valor valido. \n', consola)
        return [False, None]


def i_set(instruction, consola):

    nombre = None
    identificador = None
    tipo_relativo = None
    tipo_especifico = None
    valor = None

    if isinstance(instruction.register, Register):
        nombre = instruction.register.name
        identificador = instruction.register.position
        if instruction.register.type_ == REGISTER.TEMPORAL: tipo_relativo = TIPO_RELATIVO.TEMPORAL
        elif instruction.register.type_ == REGISTER.PARAM: tipo_relativo = TIPO_RELATIVO.PARAMETRO
        elif instruction.register.type_ == REGISTER.DEVUELTO: tipo_relativo = TIPO_RELATIVO.DEVUELTO
        elif instruction.register.type_ == REGISTER.RETURNED: tipo_relativo = TIPO_RELATIVO.RETORNADO
        elif instruction.register.type_ == REGISTER.PILA: tipo_relativo = TIPO_RELATIVO.PILA
        elif instruction.register.type_ == REGISTER.PUNTERO: tipo_relativo = TIPO_RELATIVO.PUNTERO

    elif isinstance(instruction.register, Array):
        nombre = get_array_name(instruction.register, consola) 
        identificador = instruction.register.position
        tipo_relativo = TIPO_RELATIVO.ARREGLO


    if isinstance(instruction.data, Register) or isinstance(instruction.data, Array) or isinstance(instruction.data, Primary):
        tempo = i_get_data(instruction.data, consola)
        valor = tempo[0]
        tipo_especifico = tempo[1]
    elif isinstance(instruction.data, AritmeticOperation):
        tempo = i_aritmetic_operation(instruction.data, consola)
        valor = tempo[0]
        tipo_especifico = tempo[1]
    elif isinstance(instruction.data, RelationalOperation):
        tempo = i_relational_operation(instruction.data, consola)
        valor = tempo[0]
        tipo_especifico = tempo[1]
    elif isinstance(instruction.data, LogicOperation):
        tempo = i_logic_operation(instruction.data, consola)
        valor = tempo[0]
        tipo_especifico = tempo[1]
    elif isinstance(instruction.data, BitxbitOperation):
        tempo = i_bitxbit_operation(instruction.data, consola)
        valor = tempo[0]
        tipo_especifico = tempo[1]
    elif isinstance(instruction.data, Cast):
        tempo = i_cast(instruction.data, consola)
        valor = tempo[0]
        tipo_especifico = tempo[1]
    elif isinstance(instruction.data, ArrayDeclaration):
        valor = 'Arreglo'
        tipo_especifico = TIPO_ESPECIFICO.ARRAY
    elif isinstance(instruction.data, Read):
        tempo = i_read(consola)
        valor = tempo[0]
        tipo_especifico = tempo[1]
    elif isinstance(instruction.data, Pointer):
        valor = i_puntero(instruction.data, consola)
        tipo_especifico = TIPO_ESPECIFICO.PUNTERO    
    
    if valor == None:
        addError('ERROR SINTACTICO: No se encontro el valor que se deseaba agregar el registro '+nombre+'\n', consola)
    else:
        ts.agregar(nombre, identificador, tipo_relativo, tipo_especifico, valor)


def i_read(consola):
    texto, ok = QtWidgets.QInputDialog().getText(None, 'Read', 'Cadena a registrar: ', QtWidgets.QLineEdit.Normal,
                                        QtCore.QDir().home().dirName())
    if ok and texto:
        return [str(texto), TIPO_ESPECIFICO.CADENA]
    return [None, TIPO_ESPECIFICO.CADENA]

def i_puntero(instruction, consola):
    if isinstance(instruction.register, Register):
        return instruction.register.name

    elif isinstance(instruction.register, Array):
        return get_array_name(instruction.register, consola) 
    
    addError('ERROR SINTACTICO: El registro al que se intenta apuntar no es valido', consola)
    return None


def i_get_data(expression, consola):

    data = [None, None]

    if isinstance(expression, Register):
        temp = ts.obtener(expression.name)
        if temp != None:
            data = [temp.valor, temp.tipo_especifico]
        else: 
            addError('ERROR SEMANTICO: La variable "'+expression.name+'", no a sido declarada.\n', consola)
    elif isinstance(expression, Array):
        temp = ts.obtener(get_array_name(expression, consola))
        if temp != None:
            data = [temp.valor, temp.tipo_especifico]
        else: 
            addError('ERROR SEMANTICO: La posicion especificada del arreglo "'+expression.name+'", no a sido declarada.\n', consola)
    elif isinstance(expression, Primary):
        tipo = ''
        if expression.type_ == 'ENTERO': tipo = TIPO_ESPECIFICO.ENTERO
        elif expression.type_ == 'DECIMAL': tipo = TIPO_ESPECIFICO.DECIMAL
        elif expression.type_ == 'CADENA': tipo = TIPO_ESPECIFICO.CADENA
        elif expression.type_ == 'CARACTER': tipo = TIPO_ESPECIFICO.CARACTER
        data = [expression.data, tipo]
    return data
    

def i_aritmetic_operation(expression, consola):
    
    dato1 = i_get_data(expression.expression1, consola)
    dato2 = i_get_data(expression.expression2, consola)
    
    if expression.operator == ARITMETIC_OPERATION.SUMA:
        if (dato1[1] == TIPO_ESPECIFICO.CADENA or dato1[1] == TIPO_ESPECIFICO.CARACTER) and (dato2[1] == TIPO_ESPECIFICO.CADENA or dato1[1] == TIPO_ESPECIFICO.CARACTER):
            return [dato1[0]+dato2[0], TIPO_ESPECIFICO.CADENA]
        elif dato1[1] == TIPO_ESPECIFICO.ENTERO and dato2[1] == TIPO_ESPECIFICO.ENTERO:
            return [dato1[0]+dato2[0], TIPO_ESPECIFICO.ENTERO]
        elif (dato1[1] == TIPO_ESPECIFICO.DECIMAL or dato1[1] == TIPO_ESPECIFICO.ENTERO) and (dato2[1] == TIPO_ESPECIFICO.DECIMAL or dato2[1] == TIPO_ESPECIFICO.ENTERO):
            return [dato1[0]+dato2[0], TIPO_ESPECIFICO.DECIMAL]

    elif expression.operator == ARITMETIC_OPERATION.RESTA:
        if dato1[1] == TIPO_ESPECIFICO.ENTERO and dato2[1] == TIPO_ESPECIFICO.ENTERO:
            return [int(dato1[0]-dato2[0]), TIPO_ESPECIFICO.ENTERO]
        elif (dato1[1] == TIPO_ESPECIFICO.DECIMAL or dato1[1] == TIPO_ESPECIFICO.ENTERO) and (dato2[1] == TIPO_ESPECIFICO.DECIMAL or dato2[1] == TIPO_ESPECIFICO.ENTERO):
            return [float(dato1[0]-dato2[0]), TIPO_ESPECIFICO.DECIMAL]

    elif expression.operator == ARITMETIC_OPERATION.MULT:
        if dato1[1] == TIPO_ESPECIFICO.ENTERO and dato2[1] == TIPO_ESPECIFICO.ENTERO:
            return [dato1[0]*dato2[0], TIPO_ESPECIFICO.ENTERO]
        elif (dato1[1] == TIPO_ESPECIFICO.DECIMAL or dato1[1] == TIPO_ESPECIFICO.ENTERO) and (dato2[1] == TIPO_ESPECIFICO.DECIMAL or dato2[1] == TIPO_ESPECIFICO.ENTERO):
            return [dato1[0]*dato2[0], TIPO_ESPECIFICO.DECIMAL]

    elif expression.operator == ARITMETIC_OPERATION.DIV:
        if dato1[1] == TIPO_ESPECIFICO.ENTERO and dato2[1] == TIPO_ESPECIFICO.ENTERO:
            return [dato1[0]/dato2[0], TIPO_ESPECIFICO.ENTERO]
        elif (dato1[1] == TIPO_ESPECIFICO.DECIMAL or dato1[1] == TIPO_ESPECIFICO.ENTERO) and (dato2[1] == TIPO_ESPECIFICO.DECIMAL or dato2[1] == TIPO_ESPECIFICO.ENTERO):
            return [dato1[0]/dato2[0], TIPO_ESPECIFICO.DECIMAL]

    elif expression.operator == ARITMETIC_OPERATION.MOD:
        if dato1[1] == TIPO_ESPECIFICO.ENTERO and dato2[1] == TIPO_ESPECIFICO.ENTERO:
            return [dato1[0]%dato2[0], TIPO_ESPECIFICO.ENTERO]
        elif (dato1[1] == TIPO_ESPECIFICO.DECIMAL or dato1[1] == TIPO_ESPECIFICO.ENTERO) and (dato2[1] == TIPO_ESPECIFICO.DECIMAL or dato2[1] == TIPO_ESPECIFICO.ENTERO):
            return [dato1[0]%dato2[0], TIPO_ESPECIFICO.DECIMAL]
    elif expression.operator == ARITMETIC_OPERATION.ABS:
        if dato1[1] == TIPO_ESPECIFICO.ENTERO or dato1[1] == TIPO_ESPECIFICO.DECIMAL:
            if dato1[0] >= 0:
                return [dato1[0], dato1[1]]
            else:
                return [dato1[0] + -1, dato1[1]]
    elif expression.operator == ARITMETIC_OPERATION.NEG:
        if dato1[1] == TIPO_ESPECIFICO.ENTERO or dato1[1] == TIPO_ESPECIFICO.DECIMAL:
            return [dato1[0] * -1, dato1[1]]

    addError('ERROR SEMANTICO: Los tipos de dato que se intentaron operar no son compatibles. \n', consola)
    return [None, None]

def i_relational_operation(expression, consola):

    dato1 = i_get_data(expression.expression1, consola)
    dato2 = i_get_data(expression.expression2, consola)
    if expression.operator == RELATIONAL_OPERATION.ES_IGUAL:
        if dato1[0] == dato2[0]:
            return [1, TIPO_ESPECIFICO.ENTERO]
        else:
            return [0, TIPO_ESPECIFICO.ENTERO]
    elif expression.operator == RELATIONAL_OPERATION.NO_IGUAL:
        if dato1[0] != dato2[0]:
            return [1, TIPO_ESPECIFICO.ENTERO]
        else:
            return [0, TIPO_ESPECIFICO.ENTERO]
    elif expression.operator == RELATIONAL_OPERATION.MAYOR_IGUAL:
        try:
            if dato1[0] >= dato2[0]:
                return [1, TIPO_ESPECIFICO.ENTERO]
            else:
                return [0, TIPO_ESPECIFICO.ENTERO]
        except:
            'nada'
    elif expression.operator == RELATIONAL_OPERATION.MENOR_IGUAL:
        try:
            if dato1[0] <= dato2[0]:
                return [1, TIPO_ESPECIFICO.ENTERO]
            else:
                return [0, TIPO_ESPECIFICO.ENTERO]
        except:
            'nada'
    elif expression.operator == RELATIONAL_OPERATION.MAYOR:
        try:
            if dato1[0] > dato2[0]:
                return [1, TIPO_ESPECIFICO.ENTERO]
            else:
                return [0, TIPO_ESPECIFICO.ENTERO]
        except:
            'nada'
    elif expression.operator == RELATIONAL_OPERATION.MENOR:
        try:
            if dato1[0] < dato2[0]:
                return [1, TIPO_ESPECIFICO.ENTERO]
            else:
                return [0, TIPO_ESPECIFICO.ENTERO]
        except:
            'nada'

    addError('ERROR SEMANTICO: Los tipos de dato que se intentaron operar no son compatibles. \n', consola)
    return[None, None]

def i_logic_operation(expression, consola):

    dato1 = i_get_data(expression.expression1, consola)
    dato2 = i_get_data(expression.expression2, consola)

    if (dato1[0]==1 or dato1[0]==0) and (dato2[0]==1 or dato2[0]==0):
        if expression.operator == LOGIC_OPERATION.AND:
            if dato1[0]==1 and dato2[0]==1:
                return [1, TIPO_ESPECIFICO.ENTERO]
            else:
                return [0, TIPO_ESPECIFICO.ENTERO]
        elif expression.operator == LOGIC_OPERATION.OR:
            if dato1[0]==1 or dato2[0]==1:
                return [1, TIPO_ESPECIFICO.ENTERO]
            else:
                return [0, TIPO_ESPECIFICO.ENTERO]
        elif expression.operator == LOGIC_OPERATION.XOR:
            if (dato1[0]==1 and dato2[0]==0) or (dato1[0]==0 and dato2[0]==1):
                return [1, TIPO_ESPECIFICO.ENTERO]
            else:
                return [0, TIPO_ESPECIFICO.ENTERO]
        elif expression.operator == LOGIC_OPERATION.NOT:
            if dato1[0]==0:
                return [1, TIPO_ESPECIFICO.ENTERO]
            else:
                return [0, TIPO_ESPECIFICO.ENTERO]
    else:
        addError('ERROR SEMANTICO: Los tipos de dato que se intentaron operar no son compatibles. \n', consola)
        return[None, None]

def i_bitxbit_operation(expression, consola):

    dato1 = i_get_data(expression.expression1, consola)
    dato2 = i_get_data(expression.expression2, consola)
    if expression.operator == BITXBIT_OPERATION.BIT_NOT:
        if dato1[1] == TIPO_ESPECIFICO.ENTERO:
            return [ ~int(dato1[0]), TIPO_ESPECIFICO.ENTERO]
    elif expression.operator == BITXBIT_OPERATION.BIT_AND:
        if dato1[1] == TIPO_ESPECIFICO.ENTERO and dato2[1] == TIPO_ESPECIFICO.ENTERO:
            return [dato1[0] & dato2[0], TIPO_ESPECIFICO.ENTERO]
    elif expression.operator == BITXBIT_OPERATION.BIT_OR:
        if dato1[1] == TIPO_ESPECIFICO.ENTERO and dato2[1] == TIPO_ESPECIFICO.ENTERO:
            return [dato1[0] | dato2[0], TIPO_ESPECIFICO.ENTERO]
    elif expression.operator == BITXBIT_OPERATION.BIT_XOR:
        if dato1[1] == TIPO_ESPECIFICO.ENTERO and dato2[1] == TIPO_ESPECIFICO.ENTERO:
            return [dato1[0] ^ dato2[0], TIPO_ESPECIFICO.ENTERO]
    elif expression.operator == BITXBIT_OPERATION.SHIFT_IZQ:
        if dato1[1] == TIPO_ESPECIFICO.ENTERO and dato2[1] == TIPO_ESPECIFICO.ENTERO:
            return [dato1[0] << dato2[0], TIPO_ESPECIFICO.ENTERO]
    elif expression.operator == BITXBIT_OPERATION.SHIFT_DER:
        if dato1[1] == TIPO_ESPECIFICO.ENTERO and dato2[1] == TIPO_ESPECIFICO.ENTERO:
            return [dato1[0] >> dato2[0], TIPO_ESPECIFICO.ENTERO]
    
    addError('ERROR SEMANTICO: Los tipos de dato que se intentaron operar no son compatibles. \n', consola)
    return[None, None]

def i_cast(expression, consola):

    dato = i_get_data(expression.data, consola)

    if expression.casting == DATA_TYPE.INTEGER:
        if dato[1] == TIPO_ESPECIFICO.DECIMAL:
            return [int(dato[0]),TIPO_ESPECIFICO.ENTERO]
        elif dato[1] == TIPO_ESPECIFICO.CARACTER:
            return [ord(dato[0]), TIPO_ESPECIFICO.ENTERO]
        elif dato[1] == TIPO_ESPECIFICO.CADENA:
            return [ord(dato[0][0]), TIPO_ESPECIFICO.ENTERO]
        elif dato[1] == TIPO_ESPECIFICO.ARRAY:
            return [0, TIPO_ESPECIFICO.ENTERO]

    elif expression.casting == DATA_TYPE.FLOAT:
        if dato[1] == TIPO_ESPECIFICO.ENTERO:
            return [float(dato[0]),TIPO_ESPECIFICO.DECIMAL]
        elif dato[1] == TIPO_ESPECIFICO.CARACTER:
            return [float(ord(dato[0])), TIPO_ESPECIFICO.DECIMAL]
        elif dato[1] == TIPO_ESPECIFICO.CADENA:
            return [float(ord(dato[0][0])), TIPO_ESPECIFICO.DECIMAL]
        elif dato[1] == TIPO_ESPECIFICO.ARRAY:
            return [0, TIPO_ESPECIFICO.DECIMAL]

    elif expression.casting == DATA_TYPE.CHARACTER:
        if dato[1] == TIPO_ESPECIFICO.ENTERO or dato[1] == TIPO_ESPECIFICO.DECIMAL:
            if dato[0] <= 255:
                return [chr(int(dato[0])),TIPO_ESPECIFICO.CARACTER]
            else:
                return [chr(int(dato[0]%255)), TIPO_ESPECIFICO.CARACTER]
        elif dato[1] == TIPO_ESPECIFICO.CADENA:
            return [dato[0][0], TIPO_ESPECIFICO.CARACTER]
        elif dato[1] == TIPO_ESPECIFICO.ARRAY:
            return [0, TIPO_ESPECIFICO.CARACTER]

    addError('ERROR SEMANTICO: El casteo entre los tipos indicados nos es soportado por el lenguaje. \n', consola)
    return[None, None]

def get_array_name(array, consola):
    name = array.name
    for index in array.indexs:
        name += '#'
        name += str(i_get_data(index.index, consola)[0]) 
    return name 