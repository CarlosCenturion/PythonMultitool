import requests
from colorama import init, Fore, Style

init(autoreset=True)
BASE_URL = 'http://127.0.0.1:5000'

def mostrar_logo():
    logo = f"{Fore.GREEN}" + "="*50 + f"{Style.RESET_ALL}"
    print(logo)

def agregar_usuario(name, email, password, permissions='user'):
    url = f'{BASE_URL}/user'
    data = {'name': name, 'email': email, 'password': password, 'permissions': permissions}
    try:
        response = requests.post(url, json=data)
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
    except ValueError as e:
        return {'error': 'Invalid response from server'}

def obtener_usuarios():
    url = f'{BASE_URL}/users'
    response = requests.get(url)
    return response.json()

def obtener_usuario(user_id):
    url = f'{BASE_URL}/user/{user_id}'
    response = requests.get(url)
    return response.json()

def eliminar_usuario(user_id):
    url = f'{BASE_URL}/user/{user_id}'
    response = requests.delete(url)
    return response.json()

def actualizar_permisos(user_id, permissions):
    url = f'{BASE_URL}/user/{user_id}/permissions'
    data = {'permissions': permissions}
    response = requests.put(url, json=data)
    return response.json()

def login(name, password):
    url = f'{BASE_URL}/login'
    data = {'name': name, 'password': password}
    response = requests.post(url, json=data)
    return response.json()

def actualizar_saldo(user_id, saldo):
    url = f'{BASE_URL}/user/{user_id}/saldo'
    data = {'saldo': saldo}
    response = requests.put(url, json=data)
    return response.json()

def obtener_pozo():
    url = f'{BASE_URL}/pozo'
    response = requests.get(url)
    return response.json()

def actualizar_pozo(amount):
    url = f'{BASE_URL}/pozo'
    data = {'amount': amount}
    response = requests.put(url, json=data)
    return response.json()

def obtener_settings():
    url = f'{BASE_URL}/settings'
    response = requests.get(url)
    return response.json()

def actualizar_settings(win_probability, max_wins):
    url = f'{BASE_URL}/settings'
    data = {'win_probability': win_probability, 'max_wins': max_wins}
    response = requests.put(url, json=data)
    return response.json()

def mostrar_permisos():
    permisos = {
        'admin': 'Acceso total a todas las funcionalidades.',
        'editor': 'Puede editar contenidos, pero no gestionar usuarios.',
        'viewer': 'Solo puede visualizar contenidos, sin realizar modificaciones.',
        'user': 'Permisos básicos para usuarios regulares.'
    }
    print(f"{Fore.CYAN}Permisos disponibles:")
    for clave, descripcion in permisos.items():
        print(f"{Fore.YELLOW}{clave}: {Fore.WHITE}{descripcion}")

