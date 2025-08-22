# =========
# Builder
# =========
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Paquetes para compilar dependencias nativas si hiciera falta (bcrypt/argon2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependencias en un venv para reducir tamaño final
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip setuptools wheel && \
    /opt/venv/bin/pip install -r requirements.txt

# =========
# Runtime
# =========
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Dependencias mínimas de runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Usuario no root
RUN useradd -m appuser

# Copiamos el entorno de Python del builder
COPY --from=builder /opt/venv /opt/venv

# Copiamos el código de la app
COPY . .

# Exponemos el puerto por defecto de FastAPI CLI (ajustable con --port)
EXPOSE 8000

# Permisos
RUN chown -R appuser:appuser /app
USER appuser

# CMD usando fastapi CLI (ajusta --host/--port si lo deseas)
# Si main.py no está en la raíz, cambia la ruta (p. ej. app/main.py)
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
