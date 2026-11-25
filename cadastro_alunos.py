import csv
import os
import re
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

DB_NAME = "alunos.db"
SQL_SCRIPT = "banco.sql"


def criar_conexao():
    return sqlite3.connect(DB_NAME)


def criar_tabela():
    conn = criar_conexao()
    cursor = conn.cursor()
    if os.path.exists(SQL_SCRIPT):
        with open(SQL_SCRIPT, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
    else:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS alunos (
                matricula TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                curso TEXT NOT NULL,
                email TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
    conn.commit()
    conn.close()


def inserir_aluno(dados):
    conn = criar_conexao()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO alunos (matricula, nome, curso, email) VALUES (?, ?, ?, ?)",
            (dados["matricula"], dados["nome"], dados["curso"], dados["email"]),
        )
        conn.commit()
        return True, "Aluno cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Erro: Já existe um aluno cadastrado com esta matrícula!"
    finally:
        conn.close()


def buscar_aluno(termo):
    conn = criar_conexao()
    cursor = conn.cursor()
    like_termo = f"%{termo}%"
    cursor.execute(
        """
        SELECT matricula, nome, curso, email, data_cadastro
        FROM alunos
        WHERE matricula LIKE ? OR nome LIKE ?
        ORDER BY nome
        """,
        (like_termo, like_termo),
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def atualizar_aluno(dados):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE alunos
        SET nome = ?, curso = ?, email = ?
        WHERE matricula = ?
        """,
        (dados["nome"], dados["curso"], dados["email"], dados["matricula"]),
    )
    alterados = cursor.rowcount
    conn.commit()
    conn.close()
    if alterados == 0:
        return False, "Nenhum aluno encontrado com esta matrícula para atualizar."
    return True, "Dados do aluno atualizados com sucesso!"


def excluir_aluno(matricula):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alunos WHERE matricula = ?", (matricula,))
    removidos = cursor.rowcount
    conn.commit()
    conn.close()
    return removidos > 0


def listar_todos():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT matricula, nome, curso, email, data_cadastro FROM alunos ORDER BY nome"
    )
    alunos = cursor.fetchall()
    conn.close()
    return alunos


def validar_campos(matricula, nome, curso, email):
    if not matricula or not nome or not curso:
        return False, "Os campos Matrícula, Nome e Curso são obrigatórios."
    if email:
        padrao_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(padrao_email, email):
            return False, "Formato de e-mail inválido (ex: aluno@ufsc.br)."
    return True, ""