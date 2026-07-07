#TRATATIVA DE ENTRADAS
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

