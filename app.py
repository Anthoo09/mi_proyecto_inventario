from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json
import csv

app = Flask(__name__)

# CONFIGURACIÓN BASE DE DATOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELO
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Float)

# CREAR TABLA
with app.app_context():
    db.create_all()

# INICIO
@app.route('/')
def inicio():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

# AGREGAR PRODUCTO
@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])

    nuevo = Producto(nombre=nombre, cantidad=cantidad, precio=precio)
    db.session.add(nuevo)
    db.session.commit()

    # TXT
    with open('datos.txt', 'a') as f:
        f.write(f"{nombre},{cantidad},{precio}\n")

    # JSON
    data = {"nombre": nombre, "cantidad": cantidad, "precio": precio}
    try:
        with open('datos.json', 'r') as f:
            lista = json.load(f)
    except:
        lista = []

    lista.append(data)
    with open('datos.json', 'w') as f:
        json.dump(lista, f)

    # CSV
    with open('datos.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nombre, cantidad, precio])

    return redirect('/')

# VER DATOS
@app.route('/datos')
def ver_datos():

    try:
        with open('datos.txt', 'r') as f:
            txt = f.readlines()
    except:
        txt = []

    try:
        with open('datos.json', 'r') as f:
            json_data = json.load(f)
    except:
        json_data = []

    try:
        with open('datos.csv', 'r') as f:
            csv_data = list(csv.reader(f))
    except:
        csv_data = []

    return render_template('datos.html', txt=txt, json_data=json_data, csv_data=csv_data)

# ELIMINAR
@app.route('/eliminar/<int:id>')
def eliminar(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)