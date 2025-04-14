from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Criar o banco e tabela se ainda não existem
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Função para verificar login
def verify_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user and user[2] == password:
        return True
    return False

# Função para registrar novo usuário
def register_user(username, password):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Rota principal com login e cadastro
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Verifica qual formulário foi enviado
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']

            if verify_user(username, password):
                return redirect(url_for('dashboard'))
            else:
                return "Usuário ou senha inválidos", 401

        elif 'username2' in request.form and 'password2' in request.form:
            username = request.form['username2']
            password = request.form['password2']

            if register_user(username, password):
                return redirect(url_for('home'))
            else:
                return "Usuário já existe", 400

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return "<h1>Bem-vindo ao painel!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
