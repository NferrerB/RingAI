class Carta:
    def __init__(self, tipo):
        self.tipo = tipo  # 'Bronce', 'Plata', 'Oro'
    
    def __str__(self):
        return f"Carta({self.tipo})"