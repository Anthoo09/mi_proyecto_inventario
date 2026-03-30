from flask import Flask, render_template, request, redirect, make_response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from conexion.conexion import conectar
from services.producto_service import obtener_productos, agregar_producto, eliminar_producto
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = "secreto"

# ---------------- LOGIN ----------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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
@app.route('/')
@login_required
def inicio():
    return redirect('/panel')

# ---------------- REGISTRO ----------------

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

# ---------------- LOGIN ----------------

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

# ---------------- LOGOUT ----------------

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# ---------------- PANEL ----------------

@app.route('/panel')
@login_required
def panel():
    return render_template('panel.html')

# ---------------- PRODUCTOS (CRUD) ----------------

@app.route('/productos')
@login_required
def productos():
    datos = obtener_productos()
    return render_template('productos.html', productos=datos)

@app.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        agregar_producto(nombre, cantidad, precio)
        return redirect('/productos')

    return render_template('producto_form.html')

@app.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    eliminar_producto(id)
    return redirect('/productos')

# ---------------- PDF ----------------

@app.route('/reporte')
@login_required
def reporte():
    productos = obtener_productos()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Reporte de Productos", ln=True)

    for p in productos:
        pdf.cell(200, 10, txt=f"{p[1]} - Cantidad: {p[2]} - Precio: {p[3]}", ln=True)

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte.pdf'

    return response

# ---------------- RUN ----------------

if __name__ == '__main__':
    app.run(debug=True)