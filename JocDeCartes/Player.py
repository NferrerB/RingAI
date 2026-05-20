class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.bronce = 0
        self.plata = 0
        self.oro = 0
        
        # El slot de reserva: None significa vacío. Si hay una Carta, está ocupado.
        self.reserva = None 
        self.bloqueado = False
        
        # Inicialización del mazo enlazado con las 11 cartas
        self.mazo = MazoEnlazado()
        cartas_base = [Carta('Bronce') for _ in range(7)] + \
                      [Carta('Plata') for _ in range(3)] + \
                      [Carta('Oro') for _ in range(1)]
        self.mazo.inicializar_y_mezclar(cartas_base)

    def fase_actual(self):
        if self.bronce < 7:
            return 'Bronce'
        elif self.plata < 3:
            return 'Plata'
        else:
            return 'Oro'
            
    def guardar_en_reserva(self, carta):
        """Intenta guardar una carta. Falla si ya hay una."""
        if self.reserva is None:
            self.reserva = carta
            return True
        return False # No se puede guardar, el slot está ocupado