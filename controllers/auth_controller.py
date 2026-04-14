from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models.usuario_model import UsuarioModel

def init_controller(mysql):
    auth_bp = Blueprint('auth', __name__)
    usuario_model = UsuarioModel() 

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
                flash("Conta bloqueada! Procure o administrador.", "warning")
                return redirect(url_for('auth.login'))

            if usuario_model.verificar_senha(email, senha):
                usuario_model.atualizar_ultimo_login(email)
                
                session['usuario_id'] = usuario['id']
                session['usuario_nome'] = usuario['nome']
                
                flash(f"Olá, {usuario['nome']}! Login realizado.", "success")
                return redirect(url_for('dashboard'))
            
            else:
                tentativas = usuario['tentativas_login'] + 1
                usuario_model.atualizar_tentativas(email, tentativas)

                if tentativas >= 5:
                    usuario_model.desativar_usuario(email)
                    flash("Senha incorreta. Sua conta foi BLOQUEADA por segurança!", "danger")
                else:
                    flash(f"Senha incorreta! Tentativa {tentativas} de 5.", "info")
                
                return redirect(url_for('auth.login'))

        return render_template('login.html')

    @auth_bp.route('/logout')
    def logout():
        session.clear()
        flash("Sessão encerrada com sucesso.", "info")
        return redirect(url_for('auth.login'))
    
    return auth_bp