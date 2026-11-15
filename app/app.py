"""Aplicación web Flask que expone una calculadora básica."""

import os
import secrets

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

from .calculadora import dividir, modulo, multiplicar, potencia, restar, sumar

OPERACIONES = {
    "sumar": sumar,
    "restar": restar,
    "multiplicar": multiplicar,
    "dividir": dividir,
    "potencia": potencia,
    "modulo": modulo,
}

app = Flask(__name__)
# La clave firma los tokens CSRF. En producción se define con la variable de
# entorno SECRET_KEY; si no existe se genera una aleatoria al iniciar.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
csrf = CSRFProtect(app)


@app.get("/")
def index():
    """Muestra el formulario de la calculadora sin resultado."""
    return render_template("index.html", resultado=None)


@app.post("/")
def calcular():
    """Procesa el formulario y muestra el resultado de la operación elegida."""
    try:
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        operacion = request.form["operacion"]

        funcion = OPERACIONES.get(operacion)
        if funcion is None:
            resultado = "Operación no válida"
        else:
            resultado = funcion(num1, num2)
    except ValueError:
        resultado = "Error: Introduce números válidos"
    except ZeroDivisionError:
        resultado = "Error: No se puede dividir por cero"
    except OverflowError:
        resultado = "Error: El resultado es demasiado grande"

    return render_template("index.html", resultado=resultado)


@app.get("/health")
def health():
    """Health check usado por el Load Balancer. Incluye la versión desplegada."""
    return {"status": "ok", "version": os.environ.get("APP_VERSION", "local")}


if __name__ == "__main__":  # pragma: no cover
    # Servidor de desarrollo: solo escucha en localhost y sin modo debug.
    # En el contenedor la app se sirve con Gunicorn (ver Dockerfile).
    app.run(port=5000)
