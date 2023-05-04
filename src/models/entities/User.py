from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class Usuarios(UserMixin):
    def __init__(self, id, nombre, correo_electronico, contrasena) ->None:
        self.id = id
        self.nombre = nombre
        self.correo_electronico = correo_electronico
        self.contrasena = contrasena
    
    @classmethod
    def check_password(self, hashed_password, password):
            return check_password_hash(hashed_password, password)
    
   # print(generate_password_hash('holaXD'))