from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from controllers.auth_controller import requiere_login, usuario_actual
from controllers.finance_controller import (
    obtener_categorias, registrar_movimiento, obtener_movimientos,
    eliminar_movimiento, actualizar_movimiento, obtener_resumen_mensual,
    obtener_datos_grafico_anual
)
from conexion.db import get_db_connection
from datetime import datetime

finance_bp = Blueprint('finance', __name__)

@finance_bp.before_request
def before_request():
    """Establece la conexión a la base de datos antes de cada solicitud"""
    g.db = get_db_connection()
    if g.db:
        g.cursor = g.db.cursor(dictionary=True)

@finance_bp.route('/')
@requiere_login
def dashboard():
    """Página principal del dashboard"""
    usuario = usuario_actual()
    
    # Obtener mes y año actual o de la URL
    hoy = datetime.now()
    mes = int(request.args.get('mes', hoy.month))
    anio = int(request.args.get('anio', hoy.year))
    
    # Obtener resumen mensual
    resumen = obtener_resumen_mensual(usuario['id'], mes, anio)
    
    # Obtener movimientos recientes
    movimientos = obtener_movimientos(usuario['id'], mes=mes, anio=anio)
    
    # Obtener datos para gráficos anuales
    datos_anuales = obtener_datos_grafico_anual(usuario['id'], anio)
    
    return render_template(
        'dashboard.html',
        usuario=usuario,
        resumen=resumen,
        movimientos=movimientos,
        mes_actual=mes,
        anio_actual=anio,
        datos_anuales=datos_anuales
    )

@finance_bp.route('/movimientos')
@requiere_login
def movimientos():
    """Página para ver todos los movimientos"""
    usuario = usuario_actual()
    
    # Filtros
    tipo = request.args.get('tipo')
    mes = request.args.get('mes')
    anio = request.args.get('anio')
    
    if mes and anio:
        mes = int(mes)
        anio = int(anio)
    
    # Obtener movimientos
    movimientos = obtener_movimientos(usuario['id'], tipo, mes, anio)
    
    return render_template(
        'movimientos.html',
        usuario=usuario,
        movimientos=movimientos,
        tipo_filtro=tipo,
        mes_filtro=mes,
        anio_filtro=anio
    )

@finance_bp.route('/nuevo-ingreso', methods=['GET', 'POST'])
@requiere_login
def nuevo_ingreso():
    """Página para registrar un nuevo ingreso"""
    usuario = usuario_actual()
    
    # Obtener categorías de ingresos
    categorias = obtener_categorias('ingreso')
    
    if request.method == 'POST':
        categoria_id = request.form.get('categoria_id')
        monto = request.form.get('monto')
        descripcion = request.form.get('descripcion')
        fecha = request.form.get('fecha')
        
        exito, mensaje = registrar_movimiento(
            usuario['id'], categoria_id, monto, descripcion, fecha, 'ingreso'
        )
        
        if exito:
            flash(mensaje, 'success')
            return redirect(url_for('finance.dashboard'))
        else:
            flash(mensaje, 'error')
    
    return render_template(
        'nuevo_movimiento.html',
        usuario=usuario,
        categorias=categorias,
        tipo='ingreso'
    )

@finance_bp.route('/nuevo-gasto', methods=['GET', 'POST'])
@requiere_login
def nuevo_gasto():
    """Página para registrar un nuevo gasto"""
    usuario = usuario_actual()
    
    # Obtener categorías de gastos
    categorias = obtener_categorias('gasto')
    
    if request.method == 'POST':
        categoria_id = request.form.get('categoria_id')
        monto = request.form.get('monto')
        descripcion = request.form.get('descripcion')
        fecha = request.form.get('fecha')
        
        exito, mensaje = registrar_movimiento(
            usuario['id'], categoria_id, monto, descripcion, fecha, 'gasto'
        )
        
        if exito:
            flash(mensaje, 'success')
            return redirect(url_for('finance.dashboard'))
        else:
            flash(mensaje, 'error')
    
    return render_template(
        'nuevo_movimiento.html',
        usuario=usuario,
        categorias=categorias,
        tipo='gasto'
    )

@finance_bp.route('/editar-movimiento/<int:movimiento_id>', methods=['GET', 'POST'])
@requiere_login
def editar_movimiento(movimiento_id):
    """Página para editar un movimiento"""
    usuario = usuario_actual()
    
    # Obtener datos del movimiento
    cursor = g.cursor
    cursor.execute(
        """SELECT m.*, c.tipo as tipo_movimiento 
           FROM movimientos m
           JOIN categorias c ON m.categoria_id = c.id
           WHERE m.id = %s AND m.usuario_id = %s""",
        (movimiento_id, usuario['id'])
    )
    movimiento = cursor.fetchone()
    
    if not movimiento:
        flash('No tienes permiso para editar este movimiento', 'error')
        return redirect(url_for('finance.movimientos'))
    
    # Obtener categorías según el tipo de movimiento
    categorias = obtener_categorias(movimiento['tipo_movimiento'])
    
    if request.method == 'POST':
        categoria_id = request.form.get('categoria_id')
        monto = request.form.get('monto')
        descripcion = request.form.get('descripcion')
        fecha = request.form.get('fecha')
        
        exito, mensaje = actualizar_movimiento(
            movimiento_id, usuario['id'], categoria_id, monto, descripcion, fecha
        )
        
        if exito:
            flash(mensaje, 'success')
            return redirect(url_for('finance.movimientos'))
        else:
            flash(mensaje, 'error')
    
    return render_template(
        'editar_movimiento.html',
        usuario=usuario,
        movimiento=movimiento,
        categorias=categorias
    )

@finance_bp.route('/eliminar-movimiento/<int:movimiento_id>')
@requiere_login
def eliminar_movimiento_route(movimiento_id):
    """Ruta para eliminar un movimiento"""
    usuario = usuario_actual()
    
    exito, mensaje = eliminar_movimiento(movimiento_id, usuario['id'])
    
    if exito:
        flash(mensaje, 'success')
    else:
        flash(mensaje, 'error')
    
    return redirect(url_for('finance.movimientos'))

@finance_bp.route('/api/datos-grafico')
@requiere_login
def api_datos_grafico():
    """API para obtener datos de gráficos"""
    usuario = usuario_actual()
    
    anio = int(request.args.get('anio', datetime.now().year))
    
    datos = obtener_datos_grafico_anual(usuario['id'], anio)
    
    # Formatear datos para Chart.js
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    return jsonify({
        'labels': meses,
        'datasets': [
            {
                'label': 'Ingresos',
                'data': [d['ingresos'] for d in datos],
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            },
            {
                'label': 'Gastos',
                'data': [d['gastos'] for d in datos],
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderColor': 'rgba(255, 99, 132, 1)',
                'borderWidth': 1
            }
        ]
    })
