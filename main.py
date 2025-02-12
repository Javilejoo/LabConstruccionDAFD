import funciones as fun
import shuntingyard as sy


def main():
    print("Lab 1: Construcción de AFD Directo")
    expresion = fun.leerER("ER.txt")
    print("Convertiendo la expresión regular a postfix...")
    postfix_expr = sy.convert_infix_to_postfix(expresion)
    print("Expresión regular en postfix: ", postfix_expr)
    sy.generate_expression_tree_image(postfix_expr)


if __name__ == "__main__":
    main()
