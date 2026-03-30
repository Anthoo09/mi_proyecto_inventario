from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from conexion.conexion import conectar

app = Flask(__name__)
app.secret_key = "secreto"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# MODELO USUARIO
class Usuario(UserMixin):
    def __init__(self, id, nombre, email):
        self.id = id
        self.nombre = nombre
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return Usuario(user[0], user[1], user[2])
    return None

# REGISTRO
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password)
        )
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('registro.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    mensaje = ""

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            if user[3] == password:
                usuario = Usuario(user[0], user[1], user[2])
                login_user(usuario)
                return redirect('/panel')
            else:
                mensaje = "Contraseña incorrecta"
        else:
            mensaje = "Usuario no existe"

    return render_template('login.html', mensaje=mensaje)
# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# PANEL PROTEGIDO
@app.route('/panel')
@login_required
def panel():
    return render_template('panel.html')

if __name__ == '__main__':
    app.run(debug=True)