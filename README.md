🔐 Sistema de Autenticação Flask
Um sistema de login robusto desenvolvido com Python e Flask, utilizando MySQL para persistência de dados. O projeto foca em boas práticas de segurança, como hashing de senhas e controle de tentativas de acesso.

🚀 Funcionalidades
Cadastro de Usuário: Registro com validação de e-mail único e confirmação de senha.

Login Seguro: Verificação de credenciais com werkzeug.security.

Controle de Acessos: * Bloqueio automático de conta após 3 tentativas incorretas.

Verificação de status (usuário ativo/bloqueio pelo admin).

Fluxo de Primeiro Acesso: Detecta se é o primeiro login do usuário e solicita a troca de senha obrigatória.

Sessões: Proteção de rotas através de um decorator @login_required.

Dashboard: Área restrita para usuários autenticados.

🛠️ Tecnologias Utilizadas
Python 3

Flask (Framework Web)

MySQL (Banco de Dados)

MySQL Connector (Driver de conexão)

Werkzeug (Segurança/Hash de senhas)

📋 Pré-requisitos
Antes de começar, você precisará ter instalado:

Python 3.x

MySQL Server

Pip (Gerenciador de pacotes do Python)

🔧 Instalação e Configuração
Clone o repositório:

Bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
Instale as dependências:

Bash
pip install flask mysql-connector-python werkzeug
Configure o Banco de Dados:

No seu terminal MySQL, execute o script contido no arquivo SQL ou use os comandos abaixo:

SQL
CREATE DATABASE sistema_autenticacao;
USE sistema_autenticacao;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    tentativas_login INT DEFAULT 0,
    ultimo_login DATETIME NULL
);
Ajuste as credenciais:

Abra o arquivo config.py e insira o usuário e senha do seu MySQL local.

🏃 Como Rodar
Inicie o servidor:

Bash
python main.py
Abra o navegador e acesse: http://localhost:8000

📂 Estrutura do Projeto
Plaintext
├── controllers/
│   └── auth_controller.py   # Lógica das rotas e controle de sessão
├── models/
│   └── usuario_model.py     # Interação direta com o MySQL
├── views/
│   └── templates/           # Arquivos HTML (login, cadastro, dashboard)
├── config.py                # Configurações de ambiente e DB
└── main.py                  # Ponto de entrada da aplicação
