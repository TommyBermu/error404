@echo off
setlocal ENABLEDELAYEDEXPANSION

echo =========================================
echo   Iniciando entorno Django + PostgreSQL
echo =========================================

REM 1) Levantar (primero docker-compose, luego docker compose)
docker-compose up -d --build
IF %ERRORLEVEL% NEQ 0 (
  docker compose up -d --build
  IF %ERRORLEVEL% NEQ 0 (
    echo Error al construir contenedores.
    pause
    exit /b 1
  )
)

REM 2) Esperar a que Postgres este listo
echo Esperando a que PostgreSQL responda...

REM Valores por defecto si no existen variables de entorno
IF "%DB_USER%"=="" set DB_USER=postgres
IF "%DB_NAME%"=="" set DB_NAME=SAFE_db

:wait_pg
docker compose exec -T db pg_isready -U %DB_USER% >NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
  timeout /t 2 >NUL
  goto wait_pg
)
echo PostgreSQL listo.

REM 3) Migraciones
echo Aplicando migraciones Django...
docker compose exec -T web python manage.py migrate

REM 4) (Opcional) cargar SQL si existe
IF EXIST Proyecto\SAFE\db\init.sql (
  echo Cargando init.sql...
  docker compose exec -T db psql -U %DB_USER% -d %DB_NAME% < Proyecto\SAFE\db\init.sql
)

echo ==========================================
echo   Listo: http://localhost:8000
echo ==========================================
pause