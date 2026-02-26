# La subclase rompe el contrato esperado (lanza error donde no se espera) [cite: 24, 29]
class Ave:
    def volar(self): print("Volando...")

class Pinguino(Ave):
    def volar(self):
        raise Exception("No puedo volar") # Rompe el flujo de la aplicación [cite: 30]

# Aseguramos que las jerarquías respeten las capacidades reales [cite: 25]
class Ave: pass

class AveVoladora(Ave):
    def volar(self): print("Volando...")

class Pinguino(Ave):
    def nadar(self): print("Nadando...")