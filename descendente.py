import ply.lex as lex
import ply.lex as lex
import ply.yacc as yacc
import re
from Instructions import *
from graphviz import Graph
from AST_Graph import *
from Interprete import *



errores = ''
reservadas = {
    'xor' : 'XOR',
    'abs' : 'ABS',
    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'unset' : 'UNSET',
    'print' : 'PRINT',
    'read' : 'READ',
    'exit' : 'EXIT',
    'goto' : 'GOTO',
    'main' : 'MAIN',
    'array' : 'ARRAY',
    'if' : 'IF'
}

tokens = (
    'ES_IGUAL',
    'NO_IGUAL',
    'MAYOR_IGUAL',
    'MENOR_IGUAL',
    'SHIFT_DER',
    'SHIFT_IZQ',
    'MAYOR',
    'MENOR',
    'XOR_BIT',
    'OR',
    'AND',
    'NOT_BIT',
    'AND_BIT',
    'OR_BIT',
    'NOT',
    'SUMA',
    'RESTA',
    'MULT',
    'DIV',
    'MOD',
    'PAR_IZQ',
    'PAR_DER',
    'COR_IZQ',
    'COR_DER',
    'IGUAL',
    'DOS_PUNTOS',
    'PUNTO_COMA',
    'XOR',
    'ABS',
    'INT',
    'FLOAT',
    'CHAR',
    'UNSET',
    'PRINT',
    'READ',
    'EXIT',
    'GOTO',
    'MAIN',
    'ARRAY',
    'LABEL',
    'COMENTARIO',
    'ENTERO',
    'DECIMAL',
    'CARACTER',
    'CADENA',
    'TEMPORAL',
    'PARAMETRO',
    'DEVUELTO',
    'RETORNO',
    'PILA',
    'PUNTERO',
    'IF'
)

t_ignore = ' \t'
t_ES_IGUAL = r'[=][=]'
t_NO_IGUAL = r'[!][=]'
t_MAYOR_IGUAL = r'[>][=]'
t_MENOR_IGUAL = r'[<][=]'
t_SHIFT_DER = r'[>][>]'
t_SHIFT_IZQ = r'[<][<]'
t_MAYOR = r'[>]'
t_MENOR = r'[<]'
t_XOR_BIT = r'[\\^]'
t_OR = r'[|][|]'
t_AND = r'[&][&]'
t_NOT_BIT = r'[~]'
t_AND_BIT = r'[&]'
t_OR_BIT = r'[&]'
t_NOT = r'[!]'
t_SUMA = r'[+]'
t_RESTA = r'[-]'
t_MULT = r'[*]'
t_DIV = r'[/]'
t_MOD = r'[%]'
t_PAR_IZQ = r'[(]'
t_PAR_DER = r'[)]'
t_COR_IZQ = r'[[]'
t_COR_DER = r'[]]'
t_IGUAL = r'[=]'
t_DOS_PUNTOS = r'[:]'
t_PUNTO_COMA = r'[;]'

def agregarError(texto):
    global errores
    errores += texto

def t_CARACTER(t):
    r'(\'.\')|(\".\")'
    t.value = t.value[1:-1]
    return t

def t_CADENA(t):
    r'(\'[^\']*\')|(\"[^\"]*\")'
    t.value = t.value[1:-1]
    return t

def t_TEMPORAL(t):
    r'\$(t)\d+'
    t.value = t.value[2:]
    return t

def t_PARAMETRO(t):
    r'\$(a)\d+'
    t.value = t.value[2:]
    return t

def t_DEVUELTO(t):
    r'\$(v)\d+'
    t.value = t.value[2:]
    return t

def t_RETORNO(t):
    r'\$ra'
    t.value = t.value[1:]
    return t

def t_PILA(t):
    r'\$(s)\d+'
    t.value = t.value[2:]
    return t

def t_PUNTERO(t):
    r'\$sp'
    t.value = t.value[1:]
    return t

def t_LABEL(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value.lower(),'LABEL')
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print('jijo')
        t.value = 0.0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print('jijo')
        t.value = 0
    return t

def t_COMENTARIO(t):
    r'[#].*\n'
    t.lexer.lineno += 1
    t.lexer.skip(0)

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    agregarError('ERROR LEXICO:   El simbolo "' + t.value[0] + '", declarado en la linea ' + str(t.lineno) + ', no pertenece al lenguaje. \n')
    t.lexer.skip(1)


def p_init(t):
    'init           : program'
    t[0] = [t[1][0], 'init: program \n'+t[1][1]]


