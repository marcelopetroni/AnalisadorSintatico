import ply.yacc as yacc
from lexico import *

#ANALISADOR SINTATICO:

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

# 2º Regra: declaração
def p_declaration(p):
    '''declaration : declaration_variable
                   | declaration_function
                   | declaration_structure
                   | comment'''
    p[0] = ('DECLARATION', p[1])

# 3º Regra: declaração de variavel
def p_declaration_variable(p):
    '''declaration_variable : type ID 
                           | type ID EQUAL expression
                           | type ID EQUAL NUMERO
                           | type ID EQUAL ID
                           | type ID EQUAL VSTRING
                           | type ID EQUAL LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = (p[1])
    if len(p) == 3:
        p[0] = ('DECLARATION_VARIABLE', p[1], p[2])
    else: 
        p[0] = ('DECLARATION_VARIABLE', p[1], p[2], p[4])

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
    '''declaration_function : type ID LPAREN parameters RPAREN block'''
    p[0] = ('DECLARATION_FUNCTION', p[1], p[2], p[4], p[6])

# Regra auxiliar para parâmetros
def p_parameters(p):
    '''parameters : parameter
                  | parameter COMMA parameters
                  | empty'''
    if len(p) == 2:
        p[0] = ('PARAMETERS', p[1])
    elif len(p) == 4:
        p[0] = ('PARAMETERS', p[1], p[3])
    else:
        p[0] = ('PARAMETERS', None)  # Para o caso de "empty"

# Regra auxiliar para parâmetro
def p_parameter(p):
    '''parameter : type ID
                 | type ID LBRACKETS RBRACKETS
                 | type ELLIPSIS ID'''
    if len(p) == 3:
        p[0] = ('PARAMETER', p[1], p[2])
    elif len(p) == 5:
        p[0] = ('PARAMETER', p[1], p[2], p[3], p[4])
    elif len(p) == 4:
        p[0] = ('PARAMETER', p[1], p[2], p[3])

# 6º Regra: Bloco
def p_block(p):
    '''block : LBRACE declaration RBRACE'''
    p[0] = ('BLOCK', p[2])

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
    '''atribuicao : ID EQUAL expressao_logica
                  | ID PLUS EQUAL expressao_logica
                  | ID MINUS EQUAL expressao_logica
                  | ID TIMES EQUAL expressao_logica
                  | ID DIVIDE EQUAL expressao_logica
                  | ID MODULO EQUAL expressao_logica
                  | ID AND EQUAL expressao_logica
                  | ID OR EQUAL expressao_logica'''
    if len(p) == 4:
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
                        | return_structure'''
    p[0] = p[1]
    
# Regras para if
def p_if_structure(p):
    '''if_structure : IF LPAREN expression RPAREN block
                    | IF LPAREN expression RPAREN block ELSE block'''
    if len(p) == 6:
        p[0] = ('IF', p[3], p[5])
    elif len(p) == 8:
        p[0] = ('IF', p[3], p[5], 'ELSE', p[7])

# Regras para while
def p_while_structure(p):
    '''while_structure : WHILE LPAREN expression RPAREN block'''
    p[0] = ('WHILE', p[3], p[5])

# Regras para for
def p_for_structure(p):
    '''for_structure : FOR LPAREN expression SEMICOLON expression SEMICOLON expression RPAREN block'''
    p[0] = ('FOR', p[3], p[5], p[7], p[9])

# Regras para switch
def p_switch_structure(p):
    '''switch_structure : SWITCH LPAREN expression RPAREN case_list'''
    p[0] = ('SWITCH', p[3], p[5])

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
    '''case_declaration : CASE expression COLON block
                       | DEFAULT COLON block'''
    if len(p) == 5:
        p[0] = ('CASE', p[2], p[4])
    else:
        p[0] = ('DEFAULT', p[3])

# 11º regra: Arrays
def p_array(p):
    '''array : ID LBRACKETS expression RBRACKETS
             | ID LBRACKETS RBRACKETS'''
    if len(p) == 5:
        p[0] = ('ARRAY', p[1], p[3])
    else:
        p[0] = ('ARRAY', p[1])

# Expressão lógica
def p_expressao_logica(p):
    '''expressao_logica : expressao_relacional
                        | NOT expressao_relacional
                        | expressao_logica AND expressao_relacional
                        | expressao_logica OR expressao_relacional'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = ('NOT', p[2])
    else:
        p[0] = (p[1], p[2], p[3])

# Expressão relacional
def p_expressao_relacional(p):
    '''expressao_relacional : expressao_aritmetica
                             | expressao_aritmetica MAIOR expressao_aritmetica
                             | expressao_aritmetica MAIOR EQUAL expressao_aritmetica
                             | expressao_aritmetica MENOR expressao_aritmetica
                             | expressao_aritmetica MENOR EQUAL expressao_aritmetica
                             | expressao_aritmetica NOT EQUAL expressao_aritmetica
                             | expressao_aritmetica EQUAL EQUAL expressao_aritmetica'''
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
    '''expressao_multiplicativa : expressao_unaria
                                 | expressao_multiplicativa TIMES expressao_multiplicativa
                                 | expressao_multiplicativa DIVIDE expressao_multiplicativa
                                 | expressao_multiplicativa MODULO expressao_multiplicativa '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2], p[3])

# Expressão unaria
def p_expressao_unaria(p):
    '''expressao_unaria : expressao_postfix
                        | PLUS expressao_unaria
                        | MINUS expressao_unaria'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = (p[1], p[2])
    else: 
        p[0] = (p[1], p[2], p[3])

# Expressão postfix
def p_expressao_postfix(p):
    '''expressao_postfix : primaria
                         | primaria LBRACKETS expression RBRACKETS
                         | primaria LPAREN argumentos RPAREN
                         | primaria DOT ID '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = (p[1])
    else:
        p[0] = (p[1], p[3])

# Expressão argumentos
def p_argumentos(p):
    '''argumentos : array
                  | empty'''
    if p[1] is not None:
        p[0] = p[1]
    else:
        p[0] = []

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