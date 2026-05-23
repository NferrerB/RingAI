
from aima3.games import Game, GameState
from Player import Jugador, devolver_carta_a_mazo

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
            print("4. Terminar turno")
            print("5. Bloquear oponente")
            
            opcion = input("\nSelecciona una opción (1-5): ").strip()
            
            if opcion == '1':
                if self.jugador.robar():
                    print(f"✓ Carta robada: {self.jugador.mano.tipo}")
                    accion_realizada = False  # Termina el turno después de robar
                else:
                    print("✗ No puedes robar (mano ocupada)")
                    
            elif opcion == '2':
                if self.jugador.guardar_en_reserva(None):
                    print(f"✓ Carta guardada en reserva: {self.jugador.reserva.tipo}")
                    accion_realizada = False  # Termina el turno después de guardar
                else:
                    print("✗ No puedes guardar (reserva ocupada o mano vacía)")
                    
            elif opcion == '3':
                if self.jugador.descartar_reserva():
                    print(f"✓ Reserva descartada")
                    print(f"  Fase actual: {self.jugador.fase_actual()}")
                    print(f"  Bronce: {self.jugador.bronce}/7 | Plata: {self.jugador.plata}/3 | Oro: {self.jugador.oro}/1")
                    accion_realizada = False  # Termina el turno después de descartar
                else:
                    print("✗ No tienes carta en reserva para descartar")
                    
            elif opcion == '4':
                print("\n✓ Devuelve la carta de tu mano al mazo (si tienes una) y termina tu turno.")
                devolver_carta_a_mazo(self.jugador)
                accion_realizada = False # Termina el turno sin descartar
            elif opcion == '5':
                print("\n ✓ Bloquea a tu oponente (si no está bloqueado) y termina tu turno.")
                bloquear_jugador(self.jugador)
                accion_realizada = False # Termina el turno después de bloquear
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
        Ejecuta la estrategia de la IA.
        Retorna el número de acciones realizadas.
        """
        acciones = 0
        
        # Estrategia simple: intenta descartar si puede, sino guarda en reserva
        # Esto puede mejorarse significativamente
        fase = self.ia.fase_actual()
        
        # Si tiene carta en mano y puede descartar, lo intenta
        if self.ia.reserva is not None and fase == 'Oro':
            if self.ia.descartar_reserva():
                print(f"  → IA descarta reserva")
                acciones += 1
        
        # Si tiene mano vacía, intenta guardar en reserva
        elif self.ia.mano is not None and self.ia.reserva is None:
            if self.ia.guardar_en_reserva(None):
                print(f"  → IA guarda carta en reserva: {self.ia.reserva.tipo}")
                acciones += 1
        
        return acciones
    
    def _mostrar_estado_jugador(self, jugador):
        """Muestra el estado actual del jugador."""
        print(f"\n📊 Estado de {jugador.nombre}:")
        print(f"  Fase: {jugador.fase_actual()}")
        print(f"  Bronce: {jugador.bronce}/7 | Plata: {jugador.plata}/3 | Oro: {jugador.oro}/1")
        print(f"  Mano: {jugador.mano.tipo if jugador.mano else 'Vacía'}")
        print(f"  Reserva: {jugador.reserva.tipo if jugador.reserva else 'Vacía'}")
    
    def _mostrar_estado_ia(self, ia):
        """Muestra el estado actual de la IA."""
        print(f"\n📊 Estado de la IA:")
        print(f"  Fase: {ia.fase_actual()}")
        print(f"  Bronce: {ia.bronce}/7 | Plata: {ia.plata}/3 | Oro: {ia.oro}/1")
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
            
            # Pausa entre rondas
            input("\nPresiona Enter para continuar a la siguiente ronda...")
        
        # Fin del juego
        print(f"\n{'='*40}")
        print(f"FIN DEL JUEGO")
        print(f"{'='*40}")
        print(f"\nResultado Final:")
        print(f"  {self.jugador.nombre}: Bronce {self.jugador.bronce}/7 | Plata {self.jugador.plata}/3 | Oro {self.jugador.oro}/1")
        print(f"  IA: Bronce {self.ia.bronce}/7 | Plata {self.ia.plata}/3 | Oro {self.ia.oro}/1")
        print(f"\n{self.determinar_ganador()}")
    
    # Métodos requeridos por la clase Game de aima3
    def acciones_legales(self, estado):
        """Define las acciones legales para el estado actual."""
        pass
    
    def resultado(self, estado, accion):
        """Define cómo cambia el estado después de una acción."""
        pass
    
    def es_terminal(self, estado):
        """Define la condición de fin del juego."""
        return self.juego_terminado()
    
    def utilidad(self, estado, jugador):
        """Define la función de utilidad para cada jugador."""
        pass


if __name__ == '__main__':
    # Crear jugadores
    jugador_humano = Jugador("Jugador")
    ia_bot = Jugador("IA-Bot")
    
    # Crear y ejecutar el juego
    juego = JuegoDeCartas(jugador_humano, ia_bot)
    juego.ejecutar_juego()