def p_init_vacio(t):
    'init           : '


def p_program(t):
    'program        : main labels'
    t[2][0].insert(0,t[1][0])
    t[0] = [Program(t[2][0]), 'program: main labels \n' + t[1][1] + t[2][1]]


def p_main(t):
    'main           : MAIN DOS_PUNTOS instructions'
    t[0] = [Main(t[3][0]), 'main: MAIN DOS_PUNTOS instructions \n' + t[3][1]]


def p_main_error(t):
    'main           : error instructions'
    t[0] = [None, '']

def p_labels(t):
    'labels         : label labels'
    t[2][0].insert(0,t[1][0])
    t[0] = [t[2][0], 'labels: label labels \n'+ t[1][1] + t[2][1]]


def p_labels_epsilon(t):
    'labels         : '
    t[0] = [[], 'labels: ε \n']

def p_label(t):
    'label          : LABEL DOS_PUNTOS instructions'
    t[0] = [Label(t[1], t[3][0]), 'label: LABEL DOS_PUNTOS instructions \n' + t[3][1]]

def p_label_error(t):
    'label          : error instructions'
    t[0] = [None, '']


def p_instructions(t):
    'instructions   : instruction instructionsprima'
    t[2][0].insert(0, t[1][0])
    t[0] = [t[2][0], 'instructions: instruction instructionsprima \n' + t[1][1] + t[2][1]]


def p_instructionsprima(t):
    'instructionsprima   : instruction instructionsprima'
    t[2][0].insert(0, t[1][0])
    t[0] = [t[2][0], 'instructionsprima: instruction instructionsprima \n' + t[1][1] + t[2][1]]


def p_instructionsprima_epsilon(t):
    'instructionsprima   : '
    t[0] = [[], 'instructionsprima: ε \n']


def p_instruction_exit(t):
    'instruction    : exit PUNTO_COMA'
    t[0] = [t[1][0],'instruction: exit PUNTO_COMA \n' + t[1][1]]

def p_instruction_unset(t):
    'instruction    : unset PUNTO_COMA'
    t[0] = [t[1][0], 'instruction: unset PUNTO_COMA \n' + t[1][1]]


def p_instruction_print(t):
    'instruction    : print PUNTO_COMA'
    t[0] = [t[1][0], 'instruction: print PUNTO_COMA \n' + t[1][1]]


def p_instruction_if(t):
    'instruction    : if PUNTO_COMA'
    t[0] = [t[1][0], 'instruction: if PUNTO_COMA \n' + t[1][1]]


def p_instruction_set(t):
    'instruction    : set PUNTO_COMA'
    t[0] = [t[1][0], 'instruction: set PUNTO_COMA \n' + t[1][1]]


def p_instruction_goto(t):
    'instruction    : goto PUNTO_COMA'
    t[0] = [t[1][0], 'instruction: goto PUNTO_COMA \n' + t[1][1]]


def p_instruction_error(t):
    'instruction    : error PUNTO_COMA'
    t[0] = [None, '']

def p_exit(t):
    'exit           : EXIT'
    t[0] = [Exit(), 'exit: EXIT \n']


def p_goto(t):
    'goto           : GOTO LABEL'
    t[0] = [Goto(t[2]), 'goto: GOTO LABEL \n']


def p_unset(t):
    'unset          : UNSET PAR_IZQ var PAR_DER'
    t[0] = [Unset(t[3][0]), 'unset: UNSET PAR_IZQ var PAR_DER \n' + t[3][1]]


def p_print(t):
    'print          : PRINT PAR_IZQ var PAR_DER'
    t[0] = [Print(t[3][0]), 'print: PRINT PAR_IZQ var PAR_DER \n' + t[3][1]]


def p_if(t):
    'if             : IF PAR_IZQ condition PAR_DER goto'
    t[0] = [If(t[3][0], t[5][0]), 'if: IF PAR_IZQ condition PAR_DER goto \n' + t[3][1] + t[5][1]]


def p_condition_expression(t):
    'condition      : expression'
    t[0] = [t[1][0], 'condition: expression \n' + t[1][1]]


def p_condition_var(t):
    'condition      : var'
    t[0] = [t[1][0], 'condition: var \n' + t[1][1]]


def p_set(t):
    'set            : var IGUAL assignation'
    t[0] = [Set(t[1][0], t[3][0]), 'set: var IGUAL assignation \n' + t[1][1] + t[3][1]]


def p_var(t):
    'var            : register'
    t[0] = [t[1][0], 'var: register \n' + t[1][1]]


