
from backend import main
import pytest
from unittest import mock

from backend.main import Comanda


#TESTES UNITARIOS COM PYTEST
def test_adicionar_comanda():
    pass

def test_testando_validacao_comanda():

    with pytest.raises(ValueError) as erro:  # teste com o valor da entrega negativo.
        Comanda(5,-1,2)
    print(erro)

    with pytest.raises(ValueError) as erro2: # teste com o valor da entrega como string.
        Comanda(23,"asd",2)
    print(erro2)

    comanda_teste = Comanda(2,5,7080-000) # testando a conversão do cep.
    assert isinstance(comanda_teste.cep,str)

    print(comanda_teste.cep)








