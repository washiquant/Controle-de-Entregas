# 🚚 Sistema de Controle de Entregas & Painel Analítico

> Aplicação Desktop/Web para gestão operacional de entregas, controle financeiro de comandas e análise gráfica de faturamento em tempo real.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/Flet-0.80+-512BD4?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Suíte_Passou-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/Licença-MIT-green?style=for-the-badge)

---

## 📌 Sobre o Projeto

O **Sistema de Controle de Entregas** foi projetado para resolver o problema prático do acompanhamento diário de corridas e comandas no setor de entregas. O sistema simplifica a rotina operacional ao integrar **consulta dinâmica de CEP**, validações rigorosas de dados e exibição instantânea de métricas financeiras (médias e faturamento total acumulado por dia, semana e mês).

A interface foi desenvolvida com **Flet** (estrutura reativa em Python baseada no Flutter engine), garantindo um visual moderno em Dark Mode e excelente fluidez de uso.

---

## ✨ Funcionalidades Principais

- **📦 Operacional & CRUD de Comandas:**
  - Cadastro rápido de entregas informando número da comanda, valor e CEP.
  - Atualização de valores e exclusão de entregas por ID do registro.
  - Listagem reativa e organizada em *Cards*.

- **🌐 Integração com API REST (ViaCEP):**
  - Validação e busca automática do endereço (logradouro, bairro, cidade e UF) assim que o CEP é inserido no campo ou ao clicar na busca.
  - Tratamento de exceções para CEPs inexistentes ou formatos incorretos antes da gravação no banco.

- **📊 Painel Analítico & Gráficos Dinâmicos:**
  - Cálculo consolidado de **Totais** e **Médias** (Diária, Semanal e Mensal).
  - Modal com gráfico comparativo em tempo real gerado pelo **Matplotlib**, convertido para **Base64** e renderizado nativamente no componente de imagem.

- **🧪 Cobertura de Testes Automatizados:**
  - Testes unitários para regras de negócio e validações com `pytest`.
  - Utilização de **Banco de Dados em Memória (`:memory:`)** para isolar os testes do banco de produção.
  - Uso de **Mocks (`unittest.mock`)** para simular chamadas de API externas sem depender de conexão com a internet durante os testes.

---

## 🛠️ Tecnologias e Ferramentas

- **Linguagem:** Python 3.11+
- **Interface Gráfica (GUI):** Flet
- **Banco de Dados:** SQLite3
- **Data Visualization:** Matplotlib & BytesIO / Base64
- **Consumo de API:** Requests (Webservice ViaCEP)
- **Testes Automatizados:** Pytest & Unittest.Mock
- **Boas Práticas:** Arquitetura em Camadas (Frontend / Backend / Services / Testes)

---

## 📐 Arquitetura do Repositório

```text
controle-de-entregas/
├── backend/
│   ├── __init__.py
│   ├── main.py            # Camada de persistência SQLite e regras de negócio
│   ├── grafico.py         # Módulo de renderização de gráficos Matplotlib em Base64
│   └── cep_service.py     # Serviço de consumo HTTP da API do ViaCEP
├── frontend/
│   ├── __init__.py
│   └── app.py             # Interface reativa com Flet (Views e Eventos)
├── tests/
│   ├── test_backend.py    # Testes unitários da camada de dados e lógica
│   └── test_cep.py        # Testes do serviço de CEP com Mocks
├── .gitignore             # Filtro de arquivos temporários e sensíveis
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação técnica do projeto
```

---

## 🚀 Como Executar o Projeto Localmente

```bash
# 1. Clonar o repositório
git clone [https://github.com/seu-usuario/controle-de-entregas.git](https://github.com/seu-usuario/controle-de-entregas.git)
cd controle-de-entregas

# 2. Criar e ativar o ambiente virtual (Windows)
python -m venv .venv
.venv\Scripts\activate

# OU Criar e ativar o ambiente virtual (Linux / macOS)
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar as dependências do projeto
pip install -r requirements.txt

# 4. Executar a aplicação Flet
python -m frontend.app

# 5. Executar a suíte de testes unitários (opcional)
pytest -v
```

---

## 📄 Licença

Este projeto está licenciado sob a Licença **MIT** - consulte o arquivo `LICENSE` para mais detalhes.

---

<p align="center">
Desenvolvido por <b>Washington Moreira</b> 🚀
</p>