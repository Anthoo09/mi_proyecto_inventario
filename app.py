from flask import Flask

app = Flask(__name__)

# Ruta principal
@app.route('/')
def inicio():
    return "Bienvenido a Inventario SmartTech – Control de celulares"

# Ruta dinámica
@app.route('/producto/<nombre>')
def producto(nombre):
    return f"Producto: {nombre} – disponible en inventario"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)