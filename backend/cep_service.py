import requests

def buscar_endereco_por_cep(cep: str) -> dict:
    """
    Consulta o webservice do ViaCEP e retorna as informações de endereço.
    Lança ValueError se o CEP for inválido ou não for encontrado.
    """
    cep_limpo = cep.replace("-", "").replace(".", "").strip()

    if len(cep_limpo) != 8 or not cep_limpo.isdigit():
        raise ValueError("CEP deve conter exatamente 8 dígitos numéricos.")

    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        dados = response.json()

        if "erro" in dados and dados["erro"] is True:
            raise ValueError("CEP não encontrado no cadastro do ViaCEP.")

        return {
            "logradouro": dados.get("logradouro", ""),
            "bairro": dados.get("bairro", ""),
            "localidade": dados.get("localidade", ""),
            "uf": dados.get("uf", ""),
            "resumo": f"{dados.get('logradouro', '')}, {dados.get('bairro', '')} - {dados.get('localidade', '')}/{dados.get('uf', '')}"
        }
    except requests.RequestException as err:
        raise ConnectionError(f"Falha de conexão ao consultar CEP: {err}")