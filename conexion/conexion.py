import mysql.connector

def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # déjalo vacío si no pusiste contraseña
        database="inventario_db"
    )
    return conexion