#!/bin/bash

echo "========================================="
echo "   Iniciando entorno Django + PostgreSQL"
echo "========================================="
echo ""

# 1) Levantar (primero docker-compose, luego docker compose)
if ! docker-compose up -d --build 2>/dev/null; then
  docker compose up -d --build
fi

if [ $? -ne 0 ]; then
    echo "Error al construir los contenedores"
    exit 1
fi

# 2) Esperar a que Postgres este listo
echo "=========================================="
echo "Esperando a que la base de datos inicie..."
echo "=========================================="

until docker compose exec -T db pg_isready -U "$DB_USER" >/dev/null 2>&1; do
  echo "  ...aún no, reintentando en 2s"
  sleep 2
done
echo "PostgreSQL listo"

# 3) Esperar a que las migraciones de Django terminen
echo ""
echo "==========================================="
echo "Esperando a que las migraciones terminen..."
echo "==========================================="

MAX_ATTEMPTS=20
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  if docker compose logs web | grep -q "Starting development server"; then
    echo "Django está listo"
    break
  fi
  
  if docker compose logs web | grep -q "Error"; then
    echo "ERROR: Se detectó un error en las migraciones, revisa los logs"
    exit 1
  fi
  
  echo "  ...aún migrando, reintentando en 2s (intento $((ATTEMPT+1))/$MAX_ATTEMPTS)"
  sleep 2
  ATTEMPT=$((ATTEMPT+1))
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
  echo "TIMEOUT: Las migraciones tardaron demasiado, revisa los logs"
  exit 1
fi

echo ""
echo "=========================================="
echo "  Entorno listo en http://localhost:8000"
echo "=========================================="
read -p "Presiona Enter para continuar..."