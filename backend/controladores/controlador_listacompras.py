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

    @staticmethod
    @jwt_required()
    def eliminar_producto_de_lista(listaID, productoID):
        """
        Elimina un producto de una lista de compras.
        """
        # Verificar que el usuario esté autorizado para modificar la lista
        user_id = get_jwt_identity()
        lista_compra = ListaCompra.query.filter_by(id=listaID).first()
        if not lista_compra:
            return jsonify({"error": "Lista de compras no encontrada"}), 404
        
        # Verificar que el producto esté en la lista
        producto_lista = ProductoLista.query.filter_by(id_lista=listaID, id_producto=productoID).first()
        if not producto_lista:
            return jsonify({"error": "Producto no encontrado en la lista"}), 404

        # Eliminar el producto de la lista
        db.session.delete(producto_lista)
        db.session.commit()
        return jsonify({"mensaje": "Producto eliminado exitosamente de la lista"}), 200

    @staticmethod
    @jwt_required()
    def eliminar_lista_compras(listaID):
        """
        Elimina una lista de compras completa, incluyendo todos los productos asociados.
        """
        user_id = get_jwt_identity()  # Suponiendo que la identidad es el nombre de usuario

        # Obtener la lista a eliminar
        lista_compra = ListaCompra.query.filter_by(id=listaID).first()
        if not lista_compra:
            return jsonify({"error": "Lista de compras no encontrada"}), 404
        
        # Eliminar todas las entradas de productos asociadas
        ProductoLista.query.filter_by(id_lista=listaID).delete()
        # Eliminar la lista de compras en sí
        db.session.delete(lista_compra)
        db.session.commit()

        return jsonify({"mensaje": "Lista de compras eliminada exitosamente."}), 200

    @staticmethod
    @jwt_required()
    def marcar_producto_como_comprado(listaID, productoID):
        """
        Marca un producto como comprado en una lista de compras.
        """
        # Verificar que el usuario esté autorizado para la lista
        user_id = get_jwt_identity()
        lista_compra = ListaCompra.query.filter_by(id=listaID).first()
        if not lista_compra:
            return jsonify({"error": "Lista de compras no encontrada"}), 404

        # Verificar que el producto esté en la lista
        producto_lista = ProductoLista.query.filter_by(id_lista=listaID, id_producto=productoID).first()
        if not producto_lista:
            return jsonify({"error": "Producto no encontrado en la lista"}), 404

        # Marcar el producto como comprado
        producto_lista.comprado = True
        db.session.commit()

        return jsonify({"mensaje": "Producto marcado como comprado exitosamente"}), 200

    @staticmethod
    @jwt_required()
    def marcar_lista_como_completada(listaID):
        """
        Marca todos los productos de una lista de compras como comprados y la lista como completada.
        """
        user_id = get_jwt_identity()  # Suponiendo que la identidad es el nombre de usuario
        lista_compra = ListaCompra.query.filter_by(id=listaID).first()
        if not lista_compra:
            return jsonify({"error": "Lista de compras no encontrada"}), 404

        # Marcar todos los productos como comprados
        for producto in lista_compra.productos:
            producto.comprado = True
        lista_compra.completa = True  # Marcar la lista como completada
        db.session.commit()

        return jsonify({"mensaje": "Lista de compras marcada como completada exitosamente."}), 200