def p_var_array(t):
    'var            : register positions'
    t[0] = [Array(t[1][0].name, t[1][0].type_, t[1][0].position, t[2][0]), 'var: register positions \n' + t[1][1] + t[2][1]]


def p_register_temporal(t):
    'register       : TEMPORAL'
    t[0] = [Register('$t'+t[1], REGISTER.TEMPORAL, t[1]), 'register: TEMPORAL \n']


def p_register_parametro(t):
    'register       : PARAMETRO'
    t[0] = [Register('$a'+t[1], REGISTER.PARAM, t[1]), 'register: PARAMETRO \n']


def p_register_devuelto(t):
    'register       : DEVUELTO'
    t[0] = [Register('$v'+t[1], REGISTER.DEVUELTO, t[1]), 'register: DEVUELTO \n']


def p_register_retorno(t):
    'register       : RETORNO'
    t[0] = [Register('$'+t[1], REGISTER.RETURNED, t[1]), 'register: RETORNO \n']


def p_register_pila(t):
    'register       : PILA'
    t[0] = [Register('$s'+t[1], REGISTER.PILA, t[1]), 'register: PILA \n']


def p_register_puntero(t):
    'register       : PUNTERO'
    t[0] = [Register('$'+t[1], REGISTER.PUNTERO, t[1]), 'register: PUNTERO \n']
    

def p_positions(t):
    'positions      : position positionsprima'
    t[2][0].insert(0, t[1][0])
    t[0] = [t[2][0], 'positions: position positionsprima \n' + t[1][1] + t[2][1]]


def p_positionsprima(t):
    'positionsprima : position positionsprima'
    t[2][0].insert(0, t[1][0])
    t[0] = [t[2][0], 'positionsprima: position positionsprima \n' + t[1][1] + t[2][1]]


def p_positionsprima_epsilon(t):
    'positionsprima : '
    t[0] = [[], 'positionsprima: ε \n']


def p_position(t):
    'position       : COR_IZQ cont COR_DER'
    t[0] = [Index(t[2][0]), 'position: COR_IZQ cont COR_DER \n' + t[2][1]]


def p_primary_entero(t):
    'primary        : ENTERO'
    t[0] = [Primary(t.slice[1].type, t[1]), 'primary: ENTERO \n']


def p_primary_cadena(t):
    'primary        : CADENA'
    t[0] = [Primary(t.slice[1].type, t[1]), 'primary: CADENA \n']


def p_primary_caracter(t):
    'primary        : CARACTER'
    t[0] = [Primary(t.slice[1].type, t[1]), 'primary: CARACTER \n']


def p_primary_decimal(t):
    'primary        : DECIMAL'
    t[0] = [Primary(t.slice[1].type, t[1]), 'primary: DECIMAL \n']


def p_assignation_data(t):
    'assignation    : data'
    t[0] = [t[1][0], 'assignation: data \n' + t[1][1]]


def p_assignation_array(t):
    'assignation    : array'
    t[0] = [t[1][0], 'assignation: array \n' + t[1][1]]


def p_assignation_read(t):
    'assignation    : read'
    t[0] = [t[1][0], 'assignation: read \n' + t[1][1]]


def p_assignation_cast(t):
    'assignation    : cast'
    t[0] = [t[1][0], 'assignation: cast \n' + t[1][1]]


def p_assignation_expression(t):
    'assignation    : expression'
    t[0] = [t[1][0], 'assignation: expression \n' + t[1][1]]


def p_assignation_pointer(t):
    'assignation    : pointer'
    t[0] = [t[1][0], 'assignation: pointer \n' + t[1][1]]


def p_data_primary(t):
    'data           : primary'
    t[0] = [t[1][0], 'data: primary \n' + t[1][1]]
    

def p_data_var(t):
    'data           : var'
    t[0] = [t[1][0], 'data: var \n' + t[1][1]]


def p_cont_primary(t):
    'cont           : primary'
    t[0] = [t[1][0], 'cont: primary \n' + t[1][1]]


def p_cont_register(t):
    'cont           : register'
    t[0] = [t[1][0], 'cont: register \n' + t[1][1]]


def p_array(t):
    'array          : ARRAY PAR_IZQ PAR_DER'
    t[0] = [ArrayDeclaration(), 'array: ARRAY PAR_IZQ PAR_DER \n']


def p_read(t):
    'read           : READ PAR_IZQ PAR_DER'
    t[0] = [Read(), 'read: READ PAR_IZQ PAR_DER']


