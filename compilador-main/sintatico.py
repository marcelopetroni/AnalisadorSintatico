import ply.yacc as yacc
from lexico import *

# ANALISADOR SINTATICO: PROJETO POR MARCELO NUNES E MATHEUS GARCIA

# Lista de tokens definida anteriormente
# from lexer import tokens

# Regras da gramática
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
)

# 1º Regra: programa
def p_program(p):
    '''program : declaration'''
    p[0] = ('PROGRAM', p[1])
int
# 2º Regra: declaração
def p_declaration(p):
    '''declaration : declaration_variable
                | declaration_function
                | declaration_structure
                | comment
                | NUMERO
                | VSTRING
                | ID
                | type
                | expression
                | operacoes'''
    p[0] = ('DECLARATION', p[1])

# 3º Regra: declaração de variavel
def p_declaration_variable(p):
    '''declaration_variable : ID EQUAL expression
                        | ID EQUAL EQUAL expression
                        | ID EQUAL expression declaration'''
    if len(p) == 3:
        p[0] = ('DECLARATION_VARIABLE', p[1], p[2])
    elif len(p) == 4:
        p[0] = ('DECLARATION_VARIABLE', p[1], p[2], p[3])
    elif len(p) == 5:
        p[0] = ('DECLARATION_VARIABLE', p[1], p[2], p[3], p[4])
    elif len(p) == 6:
        p[0] = ('DECLARATION_VARIABLE', p[1], p[2], p[3], p[4], p[5])

# Regra auxiliar para o Tipo
def p_type(p):
    '''type : INT
            | FLOAT
            | DOUBLE
            | CHAR
            | BOOL'''
    p[0] = ('TYPE', p[1])

# 4º Regra: declaração de função
def p_declaration_function(p):
    '''declaration_function : DEF ID LPAREN parameters RPAREN COLON declaration
                            | DEF ID LPAREN parameters RPAREN COLON declaration RETURN ID
                            | DEF ID LPAREN parameters RPAREN COLON declaration RETURN NUMERO
                            | DEF ID LPAREN parameters RPAREN COLON declaration RETURN VSTRING
                            | DEF ID LPAREN parameters RPAREN COLON declaration RETURN expression
                            | DEF ID LPAREN parameters RPAREN COLON ID EQUAL operacoes RETURN ID'''
    if len(p) == 8:
        p[0] = ('DECLARATION_FUNCTION', p[1], p[2], p[3], p[4], p[5], p[6], p[7])
    elif len(p) == 9:
        p[0] = ('DECLARATION_FUNCTION', p[1], p[2],p[3], p[4], p[5], p[6], p[7], p[8])
    elif len(p) == 10:
        p[0] = ('DECLARATION_FUNCTION', p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9])
    else:
        p[0] = ('DECLARATION_FUNCTION', p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11])

# auxiliar operacoes
def p_operacoes(p):
    '''operacoes : ID PLUS ID
            | ID MINUS ID
            | ID DIVIDE ID
            | ID TIMES ID
            | ID MODULO ID
            | NUMERO PLUS ID
            | NUMERO MINUS ID
            | NUMERO DIVIDE ID
            | NUMERO TIMES ID
            | NUMERO MODULO ID
            | NUMERO PLUS NUMERO
            | NUMERO MINUS NUMERO
            | NUMERO DIVIDE NUMERO
            | NUMERO TIMES NUMERO
            | NUMERO MODULO NUMERO
            | ID PLUS ID DIVIDE NUMERO
            | LPAREN ID PLUS NUMERO RPAREN
            | ID PLUS LPAREN NUMERO TIMES NUMERO RPAREN
            | ID TIMES NUMERO MINUS LPAREN ID DIVIDE NUMERO RPAREN
            | ID MODULO NUMERO TIMES ID PLUS NUMERO
            | ID DIVIDE LPAREN NUMERO PLUS ID MINUS NUMERO RPAREN
            | ID TIMES ID TIMES ID DIVIDE NUMERO PLUS NUMERO
            | ID PLUS ID MODULO ID MINUS NUMERO
            | ID MODULO ID TIMES NUMERO MINUS NUMERO
            | NUMERO PLUS ID TIMES NUMERO DIVIDE ID
            | ID MODULO ID PLUS ID DIVIDE NUMERO TIMES ID
            | ID MODULO ID TIMES ID DIVIDE ID PLUS ID
            | NUMERO TIMES ID MODULO NUMERO PLUS ID
            | ID PLUS ID MODULO NUMERO TIMES ID DIVIDE NUMERO
            | ID TIMES NUMERO DIVIDE ID MODULO ID PLUS ID
            | ID PLUS NUMERO PLUS ID DIVIDE NUMERO TIMES ID MODULO NUMERO
'''
    if len(p) == 4:
        p[0] = ('OPERACOES', p[1], p[2], p[3])
    else: 
        p[0] = ('OPERACOES', p[1], p[2], p[3], p[4], p[5])

