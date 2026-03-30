from flask import Flask, render_template, request, redirect
from conexion.conexion import conectar

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')

# MOSTRAR PRODUCTOS
@app.route('/productos')
def productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()
    conn.close()
    return render_template('productos.html', productos=datos)

# AGREGAR PRODUCTO
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s)",
            (nombre, cantidad, precio)
        )
        conn.commit()
        conn.close()

        return redirect('/productos')

    return render_template('producto_form.html')

# EDITAR PRODUCTO
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        cursor.execute(
            "UPDATE productos SET nombre=%s, cantidad=%s, precio=%s WHERE id=%s",
            (nombre, cantidad, precio, id)
        )
        conn.commit()
        conn.close()
        return redirect('/productos')

    cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
    producto = cursor.fetchone()
    conn.close()

    return render_template('editar.html', producto=producto)

# ELIMINAR PRODUCTO
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('/productos')


if __name__ == '__main__':
    app.run(debug=True)