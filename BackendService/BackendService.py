from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
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
        conn.commit()

@app.route('/user', methods=['POST'])
def add_user():
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
            return jsonify({'id': user[0], 'name': user[1], 'email': user[2], 'permissions': user[3], 'saldo': user[4], 'totalgastado': user[5], 'totalganado': user[6]})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/user/<int:user_id>/saldo', methods=['PUT'])
def update_saldo(user_id):
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
            conn.commit()
    app.run(debug=True)

if __name__ == '__main__':
    ejecutar()
