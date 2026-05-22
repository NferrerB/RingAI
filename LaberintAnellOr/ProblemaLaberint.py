from aima3.search import Problem, astar_search

# 1. Un grafo COMPLETAMENTE CONECTADO (Todos con todos)
# Para no escribir las 90 conexiones a mano, usamos un bucle para generarlo.
# Cada nodo se conecta con absolutamente todos los demás.
nodos = [str(i) for i in range(0, 11)]
mapa_total = {nodo: {} for nodo in nodos}
for origen in nodos:
    for destino in nodos:
        if origen != destino:
            # Asignamos un costo base de 2 (puedes cambiarlo si quieres)
            mapa_total[origen][destino] = 2

#mapa_total={'1': {'2': 5, '3': 7, '4': 11, '5': 4, '6': 9, '7': 16, '8': 4, '9': 5, '10': 12}, '2': {'1': 5, '3': 4, '4': 8, '5': 5, '6': 6, '7': 11, '8': 1, '9': 2, '10': 9}, '3': {'1': 7, '2': 4, '4': 12, '5': 3, '6': 2, '7': 9, '8': 5, '9': 6, '10': 13}, '4': {'1': 11, '2': 8, '3': 12, '5': 13, '6': 14, '7': 13, '8': 7, '9': 6, '10': 1}, '5': {'1': 4, '2': 5, '3': 3, '4': 13, '6': 5, '7': 12, '8': 6, '9': 7, '10': 14}, '6': {'1': 9, '2': 6, '3': 2, '4': 14, '5': 5, '7': 7, '8': 7, '9': 8, '10': 15}, '7': {'1': 16, '2': 11, '3': 9, '4': 13, '5': 12, '6': 7, '8': 12, '9': 13, '10': 14}, '8': {'1': 4, '2': 1, '3': 5, '4': 7, '5': 6, '6': 7, '7': 12, '9': 1, '10': 8}, '9': {'1': 5, '2': 2, '3': 6, '4': 6, '5': 7, '6': 8, '7': 13, '8': 1, '10': 7, '0': 5}, '10': {'1': 12, '2': 9, '3': 13, '4': 1, '5': 14, '6': 15, '7': 14, '8': 8, '9': 7}, '0': {'1': 2, '2': 7, '3': 9, '4': 9, '5': 6, '6': 11, '7': 18, '8': 6, '9': 5, '10': 10}}

# 2. Heurística básica admisible
heuristica = {str(i): 10 - i for i in range(0, 11)}

# 3. Clase del Problema Modificada
# El "estado" ya no es solo la ciudad actual, ahora es una tupla: (ciudad_actual, conjunto_de_visitados)
class ProblemaConMemoria(Problem):
    def __init__(self, initial, goal, graph,visitados=None):
        # El estado inicial es ('1', frozenset(['1']))
        super().__init__((initial, frozenset([initial])), (goal, None))
        self.graph = graph
        self.visited = visitados
    def actions(self, state):
        nodo_actual, visitados_en_ruta = state
        # Combinamos los ya visitados históricamente con los de la ruta actual del A*
        visitados_totales = visitados_en_ruta | self.visited        
        
        if nodo_actual == '10':
            return []
            
        acciones_validas = []
        for destino in self.graph[nodo_actual].keys():
            # --- MODIFICADO: Evita volver a pasar por anillos ya recolectados ---
            if destino in visitados_totales and destino != '0':
                continue
                
            # REGLA 1: Para ir a 7, 8, 9, debemos tener del 1 al 6
            if destino in ['7', '8', '9']:
                if not all(str(i) in visitados_totales for i in range(1, 7)):
                    continue
                    
            # REGLA 2: Para ir al 10, debemos tener del 7 al 9
            if destino == '10':
                if not all(str(i) in visitados_totales for i in range(7, 10)):
                    continue
            acciones_validas.append(destino)
        return acciones_validas

    def result(self, state, action):
        nodo_actual, visitados = state
        # El nuevo estado incluye la nueva posición y la añade al registro de visitados
        nuevo_visitados = visitados | frozenset([action])
        return (action, nuevo_visitados)

    def goal_test(self, state):
        nodo_actual, visitados_en_ruta = state
        # Combinamos lo que ya se recogió en turnos pasados con lo visitado en esta simulación
        visitados_totales = visitados_en_ruta | self.visited
        
        # Es meta si llegamos al 10 y ya se contemplaron TODOS los nodos (del 0 al 10 = 11 nodos)
        return nodo_actual == '10' and len(visitados_totales) == 11

    def path_cost(self, c, state1, action, state2):
        nodo_actual_1, _ = state1
        return c + self.graph[nodo_actual_1][action]

# 4. Ejecución del algoritmo
#problema = ProblemaConMemoria(initial='0', goal='10', graph=mapa_total)

#def calcular_h(nodo):
#    # La heurística depende del nodo actual dentro del estado
#    nodo_actual, _ = nodo.state
#    return heuristica.get(nodo_actual, 0)

#nodo_meta = astar_search(problema, h=calcular_h)

# 5. Traducir el resultado
#if nodo_meta:
    # Extraemos los nodos de la solución
#    camino = [nodo.state[0] for nodo in nodo_meta.path()]
#    print("Grafo 100% conectado. Camino forzado por reglas de estado:")
#    print(" -> ".join(camino))
#    print(f"Costo total: {nodo_meta.path_cost}")
#else:
#    print("No se encontró una ruta que cumpla las condiciones.")