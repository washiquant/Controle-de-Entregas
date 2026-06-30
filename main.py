import sqlite3
import os
from datetime import datetime




import os
import sqlite3

def get_db_path():
    return "controle_de_entregas.db"

def conectar_banco():
    # Tenta conectar. Se falhar, é erro de permissão ou caminho.
    try:
        path = get_db_path()
        banco = sqlite3.connect(path)
        return banco
    except Exception as e:
        print(f"Erro crítico ao abrir banco: {e}")
        raise
# Classe conforme seu código original
class Comanda:
    def __init__(self, numero, valor, cep):
        self.numero = numero
        self.valor = valor
        self.cep = cep
        self.data = datetime.now().strftime("%d/%m/%Y %H:%M")

def conectar_banco():
    banco = sqlite3.connect(get_db_path())
    cursor = banco.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comandas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT,
            valor REAL,
            cep TEXT,
            data TEXT
        )
    ''')
    banco.commit()
    return banco

def adicionar_comanda(c):
    banco = conectar_banco()
    cursor = banco.cursor()
    cursor.execute("INSERT INTO comandas (numero, valor, cep, data) VALUES (?, ?, ?, ?)",
                   (c.numero, c.valor, c.cep, c.data))
    banco.commit()
    banco.close()

def deletar_comanda(id_exclusao):
    banco = conectar_banco()
    cursor = banco.cursor()
    cursor.execute("DELETE FROM comandas WHERE id = ?", (id_exclusao,))
    banco.commit()
    banco.close()

def atualizar_banco_de_dados(novo_valor, id_atualizacao):
    banco = conectar_banco()
    cursor = banco.cursor()
    cursor.execute("UPDATE comandas SET valor = ? WHERE id = ?", (novo_valor, id_atualizacao))
    banco.commit()
    banco.close()

def buscar_comandas():
    banco = conectar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM comandas")
    dados = cursor.fetchall()
    banco.close()
    return dados

def total_do_dia():
    banco = conectar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT SUM(valor) FROM comandas")
    total = cursor.fetchone()[0]
    banco.close()
    return total if total else 0.0