def p_cast(t):
    'cast           : PAR_IZQ type PAR_DER var'
    t[0] = [Cast(t[2][0], t[4][0]), 'cast: PAR_IZQ type PAR_DER var \n' + t[2][1] + t[4][1]]


def p_type(t):
    '''type         : FLOAT
                    | INT
                    | CHAR'''
    if t[1] == 'float': 
        t[0] = [DATA_TYPE.FLOAT, 'type: FLOAT \n']
    elif t[1] == 'int': 
        t[0] = [DATA_TYPE.INTEGER, 'type: INT \n']
    elif t[1] == 'char': 
        t[0] = [DATA_TYPE.CHARACTER, 'type: CHAR \n']


def p_expression_aritmetic(t):
    'expression     : aritmetic'
    t[0] = [t[1][0], 'expression: aritmetic \n' + t[1][1]]


def p_expression_logical(t):
    'expression     : logical'
    t[0] = [t[1][0], 'expression: logical \n' + t[1][1]]


def p_expression_bitxbit(t):
    'expression     : bitxbit'
    t[0] = [t[1][0], 'expression: bitxbit \n' + t[1][1]]


def p_expression_ralational(t):
    'expression     : ralational'
    t[0] = [t[1][0], 'expression: ralational \n' + t[1][1]]


def p_aritmetic(t):
    '''aritmetic    : data SUMA data
                    | data RESTA data
                    | data MULT data
                    | data DIV data
                    | data MOD data
                    | RESTA data
                    | ABS PAR_IZQ data PAR_DER'''
    if t[2] == '+':
        t[0] = [AritmeticOperation(ARITMETIC_OPERATION.SUMA, t[1][0], t[3][0]), 'aritmetic: data SUMA data \n' + t[1][1] + t[3][1]]
    elif t[2] == '-':
        t[0] = [AritmeticOperation(ARITMETIC_OPERATION.RESTA, t[1][0], t[3][0]), 'aritmetic: data RESTA data \n' + t[1][1] + t[3][1]]
    elif t[2] == '/':
        t[0] = [AritmeticOperation(ARITMETIC_OPERATION.DIV, t[1][0], t[3][0]), 'aritmetic: data MULT data \n' + t[1][1] + t[3][1]]
    elif t[2] == '*':
        t[0] = [AritmeticOperation(ARITMETIC_OPERATION.MULT, t[1][0], t[3][0]), 'aritmetic: data DIV data \n' + t[1][1] + t[3][1]]
    elif t[2] == '%':
        t[0] = [AritmeticOperation(ARITMETIC_OPERATION.MOD, t[1][0], t[3][0]), 'aritmetic: data MOD data \n' + t[1][1] + t[3][1]]
    elif t[1] == '-':
        t[0] = [AritmeticOperation(ARITMETIC_OPERATION.NEG, t[2][0], None), 'aritmetic: RESTA data \n' + t[2][1]]
    elif t[1] == 'abs':
        t[0] = [AritmeticOperation(ARITMETIC_OPERATION.ABS, t[3][0], None), 'aritmetic: ABS PAR_IZQ data PAR_DER \n' + t[3][1]]


def p_logical(t):
    '''logical      : data AND data
                    | data OR data
                    | data XOR data
                    | NOT data'''
    if t[2] == '&&':
        t[0] = [LogicOperation(LOGIC_OPERATION.AND, t[1][0], t[3][0]), 'logical: data AND data \n' + t[1][1] + t[3][1]]
    elif t[2] == '||':
        t[0] = [LogicOperation(LOGIC_OPERATION.OR, t[1][0], t[3][0]), 'logical: data OR data \n' + t[1][1] + t[3][1]]
    elif t[2] == 'xor':
        t[0] = [LogicOperation(LOGIC_OPERATION.XOR, t[1][0], t[3][0]), 'logical: data XOR data \n' + t[1][1]]
    elif t[1] == '!':
        t[0] = [LogicOperation(LOGIC_OPERATION.NOT, t[2][0], None), 'logical: NOT data \n' + t[2][1]]
    


