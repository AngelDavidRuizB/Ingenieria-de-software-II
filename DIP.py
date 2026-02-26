# Dependencia directa de una clase concreta 
class MySQLDatabase:
    def guardar(self, dato): print("Guardado en MySQL")

class ServicioSoporte:
    def __init__(self):
        self.db = MySQLDatabase() 

# Inyectamos la dependencia basándonos en una abstracción
class BaseDeDatos(ABC):
    @abstractmethod
    def guardar(self, dato): pass

class ServicioSoporteSOLID:
    def __init__(self, db: BaseDeDatos): 
        self.db = db

    def ejecutar(self, dato):
        self.db.guardar(dato)

