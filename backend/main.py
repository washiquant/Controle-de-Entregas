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
    cursor.execute("SELECT SUM(valor) FROM comandas WHERE DATE(data) = DATE('now')")
    total = cursor.fetchone()[0]
    banco.close()
    return total if total else 0.0

def total_do_mes():
    banco = conectar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT SUM(valor) FROM comandas WHERE strftime('%Y-%m', data) = strftime('%Y-%m', 'now')")
    total_mes = cursor.fetchone()[0]
    banco.close()
    return total_mes if total_mes else 0.0

def total_da_semana():
    banco = conectar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT SUM(valor) FROM comandas WHERE strftime('%Y-%W', data) = strftime('%Y-%W', 'now')")
    total_semana = cursor.fetchone()[0]
    banco.close()
    return total_semana if total_semana else 0.0


def media_diaria():
    banco = conectar_banco()
    cursor = banco.cursor()
    cursor.execute("""
    SELECT AVG(total_dia) FROM(
        SELECT SUM(valor) AS total_dia
        FROM comandas
        GROUP BY DATE(data)
    )
""")
    media = cursor.fetchone()[0]
    banco.close()
    return media if media else 0.0

def media_semanal():
    banco = conectar_banco()
    cursor = banco.cursor()
    cursor.execute("""
    SELECT AVG(total_semana) 
    FROM(
        SELECT SUM(valor) AS total_semana
        FROM comandas
        GROUP BY strftime('%Y-%W', data)
    )
    """)
    media_da_semana = cursor.fetchone()[0]
    banco.close()
    return media_da_semana if media_da_semana else 0.0

def media_mensal():
    banco = conectar_banco()
    cursor = banco.cursor()
    cursor.execute("""
    SELECT AVG(total_mes) 
    FROM(
        SELECT SUM(valor) AS total_mes
        FROM comandas
        GROUP BY strftime('%Y-%m', data)
    )
    """)
    media_do_mes = cursor.fetchone()[0]
    banco.close()
    return media_do_mes if media_do_mes else 0.0