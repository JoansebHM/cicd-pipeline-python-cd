# tests/test_app.py
import re

import pytest
from app.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def post_form(client, data):
    """Hace GET para obtener el token CSRF y luego envía el formulario con él."""
    page = client.get("/")
    token = re.search(rb'name="csrf_token" value="([^"]+)"', page.data).group(1)
    return client.post("/", data={**data, "csrf_token": token.decode()})


def test_index_get(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data


def test_index_post_sumar(client):
    response = post_form(client, {"num1": "2", "num2": "3", "operacion": "sumar"})
    assert response.status_code == 200
    assert b"Resultado: 5.0" in response.data


def test_index_post_restar(client):
    response = post_form(client, {"num1": "5", "num2": "3", "operacion": "restar"})
    assert response.status_code == 200
    assert b"Resultado: 2.0" in response.data


def test_index_post_multiplicar(client):
    response = post_form(
        client, {"num1": "2", "num2": "3", "operacion": "multiplicar"}
    )
    assert response.status_code == 200
    assert b"Resultado: 6.0" in response.data


def test_index_post_dividir(client):
    response = post_form(client, {"num1": "6", "num2": "3", "operacion": "dividir"})
    assert response.status_code == 200
    assert b"Resultado: 2.0" in response.data


def test_index_post_dividir_by_zero(client):
    response = post_form(client, {"num1": "6", "num2": "0", "operacion": "dividir"})
    assert response.status_code == 200
    assert b"Error: No se puede dividir por cero" in response.data


def test_index_post_potencia(client):
    response = post_form(client, {"num1": "2", "num2": "3", "operacion": "potencia"})
    assert response.status_code == 200
    assert b"Resultado: 8.0" in response.data


def test_index_post_potencia_cero_exponente_negativo(client):
    response = post_form(client, {"num1": "0", "num2": "-1", "operacion": "potencia"})
    assert response.status_code == 200
    assert b"Error: No se puede dividir por cero" in response.data


def test_index_post_potencia_resultado_complejo(client):
    response = post_form(client, {"num1": "-8", "num2": "0.5", "operacion": "potencia"})
    assert response.status_code == 200
    assert "Error: Introduce números válidos".encode() in response.data


def test_index_post_potencia_desbordamiento(client):
    response = post_form(
        client, {"num1": "10", "num2": "1000", "operacion": "potencia"}
    )
    assert response.status_code == 200
    assert b"Error: El resultado es demasiado grande" in response.data


def test_index_post_modulo(client):
    response = post_form(client, {"num1": "7", "num2": "3", "operacion": "modulo"})
    assert response.status_code == 200
    assert b"Resultado: 1.0" in response.data


def test_index_post_modulo_por_cero(client):
    response = post_form(client, {"num1": "5", "num2": "0", "operacion": "modulo"})
    assert response.status_code == 200
    assert b"Error: No se puede dividir por cero" in response.data


def test_index_post_invalid_operation(client):
    response = post_form(client, {"num1": "6", "num2": "3", "operacion": "invalid"})
    assert response.status_code == 200
    assert "Operación no válida".encode() in response.data


def test_index_post_invalid_numbers(client):
    response = post_form(client, {"num1": "a", "num2": "b", "operacion": "sumar"})
    assert response.status_code == 200
    assert "Error: Introduce números válidos".encode() in response.data


def test_index_post_sin_token_csrf_es_rechazado(client):
    response = client.post("/", data={"num1": "2", "num2": "3", "operacion": "sumar"})
    assert response.status_code == 400


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "version": "local"}
