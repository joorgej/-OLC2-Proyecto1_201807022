import ply.lex as lex
import ply.yacc as yacc
import re
from Instructions import *
from graphviz import Graph
from AST_Graph import *
from Interprete import *

gramarReport = ''
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

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print(t.value)
    agregarError('ERROR LEXICO:   El simbolo "' + t.value[0] + '", declarado en la linea ' + str(t.lineno) + ', no pertenece al lenguaje. \n')
    t.lexer.skip(1)


def gramarAdd(addition):
    global gramarReport
    gramarReport = addition + '\n' + gramarReport


def p_init(t):
    'init           : program'
    t[0] = t[1]
    gramarAdd('init → program')

def p_init_vacio(t):
    'init           : '

def p_program_main(t):
    'program        : main'
    t[0] = Program([t[1]])
    gramarAdd('program → main')


def p_program_labels(t):
    'program        : main labels'
    t[2].insert(0,t[1])
    t[0] = Program(t[2])
    gramarAdd('program → main labels')


def p_main(t):
    'main           : MAIN DOS_PUNTOS instructions'
    t[0] = Main(t[3])
    gramarAdd('main → MAIN DOS_PUNTOS instructions')


def p_main_error(t):
    'main           : error instructions'


def p_labels(t):
    'labels         : labels label'
    t[1].append(t[2])
    t[0] = t[1]
    gramarAdd('labels → labels label')


def p_labels_simple(t):
    'labels         : label'
    t[0] = [t[1]]
    gramarAdd('labels → label')


def p_label(t):
    'label         : LABEL DOS_PUNTOS instructions'
    t[0] = Label(t[1], t[3])
    gramarAdd('label → LABEL DOS_PUNTOS instructions')

def p_label_error(t):
    'label           : error instructions'


def p_instructions(t):
    'instructions   : instructions instruction'
    t[1].append(t[2])
    t[0] = t[1]
    gramarAdd('instructions → instructions instruction')


def p_instructions_simple(t):
    'instructions   : instruction'
    t[0] = [t[1]]
    gramarAdd('instructions → instruction')


def p_instruction_exit(t):
    'instruction    : exit PUNTO_COMA'
    t[0] = t[1]
    gramarAdd('instruction → exit PUNTO_COMA')

def p_instruction_unset(t):
    'instruction    : unset PUNTO_COMA'
    t[0] = t[1]
    gramarAdd('instruction → unset PUNTO_COMA')


def p_instruction_print(t):
    'instruction    : print PUNTO_COMA'
    t[0] = t[1]
    gramarAdd('instruction → print PUNTO_COMA')


def p_instruction_if(t):
    'instruction    : if PUNTO_COMA'
    t[0] = t[1]
    gramarAdd('instruction → if PUNTO_COMA')


def p_instruction_set(t):
    'instruction    : set PUNTO_COMA'
    t[0] = t[1]
    gramarAdd('instruction → set PUNTO_COMA')


def p_instruction_goto(t):
    'instruction    : goto PUNTO_COMA'
    t[0] = t[1]
    gramarAdd('instruction → goto PUNTO_COMA')


def p_instruction_error(t):
    'instruction    : error PUNTO_COMA'


def p_exit(t):
    'exit           : EXIT'
    t[0] = Exit()
    gramarAdd('exit → EXIT')


def p_goto(t):
    'goto           : GOTO LABEL'
    t[0] = Goto(t[2])
    gramarAdd('goto → GOTO LABEL')


def p_unset(t):
    'unset          : UNSET PAR_IZQ var PAR_DER'
    t[0] = Unset(t[3])
    gramarAdd('unset → UNSET PAR_IZQ var PAR_DER')


def p_print(t):
    'print          : PRINT PAR_IZQ var PAR_DER'
    t[0] = Print(t[3])
    gramarAdd('print → PRINT PAR_IZQ var PAR_DER')


def p_if(t):
    'if             : IF PAR_IZQ condition PAR_DER goto'
    t[0] = If(t[3], t[5])
    gramarAdd('if → IF PAR_IZQ condition PAR_DER goto')


