import mysql.connector 
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class UsuarioModel:

    def __init__(self, config=None):
        self.connection_config = config or {
            'host': 'localhost',
            'user': 'root',
            'password': 'admin',
            'database': 'sistema_autenticacao'
        }

    def _get_connection(self):
        try:
            connection = mysql.connector.connect(**self.connection_config)
            return connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None

    def verificar_senha(self, email, senha_digitada):
        # Lógica de Login: Busca o usuário no banco e usa a Werkzeug para 
        # comparar a senha digitada com o hash criptografado.
        usuario = self.buscar_usuario(email)
        if usuario:
            if check_password_hash(usuario['senha'], senha_digitada):
                return True
        return False

    def criar_usuario(self, nome, email, senha):
        connection = self._get_connection()
        if not connection: return
        
        hashed_senha = generate_password_hash(senha)
        try:
            cursor = connection.cursor()
            query = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
            cursor.execute(query, (nome, email, hashed_senha))
            connection.commit()
        except Error as e:
            print(f"Erro ao criar usuário: {e}")
        finally:
            cursor.close()
            connection.close()
            
    def listar_todos(self):
        connection = self._get_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, nome, email, ativo, ultimo_login FROM usuarios")
            return cursor.fetchall()
        finally:
            connection.close()

    def buscar_usuario(self, email):
        # SELECT: Busca todos os dados de um usuário pelo e-mail.
        # O parâmetro 'dictionary=True' faz o MySQL retornar os dados como um dicionário do Python (ex: usuario['nome']), o que é muito mais fácil de usar.
        connection = self._get_connection()
        if not connection: return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,)) # O '%s' evita SQL Injection (ataque hacker)
            return cursor.fetchone() # Retorna apenas um resultado
        except Error as e:
            print(f"Erro ao buscar usuário: {e}")
        finally:
            cursor.close()
            connection.close()

    def atualizar_tentativas(self, email, tentativas):
        # UPDATE: Atualiza quantas vezes o usuário errou a senha.
        # Útil para bloquear a conta após X tentativas.
        connection = self._get_connection()
        if not connection: return
        
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE usuarios SET tentativas_login = %s WHERE email = %s", (tentativas, email))
            connection.commit() # Salva as alterações no banco
        except Error as e:
            print(f"Erro ao atualizar tentativas: {e}")
        finally:
            cursor.close()
            connection.close()

    def desativar_usuario(self, email):
        # Soft Delete: Em vez de apagar o usuário, apenas mudamos o status para 'Inativo'.
        # Isso mantém o histórico de dados no seu sistema.
        connection = self._get_connection()
        if not connection: return
        
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE usuarios SET ativo = FALSE WHERE email = %s", (email,))
            connection.commit()
        except Error as e:
            print(f"Erro ao desativar usuário: {e}")
        finally:
            cursor.close()
            connection.close()

    def atualizar_ultimo_login(self, email):
        # UPDATE: Grava o momento exato do login e zera as tentativas de erro.
        connection = self._get_connection()
        if not connection: return
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE usuarios SET ultimo_login = %s, tentativas_login = 0 WHERE email = %s", 
                (datetime.now(), email)
            )
            connection.commit()
        except Error as e:
            print(f"Erro ao atualizar último login: {e}")
        finally:
            cursor.close()
            connection.close()

    def trocar_senha(self, email, nova_senha):
        # SEGURANÇA: Transforma a senha em um Hash (embaralhado) antes de salvar.
        # Mesmo que alguém acesse o banco, não saberá a senha real.
        hashed = generate_password_hash(nova_senha) #criptografia da senha
        connection = self._get_connection()
        if not connection: return
        
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE usuarios SET senha = %s WHERE email = %s", (hashed, email))
            connection.commit()
            self.atualizar_ultimo_login(email) # reutiliza  a função de login para atualizar o timestamp
        except Error as e:
            print(f"Erro ao trocar senha: {e}")
        finally:
            cursor.close()
            connection.close()