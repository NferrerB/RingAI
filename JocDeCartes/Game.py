
from aima3.games import Game, GameState
from Player import Jugador, bloquear_jugador, devolver_carta_a_mazo, descartar_mano, desbloquear_jugador

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
            print("7. Terminar turno sin hacer nada")
            print("8. Salir del juego")
            
            opcion = input("\nSelecciona una opción (1-8): ").strip()
            
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
                print("\n✓Termina tu turno sin hacer nada.")
                accion_realizada = False # Termina el turno sin hacer nada
            elif opcion == '8':
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
        Ejecuta la estrategia de la IA.
        Retorna el número de acciones realizadas.
        """
        acciones = 0
        
        # La IA usara el codigo implementado en IA.py para decidir su jugada
        # Las jugadas posibles seran: robar, guardar en reserva, descartar reserva, 
        # descartar mano, bloquear jugador o devolver carta a mazo
        
        fase = self.ia.fase_actual()
        
        # Estrategia: 
        # 1. Descartar reserva si es posible
        if self.ia.reserva is not None:
            if self.ia.descartar_reserva():
                print(f"  → IA descarta reserva")
                acciones += 1
        
        # 2. Descartar mano si el tipo coincide con la fase actual
        if self.ia.mano is not None and self.ia.mano.tipo == fase:
            carta_descartada = self.ia.mano
            self.ia.mano = None
            if carta_descartada.tipo == 'Bronce':
                self.ia.bronce += 1
            elif carta_descartada.tipo == 'Plata':
                self.ia.plata += 1
            elif carta_descartada.tipo == 'Oro':
                self.ia.oro += 1
            print(f"  → IA descarta carta de la mano")
            acciones += 1
        
        # 3. Guardar en reserva si aún hay carta en mano y reserva está vacía
        elif self.ia.mano is not None and self.ia.reserva is None:
            if self.ia.guardar_en_reserva(None):
                print(f"  → IA guarda carta en reserva")
                acciones += 1
        
        # 4. Robar si la mano está vacía
        elif self.ia.mano is None:
            if self.ia.robar():
                print(f"  → IA roba una carta: {self.ia.mano.tipo}")
                acciones += 1
        
        # 5. Bloquear jugador si no ha hecho nada aún y el jugador no está bloqueado
        # y no fue desbloqueado en esta ronda (para evitar ciclo de bloqueo/desbloqueo)
        if acciones == 0 and not self.jugador.bloqueado and not self.jugador_fue_desbloqueado_esta_ronda:
            if bloquear_jugador(self.jugador):
                print(f"  → IA bloquea al jugador")
                acciones += 1
        
        # 6. Devolver carta al mazo si aún no ha hecho nada
        if acciones == 0 and self.ia.mano is not None:
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