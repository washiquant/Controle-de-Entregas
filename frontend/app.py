import flet as ft
from backend.main import (
    Comanda,
    adicionar_comanda,
    deletar_comanda,
    atualizar_banco_de_dados,
    total_do_dia,
    buscar_comandas,
    validar_numero_comanda
)


def main(page: ft.Page):
    mensagem = ft.Text()
    lista_comandas = ft.Column()
    page.title = ("REGRESSAO 2 ( com atualizar)")
    page.scroll = ft.ScrollMode.AUTO
    def carregar_comandas():

        lista_comandas.controls.clear()

        comandas = buscar_comandas()

        for linha in comandas:
            lista_comandas.controls.append(

                ft.Card(
                    elevation=5,
                    content=ft.Container(
                        padding=15,
                        content=ft.Column(
                            [
                                ft.Text(
                                    f"🆔 ID: {linha[0]}",
                                    size=16,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text(
                                    f"📦 Comanda: {linha[1]}",
                                    size=16
                                ),

                                ft.Text(
                                    f"💰 Entrega: R$ {linha[2]}",
                                    size=18,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text(
                                    f"📍 CEP: {linha[3]}",
                                    size=15
                                )
                            ],
                            spacing=5
                        )
                    )
                )

            )

    def atualizar_total():

        total.value = (
            f"Total do Dia: R$ {total_do_dia()}"
        )

    def adicionar(e):

        try:
            #validando
            validar_numero_comanda(numero_comanda.value,valor_entrega.value,cep.value)
            #convertendo tipos :

            comanda = Comanda(
                int(numero_comanda.value),
                float(valor_entrega.value),
                cep.value
            )
            #salvando
            adicionar_comanda(comanda)
            numero_comanda.value = ""
            valor_entrega.value = ""
            cep.value = ""
            mensagem.value = "Comanda adicionada!"
            carregar_comandas()
            atualizar_total()
        except Exception as erro:

            mensagem.value = str(erro)

        page.update()

    titulo = ft.Column(
        [
            ft.Container(height=60),

            ft.Text(
                "🚚 CONTROLE DE\nENTREGAS",
                size=22,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    def quantidade_entregas():

        return len(buscar_comandas())
    def excluir(e):

        try:

            deletar_comanda(
                int(id_exclusao.value)
            )

            mensagem.value = "Comanda excluída!"

            id_exclusao.value = ""

            carregar_comandas()
            atualizar_total()
        except Exception as erro:

            mensagem.value = str(erro)

        page.update()

    def atualizar(e):

        try:

            atualizar_banco_de_dados(
                float(novo_valor.value),
                int(id_atualizacao.value)
            )

            mensagem.value = "Comanda atualizada!"

            id_atualizacao.value = ""
            novo_valor.value = ""

            carregar_comandas()
            atualizar_total()

        except Exception as erro:

            mensagem.value = str(erro)
        page.update()
    def confirmar_exclusao(e):

        def fechar_dialog(ev):

            dialog.open = False
            page.update()

        def excluir_confirmado(ev):

            try:

                deletar_comanda(
                    int(id_exclusao.value)
                )

                mensagem.value = "🗑️ Comanda excluída!"

                id_exclusao.value = ""

                carregar_comandas()
                atualizar_total()

                dialog.open = False

                page.update()

            except Exception as erro:

                mensagem.value = str(erro)

                page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar exclusão"),
            content=ft.Text(
                "Deseja realmente excluir esta comanda?"
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=fechar_dialog
                ),
                ft.TextButton(
                    "Excluir",
                    on_click=excluir_confirmado
                )
            ]
        )

        page.overlay.append(dialog)

        dialog.open = True

        page.update()

        def fechar_dialog(ev):

            dialog.open = False
            page.update()

            page.overlay.append(dialog)

            dialog.open = True

            page.update()
        page.update()

    total = ft.Text(
        f"💰 Total do Dia: R$ {total_do_dia():.2f}",
        size=24,
        weight=ft.FontWeight.BOLD
    )
    quantidade = ft.Text(
        f"📊 Entregas: {quantidade_entregas()}",
        size=18
    )
    numero_comanda = ft.TextField(
        label="Número da Comanda"
    )

    valor_entrega = ft.TextField(
        label="Valor da Entrega"
    )

    cep = ft.TextField(
        label="CEP"
    )
    id_exclusao = ft.TextField(
        label="ID para excluir"
    )
    id_atualizacao = ft.TextField(
        label="ID para atualizar"
    )
    novo_valor = ft.TextField(
    label="Novo valor da entrega"
)
    btn_adicionar = ft.OutlinedButton(
        "Adicionar Comanda",
        on_click=adicionar
    )
    btn_excluir = ft.OutlinedButton(
        "🗑️ Excluir Comanda",
        on_click=confirmar_exclusao
    )
    btn_atualizar = ft.OutlinedButton(
        "Atualizar Valor",
        on_click=atualizar
    )
    carregar_comandas()
    page.add(

        ft.Container(height=15),

        titulo,
        total,
        quantidade,
        ft.Divider(),
        numero_comanda,
        valor_entrega,
        cep,
        btn_adicionar,
        ft.Divider(),
        id_exclusao,
        btn_excluir,
        ft.Divider(),
        id_atualizacao,
        novo_valor,
        btn_atualizar,
        mensagem,
        ft.Text(
            "COMANDAS CADASTRADAS",
            size=20,
            weight=ft.FontWeight.BOLD
        ),

        lista_comandas,
        ft.Container(height=100)
    )

ft.app(target=main)

