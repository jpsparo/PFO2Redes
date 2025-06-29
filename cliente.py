import requests

API_URL = "http://127.0.0.1:5000"

# -------- REGISTRO DE USUARIO --------
def registrar():
    print("\n--- Registro de Usuario ---")
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    datos = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    respuesta = requests.post(f"{API_URL}/registro", json=datos)
    try:
        print(respuesta.json()['mensaje'])
    except:
        print("❌ Error inesperado:", respuesta.text)

# -------- INICIO DE SESIÓN --------
def login():
    print("\n--- Inicio de Sesión ---")
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    datos = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    respuesta = requests.post(f"{API_URL}/login", json=datos)

    if respuesta.status_code == 200:
        print("✅ Login exitoso.")
        menu_tareas(usuario)
    else:
        print("❌ Error:", respuesta.json()['mensaje'])

# -------- VER HTML DE BIENVENIDA --------
def ver_bienvenida():
    print("\n--- Página de Bienvenida ---")
    respuesta = requests.get(f"{API_URL}/bienvenida")
    print(respuesta.text)

# -------- SUBMENÚ DE TAREAS --------
def menu_tareas(usuario):
    while True:
        print(f"\n=== Menú de Tareas (usuario: {usuario}) ===")
        print("1. Ver tareas")
        print("2. Crear nueva tarea")
        print("3. Actualizar tarea")
        print("4. Eliminar tarea")
        print("5. Volver al menú principal")

        opcion = input("Elija una opción: ")

        if opcion == "1":
            listar_tareas(usuario)
        elif opcion == "2":
            crear_tarea(usuario)
        elif opcion == "3":
            actualizar_tarea()
        elif opcion == "4":
            eliminar_tarea()
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")

# -------- CREAR TAREA --------
def crear_tarea(usuario):
    print("\n--- Crear nueva tarea ---")
    titulo = input("Título: ")
    descripcion = input("Descripción: ")

    datos = {
        "usuario": usuario,
        "titulo": titulo,
        "descripcion": descripcion
    }

    respuesta = requests.post(f"{API_URL}/tareas", json=datos)
    try:
        print(respuesta.json()['mensaje'])
    except:
        print("❌ Error al crear tarea:", respuesta.text)

# -------- LISTAR TAREAS --------
def listar_tareas(usuario):
    print("\n--- Lista de tareas ---")
    respuesta = requests.get(f"{API_URL}/tareas/{usuario}")
    if respuesta.status_code == 200:
        tareas = respuesta.json()
        if tareas:
            for tarea in tareas:
                print(f"[{tarea['id']}] {tarea['titulo']}: {tarea['descripcion']}")
        else:
            print("No hay tareas registradas.")
    else:
        print("❌", respuesta.json()['mensaje'])

# -------- ACTUALIZAR TAREA --------
def actualizar_tarea():
    print("\n--- Actualizar tarea ---")
    tarea_id = input("ID de la tarea a actualizar: ")
    nuevo_titulo = input("Nuevo título: ")
    nueva_desc = input("Nueva descripción: ")

    datos = {
        "titulo": nuevo_titulo,
        "descripcion": nueva_desc
    }

    respuesta = requests.put(f"{API_URL}/tareas/{tarea_id}", json=datos)
    try:
        print(respuesta.json()['mensaje'])
    except:
        print("❌ Error al actualizar:", respuesta.text)

# -------- ELIMINAR TAREA --------
def eliminar_tarea():
    print("\n--- Eliminar tarea ---")
    tarea_id = input("ID de la tarea a eliminar: ")

    respuesta = requests.delete(f"{API_URL}/tareas/{tarea_id}")
    try:
        print(respuesta.json()['mensaje'])
    except:
        print("❌ Error al eliminar:", respuesta.text)

# -------- MENÚ PRINCIPAL --------
def menu():
    while True:
        print("\n=== Menú Principal ===")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Ver página de bienvenida")
        print("4. Salir")

        opcion = input("Elija una opción: ")

        if opcion == "1":
            registrar()
        elif opcion == "2":
            login()
        elif opcion == "3":
            ver_bienvenida()
        elif opcion == "4":
            print("Hasta luego!")
            break
        else:
            print("Opción inválida.")

# -------- PUNTO DE ENTRADA --------
if __name__ == '__main__':
    menu()