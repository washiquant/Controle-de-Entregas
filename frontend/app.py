import flet as ft
from backend.main import (
    Comanda,
    adicionar_comanda,
    deletar_comanda,
    atualizar_banco_de_dados,
    buscar_comandas,
    total_do_dia,
    total_da_semana,
    total_do_mes,
    media_diaria,
    media_semanal,
    media_mensal
)
from backend.grafico import gerar_grafico_faturamento_base64
from backend.cep_service import buscar_endereco_por_cep

# Imagem transparente inicial (1x1 px em formato Data URI)
IMG_PLACEHOLDER = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="


def main(page: ft.Page):
    page.title = "Sistema de Controle de Entregas"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 15

    mensagem = ft.Text(size=14, weight=ft.FontWeight.BOLD)
    lista_comandas = ft.Column(spacing=10)

    # ------------------------------------------------------------------
    # COMPONENTES DO MODAL ANALÍTICO (DASHBOARD & GRÁFICO)
    # ------------------------------------------------------------------
    img_chart = ft.Image(src=IMG_PLACEHOLDER, fit="contain", height=280)
    txt_stats_resumo = ft.Text("A carregar métricas...", size=13, color=ft.Colors.GREY_300)

    def fechar_dialogo(e=None):
        dialogo_dashboard.open = False
        page.update()

    dialogo_dashboard = ft.AlertDialog(
        title=ft.Row([
            ft.Text("📊 Painel Analítico & Gráficos", size=16, weight=ft.FontWeight.BOLD),
            ft.IconButton(ft.Icons.CLOSE, on_click=fechar_dialogo)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        content=ft.Container(
            content=ft.Column([
                img_chart,
                ft.Divider(height=15),
                txt_stats_resumo
            ], tight=True, spacing=10),
            width=380,
            padding=10
        )
    )

    page.overlay.append(dialogo_dashboard)

    def abrir_dashboard(e):
        dialogo_dashboard.open = True
        page.update()

        try:
            d_total = total_do_dia()
            s_total = total_da_semana()
            m_total = total_do_mes()

            d_media = media_diaria()
            s_media = media_semanal()
            m_media = media_mensal()

            dados_totais = {
                "Hoje": d_total,
                "Semana": s_total,
                "Mês": m_total
            }

            b64_str = gerar_grafico_faturamento_base64(dados_totais)
            img_chart.src = f"data:image/png;base64,{b64_str}"

            txt_stats_resumo.value = (
                f"📈 MÉDIAS: Dia: R$ {d_media:.2f} | Sem: R$ {s_media:.2f} | Mês: R$ {m_media:.2f}\n"
                f"💰 TOTAIS: Dia: R$ {d_total:.2f} | Sem: R$ {s_total:.2f} | Mês: R$ {m_total:.2f}"
            )
        except Exception as err:
            txt_stats_resumo.value = f"Erro ao gerar métricas: {err}"

        page.update()

    # ------------------------------------------------------------------
    # INTEGRAÇÃO VIA CEP & CAMPOS DE ENTRADA
    # ------------------------------------------------------------------
    txt_info_endereco = ft.Text(size=11, color=ft.Colors.GREY_400)

    def acao_consultar_cep(e):
        if not txt_cep.value:
            txt_info_endereco.value = ""
            page.update()
            return

        try:
            dados_cep = buscar_endereco_por_cep(txt_cep.value)
            txt_info_endereco.value = f"📍 {dados_cep['resumo']}"
            txt_info_endereco.color = ft.Colors.GREEN_400
        except Exception as err:
            txt_info_endereco.value = f"⚠️ CEP: {err}"
            txt_info_endereco.color = ft.Colors.RED_400
        page.update()

    txt_num_comanda = ft.TextField(label="Nº Comanda", expand=True)
    txt_val_entrega = ft.TextField(label="Valor (R$)", expand=True)
    txt_cep = ft.TextField(
        label="CEP",
        expand=True,
        on_blur=acao_consultar_cep,
        hint_text="Ex: 07010-010"
    )

    txt_id_excluir = ft.TextField(label="ID Excluir", width=120)
    txt_id_atualizar = ft.TextField(label="ID Alterar", width=110)
    txt_novo_valor = ft.TextField(label="Novo R$", width=110)

    # ------------------------------------------------------------------
    # OPERAÇÕES DE BANCO E REGRA DE NEGÓCIO
    # ------------------------------------------------------------------
    def carregar_comandas():
        lista_comandas.controls.clear()
        try:
            comandas = buscar_comandas()
            if not comandas:
                lista_comandas.controls.append(
                    ft.Text("Nenhuma comanda registrada.", color=ft.Colors.GREY_500)
                )
            else:
                for linha in comandas:
                    c_id, c_num, c_val, c_cep, c_data = linha[0], linha[1], linha[2], linha[3], linha[4]
                    card = ft.Card(
                        elevation=2,
                        content=ft.Container(
                            padding=12,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Column([
                                        ft.Text(f"📦 Comanda #{c_num}", size=15, weight=ft.FontWeight.BOLD),
                                        ft.Text(f"📍 CEP: {c_cep} | 🆔 ID: {c_id}", size=11, color=ft.Colors.GREY_400),
                                        ft.Text(f"🕒 {c_data}", size=10, color=ft.Colors.GREY_500),
                                    ], spacing=2),
                                    ft.Text(f"R$ {c_val:.2f}", size=16, weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.GREEN_400)
                                ]
                            )
                        )
                    )
                    lista_comandas.controls.append(card)
        except Exception as err:
            print(f"Erro ao carregar comandas: {err}")

    def acao_adicionar(e):
        try:
            if not txt_num_comanda.value or not txt_val_entrega.value or not txt_cep.value:
                raise ValueError("Preencha todos os campos!")

            # Tenta validar o CEP na API antes de salvar
            buscar_endereco_por_cep(txt_cep.value)

            val_limpo = float(txt_val_entrega.value.replace(",", "."))
            nova_comanda = Comanda(int(txt_num_comanda.value), val_limpo, txt_cep.value)
            adicionar_comanda(nova_comanda)

            txt_num_comanda.value = ""
            txt_val_entrega.value = ""
            txt_cep.value = ""
            txt_info_endereco.value = ""

            mensagem.value = "✅ Comanda adicionada!"
            mensagem.color = ft.Colors.GREEN_400
            carregar_comandas()
            page.update()
        except Exception as err:
            mensagem.value = f"⚠️ Erro: {err}"
            mensagem.color = ft.Colors.RED_400
            page.update()

    def acao_excluir(e):
        try:
            if not txt_id_excluir.value.isdigit():
                raise ValueError("Informe um ID válido.")
            deletar_comanda(int(txt_id_excluir.value))
            txt_id_excluir.value = ""
            mensagem.value = "🗑️ Comanda excluída!"
            mensagem.color = ft.Colors.GREEN_400
            carregar_comandas()
            page.update()
        except Exception as err:
            mensagem.value = f"⚠️ Erro: {err}"
            mensagem.color = ft.Colors.RED_400
            page.update()

    def acao_atualizar(e):
        try:
            if not txt_id_atualizar.value.isdigit():
                raise ValueError("ID inválido.")
            novo_val = float(txt_novo_valor.value.replace(",", "."))
            atualizar_banco_de_dados(novo_val, int(txt_id_atualizar.value))
            txt_id_atualizar.value = ""
            txt_novo_valor.value = ""
            mensagem.value = "🔄 Valor atualizado!"
            mensagem.color = ft.Colors.GREEN_400
            carregar_comandas()
            page.update()
        except Exception as err:
            mensagem.value = f"⚠️ Erro: {err}"
            mensagem.color = ft.Colors.RED_400
            page.update()

    # ------------------------------------------------------------------
    # ESTRUTURA DO LAYOUT
    # ------------------------------------------------------------------
    header = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Text("🚚 Controle de Entregas", size=18, weight=ft.FontWeight.BOLD),
            ft.IconButton(
                icon=ft.Icons.MORE_VERT,
                icon_color=ft.Colors.WHITE,
                tooltip="Painel Analítico",
                on_click=abrir_dashboard
            )
        ]
    )

    tab_operacional = ft.Column([
        ft.Text("➕ Nova Entrega", size=15, weight=ft.FontWeight.BOLD),
        ft.Row([txt_num_comanda, txt_val_entrega]),
        ft.Row([txt_cep, ft.IconButton(icon=ft.Icons.SEARCH, tooltip="Buscar CEP", on_click=acao_consultar_cep)]),
        txt_info_endereco,
        ft.ElevatedButton(
            "Cadastrar Entrega",
            icon=ft.Icons.ADD,
            on_click=acao_adicionar,
            style=ft.ButtonStyle(color=ft.Colors.GREEN_400)
        ),
        ft.Divider(),

        ft.Text("⚙️ Gerenciar", size=15, weight=ft.FontWeight.BOLD),
        ft.Row([txt_id_excluir, ft.OutlinedButton("Excluir", icon=ft.Icons.DELETE, on_click=acao_excluir)]),
        ft.Row([txt_id_atualizar, txt_novo_valor,
                ft.OutlinedButton("Atualizar", icon=ft.Icons.EDIT, on_click=acao_atualizar)]),
        ft.Divider(),

        ft.Text("📋 Comandas Registradas", size=15, weight=ft.FontWeight.BOLD),
        lista_comandas
    ], spacing=12)

    page.add(
        header,
        mensagem,
        ft.Divider(height=10),
        tab_operacional
    )

    carregar_comandas()


if __name__ == "__main__":
    import os
    # Se estiver a rodar dentro do Docker ou ambiente com PORT definida
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")