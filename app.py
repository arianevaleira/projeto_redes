from flask import Flask, render_template, redirect, url_for, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import Users, conexao
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'sua-chave-secreta'

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = Users.get_by_email(email)
        if user and check_password_hash(user.senha, senha):
            login_user(user)
            return redirect(url_for('home'))
        else:
            return "Email ou senha incorretos"

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        user = Users.get_by_email(email)
        if user:
            return "Email já registrado. Faça login."

        senha_hash = generate_password_hash(senha)

        conn = conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tb_usuarios (usu_nome, usu_email,usu_senha) VALUES (?, ?, ?)', (nome, email ,senha_hash))
        conn.commit()
        conn.close()

        new_user = Users.get_by_email(email)
        login_user(new_user)

        return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html', email=current_user.email)

@app.route('/usuarios')
def usuarios():
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_usuarios')
    usuarios_data = cursor.fetchall()  # Obtém todos os dados de usuários
    conn.close()

    # Convertendo os dados para uma lista de instâncias da classe Usuario
    usuarios = [Users(user['usu_id'], user['usu_nome'] ,user['usu_email'], user['usu_senha']) for user in usuarios_data]

    return render_template('usuarios.html', usuarios=usuarios)



@app.route('/sobre')
def sobre():
    return render_template('sobre.html')