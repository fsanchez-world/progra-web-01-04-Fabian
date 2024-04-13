from flask import Blueprint
from backend.controladores.controlador_usuarios import ControladorUsuarios

# Definiendo el Blueprint para el módulo de usuarios
usuarios_bp = Blueprint('usuarios_bp', __name__)

# API endpoints y sus respectivas funciones de controlador
usuarios_bp.route('/v1/registro', methods=['POST'])(ControladorUsuarios.registro_usuario)
usuarios_bp.route('/v1/login', methods=['POST'])(ControladorUsuarios.login_usuario)
usuarios_bp.route('/v1/logout', methods=['POST'])(ControladorUsuarios.logout)