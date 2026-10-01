from flask import Flask, render_template, request, redirect, session, url_for
from utils.storage import load_users, save_users
import hashlib

app = Flask(__name__)
app.secret_key = 'segredo_top_seguro'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Conteúdo dos cursos
cursos_conteudo = {
    '1': {
        'titulo': 'Introdução à Lógica',
        'descricao': 'Entenda os princípios básicos do raciocínio lógico.',
        'imagem': 'capalogica.png',
        'video': 'https://www.youtube.com/embed/PltqUuwR9ec',
        'texto': 'Lógica é a base da programação e do pensamento matemático. Neste curso você aprenderá sobre proposições, conectivos lógicos, tabelas verdade e muito mais.'
    },
    '2': {
        'titulo': 'Programação com Python',
        'descricao': 'Aprenda a programar com a linguagem Python.',
        'imagem': 'capapython.png',
        'video': 'https://www.youtube.com/embed/kqtD5dpn9C8',
        'texto': 'Neste curso você aprenderá sobre variáveis, estruturas de controle, funções, listas, dicionários e como escrever programas em Python.'
    },
    '3': {
        'titulo': 'Segurança Digital',
        'descricao': 'Proteja-se no mundo digital com boas práticas.',
        'imagem': 'capaseguranca.png',
        'video': 'https://www.youtube.com/embed/Gfh2bxe3hGU',
        'texto': 'Aprenda sobre criação de senhas seguras, autenticação em dois fatores, engenharia social, e como se proteger de ameaças online.'
    }
}

# Login
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username]["password"] == hash_password(password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Credenciais inválidas.')
    return render_template('login.html')

# Registro
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return render_template('register.html', error='Usuário já existe.')
        users[username] = {
            "password": hash_password(password),
            "progress": []
        }
        save_users(users)
        return redirect(url_for('login_page'))
    return render_template('register.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login_page'))

    users = load_users()
    progresso = users[session['user']].get("progress", [])
    return render_template('dashboard.html',
                           user=session['user'],
                           progresso=progresso,
                           total_cursos=len(cursos_conteudo))

# Página de cursos (lista)
@app.route('/cursos')
def cursos():
    if 'user' not in session:
        return redirect(url_for('login_page'))

    users = load_users()
    progresso = users[session['user']].get("progress", [])
    return render_template('cursos.html', cursos=cursos_conteudo, progresso=progresso)

# Página individual de curso
@app.route('/curso/<curso_id>')
def ver_curso(curso_id):
    if 'user' not in session:
        return redirect(url_for('login_page'))
    
    curso = cursos_conteudo.get(curso_id)
    if not curso:
        return "Curso não encontrado", 404

    users = load_users()
    progresso = users[session['user']].get("progress", [])
    if curso_id not in progresso:
        progresso.append(curso_id)
        users[session['user']]["progress"] = progresso
        save_users(users)

    return render_template('ver_curso.html', curso=curso)

@app.route('/estatisticas')
def estatisticas():
    if 'user' not in session:
        return redirect(url_for('login_page'))

    users = load_users()
    user = session['user']
    progresso_usuario = len(users[user].get("progress", []))

    acessos = [len(u.get("progress", [])) for u in users.values()]
    nomes = list(users.keys())  # nomes dos usuários

    from statistics import mean, median, mode, StatisticsError

    media = mean(acessos) if acessos else 0
    mediana = median(acessos) if acessos else 0
    try:
        moda = mode(acessos)
    except StatisticsError:
        moda = "Não definida (valores múltiplos)"

    return render_template('estatisticas.html',
                           user=user,
                           progresso=progresso_usuario,
                           media=media,
                           mediana=mediana,
                           moda=moda,
                           nomes=nomes,
                           acessos=acessos)

@app.route('/remover_progresso/<curso_id>')
def remover_progresso(curso_id):
    if 'user' not in session:
        return redirect(url_for('login_page'))

    users = load_users()
    user = session['user']
    progresso = users[user].get("progress", [])

    if curso_id in progresso:
        progresso.remove(curso_id)
        users[user]["progress"] = progresso
        save_users(users)

    return redirect(url_for('cursos'))

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login_page'))

# Rota raiz
@app.route('/')
def index():
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
