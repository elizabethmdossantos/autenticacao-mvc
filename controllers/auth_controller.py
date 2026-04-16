from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models.usuario_model import UsuarioModel
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash("Acesso restrito! Por favor, faça login.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def init_controller(app):
    auth_bp = Blueprint('auth', __name__)

    db_config = {
        'host': app.config['MYSQL_HOST'],
        'user': app.config['MYSQL_USER'],
        'password': app.config['MYSQL_PASSWORD'],
        'database': app.config['MYSQL_DB']
    }
    usuario_model = UsuarioModel(db_config)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():

        if request.method == 'POST':
            email = request.form.get('email')
            senha = request.form.get('senha')
            usuario = usuario_model.buscar_usuario(email)

            if not usuario:
                flash("E-mail não encontrado!", "danger")
                return redirect(url_for('auth.login'))

            if not usuario['ativo']:
                flash("⚠️ Conta bloqueada! Procure o administrador.", "warning")
                return redirect(url_for('auth.login'))

            if usuario_model.verificar_senha(email, senha):
                eh_primeiro_acesso = usuario.get('ultimo_login') is None
                
                usuario_model.atualizar_ultimo_login(email)
                
                session['usuario_id'] = usuario['id']
                session['usuario_nome'] = usuario['nome']
                session['usuario_email'] = email 

                if eh_primeiro_acesso:
                    flash("Primeiro acesso! Por segurança, troque sua senha.", "info")
                    return redirect(url_for('auth.primeiro_acesso'))
                
                flash(f"✅ Olá, {usuario['nome']}! Login realizado com sucesso.", "success")
                return redirect(url_for('auth.dashboard'))
            
            else:
                tentativas = usuario['tentativas_login'] + 1
                usuario_model.atualizar_tentativas(email, tentativas)
                
                if tentativas >= 3:
                    usuario_model.desativar_usuario(email)
                    flash("❌ Sua conta foi BLOQUEADA por excesso de tentativas!", "danger")
                else:
                    flash(f"❌ Senha incorreta! Tentativa {tentativas} de 3.", "info")
                return redirect(url_for('auth.login'))

        return render_template('login.html')

    @auth_bp.route('/cadastrar', methods=['GET', 'POST'])
    def cadastrar_usuario():
        if request.method == 'POST':
            email = request.form.get('email')
            senha = request.form.get('senha')
            confirmar = request.form.get('confirmar_senha')

            if senha != confirmar:
                flash("As senhas não coincidem!", "danger")
                return redirect(url_for('auth.cadastrar_usuario'))

            if usuario_model.buscar_usuario(email):
                flash("Este e-mail já está cadastrado!", "warning")
                return redirect(url_for('auth.cadastrar_usuario'))

            nome = email.split('@')[0].capitalize() 
            usuario_model.criar_usuario(nome, email, senha)
            flash("✅ Conta criada com sucesso! Faça login.", "success")
            return redirect(url_for('auth.login'))

        return render_template('cadastrar_usuario.html')

    @auth_bp.route('/primeiro-acesso', methods=['GET', 'POST'])
    @login_required
    def primeiro_acesso():
        if request.method == 'POST':
            nova_senha = request.form.get('nova_senha')
            confirmar = request.form.get('confirmar_senha')
            
            if nova_senha != confirmar:
                flash("As novas senhas não coincidem!", "danger")
                return render_template('primeiro_acesso.html')
            
            usuario_model.trocar_senha(session['usuario_email'], nova_senha)
            flash("✅ Senha atualizada! Bem-vindo ao sistema.", "success")
            return redirect(url_for('auth.dashboard'))
            
        return render_template('primeiro_acesso.html')

    @auth_bp.route('/dashboard')
    @login_required 
    def dashboard():
        return render_template('dashboard.html', usuario_nome=session['usuario_nome'])

    @auth_bp.route('/logout')
    def logout():
        session.clear()
        flash("👋 Logout realizado com sucesso!", "info")
        return redirect(url_for('auth.login'))

    return auth_bp