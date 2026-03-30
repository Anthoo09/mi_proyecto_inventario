from database import conectar

class Producto:
    def __init__(self, nombre, cantidad, precio):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio


class Inventario:

    def agregar_producto(self, producto):
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
            (producto.nombre, producto.cantidad, producto.precio)
        )

        conexion.commit()
        conexion.close()

    def obtener_productos(self):
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        conexion.close()
        return productos

    def eliminar_producto(self, id):
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM productos WHERE id = ?", (id,))

        conexion.commit()
        conexion.close()