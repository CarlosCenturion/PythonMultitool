from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import sqlite3
import os
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Reemplaza 'your_secret_key' con una clave secreta segura
DATABASE = 'database.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL UNIQUE,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            permissions TEXT NOT NULL DEFAULT 'user',
                            saldo REAL DEFAULT 0.0,
                            totalgastado REAL DEFAULT 0.0,
                            totalganado REAL DEFAULT 0.0)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS pozo (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            amount REAL DEFAULT 100000.0)''')
        cursor.execute('INSERT OR IGNORE INTO pozo (id, amount) VALUES (1, 100000.0)')
        cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            win_probability REAL DEFAULT 0.5,
                            max_wins INTEGER DEFAULT 10)''')
        cursor.execute('INSERT OR IGNORE INTO settings (id, win_probability, max_wins) VALUES (1, 0.5, 10)')
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_bets (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            cantidad REAL NOT NULL,
                            resultado TEXT NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES users(id))''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/admin')
def admin_page():
    if 'user_id' not in session or session.get('permissions') != 'admin':
        return redirect(url_for('login_page'))
    return render_template('admin.html')

@app.route('/view-users')
def view_users_page():
    if 'user_id' not in session or session.get('permissions') != 'admin':
        return redirect(url_for('login_page'))
    return render_template('view_users.html')

@app.route('/create-user')
def create_user_page():
    if 'user_id' not in session or session.get('permissions') != 'admin':
        return redirect(url_for('login_page'))
    return render_template('create_user.html')

@app.route('/update-pozo')
def update_pozo_page():
    if 'user_id' not in session or session.get('permissions') != 'admin':
        return redirect(url_for('login_page'))
    return render_template('update_pozo.html')

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if 'user_id' not in session or session.get('permissions') != 'admin':
        return jsonify({'error': 'Permission denied'}), 403

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    permissions = data.get('permissions')

    if not name or not email or not password or not permissions:
        return jsonify({'error': 'All fields are required'}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET name = ?, email = ?, password = ?, permissions = ? WHERE id = ?', (name, email, password, permissions, user_id))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': 'User updated successfully'})
        else:
            return jsonify({'error': 'User not found'}), 404

@app.route('/settings')
def settings_page():
    if 'user_id' not in session or session.get('permissions') != 'admin':
        return redirect(url_for('login_page'))
    return render_template('settings.html')

@app.route('/user', methods=['POST'])
def add_user():
    if 'user_id' not in session or session.get('permissions') != 'admin':
        return jsonify({'error': 'Permission denied'}), 403

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    permissions = data.get('permissions', 'user')
    if not name or not email or not password:
        return jsonify({'error': 'Name, email, and password are required'}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (name, email, password, permissions) VALUES (?, ?, ?, ?)', (name, email, password, permissions))
            conn.commit()
        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint failed: users.email' in str(e):
                return jsonify({'error': 'Email already exists'}), 400
            elif 'UNIQUE constraint failed: users.name' in str(e):
                return jsonify({'error': 'Username already exists'}), 400

    return jsonify({'message': 'User added successfully'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, permissions, saldo, totalgastado, totalganado FROM users')
        users = cursor.fetchall()
        return jsonify(users)

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, permissions, saldo, totalgastado, totalganado FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        if user:
            return jsonify(user)
        else:
            return jsonify({'error': 'User not found'}), 404

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if 'user_id' not in session or session.get('permissions') != 'admin':
        return jsonify({'error': 'Permission denied'}), 403

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'error': 'User not found'}), 404

@app.route('/user/<int:user_id>/permissions', methods=['PUT'])
def update_permissions(user_id):
    if 'user_id' not in session or session.get('permissions') != 'admin':
        return jsonify({'error': 'Permission denied'}), 403

    data = request.get_json()
    permissions = data.get('permissions')
    if not permissions:
        return jsonify({'error': 'Permissions are required'}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET permissions = ? WHERE id = ?', (permissions, user_id))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': 'Permissions updated successfully'})
        else:
            return jsonify({'error': 'User not found'}), 404

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    if not name or not password:
        return jsonify({'error': 'Name and password are required'}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, permissions, saldo, totalgastado, totalganado FROM users WHERE name = ? AND password = ?', (name, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user[0]
            session['permissions'] = user[3]
            return jsonify({'id': user[0], 'name': user[1], 'email': user[2], 'permissions': user[3], 'saldo': user[4], 'totalgastado': user[5], 'totalganado': user[6]})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('permissions', None)
    return jsonify({'message': 'Logged out successfully'})

@app.route('/user/<int:user_id>/saldo', methods=['PUT'])
def update_saldo(user_id):
    if 'user_id' not in session or session.get('permissions') != 'admin':
        return jsonify({'error': 'Permission denied'}), 403

    data = request.get_json()
    saldo = data.get('saldo')
    if saldo is None:
        return jsonify({'error': 'Saldo is required'}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET saldo = ? WHERE id = ?', (saldo, user_id))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': 'Saldo updated successfully'})
        else:
            return jsonify({'error': 'User not found'}), 404

