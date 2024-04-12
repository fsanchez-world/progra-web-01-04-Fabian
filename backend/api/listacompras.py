from flask import Blueprint
from backend.controladores.controlador_listacompras import ControladorListaCompras

listas_compras_bp = Blueprint('listas_compras_bp', __name__)

# Punto de API para crear nuevas listas de compras
listas_compras_bp.route('/v1/listascompras', methods=['POST'])(ControladorListaCompras.crear_lista_compras)

# Punto de API para agregar productos a una lista de compras
listas_compras_bp.route('/v1/listascompras/<int:listaID>/productos', methods=['POST'])(ControladorListaCompras.agregar_producto_a_lista)

# Punta de API para consultar todas las listas de compras de un usuario
listas_compras_bp.route('/v1/listascompras', methods=['GET'])(ControladorListaCompras.consultar_listas_compras)

# Punta de API para eliminar un producto de una lista de compras
listas_compras_bp.route('/v1/listascompras/<int:listaID>/productos/<int:productoID>', methods=['DELETE'])(ControladorListaCompras.eliminar_producto_de_lista)