class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mazo = Mazo()  # ¡Cada jugador tiene ahora su propio mazo!
        self.bronce = 0
        self.plata = 0
        self.oro = 0
        self.reserva = None
        self.bloqueado = False

    def fase_actual(self):
        if self.bronce < 7:
            return 'Bronce'
        elif self.plata < 3:
            return 'Plata'
        else:
            return 'Oro'
            
    def puntuar_carta(self, carta):
        if carta.tipo == 'Bronce':
            self.bronce += 1
        elif carta.tipo == 'Plata':
            self.plata += 1
        elif carta.tipo == 'Oro':
            self.oro += 1