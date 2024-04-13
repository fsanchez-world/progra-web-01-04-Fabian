from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, name='IDUsuario')
    nombre_usuario = db.Column('NombreUsuario', db.String(50), nullable=False, unique=True)
    hash_contrasena = db.Column('HashContrasena', db.String(255), nullable=False)
    creado_en = db.Column('CreadoEn', db.DateTime, nullable=False, default=db.func.now())
    actualizado_en = db.Column('ActualizadoEn', db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())
    # Add cascade="all, delete-orphan" for cascading deletes
    listas_compras = db.relationship('ListaCompra', backref='usuario', lazy=True, cascade="all, delete-orphan")

    def hashear_contrasena(self, contrasena_original):
        self.hash_contrasena = bcrypt.hashpw(contrasena_original.encode('utf-8'), bcrypt.gensalt())

    def verificar_contrasena(self, contrasena):
        return bcrypt.checkpw(contrasena.encode('utf-8'), self.hash_contrasena.encode('utf-8'))

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, name='IDProducto')
    nombre = db.Column('Nombre', db.String(100), nullable=False)
    tipo_medida = db.Column('TipoMedida', db.String(50), nullable=False)
    creado_en = db.Column('CreadoEn', db.DateTime, nullable=False, default=db.func.now())
    actualizado_en = db.Column('ActualizadoEn', db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())
    listas_productos = db.relationship('ProductoLista', backref='producto', lazy=True)

class ListaCompra(db.Model):
    __tablename__ = 'listas_compras'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, name='IDLista')
    id_usuario = db.Column('IDUsuario', db.Integer, db.ForeignKey('usuarios.IDUsuario'), nullable=False)
    nombre = db.Column('Nombre', db.String(100), nullable=False)
    completa = db.Column('Completa', db.Boolean, nullable=False, default=True)
    creado_en = db.Column('CreadoEn', db.DateTime, nullable=False, default=db.func.now())
    actualizado_en = db.Column('ActualizadoEn', db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())
    # Add cascade="all, delete-orphan" for cascading deletes
    productos = db.relationship('ProductoLista', backref='lista_compra', lazy=True, cascade="all, delete-orphan")

class ProductoLista(db.Model):
    __tablename__ = 'producto_lista'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, name='IDProductoLista')
    id_producto = db.Column('IDProducto', db.Integer, db.ForeignKey('productos.IDProducto'), nullable=False)
    id_lista = db.Column('IDLista', db.Integer, db.ForeignKey('listas_compras.IDLista'), nullable=False)
    cantidad = db.Column('Cantidad', db.Integer, nullable=False)
    comprado = db.Column('Comprado', db.Boolean, nullable=False, default=False)
    creado_en = db.Column('CreadoEn', db.DateTime, nullable=False, default=db.func.now())
    actualizado_en = db.Column('ActualizadoEn', db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), unique=True, nullable=False)  # jti es el identificador único para JWT

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
