
from aima3.games import Game, GameState
from Player import Jugador, bloquear_jugador, devolver_carta_a_mazo, devolver_reserva_a_mazo, descartar_mano, desbloquear_jugador
from IA import IA, alphabeta_cutoff_search
from copy import deepcopy

class JuegoDeCartas(Game):
    def __init__(self, jugador, ia):
        """
        Inicializa el juego con un jugador humano y una IA.
        
        Args:
            jugador: Instancia de la clase Jugador (jugador humano)
            ia: Instancia de la clase IA (inteligencia artificial)
        """
        self.jugador = jugador
        self.ia = ia
        self.turno_actual = None  # Quién juega: 'jugador' o 'ia'
        self.juego_activo = True
        self.historial_turnos = []
        # Control de bloqueo: impide que la IA rebloquee en el turno siguiente al desbloqueo
        self.jugador_fue_desbloqueado_esta_ronda = False
        self.ia_fue_desbloqueada_esta_ronda = False
        
    def iniciar_juego(self):
        """Inicia el juego y comienza con el turno del jugador."""
        print(f"=== INICIO DEL JUEGO ===")
        print(f"Jugador: {self.jugador.nombre}")
        print(f"IA: {self.ia.nombre if hasattr(self.ia, 'nombre') else 'IA'}")
        print()
        self.turno_actual = 'jugador'
        
    def robar_carta_si_necesario(self, jugador_actual):
        """
        Al inicio del turno, roba una carta si la mano está vacía.
        
        Args:
            jugador_actual: El jugador cuyo turno es (Jugador o IA)
        """
        if jugador_actual.mano is None:
            carta_robada = jugador_actual.robar()
            nombre = jugador_actual.nombre if hasattr(jugador_actual, 'nombre') else "IA"
            if carta_robada:
                print(f"→ {nombre} roba una carta: {jugador_actual.mano.tipo}")
            else:
                print(f"⚠ {nombre} no pudo robar carta (mazo vacío)")
        
    def turno_jugador(self):
        """
        Ejecuta el turno del jugador humano.
        El jugador realiza acciones hasta que decide terminar su turno.
        """
        print(f"\n{'='*40}")
        print(f"TURNO DEL JUGADOR: {self.jugador.nombre}")
        print(f"{'='*40}")
        
        # Verificar si el jugador está bloqueado
        if self.jugador.bloqueado:
            print(f"✗ {self.jugador.nombre} está bloqueado y SALTA este turno.")
            desbloquear_jugador(self.jugador)
            self.jugador_fue_desbloqueado_esta_ronda = True  # Marcar que fue desbloqueado
            print(f"✓ {self.jugador.nombre} ha sido desbloqueado.")
            return
        
        # Robar carta al inicio del turno si es necesario
        self.robar_carta_si_necesario(self.jugador)
        
        # Mostrar estado actual
        self._mostrar_estado_jugador(self.jugador)
        
        # Loop de acciones del jugador
        accion_realizada = True
        while accion_realizada:
            print("\nOpciones disponibles:")
            print("1. Robar carta")
            print("2. Guardar en reserva")
            print("3. Descartar reserva")
            print("4. Descartar carta de la mano")
            print("5. Bloquear oponente")
            print("6. Devolver carta de la mano al mazo")
            print("7. Devolver carta de reserva al mazo")
            print("8. Terminar turno sin hacer nada")
            print("9. Salir del juego")
            
            opcion = input("\nSelecciona una opción (1-9): ").strip()
            
            if opcion == '1':
                if self.jugador.robar():
                    print(f"\n✓ Carta robada: {self.jugador.mano.tipo}")
                    accion_realizada = False  # Termina el turno después de robar
                else:
                    print("✗ No puedes robar (mano ocupada)")
                    
            elif opcion == '2':
                if self.jugador.guardar_en_reserva(None):
                    print(f"\n✓ Carta guardada en reserva: {self.jugador.reserva.tipo}")
                    accion_realizada = False  # Termina el turno después de guardar
                else:
                    print("✗ No puedes guardar (reserva ocupada o mano vacía)")
                    
            elif opcion == '3':
                if self.jugador.descartar_reserva():
                    print(f"\n✓ Reserva descartada")
                    accion_realizada = False  # Termina el turno después de descartar
                else:
                    print("✗ No tienes carta en reserva para descartar o no coincide con tu fase")

                    
            elif opcion == '4':
                print("\n✓ Intenta descartar la carta de tu mano.")
                carta_descartada = descartar_mano(self.jugador)
                if carta_descartada:
                    print(f"✓ Carta descartada: {carta_descartada.tipo}")
                    accion_realizada = False
                else:
                    print("✗ No puedes descartar (mano vacía o carta no coincide con tu fase)")

            elif opcion == '5':
                print("\n ✓ Bloquea a tu oponente (si no está bloqueado) y termina tu turno.")
                if bloquear_jugador(self.ia):
                    print("✓ Oponente bloqueado.")
                else:
                    print("✗ El oponente ya estaba bloqueado.")
                accion_realizada = False # Termina el turno después de bloquear
            elif opcion == '6':
                print("\n✓ Devuelve la carta de la mano al mazo.")
                devolver_carta_a_mazo(self.jugador)
                accion_realizada = False # Termina el turno después de devolver la carta
            elif opcion == '7':
                print("\n✓ Devuelve la carta de reserva al mazo.")
                if devolver_reserva_a_mazo(self.jugador):
                    print("✓ Reserva devuelta al mazo")
                    accion_realizada = False # Termina el turno después de devolver la reserva
                else:
                    print("✗ No tienes carta en reserva para devolver")
            elif opcion == '8':
                print("\n✓Termina tu turno sin hacer nada.")
                accion_realizada = False # Termina el turno sin hacer nada
            elif opcion == '9':
                print("\n✓ Salir de la partida.")
                exit()
            else:
                print("✗ Opción inválida. Intenta de nuevo.")
            
            self._mostrar_estado_jugador(self.jugador)
    
    def turno_ia(self):
        """
        Ejecuta el turno de la IA.
        La IA ejecuta su estrategia automáticamente.
        """
        print(f"\n{'='*40}")
        print(f"TURNO DE LA IA")
        print(f"{'='*40}")
        
        # Verificar si la IA está bloqueada
        if self.ia.bloqueado:
            print(f"✗ La IA está bloqueada y SALTA este turno.")
            desbloquear_jugador(self.ia)
            self.ia_fue_desbloqueada_esta_ronda = True  # Marcar que fue desbloqueada
            print(f"✓ La IA ha sido desbloqueada.")
            return
        
        # Robar carta al inicio del turno si es necesario
        self.robar_carta_si_necesario(self.ia)
        
        # Mostrar estado actual
        self._mostrar_estado_ia(self.ia)
        
        # Lógica de IA simplificada (puedes mejorarla después)
        print("\n→ La IA está pensando...")
        acciones_realizadas = self._ejecutar_estrategia_ia()
        
        print(f"✓ Turno de la IA finalizado ({acciones_realizadas} acciones realizadas)")
    
    def _ejecutar_estrategia_ia(self):
        """
        Ejecuta la estrategia de la IA usando alphabeta_cutoff_search.
        Retorna el número de acciones realizadas.
        """
        acciones = 0
        
        # Obtener el estado actual
        estado = self._serializar_estado()
        
        # Definir la función de corte (profundidad máxima de búsqueda)
        def cutoff_test(state, depth):
            return depth > 3  # Buscar hasta profundidad 3
        
        # Usar alphabeta_cutoff_search para encontrar la mejor acción
        mejor_accion = alphabeta_cutoff_search(
            estado, 
            self, 
            d=3,
            cutoff_test=cutoff_test,
            eval_fn=self.utility
        )
        
        if mejor_accion is None:
            return acciones
        
        # Ejecutar la mejor acción encontrada
        if mejor_accion == ('robar',):
            if self.ia.robar():
                print(f"  → IA roba una carta: {self.ia.mano.tipo}")
                acciones += 1
        
        elif mejor_accion == ('guardar_reserva',):
            if self.ia.guardar_en_reserva(None):
                print(f"  → IA guarda carta en reserva")
                acciones += 1
        
        elif mejor_accion == ('descartar_reserva',):
            if self.ia.descartar_reserva():
                print(f"  → IA descarta reserva")
                acciones += 1
        
        elif mejor_accion == ('devolver_reserva',):
            if self.ia.reserva is not None:
                self.ia.reserva = None
                print(f"  → IA devuelve reserva al mazo")
                acciones += 1
        
        elif mejor_accion == ('descartar_mano',):
            carta_descartada = descartar_mano(self.ia)
            if carta_descartada:
                print(f"  → IA descarta carta de la mano")
                acciones += 1
        
        elif mejor_accion == ('bloquear',):
            if bloquear_jugador(self.jugador):
                print(f"  → IA bloquea al jugador")
                acciones += 1
        
        elif mejor_accion == ('devolver_mazo',):
            devolver_carta_a_mazo(self.ia)
            print(f"  → IA devuelve carta de mano al mazo")
            acciones += 1
        
        return acciones
    
    def _mostrar_estado_jugador(self, jugador):
        """Muestra el estado actual del jugador."""
        print(f"\n📊 Estado de {jugador.nombre}:")
        print(f"  Fase: {jugador.fase_actual()}")
        print(f"  Bronce: {jugador.bronce}/6 | Plata: {jugador.plata}/3 | Oro: {jugador.oro}/1")
        print(f"  Mano: {jugador.mano.tipo if jugador.mano else 'Vacía'}")
        print(f"  Reserva: {jugador.reserva.tipo if jugador.reserva else 'Vacía'}")
    
    def _mostrar_estado_ia(self, ia):
        """Muestra el estado actual de la IA."""
        print(f"\n📊 Estado de la IA:")
        print(f"  Fase: {ia.fase_actual()}")
        print(f"  Bronce: {ia.bronce}/6 | Plata: {ia.plata}/3 | Oro: {ia.oro}/1")
        print(f"  Mano: {ia.mano.tipo if ia.mano else 'Vacía'}")
        print(f"  Reserva: {ia.reserva.tipo if ia.reserva else 'Vacía'}")
    
    def juego_terminado(self):
        """Verifica si el juego ha terminado."""
        # El juego termina cuando alguien completa todas las fases (Bronce, Plata, Oro)
        return (self.jugador.oro >= 1 or self.ia.oro >= 1)
    
    def determinar_ganador(self):
        """Determina quién ganó el juego."""
        if self.jugador.oro >= 1 and self.ia.oro < 1:
            return f"🏆 ¡{self.jugador.nombre} ha ganado!"
        elif self.ia.oro >= 1 and self.jugador.oro < 1:
            return "🏆 ¡La IA ha ganado!"
        else:
            return "🤝 ¡Empate!"
    
    def ejecutar_juego(self):
        """Bucle principal del juego."""
        self.iniciar_juego()
        
        numero_ronda = 1
        while self.juego_activo and not self.juego_terminado():
            print(f"\n{'#'*40}")
            print(f"RONDA {numero_ronda}")
            print(f"{'#'*40}")
            
            # Turno del jugador
            self.turno_jugador()
            
            if self.juego_terminado():
                break
            
            # Turno de la IA
            self.turno_ia()
            
            numero_ronda += 1
            
            # Resetear flags de desbloqueo para la siguiente ronda
            self.jugador_fue_desbloqueado_esta_ronda = False
            self.ia_fue_desbloqueada_esta_ronda = False
            
            # Pausa entre rondas
            input("\nPresiona Enter para continuar a la siguiente ronda...")
        
        # Fin del juego
        print(f"\n{'='*40}")
        print(f"FIN DEL JUEGO")
        print(f"{'='*40}")
        print(f"\nResultado Final:")
        print(f"  {self.jugador.nombre}: Bronce {self.jugador.bronce}/6 | Plata {self.jugador.plata}/3 | Oro {self.jugador.oro}/1")
        print(f"  IA: Bronce {self.ia.bronce}/6 | Plata {self.ia.plata}/3 | Oro {self.ia.oro}/1")
        print(f"\n{self.determinar_ganador()}")
    
    # Métodos requeridos por alphabeta_cutoff_search
    def to_move(self, state):
        """Retorna de quién es el turno en el estado actual."""
        return state['turno']
    
    def actions(self, state):
        """Retorna las acciones disponibles para la IA en el estado actual."""
        ia_state = state['ia']
        jugador_state = state['jugador']
        acciones = []
        
        # 1. Robar si la mano está vacía
        if ia_state['mano'] is None:
            acciones.append(('robar',))
        
        # 2. Guardar en reserva si hay carta en mano y reserva está vacía
        if ia_state['mano'] is not None and ia_state['reserva'] is None:
            acciones.append(('guardar_reserva',))
        
        # 3. Descartar reserva solo si coincide con la fase actual
        if ia_state['reserva'] is not None and ia_state['reserva']['tipo'] == ia_state['fase']:
            acciones.append(('descartar_reserva',))
        
        # 3b. Devolver reserva al mazo si NO coincide con la fase actual
        if ia_state['reserva'] is not None and ia_state['reserva']['tipo'] != ia_state['fase']:
            acciones.append(('devolver_reserva',))
        
        # 4. Descartar mano si coincide con la fase actual
        if ia_state['mano'] is not None and ia_state['mano']['tipo'] == ia_state['fase']:
            acciones.append(('descartar_mano',))
        
        # 5. Bloquear oponente si no está bloqueado
        if not jugador_state['bloqueado'] and not self.jugador_fue_desbloqueado_esta_ronda:
            acciones.append(('bloquear',))
        
        # 6. Devolver carta al mazo si hay carta en mano
        if ia_state['mano'] is not None:
            acciones.append(('devolver_mazo',))
        
        return acciones if acciones else [('pasar',)]
    
    def _obtener_fase(self, bronce, plata, oro):
        """Retorna la fase actual basada en los contadores."""
        if bronce < 6:
            return 'Bronce'
        elif plata < 3:
            return 'Plata'
        else:
            return 'Oro'
    
    def _serializar_estado(self):
        """Convierte el estado actual a un diccionario para alphabeta_cutoff_search."""
        return {
            'jugador': {
                'bronce': self.jugador.bronce,
                'plata': self.jugador.plata,
                'oro': self.jugador.oro,
                'mano': {'tipo': self.jugador.mano.tipo} if self.jugador.mano else None,
                'reserva': {'tipo': self.jugador.reserva.tipo} if self.jugador.reserva else None,
                'bloqueado': self.jugador.bloqueado,
                'fase': self.jugador.fase_actual()
            },
            'ia': {
                'bronce': self.ia.bronce,
                'plata': self.ia.plata,
                'oro': self.ia.oro,
                'mano': {'tipo': self.ia.mano.tipo} if self.ia.mano else None,
                'reserva': {'tipo': self.ia.reserva.tipo} if self.ia.reserva else None,
                'bloqueado': self.ia.bloqueado,
                'fase': self.ia.fase_actual()
            },
            'turno': 'ia'
        }
    
    def result(self, state, action):
        """Aplica la acción al estado y retorna el nuevo estado."""
        nuevo_estado = deepcopy(state)
        ia_state = nuevo_estado['ia']
        jugador_state = nuevo_estado['jugador']
        
        if action == ('robar',):
            # Simular robo de carta (asumimos que siempre hay cartas)
            ia_state['mano'] = {'tipo': 'Bronce'}  # Simplificación
        
        elif action == ('guardar_reserva',):
            if ia_state['mano'] is not None and ia_state['reserva'] is None:
                ia_state['reserva'] = ia_state['mano']
                ia_state['mano'] = None
        
        elif action == ('descartar_reserva',):
            if ia_state['reserva'] is not None:
                tipo_reserva = ia_state['reserva']['tipo']
                if tipo_reserva == 'Bronce' and ia_state['fase'] == 'Bronce':
                    ia_state['bronce'] += 1
                elif tipo_reserva == 'Plata' and ia_state['fase'] == 'Plata':
                    ia_state['plata'] += 1
                elif tipo_reserva == 'Oro' and ia_state['fase'] == 'Oro':
                    ia_state['oro'] += 1
                ia_state['reserva'] = None
                ia_state['fase'] = self._obtener_fase(ia_state['bronce'], ia_state['plata'], ia_state['oro'])
        
        elif action == ('devolver_reserva',):
            # Devuelve la reserva al mazo si no coincide con la fase actual
            ia_state['reserva'] = None
        
        elif action == ('descartar_mano',):
            if ia_state['mano'] is not None:
                tipo_mano = ia_state['mano']['tipo']
                if tipo_mano == 'Bronce':
                    ia_state['bronce'] += 1
                elif tipo_mano == 'Plata':
                    ia_state['plata'] += 1
                elif tipo_mano == 'Oro':
                    ia_state['oro'] += 1
                ia_state['mano'] = None
                ia_state['fase'] = self._obtener_fase(ia_state['bronce'], ia_state['plata'], ia_state['oro'])
        
        elif action == ('bloquear',):
            jugador_state['bloqueado'] = True
        
        elif action == ('devolver_mazo',):
            ia_state['mano'] = None
        
        return nuevo_estado
    
    def terminal_test(self, state):
        """Prueba si el estado es terminal (fin del juego)."""
        return state['ia']['oro'] >= 1 or state['jugador']['oro'] >= 1
    
    def utility(self, state, player=None):
        """Función de utilidad para evaluar un estado."""
        ia_state = state['ia']
        jugador_state = state['jugador']
        
        # Evaluación básica: considerar progreso en fases
        # Puntos por avance de fases
        ia_score = ia_state['bronce'] + ia_state['plata'] * 2 + ia_state['oro'] * 10
        jugador_score = jugador_state['bronce'] + jugador_state['plata'] * 2 + jugador_state['oro'] * 10
        
        # Bonificación si el oponente está bloqueado
        if jugador_state['bloqueado']:
            ia_score += 2
        
        return ia_score - jugador_score


if __name__ == '__main__':
    # Crear jugadores
    jugador_humano = Jugador("Jugador")
    ia_bot = IA("IA-Bot")
    
    # Crear y ejecutar el juego
    juego = JuegoDeCartas(jugador_humano, ia_bot)
    juego.ejecutar_juego()