@app.route('/settings', methods=['GET', 'PUT'])
def settings():
    if 'user_id' not in session or session.get('permissions') != 'admin':
        return jsonify({'error': 'Permission denied'}), 403

    if request.method == 'GET':
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT win_probability, max_wins FROM settings WHERE id = 1')
            settings = cursor.fetchone()
            if settings:
                return jsonify({'win_probability': settings[0], 'max_wins': settings[1]})
            else:
                return jsonify({'error': 'Settings not found'}), 404
    elif request.method == 'PUT':
        data = request.get_json()
        win_probability = data.get('win_probability')
        max_wins = data.get('max_wins')
        if win_probability is None or max_wins is None:
            return jsonify({'error': 'win_probability and max_wins are required'}), 400

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE settings SET win_probability = ?, max_wins = ? WHERE id = 1', (win_probability, max_wins))
            conn.commit()
            return jsonify({'message': 'Settings updated successfully'})

@app.route('/pozo', methods=['GET'])
def get_pozo():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT amount FROM pozo WHERE id = 1')
        pozo = cursor.fetchone()
        if pozo:
            return jsonify({'pozo': pozo[0]})
        else:
            return jsonify({'error': 'Pozo not found'}), 404

@app.route('/pozo', methods=['PUT'])
def update_pozo():
    if 'permissions' not in session or session['permissions'] != 'admin':
        return jsonify({'error': 'Permission denied'}), 403

    data = request.get_json()
    amount = data.get('amount')
    if amount is None:
        return jsonify({'error': 'Amount is required'}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE pozo SET amount = ? WHERE id = 1', (amount,))
        conn.commit()
        return jsonify({'message': 'Pozo updated successfully'})

@app.route('/edit-user')
def edit_user_page():
    if 'user_id' not in session or session.get('permissions') != 'admin':
        return redirect(url_for('login_page'))
    return render_template('edit_user.html')


@app.route('/user/<int:user_id>/apostar', methods=['POST'])
def apostar(user_id):
    data = request.get_json()
    cantidad = data.get('cantidad')
    if cantidad is None:
        return jsonify({'error': 'Cantidad is required'}), 400

    # Convertir la cantidad a float
    try:
        cantidad = float(cantidad)
    except ValueError:
        return jsonify({'error': 'Invalid amount format'}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT saldo FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        saldo = user[0]
        if cantidad > saldo:
            return jsonify({'error': 'Saldo insuficiente'}), 400

        cursor.execute('SELECT amount FROM pozo WHERE id = 1')
        pozo = cursor.fetchone()[0]

        cursor.execute('SELECT win_probability, max_wins FROM settings WHERE id = 1')
        settings = cursor.fetchone()
        win_probability = settings[0]
        max_wins = settings[1]

        cursor.execute('SELECT COUNT(*) FROM user_bets WHERE user_id = ? AND resultado = "ganaste"', (user_id,))
        user_wins = cursor.fetchone()[0]

        if user_wins >= max_wins:
            return jsonify({'error': 'Max wins reached'}), 400

        # Verificar si el pozo es suficiente para pagar una posible victoria
        if cantidad * 2 > pozo:
            # Forzar derrota
            nuevo_saldo = saldo - cantidad
            nuevo_pozo = pozo + cantidad
            resultado = "perdiste"
            cursor.execute('UPDATE users SET saldo = ?, totalgastado = totalgastado + ? WHERE id = ?', (nuevo_saldo, cantidad, user_id))
        else:
            # Determinar el resultado basado en la probabilidad de ganar
            if random.random() < win_probability:
                # Usuario gana
                nuevo_saldo = saldo + cantidad
                nuevo_pozo = pozo - cantidad
                resultado = "ganaste"
                cursor.execute('UPDATE users SET saldo = ?, totalganado = totalganado + ? WHERE id = ?', (nuevo_saldo, cantidad, user_id))
            else:
                # Usuario pierde
                nuevo_saldo = saldo - cantidad
                nuevo_pozo = pozo + cantidad
                resultado = "perdiste"
                cursor.execute('UPDATE users SET saldo = ?, totalgastado = totalgastado + ? WHERE id = ?', (nuevo_saldo, cantidad, user_id))

        cursor.execute('UPDATE pozo SET amount = ? WHERE id = 1', (nuevo_pozo,))
        cursor.execute('INSERT INTO user_bets (user_id, cantidad, resultado) VALUES (?, ?, ?)', (user_id, cantidad, resultado))
        conn.commit()

    return jsonify({'resultado': resultado, 'nuevo_saldo': nuevo_saldo, 'nuevo_pozo': nuevo_pozo})

def ejecutar():
    if not os.path.exists(DATABASE):
        init_db()
    else:
        # Verifica si las columnas saldo, totalgastado y totalganado existen, y si no, las agrega
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in cursor.fetchall()]
            if 'saldo' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN saldo REAL DEFAULT 0.0")
            if 'totalgastado' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN totalgastado REAL DEFAULT 0.0")
            if 'totalganado' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN totalganado REAL DEFAULT 0.0")
            cursor.execute('''CREATE TABLE IF NOT EXISTS pozo (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                amount REAL DEFAULT 100000.0)''')
            cursor.execute('INSERT OR IGNORE INTO pozo (id, amount) VALUES (1, 100000.0)')
            cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                win_probability REAL DEFAULT 0.5,
                                max_wins INTEGER DEFAULT 10)''')
            cursor.execute('INSERT OR IGNORE INTO settings (id, win_probability, max_wins) VALUES (1, 0.5, 10)')
            cursor.execute('''CREATE TABLE IF NOT EXISTS user_bets (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER NOT NULL,
                                cantidad REAL NOT NULL,
                                resultado TEXT NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES users(id))''')
            conn.commit()
    app.run(debug=True)

if __name__ == '__main__':
    ejecutar()
