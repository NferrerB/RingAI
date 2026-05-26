import random
import heapq
import collections
from collections import deque
from ProblemaLaberint import Problem, ProblemaConMemoria, astar_search
#from distanceCalculator import encontrar_distancia_minima

# --- CONFIGURACIÓN ---
TAMAÑO = 12
BRONZE = 6
PLATA = 3
ORO = 1
BARRERAS = [5, 4, 3, 3, 3]




class LaberintAnellOr:
    def __init__(self):
        self.tablero = [['.' for _ in range(TAMAÑO)] for _ in range(TAMAÑO)]
        self.barreras = []
        self.anillos = {'B': [], 'P': [], 'O': []}
        self.anillos_pos_number = {}
        self.anillos_pendientes = {1,2,3,4,5,6,7,8,9,10}
        self.posicion = None
        self.recojidos = {'B': 0, 'P': 0, 'O': 0}
        self.pasos = 0
        self.nodo_meta = None
        self.mapa=None
        self.heuristica = {}
        self.problema=None
        self.iniciarJuego()
        self.minimo_coste=0;
        
    def iniciarJuego(self):
        # 1. Col·locar barreres
        for mida in BARRERAS:
            self.colocarBarrera(mida)
        
        # 2. Col·locar anells
        self.anillos['B'] = self.colocarItems('B', BRONZE,0)
        self.anillos['P'] = self.colocarItems('P', PLATA,BRONZE)
        self.anillos['O'] = self.colocarItems('O', ORO,BRONZE+PLATA)
        # 3. Posició jugador
        self.posicion = self.getPosicionLibre()
        self.mapa, self.heuristica, self.problema = self.calcular_ruta()
      

        def calcular_h(nodo):
            # La heurística depende del nodo actual dentro del estado
            nodo_actual, _ = nodo.state
            return self.heuristica.get(nodo_actual, 0)
        #Calcul de la ruta desde el punt inicial amb A*
        self.nodo_meta = astar_search(self.problema, h=calcular_h)

    def recalcular_ruta(self):
        # Cada vez que se mueve el jugador, recalculamos el mapa, la heurística y el problema para reflejar los cambios en el estado del juego
        self.mapa, self.heuristica, self.problema = self.calcular_ruta()
        def calcular_h(nodo):
            # La heurística depende del nodo actual dentro del estado
            nodo_actual, _ = nodo.state
            return self.heuristica.get(nodo_actual, 0)
        # Recalculamos la ruta desde el punto actual con A*
        self.nodo_meta = astar_search(self.problema, h=calcular_h)
        if(self.minimo_coste==0):
            self.minimo_coste=self.nodo_meta.path_cost
    def calcular_ruta(self):
        # Para calcular el mapa de conexiones entre nodos, necesitamos considerar las posiciones actuales de los anillos pendientes y el jugador, y calcular los pasos mínimos entre ellos teniendo en cuenta las barreras.
        nodos = [str(i) for i in range(0, 11)]
        mapa_total = {nodo: {} for nodo in nodos}
        # Calculamos los pasos mínimos entre cada par de nodos relevantes (jugador y anillos pendientes)
        for anilloOri in range(1, 7):
            for anilloDest in range(1, 11):
                if(anilloOri != anilloDest) and  (anilloOri  in self.anillos_pendientes and anilloDest  in self.anillos_pendientes):
                    mapa_total[(str(anilloOri))][str(anilloDest)] = self.calcular_pasos(self.anillos_pos_number.get(str(anilloOri)), self.anillos_pos_number.get(str(anilloDest)))
        for anilloOri in range(7,10):
            for anilloDest in range(1, 11):
                if(anilloOri != anilloDest and  (anilloOri  in self.anillos_pendientes and anilloDest  in self.anillos_pendientes)):
                    mapa_total[(str(anilloOri))][str(anilloDest)] = self.calcular_pasos(self.anillos_pos_number.get(str(anilloOri)), self.anillos_pos_number.get(str(anilloDest)))
        for anilloDest in range(1, 11):
            if(10 != anilloDest and (anilloOri  in self.anillos_pendientes and anilloDest  in self.anillos_pendientes)):
                mapa_total[('10')][str(anilloDest)] = self.calcular_pasos(self.anillos_pos_number.get('10'), self.anillos_pos_number.get(str(anilloDest)))
        
        # Calculamos los pasos mínimos desde la posición actual del jugador a cada anillo pendiente, y viceversa
        for anilloDest in range(1, 11):
            if((anilloDest  in self.anillos_pendientes)):
                mapa_total['0'][str(anilloDest)] = self.calcular_pasos(self.posicion, self.anillos_pos_number.get(str(anilloDest)))
                mapa_total[(str(anilloOri))]['0'] = self.calcular_pasos(self.anillos_pos_number.get(str(anilloOri)), self.posicion)
        

        nodo_meta_id = '10'  # El anillo de oro es tu meta final
        pos_meta = self.anillos_pos_number.get(nodo_meta_id)
        for i in range(0, 11):
            nodo_actual_id = str(i)
            
            if nodo_actual_id == '0':
                # Distancia desde la posición actual del jugador hasta la meta
                pos_actual = self.posicion
            else:
                # Distancia desde la posición de este anillo hasta la meta
                pos_actual = self.anillos_pos_number.get(nodo_actual_id)
                
            if pos_actual and pos_meta:
                # Guardamos el cálculo geométrico aproximado en el diccionario de la heurística
                self.heuristica[nodo_actual_id] = self.heuristicaCalc(pos_actual, pos_meta)
            else:
                self.heuristica[nodo_actual_id] = 0

       # Para el problema de búsqueda, el estado incluirá la posición actual del jugador y un registro de los anillos ya visitados en esta ruta. Además, el problema tendrá conocimiento de los anillos que ya se han recogido en turnos anteriores para aplicar las reglas de bloqueo.
        anillos_visited = frozenset(['0'])
        for i in range(1, 11):
            if i not in self.anillos_pendientes:
                anillos_visited = anillos_visited | frozenset([str(i)])

        problema = ProblemaConMemoria(initial='0', goal='10', graph=mapa_total, visitados=anillos_visited)

        return mapa_total, self.heuristica, problema


    #def calcular_mejor_movimiento(self):






    def colocarBarrera(self, mida):
        colocada = False
        while not colocada:
            r= random.randint(0, TAMAÑO-1)
            c= random.randint(0, TAMAÑO-1)
            dirx = random.randint(-1, 1)
            diry = random.randint(-1, 1)
            caselles = []
            possible = True
            for i in range(mida):
                nr= r + dirx*i
                nc= c + diry*i
                if nr>=0 and nr < TAMAÑO and nc>=0 and nc < TAMAÑO and self.tablero[nr][nc] == '.':
                    caselles.append((nr, nc))
                else:
                    possible = False
                    break
            if possible:
                for br, bc in caselles:
                    self.tablero[br][bc] = 'X'
                colocada = True

    def colocarItems(self, rango, quantitat, offset):
        posicions = []
        for i in range(quantitat):
            r, c = self.getPosicionLibre()
            self.tablero[r][c] = rango
            posicions.append((r, c))
            # Guardamos la posición de cada anillo con su número correspondiente para facilitar la conversión entre nodos y posiciones reales
            self.anillos_pos_number[(str)(offset + i + 1)] = (r, c)
        return posicions

    def getPosicionLibre(self):
        while True:
            r, c = random.randint(0, TAMAÑO-1), random.randint(0, TAMAÑO-1)
            if self.tablero[r][c] == '.':
                return (r, c)

    # --- LÒGICA DE JOC ---
    def mover(self, nova_pos):
        r, c = nova_pos
        if not (0 <= r < TAMAÑO and 0 <= c < TAMAÑO) or self.tablero[r][c] == 'X':
            return False, "Moviment bloquejat per barrera."

        casilla = self.tablero[r][c]
        if casilla == 'P' and self.recojidos['B'] < BRONZE:
            print("Has de recoger todos los de bronze antes")
            return False
        if casilla == 'O' and self.recojidos['P'] < PLATA:
            print( "Has de recoger todos los de plata antes")
            return False

        if casilla in ['B', 'P', 'O']:
            self.recojidos[casilla] += 1
            for key, value in self.anillos_pos_number.items():
                if value == (r, c):
                    self.anillos_pendientes.discard(int(key))

                    break     
            self.tablero[r][c] = '.'
        
        self.posicion = nova_pos
        self.pasos += 1
        self.recalcular_ruta()
        print( "OK")
        return True

    def mostrar(self):
        print("\n  " + " ".join([hex(i)[2:].upper() for i in range(TAMAÑO)]))
        for i, fila in enumerate(self.tablero):
            display_fila = []
            for j, cell in enumerate(fila):
                if (i, j) == self.posicion: display_fila.append('J')
                else: display_fila.append(cell)
            print(f"{hex(i)[2:].upper()} {' '.join(display_fila)}")
        print(f"\nCost: {self.pasos}")
        print(f"Recollits: B:{self.recojidos['B']}/{BRONZE} P:{self.recojidos['P']}/{PLATA} O:{self.recojidos['O']}/{ORO}")

    def heuristicaCalc(self, pos1, pos2):
        return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))

    def calcular_pasos(self, inicio, destino):
        cola = deque([(inicio[0], inicio[1], 0)])
        
        visitados = set()
        visitados.add(inicio)
        
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while cola:
            fila_act, col_act, pasos = cola.popleft()
            
            if (fila_act, col_act) == destino:
                return pasos

            for df, dc in movimientos:
                nueva_f, nueva_c = fila_act + df, col_act + dc
                if(nueva_f >= 0 and nueva_f < TAMAÑO and nueva_c >= 0 and nueva_c < TAMAÑO):
                    casilla = self.tablero[nueva_f][nueva_c] 
                    if (self.tablero[nueva_f][nueva_c] != "X" and 
                        (nueva_f, nueva_c) not in visitados ):
                        if(self.tablero[inicio[0]][inicio[1]] == 'B' and self.tablero[destino[0]][destino[1]] == 'B'):
                            if(casilla == 'P' or casilla == 'O'):
                                continue
                        if(self.tablero[inicio[0]][inicio[1]] == 'P' and self.tablero[destino[0]][destino[1]] == 'P'):
                            if(casilla == 'O'):
                                continue
                        visitados.add((nueva_f, nueva_c))
                        cola.append((nueva_f, nueva_c, pasos + 1))
        return -1

