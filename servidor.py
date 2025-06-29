from flask import Flask, request, jsonify, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_NAME = 'tareas.db'

# Crear tablas si no existen
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contrasena TEXT NOT NULL
            )
        ''')

        # Tabla de tareas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')

        conn.commit()

# Ruta: Registro de usuario
@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    usuario = datos.get('usuario')
    contrasena = datos.get('contraseña')
    
    if not usuario or not contrasena:
        return jsonify({'mensaje': 'Usuario y contraseña requeridos'}), 400

    hash_contra = generate_password_hash(contrasena)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, hash_contra))
            conn.commit()
        return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'mensaje': 'El usuario ya existe'}), 400

# Ruta: Login
@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    usuario = datos.get('usuario')
    contrasena = datos.get('contraseña')

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
        fila = cursor.fetchone()

        if fila and check_password_hash(fila[0], contrasena):
            return jsonify({'mensaje': 'Inicio de sesión exitoso'}), 200
        else:
            return jsonify({'mensaje': 'Credenciales incorrectas'}), 401

# Ruta: HTML de bienvenida (antes causaba conflicto con POST /tareas)
@app.route('/bienvenida', methods=['GET'])
def bienvenida():
    return render_template_string("""
        <html>
            <head><title>Bienvenido</title></head>
            <body>
                <h1>Bienvenido al Sistema de Gestión de Tareas</h1>
                <p>Login exitoso. Aquí irían las tareas.</p>
            </body>
        </html>
    """)

# Ruta: Crear tarea (POST)
@app.route('/tareas', methods=['POST'])
def crear_tarea():
    datos = request.get_json()
    usuario = datos.get('usuario')
    titulo = datos.get('titulo')
    descripcion = datos.get('descripcion')

    if not usuario or not titulo:
        return jsonify({'mensaje': 'Usuario y título son obligatorios'}), 400

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario,))
        fila = cursor.fetchone()

        if not fila:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        usuario_id = fila[0]

        cursor.execute("INSERT INTO tareas (usuario_id, titulo, descripcion) VALUES (?, ?, ?)",
                       (usuario_id, titulo, descripcion))
        conn.commit()

    return jsonify({'mensaje': 'Tarea creada correctamente'}), 201

# Ruta: Listar tareas por usuario
@app.route('/tareas/<usuario>', methods=['GET'])
def listar_tareas(usuario):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario,))
        fila = cursor.fetchone()

        if not fila:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        usuario_id = fila[0]
        cursor.execute("SELECT id, titulo, descripcion FROM tareas WHERE usuario_id = ?", (usuario_id,))
        tareas = cursor.fetchall()

        tareas_formateadas = [{'id': t[0], 'titulo': t[1], 'descripcion': t[2]} for t in tareas]

        return jsonify(tareas_formateadas), 200

# Ruta: Actualizar tarea por ID
@app.route('/tareas/<int:tarea_id>', methods=['PUT'])
def actualizar_tarea(tarea_id):
    datos = request.get_json()
    nuevo_titulo = datos.get('titulo')
    nueva_descripcion = datos.get('descripcion')

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tareas SET titulo = ?, descripcion = ? WHERE id = ?",
                       (nuevo_titulo, nueva_descripcion, tarea_id))
        conn.commit()

    return jsonify({'mensaje': 'Tarea actualizada'}), 200

# Ruta: Eliminar tarea por ID
@app.route('/tareas/<int:tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
        conn.commit()

    return jsonify({'mensaje': 'Tarea eliminada'}), 200

# Inicializar base y ejecutar servidor
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

