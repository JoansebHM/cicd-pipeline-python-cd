# Dockerfile
# Usa una imagen base oficial de Python. Elige una versión específica para consistencia.
FROM python:3.13-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia solo el archivo lock primero para aprovechar el cache de Docker.
# requirements.lock fija todas las dependencias (incluidas las transitivas) con sus hashes.
COPY requirements.lock .

# Instala solo las dependencias de ejecución (Flask, Flask-WTF y Gunicorn):
# --require-hashes verifica cada paquete contra el hash del lock
# --only-binary :all: instala solo wheels, sin ejecutar scripts setup.py
# --no-cache-dir reduce el tamaño de la imagen
RUN pip install --no-cache-dir --require-hashes --only-binary :all: -r requirements.lock

# Crea un usuario sin privilegios para no ejecutar la aplicación como root
RUN useradd --create-home --uid 10001 appuser

# Copia el código de la aplicación (solo la carpeta app)
COPY app/ ./app/

# A partir de aquí todo se ejecuta como el usuario sin privilegios
USER appuser

# Expón el puerto en el que Gunicorn servirá la aplicación
# Gunicorn por defecto usa 8000, así que usaremos ese.
EXPOSE 8000

# Comando para ejecutar la aplicación usando Gunicorn cuando el contenedor inicie
# 'app.app:app' significa: del archivo app.py dentro del paquete app, usa la instancia 'app' de Flask.
# 'workers=4' es un ejemplo, ajusta según sea necesario.
# 'bind 0.0.0.0:8000' hace que Gunicorn escuche en todas las interfaces de red en el puerto 8000.
# '--preload' carga la app una sola vez antes de crear los workers, así todos comparten
# la misma SECRET_KEY y un token CSRF emitido por un worker es válido en los demás.
CMD ["gunicorn", "--workers=4", "--preload", "--bind=0.0.0.0:8000", "app.app:app"]
