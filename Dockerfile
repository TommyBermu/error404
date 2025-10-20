
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar PostgreSQL client (necesario para psycopg2)
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY Proyecto/SAFE/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY Proyecto/SAFE/ .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]