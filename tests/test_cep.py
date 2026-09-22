import pytest
from unittest import mock
from backend.cep_service import buscar_endereco_por_cep

def test_cep_formato_invalido():
    """Valida erro quando o formato do CEP tem tamanho ou caracteres incorretos."""
    with pytest.raises(ValueError, match="8 dígitos"):
        buscar_endereco_por_cep("123")

def test_buscar_cep_com_sucesso_mock():
    """Testa o retorno do serviço simulando uma resposta positiva do ViaCEP."""
    resposta_mock = mock.Mock()
    resposta_mock.status_code = 200
    resposta_mock.json.return_value = {
        "logradouro": "Rua Capitão Gabriel",
        "bairro": "Centro",
        "localidade": "Guarulhos",
        "uf": "SP"
    }

    with mock.patch("requests.get", return_value=resposta_mock):
        resultado = buscar_endereco_por_cep("07010-010")
        assert resultado["bairro"] == "Centro"
        assert resultado["localidade"] == "Guarulhos"
        assert "Rua Capitão Gabriel" in resultado["resumo"]