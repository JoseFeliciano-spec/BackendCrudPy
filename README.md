# 🚀 BackendCrudPy

**BackendCrudPy** es un backend **CRUD** (Crear, Leer, Actualizar, Eliminar) desarrollado con **FastAPI** y **MongoDB**.
Proporciona una **API RESTful** para gestionar productos y usuarios, incluyendo **autenticación basada en JWT**.

Ideal para proyectos que requieran:
✅ Gestión de usuarios con registro e inicio de sesión.
✅ Control de acceso mediante tokens **JWT**.
✅ CRUD de productos.
✅ Escalabilidad con contenedores **Docker**.

---

## 📌 Características

* 🔐 **Autenticación con JWT** (JSON Web Tokens).
* 📦 **Gestión de Productos** (crear, listar, actualizar y eliminar).
* 🗂️ Arquitectura **modular y escalable**.
* 🐳 **Dockerfile listo** para ejecutar en contenedores.
* 📖 Documentación automática con **Swagger UI** (`/docs`).

---

## 🛠️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalados:

* [Python 3.10+](https://www.python.org/downloads/)
* [MongoDB](https://www.mongodb.com/try/download/community)
* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/) (opcional, para ejecución en contenedor)

---

## 📂 Estructura del Proyecto

```
.
├── app/
│   ├── api/v1/
│   │   ├── auth_router.py      # Endpoints de autenticación
│   │   └── product_router.py   # Endpoints de productos
│   ├── core/
│   │   ├── config.py           # Configuración general
│   │   ├── db/
│   │   │   └── mongo.py        # Conexión a MongoDB
│   │   └── security.py         # JWT y seguridad
│   ├── features/
│   │   ├── auth/               # Lógica de negocio de autenticación
│   │   └── products/           # Lógica de negocio de productos
├── main.py                     # Punto de entrada FastAPI
├── requirements.txt            # Dependencias
├── Dockerfile                  # Configuración de contenedor
└── .env.example                # Variables de entorno de ejemplo
```

---

## ⚙️ Instalación Local

1. **Clonar repositorio**

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_DIRECTORIO>
   ```

2. **Crear entorno virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   Copiar `.env.example` a `.env` y completar los valores:

   ```
   MONGO_URL="mongodb://<user>:<password>@<host>:<port>"
   MONGO_DB_NAME="<database_name>"
   SECRET_KEY="<clave_secreta_jwt>"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Iniciar servidor**

   ```bash
   fastapi dev main.py
   ```

📍 Acceso a la API: `http://127.0.0.1:8000`
📍 Documentación interactiva: `http://127.0.0.1:8000/docs`

---

## 🐳 Ejecución con Docker

1. **Construir la imagen**

   ```bash
   docker build -t backend-crud-py .
   ```

2. **Ejecutar contenedor**

   ```bash
   docker run -d -p 8000:8000 --env-file .env backend-crud-py
   ```

3. **Acceder a la API**
   👉 `http://localhost:8000`

---

## 🔑 Autenticación (`/v1/auth`)

### 📌 Registro de usuario

**POST** `/v1/auth/register`

📤 **Body:**

```json
{
  "email": "user@example.com",
  "password": "string",
  "name": "string"
}
```

📥 **Respuesta 201:**

```json
{
  "id": "abc123",
  "name": "user",
  "email": "user@example.com",
  "created_at": "2025-08-22T20:49:17.149Z"
}
```

---

### 📌 Inicio de sesión

**POST** `/v1/auth/login`

📤 **Body:**

```json
{
  "email": "user@example.com",
  "password": "string"
}
```

📥 **Respuesta 200:**

```json
{
  "access_token": "jwt_token_aqui",
  "token_type": "bearer"
}
```

---

### 📌 Usuario actual

**GET** `/v1/auth/me`
📤 **Headers:**

```
Authorization: Bearer <jwt_token>
```

📥 **Respuesta 200:**

```json
{
  "data": {
    "id": "abc123",
    "name": "user",
    "email": "user@example.com",
    "created_at": "2025-08-22T20:49:17.153Z"
  },
  "statusCode": 200
}
```

---

## 📦 Productos (`/v1/products`)

### 📌 Crear producto

**POST** `/v1/products`
📤 **Body:**

```json
{
  "marca": "Nike",
  "titulo": "Air Force 1",
  "estado": "activo"
}
```

📥 **Respuesta 201:**

```json
{
  "marca": "Nike",
  "titulo": "Air Force 1",
  "estado": "activo",
  "id": "p123",
  "owner_id": "u123"
}
```

---

### 📌 Listar productos

**GET** `/v1/products?skip=0&limit=50`
📥 **Respuesta 200:**

```json
[
  {
    "marca": "Nike",
    "titulo": "Air Force 1",
    "estado": "activo",
    "id": "p123",
    "owner_id": "u123"
  }
]
```

---

### 📌 Obtener producto

**GET** `/v1/products/{product_id}`

📥 **Respuesta 200:**

```json
{
  "marca": "Nike",
  "titulo": "Air Force 1",
  "estado": "activo",
  "id": "p123",
  "owner_id": "u123"
}
```

---

### 📌 Actualizar producto

**PUT** `/v1/products/{product_id}`

📤 **Body:**

```json
{
  "marca": "Adidas",
  "titulo": "Superstar",
  "estado": "activo"
}
```

📥 **Respuesta 200:**

```json
{
  "marca": "Adidas",
  "titulo": "Superstar",
  "estado": "activo",
  "id": "p123",
  "owner_id": "u123"
}
```

---

### 📌 Eliminar producto

**DELETE** `/v1/products/{product_id}`

📥 **Respuesta 204:** (sin contenido)

---

## 🧪 Ejemplos con `curl`

### Registro

```bash
curl -X POST http://localhost:8000/v1/auth/register \
 -H "Content-Type: application/json" \
 -d '{"email":"user@example.com","password":"123456","name":"User"}'
```

### Login

```bash
curl -X POST http://localhost:8000/v1/auth/login \
 -H "Content-Type: application/json" \
 -d '{"email":"user@example.com","password":"123456"}'
```

### Crear Producto

```bash
curl -X POST http://localhost:8000/v1/products \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer <jwt_token>" \
 -d '{"marca":"Nike","titulo":"Air Force 1","estado":"activo"}'
```

---

## 🚧 Futuras Mejoras

* ✅ Roles de usuario (admin, cliente, etc).
* ✅ Paginación avanzada y filtros en productos.
* ✅ Documentación con **Redoc** y ejemplos interactivos.
* ✅ Tests automatizados con `pytest`.
* ✅ Integración continua con **GitHub Actions**.

---

💡 Creado por **Jose Feliciano**