# Regra auxiliar para parâmetros
def p_parameters(p):
    '''parameters : parameter
                | parameter COMMA parameters
                | empty'''
    if len(p) == 2:
        p[0] = ('PARAMETERS', p[1])
    elif len(p) == 4:
        p[0] = ('PARAMETERS', p[1], p[2], p[3])
    else:
        p[0] = ('PARAMETERS', None)  # Para o caso de "empty"

# Regra auxiliar para parâmetro
def p_parameter(p):
    '''parameter : ID
                | type ID
                | type ID LBRACKETS RBRACKETS
                | type ELLIPSIS ID'''
    if len(p) == 3:
        p[0] = ('PARAMETER', p[1], p[2])
    elif len(p) == 5:
        p[0] = ('PARAMETER', p[1], p[2], p[3], p[4])
    elif len(p) == 4:
        p[0] = ('PARAMETER', p[1], p[2], p[3])

# 7º Regra: Comentário
def p_comment(p):
    '''comment : SINGLE_LINE_COMMENT
            | MULTI_LINE_COMMENT'''
    p[0] = ('COMMENT', p[1])

# 8ª Regra: Expressões
def p_expression(p):
    '''expression : atribuicao'''
    p[0] = p[1]

# Regras para Atribuição
def p_atribuicao(p):
    '''atribuicao : expressao_logica
                | ID PLUS EQUAL expressao_logica
                | ID MINUS EQUAL expressao_logica
                | ID TIMES EQUAL expressao_logica
                | ID DIVIDE EQUAL expressao_logica
                | ID MODULO EQUAL expressao_logica'''
    if len(p) == 2:
        p[0] = ('ATRIBUICAO', p[1])
    elif len(p) == 4: 
        p[0] = ('ATRIBUICAO', p[1], p[2], p[3])
    else: 
        p[0] = ('ATRIBUICAO', p[1], p[2], p[3], p[4])

# 9º regra: Estruturas de Controle
def p_declaration_structure(p):
    '''declaration_structure : if_structure
                        | while_structure
                        | for_structure
                        | switch_structure
                        | break_structure
                        | continue_structure
                        | return_structure
                        | print_structure'''
    p[0] = p[1]

# Regra print
def p_print_structure(p):
    '''print_structure : PRINT LPAREN VSTRING RPAREN
                | PRINT LPAREN NUMERO RPAREN
                | PRINT LPAREN ID RPAREN
                | PRINT LPAREN expression RPAREN'''
    p[0] = ('PRINT_STRUCTURE', p[1], p[2], p[3], p[4])

# Regras para if
def p_if_structure(p):
    '''if_structure : IF expression COLON declaration
                    | IF NOT expression COLON declaration
                    | IF expression NOT IN expression COLON declaration
                    | IF expression COLON declaration else_structure
                    | IF NOT expression COLON declaration else_structure
                    | IF expression NOT IN expression COLON declaration else_structure'''
    if len(p) == 5:
        p[0] = ('IF_STRUCTURE', p[1], p[2], p[3], p[4])
    elif len(p) == 6: 
        p[0] = ('IF_STRUCTURE', p[1], p[2], p[3], p[4], p[5])
    elif len(p) == 7: 
        p[0] = ('IF_STRUCTURE', p[1], p[2], p[3], p[4], p[5], p[6])
    else:
        p[0] = ('IF_STRUCTURE', p[1], p[2], p[3], p[4], p[5], p[6], p[7])

def p_else_structure(p):
    '''else_structure : ELIF expression COLON declaration
                    | ELIF NOT expression COLON declaration
                    | ELIF expression NOT IN expression COLON declaration
                    | ELSE COLON declaration'''
    if len(p) == 5:
        p[0] = ('ELSE_STRUCTURE', p[1], p[2], p[3], p[4])
    elif len(p) == 6: 
        p[0] = ('ELSE_STRUCTURE', p[1], p[2], p[3], p[4], p[5])
    elif len(p) == 8: 
        p[0] = ('ELSE_STRUCTURE', p[1], p[2], p[3], p[4], p[5], p[6], p[7])
    else:
        p[0] = ('ELSE_STRUCTURE', p[1], p[2], p[3])

