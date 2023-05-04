from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user,logout_user, login_required

from config import config

from models.ModelUser import ModelUser
from models.entities.User import Usuarios

app=Flask(__name__)



db = MySQL(app)
login_manager_app = LoginManager(app)

#ya deja de confundir las "." con las comas "," nos haces perder tiempo XD
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

@app.route('/')
def index(): 
    return redirect(url_for('login'))


#  ENLACE AL LOGIN 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Usuarios(0, request.form['name'], request.form['correo_electronico'], request.form['contrasena'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.contrasena:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash('Contrasena incorrecta')
                return render_template('auth/login.html')
        else:
            flash('La contraseña o el nombre son incorrectos')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

#   ENLACE A LOGOUT 

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


#   ENLACE A HOME

@app.route('/home')
def home():
    return render_template('auth/home.html')



#   ENALCE A PROTECTED pagina de prueba que solo usuarios registrados podran entrar


@app.route('/protected')
@login_required
def protected():
    return "<h1> Estas es una vista de preueba pero ambos sabemos que haremos de esta pagina </h1>"


#   ENLACES DE ERRORES 401 Y 404

def status_401(error):
    return redirect(url_for('login'))
def status_404(error):
    return "<h1> Pagina no encontrada </h1>", 404


# Secion de los CRUDS en teoria

@app.route('/c_autores')
def contacto():
    return render_template('CRUDs/autores/t_autores.html')

@app.route('/autores', methods=['GET'])
def t_autores():
    try:
        cursor = db.connection.cursor()
        # Si encuentras un error revisa los pasos que primero hiciste y como putas escribiste XD te odio
        sql = "SELECT id, nombre, nacionalidad, biografia FROM autores"
        cursor.execute(sql)
        datos = cursor.fetchall()
        autor=[]
        for fila in datos:
            autores={'id':fila[0], 'nombre':fila[1], 'nacionalidad':fila[2], 'biografia':[3]}
            autor.append(autores)
            #Aca transforma los parametros de los atributos que pusimos en un formato JSON
        return jsonify({'autor': autor, 'mensaje': 'Misteriosamente funciona'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

# OBTENER informacion de la tabla
@app.route('/autores/<id>', methods=['GET'])
def leer_autores(id):
    try:
        cursor = db.connection.cursor()
        sql = "SELECT id, nombre, nacionalidad, biografia FROM autores WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None: 
            autores = {'id': datos[0], 'nombre': datos[1], 'nacionalidad': datos[2], 'biografia': datos[3]}
            return jsonify({'autores': autores, 'mensaje': "Milagrosametne funciona version GET"})
        else: 
            return jsonify({'mensaje': "No funciona porque creo que hiciste algo mal revisa las 90 lineas de codigo para que sea un error ortografico"})
    except Exception as ex:
        return jsonify({'mensaje': "Np hay datos los cuales pedir dude"})

# AGREGAR informacion a la tabla // como anecdota 1 si estas con sue'o no trates de resolver muchos porblemas jejeje y 2 el 
# CSRF bloquea OBVIAMENTE las peticiones POST XD 
@app.route('/autores', methods=['POST'])
def p_autores():
    try: 
        cursor = db.connection.cursor()
        sql = """INSERT INTO autores(nombre, nacionalidad, biografia) 
        VALUES ('{0}', '{1}', '{2}')""".format(request.json['nombre'], request.json['nacionalidad'], request.json['biografia'])
        cursor.execute(sql)
        db.connection.commit() 
        return jsonify({'mensaje': "Milagrosametne funciona version POST"})
    except Exception as ex: 
        return jsonify({'mensaje': "Esto no esta conectado a la BDA  aiuda"})



# ACTUALIZAR los datos de la tabla
@app.route('/autores/<id>', methods=['PUT'])
def u_autores(id):
    try:
        cursor = db.connection.cursor()

        sql = """UPDATE autores SET nombre = '{0}', nacionalidad = '{1}', biografia = '{2}'
        WHERE id = '{3}'""".format(request.json['nombre'], request.json['nacionalidad'], request.json['biografia'], id)

        cursor.execute(sql)
        db.connection.commit()
        return jsonify({'mensaje': "No se si funciona XD"})
    except Exception as ex:
        return jsonify({'mensaje': "Esto no esta con bda dude"})



# DELETE eliminar XD nada mas que aportar
@app.route('/autores/<id>', methods=['DELETE'])
def d_autores(id):
    try:
        cursor = db.connection.cursor()
        sql = "DELETE FROM autores WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        db.connection.commit()
        return jsonify({'mensaje': "Milogrosamente funciona version DELETE"})
    except Exception as ex:
        return jsonify({'mensaje': "No esta conectado a la base de datos XD"})
    



# Configuraciones de la aplicacion de desarrollo
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()   