def p_bitxbit(t):
    '''bitxbit      : data AND_BIT data
                    | data OR_BIT data
                    | data XOR_BIT data
                    | data SHIFT_DER data
                    | data SHIFT_IZQ data
                    | NOT_BIT data'''
    if t[2] == '&':
        t[0] = [BitxbitOperation(BITXBIT_OPERATION.BIT_AND, t[1][0], t[3][0]), 'bitxbit: data AND_BIT data \n' + t[1][1] + t[3][1]]
    elif t[2] == '|':
        t[0] = [BitxbitOperation(BITXBIT_OPERATION.BIT_OR, t[1][0], t[3][0]), 'bitxbit: data OR_BIT data \n' + t[1][1] + t[3][1]]
    elif t[2] == '^':
        t[0] = [BitxbitOperation(BITXBIT_OPERATION.BIT_XOR, t[1][0], t[3][0]), 'bitxbit: data XOR_BIT data \n' + t[1][1] + t[3][1]]
    elif t[2] == '<<':
        t[0] = [BitxbitOperation(BITXBIT_OPERATION.SHIFT_IZQ, t[1][0], t[3][0]), 'bitxbit: data SHIFT_DER data \n' + t[1][1] + t[3][1]]
    elif t[2] == '>>':
        t[0] = [BitxbitOperation(BITXBIT_OPERATION.SHIFT_DER, t[1][0], t[3][0]), 'bitxbit: data SHIFT_IZQ data \n' + t[1][1] + t[3][1]]
    elif t[1] == '~':
        t[0] = [BitxbitOperation(BITXBIT_OPERATION.BIT_NOT, t[2][0], None), 'bitxbit: NOT_BIT data \n' + t[2][1]]
    

def p_relational(t):
    '''ralational   : data ES_IGUAL data
                    | data NO_IGUAL data
                    | data MAYOR data
                    | data MENOR data
                    | data MAYOR_IGUAL data
                    | data MENOR_IGUAL data'''
    if t[2] == '==':
        t[0] = [RelationalOperation(RELATIONAL_OPERATION.ES_IGUAL, t[1][0], t[3][0]), 'ralational: data ES_IGUAL data \n' + t[1][1] + t[3][1]]
    elif t[2] == '!=':
        t[0] = [RelationalOperation(RELATIONAL_OPERATION.NO_IGUAL, t[1][0], t[3][0]), 'ralational: data NO_IGUAL data \n' + t[1][1] + t[3][1]]
    elif t[2] == '>':
        t[0] = [RelationalOperation(RELATIONAL_OPERATION.MAYOR, t[1][0], t[3][0]), 'ralational: data MAYOR data \n' + t[1][1] + t[3][1]]
    elif t[2] == '<':
        t[0] = [RelationalOperation(RELATIONAL_OPERATION.MENOR, t[1][0], t[3][0]), 'ralational: data MENOR data \n' + t[1][1] + t[3][1]]
    elif t[2] == '>=':
        t[0] = [RelationalOperation(RELATIONAL_OPERATION.MAYOR_IGUAL, t[1][0], t[3][0]), 'ralational: data MAYOR_IGUAL data \n' + t[1][1] + t[3][1]]
    elif t[2] == '<=':
        t[0] = [RelationalOperation(RELATIONAL_OPERATION.MENOR_IGUAL, t[1][0], t[3][0]), 'ralational: data MENOR_IGUAL data \n' + t[1][1] + t[3][1]]


def p_pointer(t):
    'pointer        : AND_BIT var'
    t[0] = [Pointer(t[2][0]), 'pointer: AND_BIT var \n' + t[2][1]]


def p_error(t):
    agregarError('ERROR SINTACTICO: El simbolo "' + str(t.value) + '", identificador como '+str(t.type)+', no era el esperado en la linea '+ str(t.lineno)+'.\n')





def analizar(texto, textview):
    global errores
    errores = ''
    returned = [None, None]
    try:
        lexer = lex.lex()
        lexer.input(texto)
        parser = yacc.yacc() 
        returned = parser.parse(texto)   
    except:
        errores = ''
        agregarError('ERROR NO CONTROLADO: A ocurrido un problema en el analisis lexico y sintactico. \nPara recivir soporte pongase en contacto con siguiente correo: jorgejuarezdal@gmail.com')
    finally:
        textview.setText(errores)   

    return returned

'''lexer = lex.lex()
parser = yacc.yacc()
#input ='main: \t\n $t0[1][3] = 4; \t\n goto t2; \n ret0: \t\n print($t5); \t\n exit; \t\n f1: \n $a1 = $a0; \t\n goto f2; \t\n ret1: \n $v0 = $v1; \t\n goto ret0; \t\n f2: \n $v1 = $a1*$a1; \t\n goto ret1;'
#input = 'main: \t\n $t1 = 54; \t\n exit;'
lexer.input(input)

perreo = parser.parse(input)

GraphAST(perreo[0])

print(perreo[1])

interpretar(perreo[0])'''
