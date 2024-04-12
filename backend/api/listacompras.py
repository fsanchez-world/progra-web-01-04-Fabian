from flask import Blueprint
from backend.controladores.controlador_listacompras import ControladorListaCompras

listas_compras_bp = Blueprint('listas_compras_bp', __name__)

# API endpoint para crear nuevas listas de compras
listas_compras_bp.route('/v1/listascompras', methods=['POST'])(ControladorListaCompras.crear_lista_compras)

# API endpoint para agregar productos a una lista de compras
listas_compras_bp.route('/v1/listascompras/<int:listaID>/productos', methods=['POST'])(ControladorListaCompras.agregar_producto_a_lista)

# API endpoint para consultar todas las listas de compras de un usuario
listas_compras_bp.route('/v1/listascompras', methods=['GET'])(ControladorListaCompras.consultar_listas_compras)

# API endpoint para eliminar un producto de una lista de compras
listas_compras_bp.route('/v1/listascompras/<int:listaID>/productos/<int:productoID>', methods=['DELETE'])(ControladorListaCompras.eliminar_producto_de_lista)

# API endpoint para eliminar una lista de compras
listas_compras_bp.route('/v1/listascompras/<int:listaID>', methods=['DELETE'])(ControladorListaCompras.eliminar_lista_compras)

# API endpoint para marcar un producto como comprado en una lista de compras
listas_compras_bp.route('/v1/listascompras/<int:listaID>/productos/<int:productoID>', methods=['PATCH'])(ControladorListaCompras.marcar_producto_como_comprado)

# API endpoint para marcar todos los productos de una lista como comprados y la lista como completa
listas_compras_bp.route('/v1/listascompras/<int:listaID>/completar', methods=['PATCH'])(ControladorListaCompras.marcar_lista_como_completada)