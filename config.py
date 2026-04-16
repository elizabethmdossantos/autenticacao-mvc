import os

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-flask-2026'
    
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'admin'  
    MYSQL_DB = 'sistema_autenticacao'
    
    MAX_TENTATIVAS = 3