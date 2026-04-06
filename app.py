from flask import Flask, render_template, request, redirect, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from conexion.conexion import conectar
import hashlib
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secreto123"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


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


# LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ""

    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and user[3] == password:
            login_user(Usuario(user[0], user[1], user[2]))
            return redirect('/panel')
        else:
            mensaje = "❌ Datos incorrectos"

    return render_template('login.html', mensaje=mensaje)


# PANEL
@app.route('/panel')
@login_required
def panel():
    return render_template('panel.html')


# PRODUCTOS
@app.route('/productos')
@login_required
def productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()
    conn.close()

    return render_template('productos.html', productos=datos)


# AGREGAR
@app.route('/agregar', methods=['POST'])
@login_required
def agregar():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO productos (nombre, cantidad, precio) VALUES (%s,%s,%s)",
        (request.form['nombre'], request.form['cantidad'], request.form['precio'])
    )

    conn.commit()
    conn.close()

    return redirect('/productos')


# EDITAR
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute(
            "UPDATE productos SET nombre=%s, cantidad=%s, precio=%s WHERE id=%s",
            (request.form['nombre'], request.form['cantidad'], request.form['precio'], id)
        )
        conn.commit()
        conn.close()
        return redirect('/productos')

    cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
    producto = cursor.fetchone()
    conn.close()

    return render_template('editar.html', producto=producto)


# ELIMINAR
@app.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM productos WHERE id=%s", (id,))

    conn.commit()
    conn.close()

    return redirect('/productos')


# VENTAS
@app.route('/ventas', methods=['GET', 'POST'])
@login_required
def ventas():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        id_producto = request.form['producto']
        cantidad = int(request.form['cantidad'])
        fecha = request.form['fecha']

        cursor.execute(
            "INSERT INTO ventas (id_producto, fecha) VALUES (%s,%s)",
            (id_producto, fecha)
        )

        cursor.execute(
            "UPDATE productos SET cantidad = cantidad - %s WHERE id=%s",
            (cantidad, id_producto)
        )

        conn.commit()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()

    return render_template('ventas.html', productos=productos)


# PDF
@app.route('/pdf')
@login_required
def pdf():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()
    conn.close()

    doc = SimpleDocTemplate("reporte.pdf")
    estilos = getSampleStyleSheet()

    elementos = []
    elementos.append(Paragraph("📱 REPORTE DE PRODUCTOS", estilos['Title']))
    elementos.append(Spacer(1, 10))
    elementos.append(Paragraph(f"Fecha: {datetime.now()}", estilos['Normal']))
    elementos.append(Spacer(1, 20))

    tabla_data = [["ID", "Nombre", "Cantidad", "Precio"]]

    for d in datos:
        tabla_data.append([d[0], d[1], d[2], d[3]])

    tabla = Table(tabla_data)
    tabla.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    elementos.append(tabla)
    doc.build(elementos)

    return send_file("reporte.pdf", as_attachment=True)


# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)