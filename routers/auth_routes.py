from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from controllers.auth_controller import registrar_usuario, iniciar_sesion, cerrar_sesion, usuario_actual
from conexion.db import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.before_request
def before_request():
    """Establece la conexión a la base de datos antes de cada solicitud"""
    g.db = get_db_connection()
    if g.db:
        g.cursor = g.db.cursor(dictionary=True)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Ruta para el registro de usuarios"""
    # Si el usuario ya está logueado, redirigir al dashboard
    if usuario_actual():
        return redirect(url_for('finance.dashboard'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        
        exito, mensaje = registrar_usuario(nombre, email, password)
        
        if exito:
            flash(mensaje, 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(mensaje, 'error')
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta para el inicio de sesión"""
    # Si el usuario ya está logueado, redirigir al dashboard
    if usuario_actual():
        return redirect(url_for('finance.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        exito, mensaje = iniciar_sesion(email, password)
        
        if exito:
            flash(mensaje, 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('finance.dashboard'))
        else:
            flash(mensaje, 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Ruta para cerrar sesión"""
    cerrar_sesion()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('auth.login'))