# Regras para while
def p_while_structure(p):
    '''while_structure : WHILE expression COLON declaration'''
    p[0] = ('WHILE', p[2], p[4])

# Regras para for
def p_for_structure(p):
    '''for_structure : FOR ID IN primaria COLON declaration
                    | FOR ID IN RANGE LPAREN primaria RPAREN COLON declaration
                    | FOR ID COMMA ID IN ID COLON declaration'''
    if len(p) == 7: 
        p[0] = ('FOR_STRUCTURE', p[1], p[2], p[3], p[4], p[5], p[6])
    elif len(p) == 9:
        p[0] = ('FOR_STRUCTURE', p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])
    else:
        p[0] = ('FOR_STRUCTURE', p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9])

# Regras para switch
def p_switch_structure(p):
    '''switch_structure : SWITCH expression COLON case_list'''
    p[0] = ('SWITCH', p[2], p[4])

# Regras para break
def p_break_structure(p):
    '''break_structure : BREAK'''
    p[0] = ('BREAK',)

# Regras para continue
def p_continue_structure(p):
    '''continue_structure : CONTINUE'''
    p[0] = ('CONTINUE',)

# Regras para return
def p_return_structure(p):
    '''return_structure : RETURN expression'''
    p[0] = ('RETURN', p[2])

# Regras para Case list
def p_case_list(p):
    '''case_list : case_declaration_star'''
    p[0] = ('CASE_LIST', p[1])

def p_case_declaration_star(p):
    '''case_declaration_star : empty
                            | case_declaration_star case_declaration'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_case_declaration(p):
    '''case_declaration : CASE expression COLON
                    | DEFAULT COLON'''
    if len(p) == 3:
        p[0] = ('CASE', p[1], p[2], p[3])
    else:
        p[0] = ('DEFAULT', p[1], [2])

# 11º regra: Arrays
def p_array(p):
    '''array : ID LBRACKETS NUMERO RBRACKETS
            | ID LBRACKETS empty RBRACKETS'''
    if len(p) == 5:
        p[0] = ('ARRAY', p[1], p[3])
    else:
        p[0] = ('ARRAY', p[1])

# Expressão lógica
def p_expressao_logica(p):
    '''expressao_logica : expressao_relacional
                        | NOT expressao_logica
                        | expressao_logica AND expressao_logica
                        | expressao_logica OR expressao_logica'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = (p[1], p[2], p[3])

# Expressão relacional
def p_expressao_relacional(p):
    '''expressao_relacional : expressao_aritmetica
                            | expressao_relacional MAIOR expressao_relacional
                            | expressao_relacional MAIOR EQUAL expressao_relacional
                            | expressao_relacional MENOR expressao_relacional
                            | expressao_relacional MENOR EQUAL expressao_relacional
                            | expressao_relacional NOT EQUAL expressao_relacional
                            | expressao_relacional EQUAL EQUAL expressao_relacional'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    else:
        p[0] = (p[1], p[2], p[3], p[4])

# Expressão aritmetica
def p_expressao_aritmetica(p):
    '''expressao_aritmetica : expressao_multiplicativa
                            | expressao_aritmetica PLUS expressao_aritmetica
                            | expressao_aritmetica MINUS expressao_aritmetica'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2], p[3])

# Expressão multiplicativa
def p_expressao_multiplicativa(p):
    '''expressao_multiplicativa : primaria
                                | expressao_multiplicativa TIMES expressao_multiplicativa
                                | expressao_multiplicativa DIVIDE expressao_multiplicativa
                                | expressao_multiplicativa MODULO expressao_multiplicativa '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2], p[3])

# Primaria
def p_primaria(p):
    '''primaria : ID
                | NUMERO
                | VSTRING
                | LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2], p[3])

# ERRO
def p_error(p):
    print(f"Erro de sintaxe: Token inesperado '{p.value}' linha {p.lineno}")
    raise Exception("Erro de sintaxe")

print('\n_____________ANALISADOR SINTATICO____________\n')

#Cria o sintatico
parser = yacc.yacc()

try:
    result = parser.parse(data, lexer=lexer)
    print('Não foi encontrado nenhum erro.')
    
except Exception as e:
    print('Não foi possivel construir árvore sintática.')