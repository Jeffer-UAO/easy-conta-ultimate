# Usa la imagen base de Python
FROM python:3.10-slim

# Instala las dependencias del sistema necesarias para WeasyPrint
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear y activar un entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar el archivo requirements.txt y instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . /app
WORKDIR /app

# Run collectstatic
RUN python manage.py collectstatic --noinput

# Exponer el puerto y especificar el comando de inicio
EXPOSE 8080
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8080"]