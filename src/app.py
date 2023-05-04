from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user,logout_user, login_required

from config import config

from models.ModelUser import ModelUser
from models.entities.User import Usuarios

app=Flask(__name__)

csrf=CSRFProtect()

db = MySQL(app)
login_manager_app = LoginManager(app)

#ya deja de confundir las "." con las comas "," nos haces perder tiempo XD
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

@app.route('/')
def index(): 
    return redirect(url_for('login'))

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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template('auth/home.html')

@app.route('/protected')
@login_required
def protected():
    return "<h1> Estas es una vista de preueba pero ambos sabemos que haremos de esta pagina </h1>"

def status_401(error):
    return redirect(url_for('login'))
def status_404(error):
    return "<h1> Pagina no encontrada </h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()   

