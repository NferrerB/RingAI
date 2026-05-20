import random

class Mazo:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def agregar_al_final(self, carta):
        """Inserta una carta al fondo del mazo (para devolver cartas)."""
        nuevo_nodo = Nodo(carta)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo

    def extraer_del_frente(self):
        """Roba la carta superior del mazo."""
        if self.cabeza is None:
            return None # El mazo está vacío
        
        carta_extraida = self.cabeza.carta
        self.cabeza = self.cabeza.siguiente
        
        if self.cabeza is None:
            self.cola = None # Si sacamos la última carta, la cola también es None
            
        return carta_extraida

    def inicializar_y_mezclar(self, lista_cartas):
        """Recibe una lista estándar, la mezcla y la convierte en lista enlazada."""
        random.shuffle(lista_cartas)
        for carta in lista_cartas:
            self.agregar_al_final(carta)