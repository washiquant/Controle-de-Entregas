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


def main(page: ft.Page):
    page.title = "Sistema de Controle de Entregas"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    # Componentes globais de feedback
    mensagem = ft.Text(size=14, weight=ft.FontWeight.BOLD)
    lista_comandas = ft.Column(spacing=10)

    # ------------------------------------------------------------------
    # PIPELINE DE VALIDAÇÃO (Regras de Negócio no Frontend/Apresentação)
    # ------------------------------------------------------------------
    def validar_e_extrair_entradas(num_str: str, val_str: str, cep_str: str):
        if not num_str.strip() or not val_str.strip() or not cep_str.strip():
            raise ValueError("⚠️ Preencha todos os campos obrigatórios!")

        if not num_str.isdigit():
            raise ValueError("⚠️ O número da comanda deve conter apenas números inteiros.")

        val_limpo = val_str.replace(",", ".")
        try:
            val_float = float(val_limpo)
        except ValueError:
            raise ValueError("⚠️ O valor da entrega deve ser um número válido (ex: 15.50).")

        if val_float <= 0:
            raise ValueError("⚠️ O valor da entrega deve ser maior que zero!")

        return int(num_str), val_float, cep_str.strip()

    # ------------------------------------------------------------------
    # ATUALIZAÇÃO DA INTERFACE & DASHBOARD
    # ------------------------------------------------------------------
    def carregar_comandas():
        lista_comandas.controls.clear()
        comandas = buscar_comandas()

        if not comandas:
            lista_comandas.controls.append(
                ft.Text("Nenhuma comanda registrada hoje.", color=ft.Colors.GREY_500)
            )
        else:
            for linha in comandas:
                # linha: (id, numero, valor, cep, data)
                c_id, c_num, c_val, c_cep, c_data = linha[0], linha[1], linha[2], linha[3], linha[4]

                card = ft.Card(
                    elevation=3,
                    content=ft.Container(
                        padding=15,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column([
                                    ft.Text(f"📦 Comanda #{c_num}", size=16, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"📍 CEP: {c_cep} | 🆔 ID: {c_id}", size=12, color=ft.Colors.GREY_400),
                                    ft.Text(f"🕒 {c_data}", size=11, color=ft.Colors.GREY_500),
                                ]),
                                ft.Text(f"R$ {c_val:.2f}", size=18, weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.GREEN_400)
                            ]
                        )
                    )
                )
                lista_comandas.controls.append(card)

    def atualizar_dashboard():
        # Obtendo dados das queries SQL do backend
        t_dia = total_do_dia()
        t_sem = total_da_semana()
        t_mes = total_do_mes()
        m_dia = media_diaria()
        m_sem = media_semanal()
        m_mes = media_mensal()

        txt_total_dia.value = f"R$ {t_dia:.2f}"
        txt_total_sem.value = f"R$ {t_sem:.2f}"
        txt_total_mes.value = f"R$ {t_mes:.2f}"
        txt_media_dia.value = f"Média: R$ {m_dia:.2f}"
        txt_media_sem.value = f"Média: R$ {m_sem:.2f}"
        txt_media_mes.value = f"Média: R$ {m_mes:.2f}"

    def atualizar_tudo():
        carregar_comandas()
        atualizar_dashboard()
        page.update()

    # ------------------------------------------------------------------
    # ACOES
    # ------------------------------------------------------------------
    def acao_adicionar(e):
        try:
            c_num, c_val, c_cep = validar_e_extrair_entradas(
                txt_num_comanda.value, txt_val_entrega.value, txt_cep.value
            )

            nova_comanda = Comanda(c_num, c_val, c_cep)
            adicionar_comanda(nova_comanda)

            txt_num_comanda.value = ""
            txt_val_entrega.value = ""
            txt_cep.value = ""

            mensagem.value = "✅ Comanda adicionada com sucesso!"
            mensagem.color = ft.Colors.GREEN_400
            atualizar_tudo()

        except ValueError as err:
            mensagem.value = str(err)
            mensagem.color = ft.Colors.RED_400
            page.update()
        except Exception as err:
            mensagem.value = f"❌ Erro de banco de dados: {err}"
            mensagem.color = ft.Colors.ORANGE_400
            page.update()

    def acao_excluir(e):
        try:
            if not txt_id_excluir.value.strip().isdigit():
                raise ValueError("⚠️ Informe um ID válido para exclusão.")

            deletar_comanda(int(txt_id_excluir.value))
            txt_id_excluir.value = ""
            mensagem.value = "🗑️ Comanda excluída com sucesso!"
            mensagem.color = ft.Colors.GREEN_400
            atualizar_tudo()
        except ValueError as err:
            mensagem.value = str(err)
            mensagem.color = ft.Colors.RED_400
            page.update()

    def acao_atualizar(e):
        try:
            if not txt_id_atualizar.value.strip().isdigit():
                raise ValueError("⚠️ ID inválido para atualização.")

            val_limpo = txt_novo_valor.value.replace(",", ".")
            novo_val = float(val_limpo)
            if novo_val <= 0:
                raise ValueError("⚠️ O novo valor deve ser maior que zero.")

            atualizar_banco_de_dados(novo_val, int(txt_id_atualizar.value))
            txt_id_atualizar.value = ""
            txt_novo_valor.value = ""
            mensagem.value = "🔄 Valor atualizado com sucesso!"
            mensagem.color = ft.Colors.GREEN_400
            atualizar_tudo()
        except ValueError as err:
            mensagem.value = str(err)
            mensagem.color = ft.Colors.RED_400
            page.update()

    # ------------------------------------------------------------------
    # COMPONENTES VISUAIS (CONTROLES)
    # ------------------------------------------------------------------
    # Dashboard Cards
    txt_total_dia = ft.Text("R$ 0.00", size=20, weight=ft.FontWeight.BOLD)
    txt_media_dia = ft.Text("Média: R$ 0.00", size=12, color=ft.Colors.GREY_400)

    txt_total_sem = ft.Text("R$ 0.00", size=20, weight=ft.FontWeight.BOLD)
    txt_media_sem = ft.Text("Média: R$ 0.00", size=12, color=ft.Colors.GREY_400)

    txt_total_mes = ft.Text("R$ 0.00", size=20, weight=ft.FontWeight.BOLD)
    txt_media_mes = ft.Text("Média: R$ 0.00", size=12, color=ft.Colors.GREY_400)

    # Ajuste na criação dos cards da Dashboard para evitar o AttributeError
    def criar_card_metricas(titulo: str, txt_main, txt_sub, cor_borda):
        return ft.Container(
            expand=True,
            padding=15,
            border=ft.Border(
                top=ft.BorderSide(1, cor_borda),
                bottom=ft.BorderSide(1, cor_borda),
                left=ft.BorderSide(1, cor_borda),
                right=ft.BorderSide(1, cor_borda),
            ),
            border_radius=10,
            content=ft.Column([
                ft.Text(titulo, size=12, color=ft.Colors.GREY_300, weight=ft.FontWeight.BOLD),
                txt_main,
                txt_sub
            ], spacing=2)
        )

    row_dashboard = ft.Row([
        criar_card_metricas("HOJE", txt_total_dia, txt_media_dia, ft.Colors.BLUE_400),
        criar_card_metricas("ESTA SEMANA", txt_total_sem, txt_media_sem, ft.Colors.PURPLE_400),
        criar_card_metricas("ESTE MÊS", txt_total_mes, txt_media_mes, ft.Colors.GREEN_400),
    ])

    # Entradas de texto
    txt_num_comanda = ft.TextField(label="Nº Comanda", expand=True)
    txt_val_entrega = ft.TextField(label="Valor (R$)", expand=True)
    txt_cep = ft.TextField(label="CEP", expand=True)

    txt_id_excluir = ft.TextField(label="ID p/ Excluir", width=150)
    txt_id_atualizar = ft.TextField(label="ID p/ Alterar", width=150)
    txt_novo_valor = ft.TextField(label="Novo Valor (R$)", width=150)

    # Abas para Organização da Tela
    tab_operacional = ft.Column([
        ft.Text("➕ Nova Entrega", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([txt_num_comanda, txt_val_entrega, txt_cep]),
        ft.ElevatedButton("Cadastrar Entrega", icon=ft.Icons.ADD, on_click=acao_adicionar,
                          style=ft.ButtonStyle(color=ft.Colors.GREEN_400)),
        ft.Divider(),

        ft.Text("⚙️ Gerenciar Entregas", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([txt_id_excluir, ft.OutlinedButton("Excluir por ID", icon=ft.Icons.DELETE, on_click=acao_excluir)]),
        ft.Row([txt_id_atualizar, txt_novo_valor,
                ft.OutlinedButton("Atualizar Valor", icon=ft.Icons.EDIT, on_click=acao_atualizar)]),
        ft.Divider(),

        ft.Text("📋 Comandas Registradas", size=16, weight=ft.FontWeight.BOLD),
        lista_comandas
    ], spacing=15)

    # Layout Principal
    page.add(
        ft.Text("🚚 CONTROLE DE ENTREGAS & DASHBOARD", size=22, weight=ft.FontWeight.BOLD),
        row_dashboard,
        mensagem,
        ft.Divider(),
        tab_operacional
    )

    # Carga Inicial
    atualizar_tudo()


ft.app(target=main)