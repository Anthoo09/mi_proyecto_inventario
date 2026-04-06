from conexion.conexion import conectar

def obtener_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()
    conn.close()
    return datos

def agregar_producto(nombre, cantidad, precio):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (%s,%s,%s)", (nombre, cantidad, precio))
    conn.commit()
    conn.close()

def eliminar_producto(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=%s", (id,))
    conn.commit()
    conn.close()

def obtener_producto_por_id(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
    producto = cursor.fetchone()
    conn.close()
    return producto

def actualizar_producto(id, nombre, cantidad, precio):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET nombre=%s, cantidad=%s, precio=%s WHERE id=%s",
                   (nombre, cantidad, precio, id))
    conn.commit()
    conn.close()