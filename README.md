# Sistema de Cadastro de Alunos com GUI e SQLite (INE5201)

**Disciplina:** INE5201 - Introdução à Ciência da Computação com Python (UFSC)  
**Aluno:** Vinicius Andreani  

## Descrição do Projeto
Aplicação desktop com interface gráfica em `tkinter` (`ttk.Treeview`) e banco de dados `SQLite` para gerenciar o cadastro de alunos (CRUD completo), com validação de campos obrigatórios, unicidade de matrícula, validação de e-mail, confirmação na exclusão e exportação para CSV.

## Esquema do Banco de Dados
A tabela `alunos` utiliza `matricula` como chave primária para impedir matrículas repetidas:

```sql
CREATE TABLE IF NOT EXISTS alunos (
    matricula TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    curso TEXT NOT NULL,
    email TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Funcionalidades
* **Cadastrar:** Insere novo aluno após validar campos obrigatórios, matrícula única e formato de e-mail.
* **Buscar e Listar:** Exibe os alunos na tabela e permite filtrar por nome ou matrícula.
* **Editar:** Atualiza nome, curso e e-mail de um aluno selecionado.
* **Excluir:** Remove o registro após confirmação do usuário.
* **Limpar e Exportar CSV:** Limpa os campos do formulário e exporta a lista para `.csv`.

## Como Executar
1. Tenha o Python 3 instalado.
2. Abra o terminal na pasta do projeto e execute:
   ```bash
   python cadastro_alunos.py
   ```

## Capturas de Tela
![Tela Principal](tela-1.png)
![Cadastro e Busca](tela-2.png)

## Relato de Uso do GitHub Copilot
O GitHub Copilot foi utilizado no VS Code para auxiliar na estruturação das consultas SQL parametrizadas com `sqlite3`, na montagem da interface em `tkinter` com `ttk.Treeview` e na expressão regular de validação de e-mail. Todo o código foi revisado, testado e ajustado manualmente conforme os requisitos da disciplina.