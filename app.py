from flask import Flask, redirect, url_for
from routers.auth_routes import auth_bp
from routers.finance_routes import finance_bp
from conexion.db import init_app
import os
from datetime import datetime

def create_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave_secreta_predeterminada')
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Filtro personalizado para formato COP
    @app.template_filter('cop')
    def format_cop(value):
        try:
            return "${:,}".format(int(round(value))).replace(",", ".")
        except:
            return value
    
    # Inicializar conexión a la base de datos
    init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(finance_bp, url_prefix='/finanzas')

    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
    
    # Ruta raíz
    @app.route('/')
    def index():
        return redirect(url_for('finance.dashboard'))
    
    return app
