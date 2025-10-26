# Documentación del Patrón Singleton en SAFE

## Descripción

El patrón Singleton implementado en SAFE permite tener una única instancia de configuración global para toda la plataforma de aprendizaje. Esto asegura consistencia en la configuración y optimiza el rendimiento mediante el uso de caché.

## Componentes

### 1. SingletonModel (core/models.py)
Clase base abstracta que implementa el patrón Singleton con:
- Thread-safety usando locks
- Caché de alto rendimiento
- Prevención de eliminación de instancias
- Métodos de conveniencia para acceso global

### 2. SiteConfiguration (config/models.py)
Modelo concreto que hereda de SingletonModel y almacena:
- Nombre del sitio
- Modo de mantenimiento
- Configuraciones de exámenes
- Límites de estudiantes por curso
- Configuración de notificaciones

## Uso

### Obtener la configuración
```python
from config.models import SiteConfiguration

# Método recomendado
config = SiteConfiguration.load()

# Método alternativo
config = SiteConfiguration.get_config()

# Acceder a propiedades
print(config.site_name)
print(config.maintenance_mode)
```

### Actualizar la configuración
```python
config = SiteConfiguration.load()
config.site_name = "Nuevo nombre del sitio"
config.maintenance_mode = True
config.save()  # Automáticamente limpia el caché
```

### Crear con valores por defecto
```python
config = SiteConfiguration.get_or_create_singleton(
    site_name="Mi Plataforma",
    maintenance_mode=False
)
```

## API REST

### GET /core/singleton-example/
Obtiene la configuración actual del sitio.

### POST /core/singleton-example/
Actualiza la configuración del sitio.

### GET /core/health/
Verificación de salud del sistema.

## Admin Interface

El modelo está registrado en el admin de Django con:
- Prevención de creación de nuevas instancias
- Prevención de eliminación
- Redirección automática a la vista de edición

## Configuración de Caché

El sistema usa caché en memoria local con:
- Timeout de 1 hora
- Máximo 1000 entradas
- Limpieza automática al guardar

## Migraciones

Para crear las migraciones necesarias:

```bash
python manage.py makemigrations core
python manage.py makemigrations config
python manage.py migrate
```

## Docker

El docker-compose.yml está configurado para crear automáticamente las migraciones de todas las aplicaciones incluyendo core y config.

## Ventajas

1. **Thread-safe**: Múltiples hilos pueden acceder simultáneamente
2. **Alto rendimiento**: Caché reduce consultas a la base de datos
3. **Consistencia**: Una sola fuente de verdad para la configuración
4. **Fácil uso**: Métodos de conveniencia para acceso global
5. **Integración Django**: Funciona perfectamente con el admin y ORM
