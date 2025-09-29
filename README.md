# user-api-ghibli-role

## Ejecución del Proyecto

Hay dos formas de ejecutar el proyecto.

### Método 1: Docker

Levanta la API y la base de datos PostgreSQL.

1.  Configurar variables de entorno:
    Copiar el archivo `.env.example` a `.env` y ajustar las credenciales del `ADMIN` y los secretos de `JWT`.
    ```bash
    cp .env.example .env
    ```

2.  Levantar los servicios:
    Ejecutar el siguiente comando para construir y correr los contenedores.
    ```bash
    docker compose up -d --build
    ```
    *Nota: Puede ser necesario usar `sudo`.*

La API estará disponible en `http://localhost:8000`.

### Método 2: Manual

1.  Prerrequisitos:
    *   Disponer de una base de datos PostgreSQL activa.
    *   Instalar el gestor de paquetes `uv`.
      ```bash
      curl -LsSf https://astral.sh/uv/install.sh | sh
      ```

2.  Configurar el entorno:
    Copiar `.env.example` a `.env`.
    ```bash
    cp .env.example .env
    ```
    Abrir el archivo `.env` y configurar la `DATABASE_URL` para que apunte a la base de datos. Ajustar también las credenciales del `ADMIN` y los secretos de `JWT`.

3.  Ejecutar la aplicación:
    El comando `uv run` instala las dependencias de `pyproject.toml` y lanza el servidor.
    ```bash
    uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

## Documentación de la API

Una vez en ejecución, la documentación interactiva está disponible en las siguientes rutas:

*   **Swagger UI**: `http://localhost:8000/docs`
*   **ReDoc**: `http://localhost:8000/redoc`

## Permisos de Endpoints

Los endpoints se clasifican según su acceso. Inicialmente, solo los endpoints públicos son accesibles sin autenticación. El resto de los endpoints requieren un token JWT y su acceso está restringido según el rol del usuario (administrador o usuario normal con rol Ghibli). A continuación se detallan los permisos por tipo de usuario.


### Endpoints Públicos
- `POST /auth/login` - Iniciar sesión.
- `POST /users` - Registrar un nuevo usuario (si no se está autenticado).

### Endpoints para Administradores (Rol: `admin`)
- `GET /users` - Listar todos los usuarios.
- `POST /users` - Crear nuevos usuarios.
- `GET /users/{id}` - Obtener un usuario específico.
- `PUT /users/{id}` - Actualizar un usuario (no a sí mismo).
- `PATCH /users/{id}` - Actualizar parcialmente un usuario (no a sí mismo).
- `DELETE /users/{id}` - Eliminar un usuario (no a sí mismo).
- `GET /roles` - Listar todos los roles.
- `GET /users/me` - Obtener su propia información.

### Endpoints para Usuarios Normales (Roles: `films`, `people`, etc.)
- `GET /users/me` - Obtener su propia información.
- `PUT /users/me` - Actualizar su propia información.
- `PATCH /users/me` - Actualizar parcialmente su propia información.
- `DELETE /users/me` - Eliminar su propia cuenta.
- `GET /ghibli-api/resources/` - Acceder a la lista de recursos de Ghibli según su rol.
- `GET /ghibli-api/resources/{id}/` - Acceder a un recurso específico de Ghibli según su rol.

## Límites de Tasa (Rate Limiting)

Para controlar la frecuencia de solicitudes y por seguridad, se aplican los siguientes límites:

- **Autenticación (`/auth/login`)**: 5 solicitudes por minuto.
- **Registro de usuarios (`POST /users`)**: 10 solicitudes por minuto.
- **Resto de endpoints**: 10 solicitudes por minuto por usuario.