#!/bin/bash

echo "========================================="
echo "   Iniciando entorno Django + PostgreSQL"
echo "========================================="
echo ""

# 1) Levantar (intenta docker-compose, luego docker compose)
if ! docker-compose up -d --build 2>/dev/null; then
  docker compose up -d --build
fi

if [ $? -ne 0 ]; then
    echo "Error al construir los contenedores."
    exit 1
fi

# 2. Esperar a que PostgreSQL arranque
echo "=========================================="
echo "Esperando a que la base de datos inicie..."
echo "=========================================="

until docker compose exec -T db pg_isready -U "$DB_USER" >/dev/null 2>&1; do
  echo "  ...aún no, reintentando en 2s"
  sleep 2
done
echo "PostgreSQL listo."

# Crear proyecto Django si no existe
if [ ! -f "Proyecto/SAFE/manage.py" ]; then
    echo "Creando proyecto Django..."
    docker exec django_web django-admin startproject config .
    docker exec django_web python manage.py startapp core
fi

# Ejecutar migraciones de Django
echo "=========================================="
echo "Configurando base de datos Django..."
echo "=========================================="
docker compose exec -T web python manage.py migrate

# Cargar tablas SQL personalizadas si existen
if [ -f "Proyecto/SAFE/db/init.sql" ]; then
  echo "Cargando init.sql..."
  docker compose exec -T db psql -U "$DB_USER" -d "$DB_NAME" < Proyecto/SAFE/db/init.sql
fi

echo ""
echo "============================================"
echo "   Entorno listo en http://localhost:8000"
echo "============================================"
read -p "Presiona Enter para continuar..."