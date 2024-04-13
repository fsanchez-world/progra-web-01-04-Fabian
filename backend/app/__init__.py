import os
from flask import Flask, jsonify
from .modelos import RevokedToken, db  
from os import getenv  
from dotenv import load_dotenv  
from flask_jwt_extended import JWTManager  

# Importar los blueprints (componentes) de la aplicación
from backend.api.usuarios import usuarios_bp
from backend.api.productos import productos_bp
from backend.api.listacompras import listas_compras_bp

def jwt_callbacks(app):
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return RevokedToken.is_jti_blacklisted(jti)

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Token has been revoked"}), 401

# Definir la función para crear y configurar la instancia de la aplicación Flask
def crear_app(environment=None):
    app = Flask(__name__)  # Crear una nueva instancia de la aplicación Flask

    # Cargar las variables de entorno desde un archivo .env, si está presente
    load_dotenv()
    # Si se proporciona un nombre de entorno, configurarlo como una variable de entorno
    if(environment != None):
        os.environ['ENTORNO_FLASK'] = environment

    # Cargar el objeto de configuración apropiado basado en el entorno actual
    if getenv('ENTORNO_FLASK') == 'desarrollo':
        from backend.config.db_config import Desarrollo as Config
    elif getenv('ENTORNO_FLASK') == 'produccion':
        from backend.config.db_config import Produccion as Config
    elif getenv('ENTORNO_FLASK') == 'staging':
        from backend.config.db_config import Staging as Config
    elif getenv('ENTORNO_FLASK') == 'pruebas-caja-arena':
        from backend.config.db_config import PruebasEfimeras as Config
    elif getenv('ENTORNO_FLASK') == 'pruebas':
        from backend.config.db_config import Pruebas as Config
    else:
        # Levantar una excepción si la variable de entorno no está configurada o tiene un valor inválido
        raise ValueError("Valor de la variable de ambiente ENTORNO_FLASK incorrecto o no configurado. ¿Olvidaste definirlo en tu archivo .env? ¿Es el valor correcto?")

    # Cargar la configuración del objeto config seleccionado en la instancia de la aplicación Flask
    app.config.from_object(Config)
    # Inicializar la base de datos con la instancia de la aplicación Flask
    db.init_app(app)
    jwt_callbacks(app)

    # Registrar blueprints (componentes) con la instancia de la aplicación Flask
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(listas_compras_bp)

    # Inicializar Flask-JWT-Extended con la instancia de la aplicación Flask
    JWTManager(app)
    
    return app  # Devolver la instancia de la aplicación Flask configurada