def p_condition_expression(t):
    'condition      : expression'
    t[0] = t[1]
    gramarAdd('condition → expression')


def p_condition_var(t):
    'condition      : var'
    t[0] = t[1]
    gramarAdd('condition → var')


def p_set(t):
    'set            : var IGUAL assignation'
    t[0] = Set(t[1], t[3])
    gramarAdd('set → var IGUAL assignation')


def p_var(t):
    'var            : register'
    t[0] = t[1]
    gramarAdd('var → register')


def p_var_array(t):
    'var            : register positions'
    t[0] = Array(t[1].name, t[1].type_, t[1].position, t[2])
    gramarAdd('var → register positions')


def p_register_temporal(t):
    'register       : TEMPORAL'
    t[0] = Register('$t'+t[1], REGISTER.TEMPORAL, t[1])
    gramarAdd('register → TEMPORAL')


def p_register_parametro(t):
    'register       : PARAMETRO'
    t[0] = Register('$a'+t[1], REGISTER.PARAM, t[1]) 
    gramarAdd('register → PARAMETRO')


def p_register_devuelto(t):
    'register       : DEVUELTO'
    t[0] = Register('$v'+t[1], REGISTER.DEVUELTO, t[1])
    gramarAdd('register → DEVUELTO')


def p_register_retorno(t):
    'register       : RETORNO'
    t[0] = Register('$'+t[1], REGISTER.RETURNED, t[1])
    gramarAdd('register → RETORNO')


def p_register_pila(t):
    'register       : PILA'
    t[0] = Register('$s'+t[1], REGISTER.PILA, t[1])
    gramarAdd('register → PILA')


def p_register_puntero(t):
    'register       : PUNTERO'
    t[0] = Register('$'+t[1], REGISTER.PUNTERO, t[1])
    gramarAdd('register → PUNTERO')
    

def p_positions(t):
    'positions      : positions position'
    t[1].append(t[2])
    t[0] = t[1]
    gramarAdd('positions → positions position')


def p_positions_simple(t):
    'positions      : position'
    t[0] = [t[1]]
    gramarAdd('positions → position')


def p_position(t):
    'position       : COR_IZQ cont COR_DER'
    t[0] = Index(t[2])
    gramarAdd('position → COR_IZQ cont COR_DER')


def p_primary_entero(t):
    'primary        : ENTERO'
    t[0] = Primary(t.slice[1].type, t[1])
    gramarAdd('primary → ENTERO')


def p_primary_cadena(t):
    'primary        : CADENA'
    t[0] = Primary(t.slice[1].type, t[1])
    gramarAdd('primary → CADENA')


def p_primary_caracter(t):
    'primary        : CARACTER'
    t[0] = Primary(t.slice[1].type, t[1])
    gramarAdd('primary → CARACTER')


def p_primary_decimal(t):
    'primary        : DECIMAL'
    t[0] = Primary(t.slice[1].type, t[1])
    gramarAdd('primary → DECIMAL')


def p_assignation_data(t):
    'assignation    : data'
    t[0] = t[1]
    gramarAdd('assignation → data')


def p_assignation_array(t):
    'assignation    : array'
    t[0] = t[1]
    gramarAdd('assignation → array')


def p_assignation_read(t):
    'assignation    : read'
    t[0] = t[1]
    gramarAdd('assignation → read')


def p_assignation_cast(t):
    'assignation    : cast'
    t[0] = t[1]
    gramarAdd('assignation → cast')


def p_assignation_expression(t):
    'assignation    : expression'
    t[0] = t[1]
    gramarAdd('assignation → expression')


def p_assignation_pointer(t):
    'assignation    : pointer'
    t[0] = t[1]
    gramarAdd('assignation → pointer')


def p_data_primary(t):
    'data           : primary'
    t[0] = t[1]
    gramarAdd('data → primary')
    

def p_data_var(t):
    'data           : var'
    t[0] = t[1]
    gramarAdd('data → var')


