import os

class Config:
    # Segurança - troque em produção!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-flask-2026'
    
    # Configurações MySQL
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'admin'  
    MYSQL_DB = 'sistema_mvc'
    MYSQL_CURSORCLASS = 'DictCursor'
    
    # Regras de Negócio
    MAX_TENTATIVAS = 3