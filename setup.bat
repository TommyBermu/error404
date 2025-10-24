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

REM 3) Esperar a que las migraciones de Django terminen
echo.
echo ==========================================
echo Esperando a que las migraciones terminen...
echo ==========================================

set MAX_ATTEMPTS=20
set ATTEMPT=0

:wait_django
set /a ATTEMPT+=1

REM Verificar si Django está corriendo
docker compose logs web 2>NUL | findstr /C:"Starting development server" >NUL 2>&1
IF %ERRORLEVEL% EQU 0 (
  echo Django esta listo
  goto django_ready
)

REM Verificar si hay errores
docker compose logs web 2>NUL | findstr /C:"Error" >NUL 2>&1
IF %ERRORLEVEL% EQU 0 (
  echo ERROR: Se detecto un error en las migraciones, revisa los logs
  pause
  exit /b 1
)

REM Timeout check
IF %ATTEMPT% GEQ %MAX_ATTEMPTS% (
  echo TIMEOUT: Las migraciones tardaron demasiado, revisa los logs
  pause
  exit /b 1
)

echo   ...aun migrando, reintentando en 2s (intento %ATTEMPT%/%MAX_ATTEMPTS%)
timeout /t 2 >NUL
goto wait_django

:django_ready
echo ================================
echo   Listo: http://localhost:8000
echo ================================
pause