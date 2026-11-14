# app/calculadora.py

AUTOR = (
    "Julián Giraldo Chica | Joan Sebastian Herrera Montes | Juan José Henao Aristizábal"
)


def sumar(a, b):
    return a + b


def restar(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a / b
