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

def atualizar_tabela(tree, alunos):
    for item in tree.get_children():
        tree.delete(item)
    for aluno in alunos:
        tree.insert("", "end", values=aluno)


def criar_layout(root):
    root.title("Sistema de Cadastro de Alunos - INE5201")
    root.geometry("820x540")
    root.resizable(False, False)
    root.configure(bg="#f4f6f9")

    tk.Label(
        root,
        text="Cadastro de Alunos (SQLite)",
        font=("Arial", 16, "bold"),
        bg="#f4f6f9",
        fg="#1f2d3d",
    ).pack(pady=10)

    frame_form = tk.LabelFrame(
        root, text="Dados do Aluno", font=("Arial", 10, "bold"), bg="#f4f6f9", padx=15, pady=10
    )
    frame_form.pack(fill="x", padx=20, pady=5)

    tk.Label(frame_form, text="Matrícula *:", bg="#f4f6f9").grid(row=0, column=0, sticky="w", pady=4)
    entry_matricula = tk.Entry(frame_form, width=22)
    entry_matricula.grid(row=0, column=1, padx=8, pady=4, sticky="w")

    tk.Label(frame_form, text="Nome Completo *:", bg="#f4f6f9").grid(row=0, column=2, sticky="w", pady=4)
    entry_nome = tk.Entry(frame_form, width=38)
    entry_nome.grid(row=0, column=3, padx=8, pady=4, sticky="w")

    tk.Label(frame_form, text="Curso *:", bg="#f4f6f9").grid(row=1, column=0, sticky="w", pady=4)
    entry_curso = tk.Entry(frame_form, width=22)
    entry_curso.grid(row=1, column=1, padx=8, pady=4, sticky="w")

    tk.Label(frame_form, text="E-mail:", bg="#f4f6f9").grid(row=1, column=2, sticky="w", pady=4)
    entry_email = tk.Entry(frame_form, width=38)
    entry_email.grid(row=1, column=3, padx=8, pady=4, sticky="w")

    frame_botoes = tk.Frame(root, bg="#f4f6f9")
    frame_botoes.pack(pady=8)

    btn_cadastrar = tk.Button(frame_botoes, text="Cadastrar", width=13, bg="#27ae60", fg="white", font=("Arial", 9, "bold"))
    btn_cadastrar.grid(row=0, column=0, padx=5)

    btn_editar = tk.Button(frame_botoes, text="Editar", width=13, bg="#2980b9", fg="white", font=("Arial", 9, "bold"))
    btn_editar.grid(row=0, column=1, padx=5)

    btn_excluir = tk.Button(frame_botoes, text="Excluir", width=13, bg="#c0392b", fg="white", font=("Arial", 9, "bold"))
    btn_excluir.grid(row=0, column=2, padx=5)

    btn_limpar = tk.Button(frame_botoes, text="Limpar", width=13, bg="#7f8c8d", fg="white", font=("Arial", 9, "bold"))
    btn_limpar.grid(row=0, column=3, padx=5)

    btn_exportar = tk.Button(frame_botoes, text="Exportar CSV", width=13, bg="#8e44ad", fg="white", font=("Arial", 9, "bold"))
    btn_exportar.grid(row=0, column=4, padx=5)

    frame_busca = tk.Frame(root, bg="#f4f6f9")
    frame_busca.pack(fill="x", padx=20, pady=6)

    tk.Label(frame_busca, text="Buscar (Nome ou Matrícula):", bg="#f4f6f9", font=("Arial", 9, "bold")).pack(side="left")
    entry_busca = tk.Entry(frame_busca, width=35)
    entry_busca.pack(side="left", padx=8)

    btn_buscar = tk.Button(frame_busca, text="Buscar", width=10, bg="#34495e", fg="white")
    btn_buscar.pack(side="left", padx=3)

    btn_todos = tk.Button(frame_busca, text="Mostrar Todos", width=13)
    btn_todos.pack(side="left", padx=3)

    frame_tabela = tk.Frame(root, bg="#f4f6f9")
    frame_tabela.pack(fill="both", expand=True, padx=20, pady=8)

    colunas = ("matricula", "nome", "curso", "email", "data_cadastro")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=11)
    tree.heading("matricula", text="Matrícula")
    tree.heading("nome", text="Nome")
    tree.heading("curso", text="Curso")
    tree.heading("email", text="E-mail")
    tree.heading("data_cadastro", text="Data Cadastro")

    tree.column("matricula", width=100, anchor="center")
    tree.column("nome", width=210)
    tree.column("curso", width=160)
    tree.column("email", width=180)
    tree.column("data_cadastro", width=125, anchor="center")

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return {
        "matricula": entry_matricula,
        "nome": entry_nome,
        "curso": entry_curso,
        "email": entry_email,
        "busca": entry_busca,
        "btn_cadastrar": btn_cadastrar,
        "btn_editar": btn_editar,
        "btn_excluir": btn_excluir,
        "btn_limpar": btn_limpar,
        "btn_exportar": btn_exportar,
        "btn_buscar": btn_buscar,
        "btn_todos": btn_todos,
        "tree": tree,
    }


