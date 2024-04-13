## Documentación de la API del Sistema de Gestión de Listas de Compras

La API del sistema permite la gestión de usuarios, productos y listas de compras. Aquí se incluye una descripción detallada de cada uno de los endpoints disponibles, incluyendo los esquemas JSON para las solicitudes y respuestas, así como los códigos de error específicos que pueden ser devueltos por cada operación.

### Usuarios

#### Registro de usuario

- **Endpoint:** `POST /v1/registro`
- **Descripción:** Registra un nuevo usuario en el sistema.
- **JSON de solicitud:**
  ```json
  {
    "nombreUsuario": "string",
    "contrasena": "string"
  }
  ```
  - **Campos obligatorios:** `nombreUsuario`, `contrasena`
- **Respuestas:**
  - **201:** Usuario creado exitosamente.
    ```json
    {
      "mensaje": "Usuario creado exitosamente."
    }
    ```
  - **400:** Nombre de usuario y contraseña son requeridos.
  - **409:** El nombre de usuario ya está en uso.

#### Inicio de sesión

- **Endpoint:** `POST /v1/login`
- **Descripción:** Inicia sesión para un usuario existente y retorna un token JWT.
- **JSON de solicitud:**
  ```json
  {
    "nombreUsuario": "string",
    "contrasena": "string"
  }
  ```
  - **Campos obligatorios:** `nombreUsuario`, `contrasena`
- **Respuestas:**
  - **200:** Inicio de sesión exitoso.
    ```json
    {
      "mensaje": "Inicio de sesión exitoso",
      "token": "string"
    }
    ```
  - **400:** Nombre de usuario y contraseña son requeridos.
  - **401:** Credenciales incorrectas.

#### Cierre de sesión

- **Endpoint:** `POST /v1/logout`
- **Descripción:** Cierra la sesión revocando el token JWT utilizado.
- **Respuestas:**
  - **200:** Token revocado exitosamente.
    ```json
    {
      "mensaje": "El token ha sido revocado"
    }
    ```
  - **401:** JWT no proporcionado o inválido.

### Productos

#### Agregar producto

- **Endpoint:** `POST /v1/productos`
- **Descripción:** Agrega un nuevo producto a la base de datos.
- **JSON de solicitud:**
  ```json
  {
    "nombre": "string",
    "tipo_medida": "string"
  }
  ```
  - **Campos obligatorios:** `nombre`, `tipo_medida`
- **Respuestas:**
  - **201:** Producto agregado exitosamente.
    ```json
    {
      "mensaje": "Producto agregado exitosamente."
    }
    ```
  - **400:** Información proporcionada inválida o incompleta.

#### Consultar productos

- **Endpoint:** `GET /v1/productos`
- **Descripción:** Devuelve una lista de todos los productos.
- **Respuestas:**
  - **200:** Lista de productos.
    ```json
    [
      {
        "id": "int",
        "nombre": "string",
        "tipo_medida": "string"
      }
    ]
    ```

#### Consultar producto por ID

- **Endpoint:** `GET /v1/productos/{productoID}`
- **Descripción:** Devuelve detalles de un producto específico.
- **Respuestas:**
  - **200:** Detalles del producto.
    ```json
    {
      "id": "int",
      "nombre": "string",
      "tipo_medida": "string"
    }
    ```
  - **404:** Producto no encontrado.

#### Actualizar producto

- **Endpoint:** `PUT /v1/productos/{productoID}`
- **Descripción:** Actualiza la información de un producto existente.
- **JSON de solicitud:**
  ```json
  {
    "nombre": "string",
    "tipo_medida": "string"
  }
  ```
  - **Campos opcionales:** `nombre`, `tipo_medida`
- **Respuestas:**
  - **200:** Producto actualizado exitosamente.
    ```json
    {
      "mensaje": "Producto actualizado exitosamente."
    }
    ```
  - **400:** Ninguna propiedad provista para actualización.
  - **404:** Producto no encontrado.

#### Eliminar producto

