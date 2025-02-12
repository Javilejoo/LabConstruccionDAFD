'''
Algoritmo para transformar una expresion regular a un AFD directamente
1) aumentar la expresion regular con un simbolo de fin de cadena (#)
'''
import shuntingyard as sy
import funciones as fun
def aumentarER(expresion):
    return expresion + '#' #Aumentar la expresion regular con un simbolo de fin de cadena
expresion = fun.leerER("ER.txt") #Leer la expresion regular de un archivo


def ERtoAFD(expresion):
    expresion = sy.convert_infix_to_postfix(aumentarER(expresion))
    sy.generate_expression_tree_image(expresion)

ERtoAFD(expresion) #Convertir la expresion regular a un AFD directo