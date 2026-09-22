# 🚚 Sistema de Controle de Entregas & Painel Analítico

Aplicação desktop/web para gestão de entregas operacionais e monitoramento de faturamento, desenvolvida com **Python**, **Flet** e **SQLite**. O sistema conta com integração em tempo real com a API do **ViaCEP** para validação e busca automática de endereços, além de um painel analítico com gráficos gerados dinamicamente via **Matplotlib**.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![Flet](https://img.shields.io/badge/Flet-0.80+-purple?style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey?style=flat-square&logo=sqlite)
![Pytest](https://img.shields.io/badge/Pytest-Passed-brightgreen?style=flat-square&logo=pytest)

---

## 📸 Funcionalidades

- **Gestão de Entregas (CRUD):** Cadastro, listagem, atualização e exclusão de comandas com persistência em banco SQLite.
- **Integração com API REST (ViaCEP):** Consulta e autopreenchimento de endereço ao inserir o CEP da entrega.
- **Painel Analítico & Gráficos:** Cálculo de médias/totais (diário, semanal e mensal) e renderização de gráficos do Matplotlib codificados em Base64 para exibição reativa.
- **Testes Automatizados:** Suíte de testes unitários com `pytest` utilizando banco de dados isolado em memória (`:memory:`) e `unittest.mock` para chamadas HTTP.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Interface Gráfica:** [Flet](https://flet.dev/) (Flutter for Python)
- **Banco de Dados:** SQLite
- **Visualização de Dados:** Matplotlib & BytesIO
- **Integração HTTP:** Requests (ViaCEP API)
- **Testes Automatizados:** Pytest & Unittest.Mock

---

## 📐 Arquitetura do Projeto

```text
Controle-de-Entregas/
├── backend/
│   ├── main.py            # Regras de negócio e persistência SQLite
│   ├── grafico.py         # Geração de gráficos Matplotlib em Base64
│   └── cep_service.py     # Integração com a API do ViaCEP
├── frontend/
│   └── app.py             # Interface reativa com Flet
├── tests/
│   ├── test_backend.py    # Testes unitários do banco e regras de negócio
│   └── test_cep.py        # Testes de integração e mocks do ViaCEP
├── .gitignore             # Arquivos ignorados pelo controle de versão
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação do repositório