# --- MAIN LOOP (SIMULACIÓ TEXT) ---
if __name__ == "__main__":
    juego = LaberintAnellOr()
    
    while True:
        juego.mostrar()
        juego.recalcular_ruta()
        if juego.recojidos['O'] == 1:
            print("VICTÒRIA! Has aconseguit l'anell d'or.")
            break
        if juego.pasos > juego.minimo_coste+5:
            print("Has superat el cost minim per més de 5. ¡Has perdut!")

        print(f"Passes fetes: {juego.pasos}   Cost mínim: {juego.minimo_coste}")
        print("\nComandaments: WASD per moure, 'h' per HINT, 'g' per GOD MODE, 'q' per sortir")
        
        cmd = input("Acció: ").lower()
        
        nova_pos = list(juego.posicion)
        #Elección de que hacer segun el comando del usuario
        if cmd == 'w': 
            nova_pos[0] -= 1
            juego.mover(tuple(nova_pos))
        elif cmd == 's': 
            nova_pos[0] += 1
            juego.mover(tuple(nova_pos))
        elif cmd == 'a': 
            nova_pos[1] -= 1
            juego.mover(tuple(nova_pos))
        elif cmd == 'd': 
            nova_pos[1] += 1
            juego.mover(tuple(nova_pos))
        elif cmd == 'g':
            print("\n--- GOD MODE: ---")
            juego.recalcular_ruta()
            if juego.nodo_meta:
                camino_nodos = juego.nodo_meta.path() 
                ruta_str = []
                for nodo in camino_nodos:
                    id_nodo = nodo.state[0]
                    if id_nodo == '0':
                        ruta_str.append(f"Jugador{juego.posicion}")
                    else:
                        pos = juego.anillos_pos_number.get(id_nodo)
                        ruta_str.append(f"Anillo {id_nodo}{pos}")
                print(" -> ".join(ruta_str))
            else:
                print("No se puede calcular una ruta válida.")
        elif cmd == 'h':
            print("\n--- HINT: ---")
            print("Próximo movimiento:")
            juego.recalcular_ruta()
            if juego.nodo_meta:
                camino_nodos = juego.nodo_meta.path()
                nodo=camino_nodos[1]
                id_nodo = nodo.state[0]
                pos = juego.anillos_pos_number.get(id_nodo)
                print(f"Anillo {id_nodo}{pos}")
            else:
                print("No se puede calcular una ruta válida.")
        elif cmd == 'q': break
