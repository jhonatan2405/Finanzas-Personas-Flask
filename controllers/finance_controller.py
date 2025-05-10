from flask import g, session
from datetime import datetime

def obtener_categorias(tipo=None):
    """Obtiene las categorías de ingresos o gastos"""
    cursor = g.cursor
    
    if tipo:
        cursor.execute("SELECT id, nombre FROM categorias WHERE tipo = %s", (tipo,))
    else:
        cursor.execute("SELECT id, nombre, tipo FROM categorias")
        
    return cursor.fetchall()

def registrar_movimiento(usuario_id, categoria_id, monto, descripcion, fecha, tipo):
    """Registra un nuevo movimiento financiero"""
    try:
        cursor = g.cursor
        
        # Validar que la categoría exista y sea del tipo correcto
        cursor.execute("SELECT tipo FROM categorias WHERE id = %s", (categoria_id,))
        categoria = cursor.fetchone()
        
        if not categoria or categoria['tipo'] != tipo:
            return False, "La categoría seleccionada no es válida para este tipo de movimiento"
        
        # Convertir fecha si viene como string
        if isinstance(fecha, str):
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
            
        # Insertar movimiento
        cursor.execute(
            """INSERT INTO movimientos 
               (usuario_id, categoria_id, monto, descripcion, fecha, tipo) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (usuario_id, categoria_id, monto, descripcion, fecha, tipo)
        )
        g.db.commit()
        return True, "Movimiento registrado correctamente"
    except Exception as e:
        g.db.rollback()
        return False, f"Error al registrar movimiento: {str(e)}"

def obtener_movimientos(usuario_id, tipo=None, mes=None, anio=None):
    """Obtiene los movimientos financieros de un usuario"""
    cursor = g.cursor
    
    query = """
        SELECT m.id, m.monto, m.descripcion, m.fecha, m.tipo, c.nombre as categoria
        FROM movimientos m
        JOIN categorias c ON m.categoria_id = c.id
        WHERE m.usuario_id = %s
    """
    params = [usuario_id]
    
    if tipo:
        query += " AND m.tipo = %s"
        params.append(tipo)
    
    if mes and anio:
        query += " AND MONTH(m.fecha) = %s AND YEAR(m.fecha) = %s"
        params.append(mes)
        params.append(anio)
    
    query += " ORDER BY m.fecha DESC"
    
    cursor.execute(query, params)
    return cursor.fetchall()

def eliminar_movimiento(movimiento_id, usuario_id):
    """Elimina un movimiento financiero"""
    try:
        cursor = g.cursor
        
        # Verificar que el movimiento pertenezca al usuario
        cursor.execute(
            "SELECT id FROM movimientos WHERE id = %s AND usuario_id = %s",
            (movimiento_id, usuario_id)
        )
        
        if not cursor.fetchone():
            return False, "No tienes permiso para eliminar este movimiento"
        
        # Eliminar movimiento
        cursor.execute("DELETE FROM movimientos WHERE id = %s", (movimiento_id,))
        g.db.commit()
        
        return True, "Movimiento eliminado correctamente"
    except Exception as e:
        g.db.rollback()
        return False, f"Error al eliminar movimiento: {str(e)}"

def actualizar_movimiento(movimiento_id, usuario_id, categoria_id, monto, descripcion, fecha):
    """Actualiza un movimiento financiero"""
    try:
        cursor = g.cursor
        
        # Verificar que el movimiento pertenezca al usuario
        cursor.execute(
            "SELECT id, tipo FROM movimientos WHERE id = %s AND usuario_id = %s",
            (movimiento_id, usuario_id)
        )
        movimiento = cursor.fetchone()
        
        if not movimiento:
            return False, "No tienes permiso para actualizar este movimiento"
        
        # Validar que la categoría exista y sea del tipo correcto
        cursor.execute("SELECT tipo FROM categorias WHERE id = %s", (categoria_id,))
        categoria = cursor.fetchone()
        
        if not categoria or categoria['tipo'] != movimiento['tipo']:
            return False, "La categoría seleccionada no es válida para este tipo de movimiento"
        
        # Convertir fecha si viene como string
        if isinstance(fecha, str):
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
            
        # Actualizar movimiento
        cursor.execute(
            """UPDATE movimientos 
               SET categoria_id = %s, monto = %s, descripcion = %s, fecha = %s
               WHERE id = %s""",
            (categoria_id, monto, descripcion, fecha, movimiento_id)
        )
        g.db.commit()
        
        return True, "Movimiento actualizado correctamente"
    except Exception as e:
        g.db.rollback()
        return False, f"Error al actualizar movimiento: {str(e)}"

def obtener_resumen_mensual(usuario_id, mes, anio):
    """Obtiene un resumen de ingresos y gastos del mes"""
    cursor = g.cursor
    
    # Total de ingresos
    cursor.execute(
        """SELECT SUM(monto) as total
           FROM movimientos
           WHERE usuario_id = %s AND tipo = 'ingreso' 
           AND MONTH(fecha) = %s AND YEAR(fecha) = %s""",
        (usuario_id, mes, anio)
    )
    total_ingresos = cursor.fetchone()['total'] or 0
    
    # Total de gastos
    cursor.execute(
        """SELECT SUM(monto) as total
           FROM movimientos
           WHERE usuario_id = %s AND tipo = 'gasto' 
           AND MONTH(fecha) = %s AND YEAR(fecha) = %s""",
        (usuario_id, mes, anio)
    )
    total_gastos = cursor.fetchone()['total'] or 0
    
    # Balance
    balance = total_ingresos - total_gastos
    
    # Gastos por categoría
    cursor.execute(
        """SELECT c.nombre, SUM(m.monto) as total
           FROM movimientos m
           JOIN categorias c ON m.categoria_id = c.id
           WHERE m.usuario_id = %s AND m.tipo = 'gasto'
           AND MONTH(m.fecha) = %s AND YEAR(m.fecha) = %s
           GROUP BY c.nombre
           ORDER BY total DESC""",
        (usuario_id, mes, anio)
    )
    gastos_por_categoria = cursor.fetchall()
    
    # Ingresos por categoría
    cursor.execute(
        """SELECT c.nombre, SUM(m.monto) as total
           FROM movimientos m
           JOIN categorias c ON m.categoria_id = c.id
           WHERE m.usuario_id = %s AND m.tipo = 'ingreso'
           AND MONTH(m.fecha) = %s AND YEAR(m.fecha) = %s
           GROUP BY c.nombre
           ORDER BY total DESC""",
        (usuario_id, mes, anio)
    )
    ingresos_por_categoria = cursor.fetchall()
    
    return {
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'balance': balance,
        'gastos_por_categoria': gastos_por_categoria,
        'ingresos_por_categoria': ingresos_por_categoria
    }

def obtener_datos_grafico_anual(usuario_id, anio):
    """Obtiene datos para gráficos anuales"""
    cursor = g.cursor
    
    # Ingresos y gastos por mes
    cursor.execute(
        """SELECT MONTH(fecha) as mes, 
                  SUM(CASE WHEN tipo = 'ingreso' THEN monto ELSE 0 END) as ingresos,
                  SUM(CASE WHEN tipo = 'gasto' THEN monto ELSE 0 END) as gastos
           FROM movimientos
           WHERE usuario_id = %s AND YEAR(fecha) = %s
           GROUP BY MONTH(fecha)
           ORDER BY MONTH(fecha)""",
        (usuario_id, anio)
    )
    
    datos_mensuales = cursor.fetchall()
    
    # Completar meses faltantes
    meses_completos = []
    meses_existentes = [d['mes'] for d in datos_mensuales]
    
    for mes in range(1, 13):
        if mes in meses_existentes:
            meses_completos.append(next(d for d in datos_mensuales if d['mes'] == mes))
        else:
            meses_completos.append({'mes': mes, 'ingresos': 0, 'gastos': 0})
    
    return meses_completos
