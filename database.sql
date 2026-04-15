CREATE DATABASE sistema_autenticacao;

USE sistema_autenticacao;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL, -- Adicionado
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    tentativas_login INT DEFAULT 0,
    ultimo_login DATETIME NULL
);

INSERT INTO usuarios (nome, email, senha) 
VALUES ('Administrador', 'admin@email.com', 'COLE_O_HASH_GERADO_AQUI');