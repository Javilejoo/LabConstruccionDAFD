#Importar librerias funciones.py
import funciones as fun
import shuntingyard as sy


def main():
    print("Lab 1: construccion de AFD directo")
    expresion = fun.leerER("ER.txt")
    print("Convertiendo la expresion regular a postfix...")
    shuntingyard = sy.convert_infix_to_postfix(expresion)
    print("Expresion regular en postfix: ", shuntingyard)
    sy.generate_expression_tree_image(shuntingyard)

if __name__ == "__main__":
    main()