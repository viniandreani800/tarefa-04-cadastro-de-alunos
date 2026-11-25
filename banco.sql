CREATE TABLE IF NOT EXISTS alunos (
    matricula TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    curso TEXT NOT NULL,
    email TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);