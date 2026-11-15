"""Operaciones aritméticas básicas usadas por la calculadora web."""

AUTOR = (
    "Julián Giraldo Chica | Joan Sebastian Herrera Montes | Juan José Henao Aristizábal"
)


def sumar(a, b):
    """Devuelve la suma de ``a`` y ``b``."""
    return a + b


def restar(a, b):
    """Devuelve la resta de ``b`` a ``a``."""
    return a - b


def multiplicar(a, b):
    """Devuelve el producto de ``a`` y ``b``."""
    return a * b


def dividir(a, b):
    """Devuelve el cociente de ``a`` entre ``b``.

    Lanza ``ZeroDivisionError`` si ``b`` es cero.
    """
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a / b


def potencia(a, b):
    """Devuelve ``a`` elevado a la potencia ``b``.

    Lanza ``ZeroDivisionError`` si ``a`` es cero y ``b`` es negativo, y
    ``ValueError`` si el resultado no es un número real (por ejemplo, una
    base negativa con exponente fraccionario).
    """
    resultado = a**b
    if isinstance(resultado, complex):
        raise ValueError("El resultado no es un número real")
    return resultado


def modulo(a, b):
    """Devuelve el resto de dividir ``a`` entre ``b``.

    Lanza ``ZeroDivisionError`` si ``b`` es cero.
    """
    if b == 0:
        raise ZeroDivisionError("No se puede calcular el módulo por cero")
    return a % b
