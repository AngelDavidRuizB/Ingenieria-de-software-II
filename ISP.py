from abc import ABC, abstractmethod

#  Interfaz gigante que obliga a implementar cosas innecesarias
class Multifuncional(ABC):
    @abstractmethod
    def imprimir(self): pass
    @abstractmethod
    def escanear(self): pass

class ImpresoraBasica(Multifuncional):
    def imprimir(self): print("Imprimiendo...")
    def escanear(self): pass 

# Segregamos en interfaces pequeñas 
class Impresora(ABC):
    @abstractmethod
    def imprimir(self): pass

class Escaner(ABC):
    @abstractmethod
    def escanear(self): pass

class ImpresoraEconomica(Impresora):
    def imprimir(self): print("Solo imprimo.")