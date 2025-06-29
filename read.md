
IFTS 29. Redes PFO2: Sistema de Gestión de Tareas con API REST y Cliente en Consola.-
Alumno: Juan Pablo Sparo.-

Este proyecto implementa un sistema básico de gestión de tareas con:

- API REST desarrollada con Flask y SQLite para persistencia.
- Autenticación básica con registro e inicio de sesión de usuarios.
- Hashing de contraseñas para mayor seguridad.
- Cliente en consola que interactúa con la API para crear, ver, actualizar y eliminar tareas.
- HTML simple de bienvenida en la ruta `/bienvenida`.

Estructura del Proyecto:
 servidor.py: Código principal del servidor Flask.
 tareas.db: Base de datos SQLite que almacena usuarios y tareas.
 cliente.py: Cliente en consola que interactúa con la API para registro, login y gestión básica de tareas.
 readme.md: Instrucciones del proyecto.


Tecnologías utilizadas:

- Python 3.x
- Flask
- SQLite3
- Werkzeug (para hashing de contraseñas)
- Requests (para el cliente en consola)

Instrucciones para ejecutar el proyecto:

Clonar el repositorio  desde la consola:
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio

Instalar dependencias. Desde la terminal del sistema ejecutar: pip install flask requests werkzeug

Ejecutar el servidor: python servidor.py El servidor se iniciará en http://localhost:5000
Ejecutar cliente en consola: 
Debe Tener en funcionamiento el servidor (servidor.py) e instalada la librería requests
1.	Abra una nueva terminal en el mismo directorio del proyecto y ejecute: python cliente.py
El cliente mostrará un menú interactivo: 

=== Menú Principal ===
1. Registrarse
2. Iniciar sesión
3. Ver página de bienvenida
4. Salir
Elija una opción: 

ENDPOINTS IMPLEMENTADOS EN EL SERVIDOR y PRUEBAS CON POSTMAN:

1. POST /registro — Registrar usuario
Entrada (JSON): json
{"usuario": "nombre","contraseña": "1234"}
Respuesta esperada:
201: {"mensaje": "Usuario registrado exitosamente"}
400: {"mensaje": "El usuario ya existe"}

Postman:
Método: POST
URL: http://127.0.0.1:5000/registro
Ir a pestaña Body → raw → JSON
json
{"usuario": "nombre","contraseña": "1234"}
Click en Send

2. POST /login — Iniciar sesión
Entrada (JSON): json
{"usuario": "nombre", "contraseña": "1234"}
Respuesta esperada:
200: {"mensaje": "Inicio de sesión exitoso"}
401: {"mensaje": "Credenciales incorrectas"}


Método: POST
URL: http://127.0.0.1:5000/login
Body → raw → JSON:
json
{"usuario": "nombre", "contraseña": "1234"}

3. GET /bienvenida — Página HTML simple
Respuesta esperada:
Una página HTML con: html

<h1>Bienvenido al Sistema de Gestión de Tareas</h1>
En navegador: http://127.0.0.1:5000/bienvenida
En Postman: Método GET, sin body.

4. POST /tareas — Crear nueva tarea
Entrada (JSON): json

{ "usuario": "nombre", "titulo": "Estudiar redes", "descripcion": "Repasar conceptos de sockets"}
Respuesta esperada:
201: {"mensaje": "Tarea creada correctamente"}
404: {"mensaje": "Usuario no encontrado"}

Método: POST
URL: http://127.0.0.1:5000/tareas
Body → raw → JSON: json

{"usuario": "nombre", "titulo": "Estudiar redes", "descripcion": "Repasar conceptos de sockets"}

5. GET /tareas/<usuario> — Listar tareas
Respuesta esperada:
json
[
  {
    "id": 1,
    "titulo": "Estudiar redes",
    "descripcion": "Repasar conceptos de sockets"
  },
  ...
]

Método: GET
URL: http://127.0.0.1:5000/tareas/nombre


6. PUT /tareas/<tarea_id> — Editar tarea
Entrada (JSON):
json
{
  "titulo": "Estudiar Python",
  "descripcion": "Listas, diccionarios y funciones"
}
Respuesta esperada:
200: {"mensaje": "Tarea actualizada"}


Método: PUT
URL: htp://127.0.0.1:5000/tareas/1
(Reemplazar 1 con el ID de la tarea que querés editar)

Body → raw → JSON:json

{
  "titulo": "Estudiar Python",
  "descripcion": "Listas, diccionarios y funciones"
}

7. DELETE /tareas/<tarea_id> — Eliminar tarea
Respuesta esperada:
200: {"mensaje": "Tarea eliminada"}

Método: DELETE
URL: http://127.0.0.1:5000/tareas/1
(Reemplazar 1 por el ID de la tarea a borrar)


¿Por qué hashear contraseñas?
Las contraseñas no deben almacenarse en texto plano por seguridad. Si la base de datos se ve comprometida, los hashes no pueden ser revertidos fácilmente. El hashing es una función unidireccional, lo que significa que no es posible obtener la contraseña original desde el hash.
En este proyecto usamos werkzeug.security.generate_password_hash() para protegerlas.

Ventajas de usar SQLite
Es Ligero, sencillo y no requiere configuración, es decir, no requiere un servidor de base de datos externo y es ideal apra proyectos chicos. La base de datos es un archivo .db que podés mover, copiar o borrar fácilmente.
Además, esta integrado a Python, se accede directamente desde el módulo sqlite3, sin instalar nada extra.