def p_cont_primary(t):
    'cont           : primary'
    t[0] = t[1]
    gramarAdd('cont → primary')


def p_cont_register(t):
    'cont           : register'
    t[0] = t[1]
    gramarAdd('cont → register')


def p_array(t):
    'array          : ARRAY PAR_IZQ PAR_DER'
    t[0] = ArrayDeclaration()
    gramarAdd('array → ARRAY PAR_IZQ PAR_DER')


def p_read(t):
    'read           : READ PAR_IZQ PAR_DER'
    t[0] = Read()
    gramarAdd('read → READ PAR_IZQ PAR_DER')


def p_cast(t):
    'cast           : PAR_IZQ type PAR_DER var'
    t[0] = Cast(t[2], t[4])
    gramarAdd('cast → PAR_IZQ type PAR_DER var')


def p_type(t):
    '''type         : FLOAT
                    | INT
                    | CHAR'''
    if t[1] == 'float': 
        t[0] = DATA_TYPE.FLOAT
        gramarAdd('type → FLOAT')
    elif t[1] == 'int': 
        t[0] = DATA_TYPE.INTEGER
        gramarAdd('type → INT')
    elif t[1] == 'char': 
        t[0] = DATA_TYPE.CHARACTER
        gramarAdd('type → CHAR')


def p_expression_aritmetic(t):
    'expression     : aritmetic'
    t[0] = t[1]
    gramarAdd('expression → aritmetic')


def p_expression_logical(t):
    'expression     : logical'
    t[0] = t[1]
    gramarAdd('expression → logical')


def p_expression_bitxbit(t):
    'expression     : bitxbit'
    t[0] = t[1]
    gramarAdd('expression → bitxbit')


def p_expression_ralational(t):
    'expression     : ralational'
    t[0] = t[1]
    gramarAdd('expression → ralational')


def p_aritmetic(t):
    '''aritmetic    : data SUMA data
                    | data RESTA data
                    | data MULT data
                    | data DIV data
                    | data MOD data
                    | RESTA data
                    | ABS PAR_IZQ data PAR_DER'''
    if t[2] == '+':
        t[0] = AritmeticOperation(ARITMETIC_OPERATION.SUMA, t[1], t[3])
        gramarAdd('aritmetic → data SUMA data')
    elif t[2] == '-':
        t[0] = AritmeticOperation(ARITMETIC_OPERATION.RESTA, t[1], t[3])
        gramarAdd('aritmetic → data RESTA data')
    elif t[2] == '/':
        t[0] = AritmeticOperation(ARITMETIC_OPERATION.DIV, t[1], t[3])
        gramarAdd('aritmetic → data MULT data')
    elif t[2] == '*':
        t[0] = AritmeticOperation(ARITMETIC_OPERATION.MULT, t[1], t[3])
        gramarAdd('aritmetic → data DIV data')
    elif t[2] == '%':
        t[0] = AritmeticOperation(ARITMETIC_OPERATION.MOD, t[1], t[3])
        gramarAdd('aritmetic → data MOD data')
    elif t[1] == '-':
        t[0] = AritmeticOperation(ARITMETIC_OPERATION.NEG, t[2], None)
        gramarAdd('aritmetic → RESTA data')
    elif t[1] == 'abs':
        t[0] = AritmeticOperation(ARITMETIC_OPERATION.ABS, t[3], None)
        gramarAdd('aritmetic → ABS PAR_IZQ data PAR_DER')


def p_logical(t):
    '''logical      : data AND data
                    | data OR data
                    | data XOR data
                    | NOT data'''
    if t[2] == '&&':
        t[0] = LogicOperation(LOGIC_OPERATION.AND, t[1], t[3])
        gramarAdd('logical → data AND data')
    elif t[2] == '||':
        t[0] = LogicOperation(LOGIC_OPERATION.OR, t[1], t[3])
        gramarAdd('logical → data OR data')
    elif t[2] == 'xor':
        t[0] = LogicOperation(LOGIC_OPERATION.XOR, t[1], t[3])
        gramarAdd('logical → data XOR data')
    elif t[1] == '!':
        t[0] = LogicOperation(LOGIC_OPERATION.NOT, t[2], None)
        gramarAdd('logical → NOT data')
    


