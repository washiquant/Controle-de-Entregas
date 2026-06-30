# 🚚 Controle de Entregas

Aplicativo desenvolvido em Python utilizando Flet para gerenciamento de entregas, controle de comandas e acompanhamento do faturamento diário.

O projeto foi criado para uso real em operações de delivery, permitindo registrar entregas, atualizar valores, excluir registros e acompanhar o total arrecadado ao longo do dia.

---

## 📱 Funcionalidades

* Cadastro de novas comandas
* Registro do valor de cada entrega
* Registro opcional de CEP
* Atualização de valores cadastrados
* Exclusão de comandas com confirmação
* Cálculo automático do total do dia
* Contagem de entregas realizadas
* Armazenamento local utilizando SQLite
* Interface responsiva para Android
* Geração de APK utilizando Flet

---

## 🛠️ Tecnologias Utilizadas

* Python 3
* Flet
* SQLite
* Flutter (geração do APK Android)

---

## 📂 Estrutura do Projeto

```text
├── app.py
├── main.py
├── banco.db
├── requirements.txt
└── README.md
```

---

## 🚀 Como Executar

### Clonar o repositório

```bash
git clone https://github.com/seu-usuario/controle-entregas.git
```

### Entrar na pasta

```bash
cd controle-entregas
```

### Criar ambiente virtual

```bash
python -m venv .venv
```

### Ativar ambiente virtual

Windows:

```bash
.venv\Scripts\activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar aplicação

```bash
python app.py
```

---

## 📦 Gerar APK Android

```bash
flet build apk --module-name app
```

---

## 📸 Funcionalidades da Interface

* Visualização das entregas cadastradas
* Cards com identificação das comandas
* Total diário atualizado automaticamente
* Confirmação antes da exclusão de registros
* Layout otimizado para dispositivos móveis

---

## 🎯 Próximas Melhorias

* Dashboard financeiro
* Estatísticas de faturamento
* Ticket médio por entrega
* Histórico por período
* Gráficos de desempenho
* Backup automático do banco de dados

---

## 👨‍💻 Autor

Desenvolvido por Washington Willian R. Moreira como projeto de estudo e aplicação prática de Python, Flet e desenvolvimento mobile.
