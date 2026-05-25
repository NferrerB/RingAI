from aima3.search import Problem, astar_search




class ProblemaConMemoria(Problem):
    def __init__(self, initial, goal, graph,visitados=None):
        # El estado inicial es ('1', frozenset(['1']))
        super().__init__((initial, frozenset([initial])), (goal, None))
        self.graph = graph
        self.visited = visitados
    def actions(self, state):
        nodo_actual, visitados_en_ruta = state
        # Combinamos los ya visitados en esta ruta con los que ya se tenían registrados en turnos anteriores
        visitados_totales = visitados_en_ruta | self.visited        
        
        if nodo_actual == '10':
            return []
            
        acciones_validas = []
        for destino in self.graph[nodo_actual].keys():
            # Bloqueo de repetición
            if destino in visitados_totales and destino != '0':
                continue
                
            # Bloqueo para evitar anillos de plata antes de los de bronce
            if destino in ['7', '8', '9']:
                if not all(str(i) in visitados_totales for i in range(1, 7)):
                    continue
                    
            # Bloqueo para evitar anillos de oro antes de los de bronce y plata
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

