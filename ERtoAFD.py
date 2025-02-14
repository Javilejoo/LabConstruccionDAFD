'''
Algoritmo para transformar una ezpresion regular a un AFD directamente
1) aumentar la expresion regular con un simbolo de fin de expresion (#)
2) convertir la expresion regular a postfijo (shutingyard algorithm)
3) construir el arbol de expresion
4) asignar identificadores de posicion a los nodos hoja del arbol (simbolos no operadores)
5) calcular si un nodo es nullable
6) Calcular firstpos
7) Calcular lastpos
'''
import shuntingyard as sy
import funciones as fun
import estructuras
import graphviz_utils as gv_utils
from nullableVisitor import NullableVisitor
from firstPosVisitor import FirstPosVisitor
from lastPosVisitor import LastPosVisitor

def print_tree(node, level=0):
    """Imprime el árbol de expresión con identificadores de posición."""
    if node is not None:
        print_tree(node.right, level + 1)
        print(' ' * 4 * level + f'-> {node.value} (id={node.pos_id}) (nullable={node.nullable})')
        print_tree(node.left, level + 1)

def ERtoAFD(expresion):

    def aumentarER(expresion):
        return expresion + '#'

    postfix = sy.convert_infix_to_postfix(aumentarER(expresion))
    root = estructuras.build_expression_tree(postfix)

    def assign_pos_ids(root):
        counter = [1]  # Contador de posiciones para nodos hoja

        def traverse(node):
            if node is None:
                return
            if node.value != 'ε':
                if node.left is None and node.right is None:
                    node.pos_id = counter[0]
                    counter[0] += 1
            
                traverse(node.left)
                traverse(node.right)

        traverse(root)
        return root

    assign_pos_ids(root)
    visitorNull = NullableVisitor()
    root.accept(visitorNull)
    visitorFirstPos = FirstPosVisitor()
    root.accept(visitorFirstPos)
    visitorLastPos = LastPosVisitor()
    root.accept(visitorLastPos)
    gv_utils.generate_expression_tree_image(root, "expression_tree")

# Leer la expresión regular desde archivo
expresion = fun.leerER("ER.txt")
ERtoAFD(expresion)
