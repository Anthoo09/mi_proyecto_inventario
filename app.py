from flask import Flask, render_template, request, redirect
from database import crear_tabla
from models import Producto, Inventario

app = Flask(__name__)

inventario = Inventario()

# Crear tabla al iniciar
crear_tabla()

@app.route('/')
def inicio():
    productos = inventario.obtener_productos()
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    cantidad = request.form['cantidad']
    precio = request.form['precio']

    producto = Producto(nombre, cantidad, precio)
    inventario.agregar_producto(producto)

    return redirect('/')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    inventario.eliminar_producto(id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)