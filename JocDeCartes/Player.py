from Carta import Carta
from Mazo import Mazo
from aima3.games import Game, GameState

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.bronce = 0
        self.plata = 0
        self.oro = 0
        
        # El slot de reserva: None significa vacío. Si hay una Carta, está ocupado.
        self.reserva = None 
        self.mano = None # La carta que el jugador tiene en la mano (si la hay)
        self.bloqueado = False
        
        # Inicialización del mazo enlazado con las 10 cartas
        self.mazo = Mazo()
        cartas_base = [Carta('Bronce') for _ in range(6)] + \
                      [Carta('Plata') for _ in range(3)] + \
                      [Carta('Oro') for _ in range(1)]
        self.mazo.inicializar_y_mezclar(cartas_base)

    def fase_actual(self):
        if self.bronce < 6:
            return 'Bronce'
        elif self.plata < 3:
            return 'Plata'
        else:
            return 'Oro'
            
    def guardar_en_reserva(self, carta):
        """Intenta guardar una carta. Falla si ya hay una."""
        carta_a_guardar = carta if carta is not None else self.mano
        if self.reserva is None and carta_a_guardar is not None:
            self.reserva = carta_a_guardar
            if carta_a_guardar == self.mano:
                self.mano = None
            return True
        return False # No se puede guardar, el slot está ocupado
    
    def descartar_reserva(self):
        """Descarta la carta en reserva, si hay una."""
        if self.reserva is not None:
            if self.reserva.tipo == 'Bronce' and self.fase_actual() == 'Bronce':
                self.bronce += 1
                self.fase_actual() # Actualiza la fase después de ganar un bronce, si este llega al limite
            elif self.reserva.tipo == 'Plata' and self.fase_actual() == 'Plata':
                self.plata += 1
                self.fase_actual() # Actualiza la fase después de ganar una plata, si esta llega al limite
            elif self.reserva.tipo == 'Oro' and self.fase_actual() == 'Oro':
                self.oro += 1
                self.fase_actual() # Actualiza la fase después de ganar un oro, si este llega al limite
            else:
                # No puedes descartar una carta que no coincide con tu fase actual
                return False
            self.reserva = None
            return True
        return False # No hay carta para descartar
    
    def robar_carta(self):
        """Roba la carta superior del mazo."""
        return self.mazo.extraer_del_frente()
    
    def robar (self):
        """Intenta robar una carta. Si el slot de mano está ocupado, no se puede robar."""
        if self.mano is None:
            self.mano = self.robar_carta()
            return self.mano is not None
        return False # No se puede robar, el slot está ocupado

def descartar_mano(jugador):
    if jugador.mano is not None and jugador.mano.tipo == jugador.fase_actual():
        carta_a_descartar = jugador.mano
        if carta_a_descartar.tipo == 'Bronce':
            jugador.bronce += 1
            jugador.fase_actual() # Actualiza la fase después de ganar un bronce, si este llega al limite
        elif carta_a_descartar.tipo == 'Plata':
            jugador.plata += 1
            jugador.fase_actual() # Actualiza la fase después de ganar una plata, si esta llega al limite
        elif carta_a_descartar.tipo == 'Oro':
            jugador.oro += 1
            jugador.fase_actual() # Actualiza la fase después de ganar un oro, si este llega al limite
        
        jugador.mano = None
        return carta_a_descartar
    return None

def bloquear_jugador(oponente):
    """Bloquea al oponente (si no está bloqueado ya)."""
    if not oponente.bloqueado:
        oponente.bloqueado = True
        return True
    return False

def desbloquear_jugador(jugador):
    """Desbloquea al jugador (si está bloqueado)."""
    if jugador.bloqueado:
        jugador.bloqueado = False
        return True
    return False

def devolver_carta_a_mazo(jugador):
    if jugador.mano is not None:
        jugador.mazo.agregar_al_final(jugador.mano)
        jugador.mano = None

    