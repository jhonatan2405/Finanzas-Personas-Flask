import mysql.connector
from mysql.connector import Error
import os
from flask import g

def get_db_connection():
    """Establece y retorna una conexión a la base de datos MySQL"""
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'finanzas_personales')
            )
            g.cursor = g.db.cursor(dictionary=True)
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None
    return g.db

def close_db(e=None):
    """Cierra la conexión a la base de datos"""
    db = g.pop('db', None)
    cursor = g.pop('cursor', None)
    
    if cursor:
        cursor.close()
    
    if db and db.is_connected():
        db.close()

def init_app(app):
    """Inicializa la conexión a la base de datos en la aplicación Flask"""
    app.teardown_appcontext(close_db)
