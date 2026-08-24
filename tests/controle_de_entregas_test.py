#TRATATIVA DE ENTRADAS
from backend import main
import pytest
from unittest import mock

from backend.main import Comanda


def validar_numero_comanda(numero_comanda:str):
    if not numero_comanda.strip():
        raise ValueError("Numero da comanda obrigatório.")

    if not numero_comanda.isdigit():
        raise ValueError("A comanda deve conter apenas numeros reais")


def validar_valor_entrega(valor_entrega):
    if not valor_entrega.strip():
        raise ValueError("Numero da comanda obrigatório.")

    if not valor_entrega.isdigit():
        raise ValueError("A comanda deve conter apenas numeros reais")


#TESTES UNITARIOS COM PYTEST
def test_adicionar_comanda():
    comanda = main.Comanda(5,15,1,)
    assert isinstance(comanda.numero,str)
    assert isinstance(comanda.valor,int)

def test_testando_validacao_comanda():
    comanda = main.Comanda(5,5,3)
    assert comanda is not None

