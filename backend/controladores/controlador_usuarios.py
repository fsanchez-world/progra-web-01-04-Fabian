from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
import pytest
from backend.app.modelos import RevokedToken, db, Usuario

class ControladorUsuarios:
    @staticmethod
    def registro_usuario():
        data = request.get_json()
        nombre_usuario = data.get('nombreUsuario')
        contrasena = data.get('contrasena')
        
        if not nombre_usuario or not contrasena:
            return jsonify({"error": "Nombre de usuario y contraseña son requeridos"}), 400
        
        if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
            return jsonify({"error": "El nombre de usuario ya está en uso"}), 409
        
        nuevo_usuario = Usuario(nombre_usuario=nombre_usuario)
        nuevo_usuario.hashear_contrasena(contrasena)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return jsonify({"mensaje": "Usuario creado exitosamente."}), 201

    @staticmethod
    def login_usuario():
        data = request.get_json()
        nombre_usuario = data.get('nombreUsuario')
        contrasena = data.get('contrasena')

        if not nombre_usuario or not contrasena:
            return jsonify({"error": "Nombre de usuario y contraseña son requeridos"}), 400
        
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        if usuario is None or not usuario.verificar_contrasena(contrasena):
            return jsonify({"error": "Credenciales incorrectas"}), 401
        
        token = create_access_token(identity=nombre_usuario)
        return jsonify({"mensaje": "Inicio de sesión exitoso", "token": token}), 200
    
    @jwt_required()
    def logout():
        jti = get_jwt()['jti']  # Accede al jti (identificador único) del JWT
        revoked_token = RevokedToken(jti=jti)
        revoked_token.add()
        return jsonify({"mensaje": "El token ha sido revocado"}), 200

class TestLogoutUsuario:
    @pytest.fixture
    def usuario(self, session):
        """Create a user fixture that will be used in the tests."""
        usuario = Usuario(nombre_usuario="testLogoutUser", hash_contrasena="hashedpassword")
        usuario.hashear_contrasena("hashedpassword")
        session.add(usuario)
        session.commit()
        return usuario

    @pytest.fixture
    def token(self, usuario):
        """Generate a JWT token for the user."""
        return create_access_token(identity=usuario.nombre_usuario)

    def test_logout_exitoso(self, client, usuario, token):
        """Test that a user can successfully logout and the token is revoked."""
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = client.post('/v1/logout', headers=headers)
        assert response.status_code == 200
        assert 'El token ha sido revocado' in response.get_json()['mensaje']

        # Check the token is actually revoked
        revoked = RevokedToken.is_jti_blacklisted(get_jwt()['jti'])
        assert revoked == True

    def test_logout_con_token_invalido(self, client):
        """Test logout with an invalid token."""
        bad_token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGl0eSI6ImludmFsaWR1c2VyIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIiwianRpIjoiZGY5NzBlYTAtNWMzMy00NmRkLWE5YmItYzNkZmJjMjUyMzM3IiwiZXhwIjoxNjE5MzUyMzY3LCJuYmYiOjE2MTkzNTIwNjcsImlhdCI6MTYxOTM1MjA2N30.Pk_id7FkUpkij6R9qL4RniLf9FNXUB6KD8ZSF1vH2CE'
        headers = {
            'Authorization': bad_token
        }
        response = client.post('/v1/logout', headers=headers)
        assert response.status_code == 422  # Typically a 422 or 401 depending on JWT configuration

    def test_logout_sin_token(self, client):
        """Test logout without providing a JWT token."""
        response = client.post('/v1/logout')
        assert response.status_code == 401
        assert 'Missing Authorization Header' in response.get_json()['msg']