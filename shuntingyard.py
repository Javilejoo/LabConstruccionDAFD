import graphviz as gv
operadores = {'+', '?', '*', '|', '.', '(', ')'}
def get_precedence(operator):
    precedencia = {
        '|': 1,
        '.': 2,  
        '*': 3,
        '+': 1,
        '?': 1
    }
    return precedencia.get(operator, 0)


def expand_operators(expression):
    expanded_expression = []
    i = 0

    while i < len(expression):
        char = expression[i]

        if char == '+':
            if expanded_expression:
                if expanded_expression[-1] == ')':
                    # Manejo de paréntesis
                    open_parens = 0
                    j = len(expanded_expression) - 1
                    while j >= 0:
                        if expanded_expression[j] == ')':
                            open_parens += 1
                        elif expanded_expression[j] == '(':
                            open_parens -= 1
                        if open_parens == 0:
                            break
                        j -= 1
                    sub_expression = expanded_expression[j:]
                    expanded_expression.extend(sub_expression)
                    expanded_expression.append('*')
                else:
                    base = expanded_expression.pop()
                    expanded_expression.append(base)
                    expanded_expression.append('.')
                    expanded_expression.append(base)
                    expanded_expression.append('*')
            else:
                raise ValueError("Error de sintaxis: '+' debe estar precedido por un operando.")
        elif char == '?':
            if expanded_expression:
                base = expanded_expression.pop()
                expanded_expression.append('(')
                expanded_expression.append(base)
                expanded_expression.append('|')
                expanded_expression.append('ε')
                expanded_expression.append(')')
            else:
                raise ValueError("Error de sintaxis: '?' debe estar precedido por un operando.")
        else:
            # Insertar concatenación si es necesario
            if (expanded_expression and expanded_expression[-1] not in operadores and char not in operadores) or \
               (expanded_expression and expanded_expression[-1] in [')', '*'] and char not in operadores) or \
               (expanded_expression and expanded_expression[-1].isalnum() and char == '(') or \
               (expanded_expression and expanded_expression[-1] == ')' and char not in operadores):
                expanded_expression.append('.')
            expanded_expression.append(char)

        i += 1

    return ''.join(expanded_expression).replace('()', '')




def ShuntingYard(expresion):
    stack = []
    output = []
    i = 0
    while i < len(expresion):
        char = expresion[i]
        if char in operadores:
            if char == '(':
                stack.append(char)
            elif char == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            else:
                while stack and get_precedence(stack[-1]) >= get_precedence(char):
                    output.append(stack.pop())
                stack.append(char)
        else:
            output.append(char)
        i += 1
    while stack:
        output.append(stack.pop())
    return ''.join(output)

def convert_infix_to_postfix(expresion):
    expanded_expression = expand_operators(expresion)
    return ShuntingYard(expanded_expression)

#Crear arbol del postfix con graphviz
class Node:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class Stack:
    def __init__(self):
        self.stack = []
    
    def push(self, node):
        self.stack.append(node)
    
    def pop(self):
        if self.stack:
            return self.stack.pop()
        else:
            raise Exception("Stack is empty")

def build_expression_tree(postfix_expr):
    stack = Stack()
    
    for char in postfix_expr:
        if char in {'|', '.', '*'}:  # Operadores binarios y unarios
            if char in {'|', '.'}:  # Operadores binarios
                right = stack.pop()
                left = stack.pop()
                node = Node(char, left, right)
            else:  # Operador unario (*)
                operand = stack.pop()
                node = Node(char, operand, None)
        else:  # Operando (carácter)
            node = Node(char)
        
        stack.push(node)
    
    return stack.pop()

def draw_tree(node, graph=None, parent=None, node_id=0):
    """Función recursiva para construir el gráfico del árbol."""
    if graph is None:
        graph = gv.Digraph(comment="Árbol de Expresión")

    if node:
        current_id = str(node_id)
        graph.node(current_id, label=node.value)

        if parent is not None:
            graph.edge(parent, current_id)

        node_id = draw_tree(node.left, graph, current_id, node_id + 1)
        node_id = draw_tree(node.right, graph, current_id, node_id + 1)

    return node_id

def generate_expression_tree_image(postfix_expr, output_filename="expression_tree"):
    root = build_expression_tree(postfix_expr)
    graph = gv.Digraph(format='png')
    draw_tree(root, graph)
    graph.render(output_filename, format='png', cleanup=True)
    print(f"Árbol de expresión guardado como {output_filename}.png")


