from flask import session, flash, redirect, url_for, request, g
from werkzeug.security import generate_password_hash, check_password_hash
import re
from functools import wraps

def validar_email(email):
    """Valida el formato del email"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validar_password(password):
    """Valida que la contraseña tenga al menos 8 caracteres"""
    return len(password) >= 8

def registrar_usuario(nombre, email, password):
    """Registra un nuevo usuario en la base de datos"""
    # Validaciones
    if not nombre or not email or not password:
        return False, "Todos los campos son obligatorios"
    
    if not validar_email(email):
        return False, "El formato del email no es válido"
    
    if not validar_password(password):
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    # Verificar si el email ya existe
    cursor = g.cursor
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    if cursor.fetchone():
        return False, "El email ya está registrado"
    
    # Encriptar contraseña
    hashed_password = generate_password_hash(password)
    
    # Insertar usuario
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, hashed_password)
        )
        g.db.commit()
        return True, "Usuario registrado correctamente"
    except Exception as e:
        g.db.rollback()
        return False, f"Error al registrar usuario: {str(e)}"

def iniciar_sesion(email, password):
    """Inicia sesión de un usuario"""
    if not email or not password:
        return False, "Email y contraseña son obligatorios"
    
    cursor = g.cursor
    cursor.execute("SELECT id, nombre, email, password FROM usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()
    
    if not usuario or not check_password_hash(usuario['password'], password):
        return False, "Email o contraseña incorrectos"
    
    # Guardar datos en la sesión
    session['usuario_id'] = usuario['id']
    session['usuario_nombre'] = usuario['nombre']
    session['usuario_email'] = usuario['email']
    
    return True, "Inicio de sesión exitoso"

def cerrar_sesion():
    """Cierra la sesión del usuario"""
    session.clear()
    return True, "Sesión cerrada correctamente"

def usuario_actual():
    """Retorna el usuario actualmente logueado"""
    if 'usuario_id' in session:
        return {
            'id': session['usuario_id'],
            'nombre': session['usuario_nombre'],
            'email': session['usuario_email']
        }
    return None

def requiere_login(f):
    """Decorador para requerir inicio de sesión"""
    @wraps(f) 
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'error')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function