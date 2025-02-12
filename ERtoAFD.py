'''
Algoritmo para transformar una expresion regular a un AFD directamente
1) aumentar la expresion regular con un simbolo de fin de cadena (#)
2) aplicar el algoritmo de shunting yard para convertir la expresion regular a postfijo
3) generar el arbol de expresion
4) agregar posicion de la hoja
'''
import shuntingyard as sy
import funciones as fun
def aumentarER(expresion):
    return expresion + '#' #Aumentar la expresion regular con un simbolo de fin de cadena

def assign_pos_ids(root):
    counter = [1]  # Contador mutable para evitar problemas de scope

    def traverse(node):
        if node is None:
            return
        
        # Si es una hoja (no tiene hijos)
        if node.left is None and node.right is None:
            node.pos_id = counter[0]
            counter[0] += 1
        else:
            # Recorrer hijos recursivamente
            traverse(node.left)
            traverse(node.right)

    traverse(root)
    return root

expresion = fun.leerER("ER.txt") #Leer la expresion regular de un archivo

# En ERtoAFD.py
def print_tree(node, level=0):
    if node is not None:
        print_tree(node.right, level + 1)
        print(' ' * 4 * level + f'-> {node}')
        print_tree(node.left, level + 1)

def ERtoAFD(expresion):
    expresion_aumentada = aumentarER(expresion)
    postfix = sy.convert_infix_to_postfix(expresion_aumentada)
    root = sy.build_expression_tree(postfix)
    assign_pos_ids(root)
    print_tree(root)  # <-- Imprimir todo el árbol
    sy.generate_expression_tree_image(postfix)

ERtoAFD(expresion) #Convertir la expresion regular a un AFD directo

    
