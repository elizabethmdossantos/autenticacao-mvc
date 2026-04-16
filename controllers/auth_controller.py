from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models import usuario_model
from models.usuario_model import UsuarioModel

def init_controller(app):
    auth_bp = Blueprint('auth', __name__)

    db_config = {
        'host': app.config['MYSQL_HOST'],
        'user': app.config['MYSQL_USER'],
        'password': app.config['MYSQL_PASSWORD'],
        'database': app.config['MYSQL_DB']
    }
    usuario_model = UsuarioModel(db_config)

    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if 'usuario_id' in session:
            return redirect(url_for('auth.dashboard'))

        if request.method == 'POST':
            email = request.form.get('email')
            senha = request.form.get('senha')

            usuario = usuario_model.buscar_usuario(email)

        if not usuario:
            flash("E-mail não encontrado!", "danger")
            return redirect(url_for('auth.login'))

        if not usuario['ativo']:
            flash("Conta bloqueada! Procure o administrador.", "warning")
            return redirect(url_for('auth.login'))

        if usuario_model.verificar_senha(email, senha):
            usuario_model.atualizar_ultimo_login(email)
            
            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']

            if usuario.get('ultimo_login') is None:
                session['usuario_email'] = email 
                flash("Primeiro acesso! Troque sua senha.", "info")
                return redirect(url_for('auth.primeiro_acesso'))
            
            flash(f"Olá, {usuario['nome']}! Login realizado.", "success")
            return redirect(url_for('auth.dashboard'))
        
        else:
            tentativas = usuario['tentativas_login'] + 1
            usuario_model.atualizar_tentativas(email, tentativas)

            if tentativas >= 3:
                usuario_model.desativar_usuario(email)
                flash("Senha incorreta. Sua conta foi BLOQUEADA por segurança!", "danger")
            else:
                flash(f"Senha incorreta! Tentativa {tentativas} de 3.", "info")
            
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

            # Verifica se o e-mail já existe
            if usuario_model.buscar_usuario(email):
                flash("Este e-mail já está cadastrado!", "warning")
                return redirect(url_for('auth.cadastrar_usuario'))

            # No cadastro, o campo 'nome' pode ser extraído do e-mail ou pedido no form
            nome = email.split('@')[0].capitalize() 
            
            usuario_model.criar_usuario(nome, email, senha)
            flash("Conta criada com sucesso! Faça login.", "success")
            return redirect(url_for('auth.login'))

        return render_template('cadastrar_usuario.html')

    @auth_bp.route('/usuarios')
    def lista_usuarios():
        if 'usuario_id' not in session:
            return redirect(url_for('auth.login'))
        
        # Você precisaria criar este método no Model para listar todos
        usuarios = usuario_model.listar_todos()
        return render_template('lista_usuarios.html', usuarios=usuarios)
    
    @auth_bp.route('/primeiro-acesso', methods=['GET', 'POST'])
    @login_required
    def primeiro_acesso():
        usuario_email = session['usuario_email']  # Armazene email na session no login
        
        if request.method == 'POST':
            senha_atual = request.form.get('senha_atual')
            nova_senha = request.form.get('nova_senha')
            confirmar = request.form.get('confirmar_senha')
            
            if nova_senha != confirmar:
                flash("Senhas não coincidem!", "danger")
                return render_template('primeiro_acesso.html')
            
            if usuario_model.verificar_senha(usuario_email, senha_atual):
                usuario_model.trocar_senha(usuario_email, nova_senha)
                flash("Senha alterada! Agora acesse o dashboard.", "success")
                return redirect(url_for('auth.dashboard'))
            else:
                flash("Senha atual incorreta!", "danger")
        
        return render_template('primeiro_acesso.html')
    
    @auth_bp.route('/dashboard')
    def dashboard():
        if 'usuario_id' not in session:
            flash("Faça login para acessar esta página.", "warning")
            return redirect(url_for('auth.login'))
        return render_template('dashboard.html', usuario_nome=session['usuario_nome'])
    
    @auth_bp.route('/logout')
    def logout():
        session.clear()
        flash("Sessão encerrada com sucesso.", "info")
        return redirect(url_for('auth.login'))
    
    return auth_bp