# Multi-Platform Device Management API

Este proyecto es una API robusta para la gestión de dispositivos en múltiples plataformas, construida con Django, Django Rest Framework, Celery y Redis, totalmente contenerizada con Docker.

## ⚙️ Tecnologías Utilizadas

- Python 3.11+
- Django 5.2
- Django Rest Framework 3.17+
- Celery 5.2+
- Python Redis 4.5+
- Django Redis 5.3+
- DRF Spectacular 0.26+
- Postgresql 15
- Redis 7.0+

## 🚀 Instalación y Ejecución

El proyecto está diseñado para ejecutarse exclusivamente con Docker Compose, lo que garantiza un entorno de desarrollo consistente.

1. **Configurar variables de entorno:**
   Renombra el archivo `.env.example` a `.env` en la raíz del proyecto (donde se encuentra `docker-compose.yml`).

2. **Construir y levantar los contenedores:**
   ```bash
   docker compose up -d --build
   ```

3. **Ejecutar migraciones iniciales:**
   Al levantarse el proyecto con `docker compose up` el `docker-compose.yml` ya esta preparado para aplicar las migraciones antes de iniciar el servidor.

## 📦 Población de la Base de Datos

Para cargar los datos de prueba iniciales (Plataformas, Usuarios y Notificaciones) desde los archivos JSON ubicados en `backend/src/fixtures`, ejecuta:

```bash
docker compose exec backend python manage.py loaddata src/fixtures/platforms.json
docker compose exec backend python manage.py loaddata src/fixtures/users.json
docker compose exec backend python manage.py loaddata src/fixtures/notifications.json
```

## 🧪 Ejecución de Tests

Para validar el correcto funcionamiento de la lógica de negocio y los endpoints, utiliza el siguiente comando:

```bash
docker-compose exec backend pytest
```

## 🛠️ Configuración de Prueba (Plataformas y Usuarios)

Los fixtures ya contienen usuarios y plataformas precargados. Entre ellos un superadmin:

```bash
user: admin
password: 1q2w3e4r5t
```

Sin embargo, si deseas crear datos manualmente fuera de las fixtures:

1. **Crear un Superusuario:**

   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

2. **Crear Plataformas:** Accede al Admin y crea una `Platform` (ej. slug: `solvo-dev`).

## 👤 Registro de Usuario

Puedes crear nuevos usuarios desde el API, realiza una petición POST:

**Endpoint:** `POST /api/v1/auth/register/`
**Cuerpo (JSON):**
```json
{
    "email": "user@example.com",
    "password": "test123",
    "platform_slug": "solvo-test"
}
```

## 🔑 Obtención de Token JWT

El API utiliza JSON Web Tokens para la seguridad. Para obtener tus credenciales, realiza una petición POST:

**Endpoint:** `POST /api/v1/auth/token/`
**Cuerpo (JSON):**

```json
{
    "username": "tu_usuario",
    "password": "tu_password"
}
```

> Nota: Todos los usuarios que se cargan desde los fixtures usan el mismo password: **1q2w3e4r5t**, puedes usar cualquiera de ellos para probar, ya que cuentan con datos de dispositivos.

*Este comando te devolverá un `access` token y un `refresh` token para renovar sesion, usa el `access` token en las siguientes peticiones.*

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## 📱 Llamada al Endpoint de Dispositivos

Una vez autenticado, puedes listar o registrar dispositivos. Por defecto, el sistema filtra los dispositivos según la plataforma vinculada a tu usuario.

**Listar dispositivos:**
```bash
curl -X GET http://localhost:8000/api/v1/devices/ \
     -H "Authorization: Bearer <TU_ACCESS_TOKEN>"
```

## 🖥️ Acceso al Panel de Administración

Para gestionar los modelos de la base de datos de forma visual:

**URL:** http://localhost:8000/admin/

## 📖 Documentación API (Swagger)

El proyecto integra **Swagger** mediante `drf-spectacular`, lo que permite visualizar, documentar y probar los endpoints en tiempo real, incluyendo los filtros definidos para el endpoint de dispositivos.

**URL de Documentación Interactiva:** http://localhost:8000/api/docs/

## 🔄 Cómo pasar el Schema de Swagger a Postman

Si prefieres realizar tus pruebas desde Postman, sigue estos pasos:

1. **Obtener el Schema:** Navega a `http://localhost:8000/api/schema/` para descargar el archivo de especificación (OpenAPI YAML/JSON).
2. **Importar en Postman:**
   - Abre Postman y haz clic en el botón **Import** (esquina superior izquierda).
   - Arrastra el archivo descargado o pega la URL del schema.
3. **Generar Colección:** Postman detectará el formato OpenAPI y te permitirá generar una colección completa con todos los endpoints, parámetros de filtrado y estructuras de datos listas para usar.

---
