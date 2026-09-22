import io
import base64
import matplotlib
matplotlib.use("Agg")  # Renderer headless (não abre janela Tkinter/GUI)
import matplotlib.pyplot as plt

def gerar_grafico_faturamento_base64(totais_dict: dict) -> str:
    """
    Gera um gráfico de barras comparativo com tema Dark e retorna em string Base64.
    """
    labels = list(totais_dict.keys())
    valores = list(totais_dict.values())

    # Estilização profissional em Dark Mode
    fig, ax = plt.subplots(figsize=(6, 4.2), facecolor="#1E1E2E")
    ax.set_facecolor("#1E1E2E")

    cores = ["#89B4FA", "#A6E3A1", "#FAB387"]  # Paleta Catppuccin / Modelfuturistic
    bars = ax.bar(labels, valores, color=cores, width=0.5, edgecolor="#313244", linewidth=1.5)

    # Adiciona rótulos de valores no topo das barras
    for bar in bars:
        yval = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            yval + (max(valores) * 0.02 if max(valores) > 0 else 0.5),
            f"R$ {yval:.2f}",
            ha="center",
            va="bottom",
            color="#CDD6F4",
            fontsize=9,
            fontweight="bold"
        )

    # Ajuste de eixos e grid
    ax.set_title("Resumo de Faturamento (R$)", color="#CDD6F4", fontsize=12, pad=15, weight="bold")
    ax.tick_params(colors="#A6ADC8", labelsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#45475A")
    ax.spines["bottom"].set_color("#45475A")
    ax.yaxis.grid(True, linestyle="--", alpha=0.3, color="#6C7086")

    plt.tight_layout()

    # Exportação para buffer de memória em Base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=120, transparent=True)
    buf.seek(0)
    base64_img = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)

    return base64_img