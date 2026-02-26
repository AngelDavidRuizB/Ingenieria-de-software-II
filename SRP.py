# LA CLASE HACE DEMASIADAS COSAS: 
class GestorUsuarios:
    def guardar_usuario(self, datos):
        print(f"Guardando {datos} en la BD...")
        print(f"Enviando correo de bienvenida a {datos['email']}...")

# LAS RESPONSABILIDADES SE DIVIDEN CORRECTAMENTE
class UsuarioRepositorio:
    def guardar(self, datos):
        print(f"Guardando {datos} en la BD...")

class ServicioNotificacion:
    def enviar_bienvenida(self, email):
        print(f"Enviando correo de bienvenida a {email}...")