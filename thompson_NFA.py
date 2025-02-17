import graphviz

operadores = {'+', '?', '*', '|', '.', '(', ')'}


class AFN:
    def __init__(self):
        self.inicial = None
        self.aceptacion = None
        self.transiciones = {}

    def agregar_transicion(self, origen, destino, simbolo):
        if origen not in self.transiciones:
            self.transiciones[origen] = []
        self.transiciones[origen].append((simbolo, destino))

    def visualizar(self):
        dot = graphviz.Digraph(comment='AFN')
        for estado in self.transiciones:
            for transicion in self.transiciones[estado]:
                simbolo, destino = transicion
                dot.edge(str(estado), str(destino), label=simbolo)
        # Estado inicial con etiqueta 'start' y color verde
        dot.node(str(self.inicial), shape='circle', color='green', style='filled', label='start')
        # Estado de aceptación con etiqueta 'final' y color rojo
        dot.node(str(self.aceptacion), shape='doublecircle', color='red', style='filled', label='final')
        return dot

    def simular(self, cadena, estado_actual=None, indice=0):
        if estado_actual is None:
            estado_actual = {self.inicial}

        if indice == len(cadena):
            return self.aceptacion in estado_actual

        nuevos_estados = set()
        for estado in estado_actual:
            if estado in self.transiciones:
                for simbolo, destino in self.transiciones[estado]:
                    if simbolo == 'ε':
                        nuevos_estados.add(destino)
                    elif simbolo == cadena[indice]:
                        nuevos_estados.add(destino)

        if not nuevos_estados:
            return False

        return self.simular(cadena, nuevos_estados, indice + 1)


def generar_AFN(postfix):
    pila = []
    contador_estados = 0

    for char in postfix:
        if char not in operadores:  # Operando (ejemplo: 'a', 'b')
            afn = AFN()
            afn.inicial = contador_estados
            afn.aceptacion = contador_estados + 1
            afn.agregar_transicion(afn.inicial, afn.aceptacion, char)
            contador_estados += 2
            pila.append(afn)
        else:  # Operador
            if char == '*':  # Operador de Kleene
                afn1 = pila.pop()
                afn = AFN()
                afn.inicial = contador_estados
                afn.aceptacion = contador_estados + 1
                # Transiciones epsilon
                afn.agregar_transicion(afn.inicial, afn1.inicial, 'ε')
                afn.agregar_transicion(afn1.aceptacion, afn1.inicial, 'ε')
                afn.agregar_transicion(afn.inicial, afn.aceptacion, 'ε')
                afn.agregar_transicion(afn1.aceptacion, afn.aceptacion, 'ε')
                afn.transiciones.update(afn1.transiciones)
                contador_estados += 2
                pila.append(afn)
            
            elif char == '|':  # Operador de Unión
                afn2 = pila.pop()
                afn1 = pila.pop()
                afn = AFN()
                afn.inicial = contador_estados
                afn.aceptacion = contador_estados + 1
                # Transiciones epsilon
                afn.agregar_transicion(afn.inicial, afn1.inicial, 'ε')
                afn.agregar_transicion(afn.inicial, afn2.inicial, 'ε')
                afn.agregar_transicion(afn1.aceptacion, afn.aceptacion, 'ε')
                afn.agregar_transicion(afn2.aceptacion, afn.aceptacion, 'ε')
                afn.transiciones.update(afn1.transiciones)
                afn.transiciones.update(afn2.transiciones)
                contador_estados += 2
                pila.append(afn)
            
            elif char == '.':  # Operador de Concatenación
                afn2 = pila.pop()
                afn1 = pila.pop()
                afn = AFN()
                afn.inicial = afn1.inicial
                afn.aceptacion = afn2.aceptacion
                afn.transiciones.update(afn1.transiciones)
                afn.transiciones.update(afn2.transiciones)
                afn.agregar_transicion(afn1.aceptacion, afn2.inicial, 'ε')
                pila.append(afn)

    return pila.pop()


def main():
    with open('expresiones_regulares/postfix_expressions.txt', 'r', encoding='utf-8') as file:
        postfix_list = file.readlines()

    for i, postfix in enumerate(postfix_list):
        postfix = postfix.strip()
        print(f"Expresión postfix: {postfix}")
        afn = generar_AFN(postfix)
        afn.visualizar().render(f'nfa_graph_{i}')
        print(f"AFN visualizado como nfa_graph_{i}.png generado.\n")

        # Simulación del AFN
        cadena = input("Ingrese una cadena para simular en el AFN: ")
        if afn.simular(cadena):
            print(f"La cadena '{cadena}' es aceptada por el AFN.\n")
        else:
            print(f"La cadena '{cadena}' no es aceptada por el AFN.\n")


if __name__ == "__main__":
    main()