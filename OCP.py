# El uso de 'if' o 'switch' obliga a modificar la clase para añadir tipos
class ProcesadorPagos:
    def procesar(self, tipo, monto):
        if tipo == "web":
            print(f"Procesando pago web de {monto}")
        elif tipo == "movil": # Cada nuevo tipo requiere tocar esta función [cite: 21]
            print(f"Procesando pago móvil de {monto}")



#  Usamos un mapeo o polimorfismo para extender sin modificar el núcleo 
class MetodoPago:
    def pagar(self, monto): pass

class PagoWeb(MetodoPago):
    def pagar(self, monto): print(f"Pago web: {monto}")

class PagoMovil(MetodoPago):
    def pagar(self, monto): print(f"Pago móvil: {monto}")

def procesar_pago(metodo: MetodoPago, monto):
    metodo.pagar(monto)