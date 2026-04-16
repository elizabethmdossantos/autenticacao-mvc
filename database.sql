CREATE DATABASE sistema_autenticacao;

USE sistema_autenticacao;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL, -- Adicionado
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    tentativas_login INT DEFAULT 0,
    ultimo_login DATETIME NULL
);