from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.modelos import db, ListaCompra, Usuario, Producto, ProductoLista

class ControladorListaCompras:
    """
    ControladorListaCompras es una clase que maneja la creación de listas de compras para un usuario.
    """

    @staticmethod
    @jwt_required()
    def crear_lista_compras():
        """
        Crea una nueva lista de compras para un usuario.

        Retorna:
            Una respuesta JSON indicando el éxito o fracaso de la operación.
        """
        user_id = get_jwt_identity()  # Suponiendo que la identidad es el ID del usuario
        data = request.get_json()

        nombre_lista = data.get('nombre')
        if not nombre_lista:
            return jsonify({"error": "El nombre de la lista es requerido"}), 400
        
        # Obtener el usuario de la base de datos
        usuario = Usuario.query.filter_by(nombre_usuario=user_id).first()
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        nueva_lista = ListaCompra(nombre=nombre_lista, id_usuario=usuario.id)
        db.session.add(nueva_lista)
        db.session.commit()

        return jsonify({"mensaje": "Lista de compras creada exitosamente."}), 201

    @staticmethod
    @jwt_required()
    def agregar_producto_a_lista(listaID):
        """
        Adds a product to a shopping list with specified quantity.
        """
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validations
        if 'id_producto' not in data or 'cantidad' not in data:
            return jsonify({"error": "Información proporcionada inválida o incompleta"}), 400
        
        # Find the shopping list
        lista_compra = ListaCompra.query.filter_by(id=listaID).first()
        if not lista_compra:
            return jsonify({"error": "Lista de compras no encontrada"}), 404
        
        # Check if the product exists
        producto = Producto.query.get(data['id_producto'])
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
        
        # Create new ProductoLista entry
        nuevo_producto_lista = ProductoLista(
            id_lista=listaID,
            id_producto=data['id_producto'],
            cantidad=data['cantidad'],
            comprado=False  # default value
        )
        db.session.add(nuevo_producto_lista)
        db.session.commit()

        return jsonify({"mensaje": "Producto agregado exitosamente a la lista"}), 201

    @staticmethod
    @jwt_required()
    def consultar_listas_compras():
        user_id = get_jwt_identity()  # Suponiendo que la identidad es el nombre de usuario

        # Obtener el usuario por nombre de usuario para obtener el ID de usuario
        usuario = Usuario.query.filter_by(nombre_usuario=user_id).first()
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Obtener todas las listas de compras del usuario
        listas = ListaCompra.query.filter_by(id_usuario=usuario.id).all()
        resultados = []
        for lista in listas:
            # Obtener los productos de cada lista
            productos = []
            for producto_lista in lista.productos:
                producto = {
                    "id_producto": producto_lista.producto.id,
                    "nombre": producto_lista.producto.nombre,
                    "tipo_medida": producto_lista.producto.tipo_medida,
                    "cantidad": producto_lista.cantidad,
                    "comprado": producto_lista.comprado
                }
                productos.append(producto)
            resultado = {
                "id_lista": lista.id,
                "nombre_lista": lista.nombre,
                "completa": lista.completa,
                "productos": productos
            }
            resultados.append(resultado)

        return jsonify(resultados), 200