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
        dot = graphviz.Digraph(comment='AFN',format='png')
        for estado in self.transiciones:
            for transicion in self.transiciones[estado]:
                simbolo, destino = transicion
                dot.edge(str(estado), str(destino), label=simbolo)
        # Estado inicial con etiqueta 'start' y color verde
        dot.node(str(self.inicial), shape='circle', color='green', style='filled', label='start')
        # Estado de aceptación con etiqueta 'final' y color rojo
        dot.node(str(self.aceptacion), shape='doublecircle', color='red', style='filled', label='final')
        return dot

    def calcular_cierre_epsilon(self, estados):
        """
        Calcula el cierre epsilon de un conjunto de estados.
        """
        stack = list(estados)
        cierre = set(estados)

        while stack:
            estado = stack.pop()
            if estado in self.transiciones:
                for simbolo, destino in self.transiciones[estado]:
                    if simbolo == 'ε' and destino not in cierre:
                        cierre.add(destino)
                        stack.append(destino)

        return cierre

    def simular_AFN(self, cadena):
        """
        Simula el AFN y determina si acepta la cadena.
        """
        estados_actuales = self.calcular_cierre_epsilon({self.inicial})  # Obtener cierre-epsilon del estado inicial

        for simbolo in cadena:
            nuevos_estados = set()

            # Procesar transiciones desde los estados actuales
            for estado in estados_actuales:
                if estado in self.transiciones:
                    for trans_simbolo, destino in self.transiciones[estado]:
                        if trans_simbolo == simbolo:
                            nuevos_estados.add(destino)

            # Expandir con cierre-epsilon los nuevos estados
            estados_actuales = self.calcular_cierre_epsilon(nuevos_estados)

        # Verificar si algún estado actual es de aceptación
        return self.aceptacion in estados_actuales



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