def p_bitxbit(t):
    '''bitxbit      : data AND_BIT data
                    | data OR_BIT data
                    | data XOR_BIT data
                    | data SHIFT_DER data
                    | data SHIFT_IZQ data
                    | NOT_BIT data'''
    if t[2] == '&':
        t[0] = BitxbitOperation(BITXBIT_OPERATION.BIT_AND, t[1], t[3])
        gramarAdd('bitxbit → data AND_BIT data')
    elif t[2] == '|':
        t[0] = BitxbitOperation(BITXBIT_OPERATION.BIT_OR, t[1], t[3])
        gramarAdd('bitxbit → data OR_BIT data')
    elif t[2] == '^':
        t[0] = BitxbitOperation(BITXBIT_OPERATION.BIT_XOR, t[1], t[3])
        gramarAdd('bitxbit → data XOR_BIT data')
    elif t[2] == '<<':
        t[0] = BitxbitOperation(BITXBIT_OPERATION.SHIFT_IZQ, t[1], t[3])
        gramarAdd('bitxbit → data SHIFT_DER data')
    elif t[2] == '>>':
        t[0] = BitxbitOperation(BITXBIT_OPERATION.SHIFT_DER, t[1], t[3])
        gramarAdd('bitxbit → data SHIFT_IZQ data')
    elif t[1] == '~':
        t[0] = BitxbitOperation(BITXBIT_OPERATION.BIT_NOT, t[2], None)
        gramarAdd('bitxbit → NOT_BIT data')
    


def p_relational(t):
    '''ralational   : data ES_IGUAL data
                    | data NO_IGUAL data
                    | data MAYOR data
                    | data MENOR data
                    | data MAYOR_IGUAL data
                    | data MENOR_IGUAL data'''
    if t[2] == '==':
        t[0] = RelationalOperation(RELATIONAL_OPERATION.ES_IGUAL, t[1], t[3])
        gramarAdd('ralational → data ES_IGUAL data')
    elif t[2] == '!=':
        t[0] = RelationalOperation(RELATIONAL_OPERATION.NO_IGUAL, t[1], t[3])
        gramarAdd('ralational → data NO_IGUAL data')
    elif t[2] == '>':
        t[0] = RelationalOperation(RELATIONAL_OPERATION.MAYOR, t[1], t[3])
        gramarAdd('ralational → data MAYOR data')
    elif t[2] == '<':
        t[0] = RelationalOperation(RELATIONAL_OPERATION.MENOR, t[1], t[3])
        gramarAdd('ralational → data MENOR data')
    elif t[2] == '>=':
        t[0] = RelationalOperation(RELATIONAL_OPERATION.MAYOR_IGUAL, t[1], t[3])
        gramarAdd('ralational → data MAYOR_IGUAL data')
    elif t[2] == '<=':
        t[0] = RelationalOperation(RELATIONAL_OPERATION.MENOR_IGUAL, t[1], t[3])
        gramarAdd('ralational → data MENOR_IGUAL data')


def p_pointer(t):
    'pointer        : AND_BIT var'
    t[0] = Pointer(t[2])
    gramarAdd('pointer → AND_BIT var')


def p_error(t):

    agregarError('ERROR SINTACTICO: El simbolo "' + str(t.value) + '", identificador como '+str(t.type)+', no era el esperado en la linea '+ str(t.lineno) +'.\n')




def analizar(texto, textview):
    global errores
    errores = ''
    AST = None
    try:
        lexer = lex.lex()
        lexer.input(texto)
        parser = yacc.yacc() 
        AST = parser.parse(texto)   
    except:
        errores = ''
        agregarError('ERROR NO CONTROLADO: A ocurrido un problema en el analisis lexico y sintactico. \n                   Para recivir soporte pongase en contacto con siguiente correo: jorgejuarezdal@gmail.com')
        
    finally:
        textview.setText(errores)   

    return [AST, gramarReport]


