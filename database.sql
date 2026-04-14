-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS sistema_auth CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sistema_auth;

-- Tabela de usuários conforme especificação
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    tentativas_login INT DEFAULT 0,
    ultimo_login DATETIME NULL
);