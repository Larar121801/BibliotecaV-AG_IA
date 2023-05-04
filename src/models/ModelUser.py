from .entities.User import Usuarios

class ModelUser():
    @classmethod
    def login(self, db, usuarios):
        try:
            #cursor para la interaccion de la base de datos
            cursor=db.connection.cursor()
            #query para la solcitud para la base de datos en este caso sacamos o hacemos referencia a 4 atributos
            sql="""SELECT id, nombre, correo_electronico, contrasena FROM 
                    usuarios WHERE nombre = '{}'""".format(usuarios.nombre)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                #cada row de la liena 14 es un atributos como se cuneta desde 0 de las id hasta la contrasena
                #la parte de la contrasena hace referencia a lo que guarda en la base de datos y lo que tiene en el user.py
                usuarios = Usuarios(row[0], row[1], row[2], Usuarios.check_password(row[3],usuarios.contrasena))   
                return usuarios
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor=db.connection.cursor()
            sql="SELECT id, nombre, correo_electronico FROM usuarios WHERE id = {}".format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                return Usuarios(row[0], row[1], row[2], None)   
            else:
                return None
        except Exception as ex:
            raise Exception(ex)