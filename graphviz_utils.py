import graphviz as gv

def draw_expression_tree(node, graph=None, parent=None, node_id=0):
    """Dibuja un árbol de expresión regular con Graphviz y lo guarda como imagen."""
    if graph is None:
        graph = gv.Digraph(comment="Árbol de Expresión", format="png")

    if node:
        current_id = str(node_id)
        label = f"{node.value}"  # Etiqueta con el valor del nodo
        if node.pos_id is not None:
            label += f"\n({node.pos_id})"  # Agregar pos_id si existe
        
        graph.node(current_id, label=label)

        if parent is not None:
            graph.edge(parent, current_id)

        node_id = draw_expression_tree(node.left, graph, current_id, node_id + 1)
        node_id = draw_expression_tree(node.right, graph, current_id, node_id + 1)

    return node_id

def generate_expression_tree_image(root, output_filename="expression_tree"):
    """Genera y guarda la imagen del árbol de expresión regular."""
    graph = gv.Digraph(format='png')
    draw_expression_tree(root, graph)
    graph.render(output_filename, format='png', cleanup=True)
    print(f"Árbol de expresión guardado como {output_filename}.png")