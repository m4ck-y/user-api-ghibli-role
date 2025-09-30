# user-api-ghibli-role

## En Línea

La API está desplegada en **Google Cloud Run** y se puede acceder desde la siguiente URL de producción para probar los servicios en vivo:

[https://user-api-ghibli-role-75970756205.europe-west1.run.app/docs](https://user-api-ghibli-role-75970756205.europe-west1.run.app/docs)

## Ejecución local

El proyecto se puede ejecutar de dos maneras: con Docker (recomendado) o manualmente.

### Método 1: Docker

Este método levanta la API y la base de datos PostgreSQL de forma automática.

1.  Configurar variables de entorno:
    Copia el archivo `.env.example` a `.env` y ajusta las credenciales del `ADMIN` y los secretos de `JWT`.
    ```bash
    cp .env.example .env
    ```

2.  Levantar los servicios:
    Ejecutar el siguiente comando para construir y correr los contenedores.
    ```bash
    docker compose up -d --build
    ```

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

El acceso a la API está protegido por roles. Al principio, solo los endpoints públicos están disponibles. Para acceder al resto, se necesita un token JWT que se obtiene al iniciar sesión. Los permisos se dividen de la siguiente manera:


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

Para controlar la frecuencia de solicitudes y prevenir abusos, se aplican los siguientes límites de tasa:

- **Autenticación (`/auth/login`)**: 5 solicitudes por minuto.
- **Registro de usuarios (`POST /users`)**: 10 solicitudes por minuto.
- **Resto de endpoints**: 10 solicitudes por minuto por usuario.

## Screenshots (Despliegue en la nube) 
[https://user-api-ghibli-role-75970756205.europe-west1.run.app/docs](https://user-api-ghibli-role-75970756205.europe-west1.run.app/docs)

**[Neon](https://neon.com/)** como proveedor de base de datos en la nube, aprovechando su capa gratuita para bases de datos PostgreSQL. A continuación, se muestran varias capturas de pantalla del proceso de implementación y uso de la API en Google Cloud Platform (GCP) y la integración con la API de Studio Ghibli.

1. **URL de conexión proporcionada por Neon**:  
   Esta es la URL de conexión a la base de datos PostgreSQL proporcionada por la plataforma **Neon**, que se utilizará para conectar la API a la base de datos.  
   ![Neon URL de Conexión](https://storage.googleapis.com/user-api-ghibli/neon_url_connection.png)

2. **Configuración de GCP Run con GitHub**:  
   Configuración de **GCP Run** para vincular el repositorio de **GitHub**, donde se aloja el código del proyecto. Este paso es necesario para implementar el servicio en la nube.  
   ![GCP Run con GitHub](https://storage.googleapis.com/user-api-ghibli/gcp_run_repo.png)

3. **Configuración de GCP Run, seleccionando la rama y la dirección del Dockerfile**:  
   En esta captura se muestra cómo seleccionar la rama y la ubicación del **Dockerfile** que se usará para construir la imagen del contenedor en **Google Cloud Run**.  
   ![Configuración de GCP Run](https://storage.googleapis.com/user-api-ghibli/gcp_dockerfile.png)

4. **Permitir acceso público al servicio en GCP Run**:  
   Esta captura muestra la configuración de acceso público en **GCP Run**, lo que permite que el servicio sea accesible desde cualquier lugar a través de una URL pública.  
   ![Acceso Público en GCP Run](https://storage.googleapis.com/user-api-ghibli/gcp_public_access.png)

5. **Configuración de contenedor, puerto y variables de entorno en GCP Run**:  
   Aquí se configura el contenedor en **GCP Run**, donde se establece el puerto de escucha y las variables de entorno necesarias, como la URL de conexión a PostgreSQL que se obtuvo de **Neon**.  
   ![Configuración de Contenedor en GCP Run](https://storage.googleapis.com/user-api-ghibli/gcp_port.png)

6. **Servicio corriendo correctamente en GCP Run, mostrando la documentación con FastAPI y Swagger**:  
   En esta captura se muestra el servicio corriendo exitosamente en **GCP Run**. Se puede acceder a la documentación interactiva generada automáticamente por **FastAPI** y **Swagger UI**.  
   ![Swagger UI en GCP Run](https://storage.googleapis.com/user-api-ghibli/gcp_swagger.png)

7. **Login desde la documentación de Swagger**:  
   Esta captura muestra el proceso de inicio de sesión desde la interfaz de Swagger. Un usuario normal, con el rol de **species**, puede iniciar sesión y utilizar los endpoints según su rol.  
   ![Login con Usuario Normal](https://storage.googleapis.com/user-api-ghibli/gcp_login_normal.png)

8. **Usuario normal intentando eliminar usuarios**:  
   En esta captura se observa a un usuario normal intentando eliminar a otro usuario. El servicio está correctamente validado para que solo los administradores puedan realizar esta acción.  
   ![Usuario Normal Intentando Eliminar](https://storage.googleapis.com/user-api-ghibli/gcp_login_normal_delete.png)

9. **Usuario con rol 'species' consumiendo su servicio y listando recursos de Ghibli**:  
   Aquí se muestra cómo un usuario con el rol **species** consume el servicio y lista todos los recursos correspondientes de Ghibli. Los recursos se obtienen desde el endpoint `ghibli-api/resources/` según el rol asignado.  
   ![Listando Recursos Ghibli](https://storage.googleapis.com/user-api-ghibli/gcp_login_normal_ghibli_all.png)

10. **Usuario con rol 'species' obteniendo un recurso específico de Ghibli**:  
   Esta captura muestra cómo un usuario con el rol **species** obtiene un recurso específico de Ghibli usando el endpoint `ghibli-api/resources/{resource_id}`. Este endpoint devuelve un único recurso según el ID proporcionado.  
   ![Obteniendo un Recurso Ghibli](https://storage.googleapis.com/user-api-ghibli/gcp_login_normal_ghibli.png)