def main():
    criar_tabela()
    root = tk.Tk()
    ui = criar_layout(root)

    def limpar_campos():
        ui["matricula"].config(state="normal")
        ui["matricula"].delete(0, tk.END)
        ui["nome"].delete(0, tk.END)
        ui["curso"].delete(0, tk.END)
        ui["email"].delete(0, tk.END)
        ui["tree"].selection_remove(ui["tree"].selection())

    def acao_cadastrar():
        dados = {
            "matricula": ui["matricula"].get().strip(),
            "nome": ui["nome"].get().strip(),
            "curso": ui["curso"].get().strip(),
            "email": ui["email"].get().strip(),
        }
        valido, msg = validar_campos(dados["matricula"], dados["nome"], dados["curso"], dados["email"])
        if not valido:
            messagebox.showwarning("Validação", msg)
            return
        sucesso, retorno = inserir_aluno(dados)
        if sucesso:
            messagebox.showinfo("Sucesso", retorno)
            limpar_campos()
            atualizar_tabela(ui["tree"], listar_todos())
        else:
            messagebox.showerror("Erro", retorno)

    def ao_selecionar_linha(event):
        selecionado = ui["tree"].selection()
        if not selecionado:
            return
        valores = ui["tree"].item(selecionado[0], "values")
        ui["matricula"].config(state="normal")
        ui["matricula"].delete(0, tk.END)
        ui["matricula"].insert(0, valores[0])
        ui["matricula"].config(state="disabled")

        ui["nome"].delete(0, tk.END)
        ui["nome"].insert(0, valores[1])
        ui["curso"].delete(0, tk.END)
        ui["curso"].insert(0, valores[2])
        ui["email"].delete(0, tk.END)
        ui["email"].insert(0, valores[3])

    def acao_editar():
        matricula = ui["matricula"].get().strip()
        if not matricula:
            messagebox.showwarning("Atenção", "Selecione um aluno na tabela para editar.")
            return
        dados = {
            "matricula": matricula,
            "nome": ui["nome"].get().strip(),
            "curso": ui["curso"].get().strip(),
            "email": ui["email"].get().strip(),
        }
        valido, msg = validar_campos(dados["matricula"], dados["nome"], dados["curso"], dados["email"])
        if not valido:
            messagebox.showwarning("Validação", msg)
            return
        sucesso, retorno = atualizar_aluno(dados)
        if sucesso:
            messagebox.showinfo("Sucesso", retorno)
            limpar_campos()
            atualizar_tabela(ui["tree"], listar_todos())
        else:
            messagebox.showerror("Erro", retorno)

    def acao_excluir():
        matricula = ui["matricula"].get().strip()
        if not matricula:
            messagebox.showwarning("Atenção", "Selecione um aluno na tabela para excluir.")
            return
        if messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente excluir o aluno de matrícula {matricula}?"):
            if excluir_aluno(matricula):
                messagebox.showinfo("Excluído", "Aluno removido com sucesso.")
                limpar_campos()
                atualizar_tabela(ui["tree"], listar_todos())

    def acao_buscar():
        termo = ui["busca"].get().strip()
        if not termo:
            atualizar_tabela(ui["tree"], listar_todos())
            return
        resultados = buscar_aluno(termo)
        atualizar_tabela(ui["tree"], resultados)

    def acao_exportar():
        alunos = listar_todos()
        if not alunos:
            messagebox.showinfo("Exportar", "Não há alunos cadastrados para exportar.")
            return
        caminho = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")],
            initialfile="alunos_cadastrados.csv",
        )
        if caminho:
            with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["Matrícula", "Nome", "Curso", "E-mail", "Data Cadastro"])
                writer.writerows(alunos)
            messagebox.showinfo("Exportado", "Lista exportada com sucesso!")

    ui["btn_cadastrar"].config(command=acao_cadastrar)
    ui["btn_editar"].config(command=acao_editar)
    ui["btn_excluir"].config(command=acao_excluir)
    ui["btn_limpar"].config(command=limpar_campos)
    ui["btn_buscar"].config(command=acao_buscar)
    ui["btn_todos"].config(command=lambda: (ui["busca"].delete(0, tk.END), atualizar_tabela(ui["tree"], listar_todos())))
    ui["btn_exportar"].config(command=acao_exportar)
    ui["tree"].bind("<<TreeviewSelect>>", ao_selecionar_linha)

    atualizar_tabela(ui["tree"], listar_todos())
    root.mainloop()


if __name__ == "__main__":
    main()