- **Endpoint:** `DELETE /v1/productos/{productoID}`
- **Descripción:** Elimina un producto de la base de datos.
- **Respuestas:**
  - **200:** Producto eliminado exitosamente.
    ```json
    {
      "

mensaje": "Producto eliminado exitosamente."
    }
    ```
  - **404:** Producto no encontrado.

### Listas de Compras

#### Crear lista de compras

- **Endpoint:** `POST /v1/listascompras`
- **Descripción:** Crea una nueva lista de compras para un usuario.
- **JSON de solicitud:**
  ```json
  {
    "nombre": "string"
  }
  ```
  - **Campos obligatorios:** `nombre`
- **Respuestas:**
  - **201:** Lista de compras creada exitosamente.
    ```json
    {
      "mensaje": "Lista de compras creada exitosamente."
    }
    ```
  - **400:** El nombre de la lista es requerido.
  - **404:** Usuario no encontrado.

#### Agregar producto a una lista

- **Endpoint:** `POST /v1/listascompras/{listaID}/productos`
- **Descripción:** Agrega un producto a una lista de compras existente.
- **JSON de solicitud:**
  ```json
  {
    "id_producto": "int",
    "cantidad": "int"
  }
  ```
  - **Campos obligatorios:** `id_producto`, `cantidad`
- **Respuestas:**
  - **201:** Producto agregado exitosamente a la lista.
    ```json
    {
      "mensaje": "Producto agregado exitosamente a la lista"
    }
    ```
  - **400:** Información proporcionada inválida o incompleta.
  - **404:** Lista de compras o producto no encontrado.

#### Consultar listas de compras de un usuario

- **Endpoint:** `GET /v1/listascompras`
- **Descripción:** Devuelve todas las listas de compras asociadas a un usuario.
- **Respuestas:**
  - **200:** Listas de compras del usuario.
    ```json
    [
      {
        "id_lista": "int",
        "nombre_lista": "string",
        "completa": "boolean",
        "productos": [
          {
            "id_producto": "int",
            "nombre": "string",
            "tipo_medida": "string",
            "cantidad": "int",
            "comprado": "boolean"
          }
        ]
      }
    ]
    ```
  - **404:** Usuario no encontrado.

#### Eliminar producto de una lista

- **Endpoint:** `DELETE /v1/listascompras/{listaID}/productos/{productoID}`
- **Descripción:** Elimina un producto específico de una lista de compras.
- **Respuestas:**
  - **200:** Producto eliminado exitosamente de la lista.
    ```json
    {
      "mensaje": "Producto eliminado exitosamente de la lista"
    }
    ```
  - **404:** Lista de compras o producto no encontrado en la lista.

#### Eliminar una lista de compras

- **Endpoint:** `DELETE /v1/listascompras/{listaID}`
- **Descripción:** Elimina una lista de compras completa, incluyendo todos los productos asociados.
- **Respuestas:**
  - **200:** Lista de compras eliminada exitosamente.
    ```json
    {
      "mensaje": "Lista de compras eliminada exitosamente."
    }
    ```
  - **404:** Lista de compras no encontrada.

#### Marcar producto como comprado

- **Endpoint:** `PATCH /v1/listascompras/{listaID}/productos/{productoID}`
- **Descripción:** Marca un producto específico como comprado en una lista de compras.
- **Respuestas:**
  - **200:** Producto marcado como comprado exitosamente.
    ```json
    {
      "mensaje": "Producto marcado como comprado exitosamente"
    }
    ```
  - **404:** Lista de compras o producto no encontrado en la lista.

#### Completar una lista de compras

- **Endpoint:** `PATCH /v1/listascompras/{listaID}/completar`
- **Descripción:** Marca todos los productos de una lista de compras como comprados y la lista como completa.
- **Respuestas:**
  - **200:** Lista de compras marcada como completada exitosamente.
    ```json
    {
      "mensaje": "Lista de compras marcada como completada exitosamente."
    }
    ```
  - **404:** Lista de compras no encontrada.