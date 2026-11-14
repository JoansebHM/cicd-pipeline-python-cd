"""Aplicación web Flask que expone una calculadora básica."""

from flask import Flask, render_template, request

from .calculadora import dividir, multiplicar, restar, sumar

app = Flask(__name__)


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

        if operacion == "sumar":
            resultado = sumar(num1, num2)
        elif operacion == "restar":
            resultado = restar(num1, num2)
        elif operacion == "multiplicar":
            resultado = multiplicar(num1, num2)
        elif operacion == "dividir":
            resultado = dividir(num1, num2)
        else:
            resultado = "Operación no válida"
    except ValueError:
        resultado = "Error: Introduce números válidos"
    except ZeroDivisionError:
        resultado = "Error: No se puede dividir por cero"

    return render_template("index.html", resultado=resultado)


if __name__ == "__main__":  # pragma: no cover
    # Servidor de desarrollo: solo escucha en localhost y sin modo debug.
    # En el contenedor la app se sirve con Gunicorn (ver Dockerfile).
    app.run(port=5000)