def ejecutar():
    mostrar_logo()
    while True:
        print(f"{Fore.CYAN}Gestión de Usuarios API")
        print(f"{Fore.GREEN}1. Agregar Usuario")
        print(f"{Fore.GREEN}2. Obtener Usuarios")
        print(f"{Fore.GREEN}3. Eliminar Usuario")
        print(f"{Fore.GREEN}4. Actualizar Permisos de Usuario")
        print(f"{Fore.GREEN}5. Iniciar Sesión")
        print(f"{Fore.GREEN}6. Actualizar Saldo de Usuario")
        print(f"{Fore.GREEN}7. Ver Pozo")
        print(f"{Fore.GREEN}8. Actualizar Pozo")
        print(f"{Fore.GREEN}9. Ver Ajustes")
        print(f"{Fore.GREEN}10. Actualizar Ajustes")
        print(f"{Fore.GREEN}11. Salir")
        eleccion = input(f"{Fore.YELLOW}Selecciona una opción: ")

        if eleccion == "1":
            name = input(f"{Fore.YELLOW}Nombre: ")
            email = input(f"{Fore.YELLOW}Email: ")
            password = input(f"{Fore.YELLOW}Contraseña: ")
            permissions = input(f"{Fore.YELLOW}Permisos (opcional, por defecto 'user'): ")
            if not permissions:
                permissions = 'user'
            resultado = agregar_usuario(name, email, password, permissions)
            if 'error' in resultado:
                print(f"{Fore.RED}{resultado['error']}")
            else:
                print(f"{Fore.GREEN}{resultado['message']}")
        elif eleccion == "2":
            usuarios = obtener_usuarios()
            for usuario in usuarios:
                print(f"{Fore.CYAN}ID: {Fore.WHITE}{usuario[0]}, Nombre: {Fore.WHITE}{usuario[1]}, Email: {Fore.WHITE}{usuario[2]}, Permisos: {Fore.WHITE}{usuario[3]}, Saldo: {Fore.WHITE}{usuario[4]}, Total Gastado: {Fore.WHITE}{usuario[5]}, Total Ganado: {Fore.WHITE}{usuario[6]}")
        elif eleccion == "3":
            user_id = input(f"{Fore.YELLOW}ID de Usuario: ")
            resultado = eliminar_usuario(user_id)
            if 'error' in resultado:
                print(f"{Fore.RED}{resultado['error']}")
            else:
                print(f"{Fore.GREEN}{resultado['message']}")
        elif eleccion == "4":
            user_id = input(f"{Fore.YELLOW}ID de Usuario: ")
            usuario = obtener_usuario(user_id)
            if 'error' in usuario:
                print(f"{Fore.RED}{usuario['error']}")
            else:
                print(f"{Fore.CYAN}Nombre: {Fore.WHITE}{usuario[1]}, Permisos actuales: {Fore.WHITE}{usuario[3]}")
                mostrar_permisos()
                permissions = input(f"{Fore.YELLOW}Nuevos Permisos: ")
                resultado = actualizar_permisos(user_id, permissions)
                if 'error' in resultado:
                    print(f"{Fore.RED}{resultado['error']}")
                else:
                    print(f"{Fore.GREEN}{resultado['message']}")
        elif eleccion == "5":
            name = input(f"{Fore.YELLOW}Nombre: ")
            password = input(f"{Fore.YELLOW}Contraseña: ")
            resultado = login(name, password)
            if 'error' in resultado:
                print(f"{Fore.RED}{resultado['error']}")
            else:
                print(f"{Fore.GREEN}Inicio de sesión exitoso. ID: {resultado['id']}, Nombre: {resultado['name']}, Permisos: {resultado['permissions']}, Saldo: {resultado['saldo']}, Total Gastado: {resultado['totalgastado']}, Total Ganado: {resultado['totalganado']}")
        elif eleccion == "6":
            user_id = input(f"{Fore.YELLOW}ID de Usuario: ")
            usuario = obtener_usuario(user_id)
            if 'error' in usuario:
                print(f"{Fore.RED}{usuario['error']}")
            else:
                print(f"{Fore.CYAN}Nombre: {Fore.WHITE}{usuario[1]}, Saldo actual: {Fore.WHITE}{usuario[4]}")
                saldo = input(f"{Fore.YELLOW}Nuevo Saldo: ")
                resultado = actualizar_saldo(user_id, saldo)
                if 'error' in resultado:
                    print(f"{Fore.RED}{resultado['error']}")
                else:
                    print(f"{Fore.GREEN}{resultado['message']}")
        elif eleccion == "7":
            pozo = obtener_pozo()
            if 'error' in pozo:
                print(f"{Fore.RED}{pozo['error']}")
            else:
                print(f"{Fore.CYAN}Pozo actual: {Fore.WHITE}{pozo['pozo']}")
        elif eleccion == "8":
            amount = input(f"{Fore.YELLOW}Nuevo monto del pozo: ")
            resultado = actualizar_pozo(amount)
            if 'error' in resultado:
                print(f"{Fore.RED}{resultado['error']}")
            else:
                print(f"{Fore.GREEN}{resultado['message']}")
        elif eleccion == "9":
            settings = obtener_settings()
            if 'error' in settings:
                print(f"{Fore.RED}{settings['error']}")
            else:
                print(f"{Fore.CYAN}Probabilidad de ganar: {Fore.WHITE}{settings['win_probability']}, Máximo de victorias: {Fore.WHITE}{settings['max_wins']}")
        elif eleccion == "10":
            win_probability = input(f"{Fore.YELLOW}Nueva probabilidad de ganar (0 a 1): ")
            max_wins = input(f"{Fore.YELLOW}Nuevo máximo de victorias: ")
            resultado = actualizar_settings(win_probability, max_wins)
            if 'error' in resultado:
                print(f"{Fore.RED}{resultado['error']}")
            else:
                print(f"{Fore.GREEN}{resultado['message']}")
        elif eleccion == "11":
            print(f"{Fore.CYAN}Saliendo...")
            break
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    ejecutar()
