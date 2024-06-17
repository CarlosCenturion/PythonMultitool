import os
import subprocess
import sys
import traceback
import ast
from colorama import Fore

def analizar_imports(ruta_modulo):
    imports = set()
    for root, _, files in os.walk(ruta_modulo):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    try:
                        tree = ast.parse(f.read(), filename=file)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imports.add(alias.name.split('.')[0])
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    imports.add(node.module.split('.')[0])
                    except Exception as e:
                        print(f"{Fore.RED}Error analizando {file}: {e}")
    return imports

def validar_dependencias(ruta_reqs):
    valid_packages = set()
    try:
        output = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        installed_packages = {line.decode().split('==')[0] for line in output.splitlines()}
        
        with open(ruta_reqs, 'r') as f:
            for line in f:
                package = line.strip()
                if package and package not in installed_packages:
                    try:
                        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                        valid_packages.add(package)
                    except subprocess.CalledProcessError:
                        print(f"{Fore.RED}El paquete {package} no es válido y será eliminado de {ruta_reqs}.")
                else:
                    valid_packages.add(package)
        
        with open(ruta_reqs, 'w') as f:
            for package in valid_packages:
                f.write(f"{package}\n")
    except Exception as e:
        print(f"{Fore.RED}Error validando dependencias: {e}")

def instalar_dependencias(ruta_reqs, ruta_modulo):
    if not os.path.exists(ruta_reqs):
        print(f"{Fore.YELLOW}El archivo {ruta_reqs} no existe. Creando un archivo...")
        with open(ruta_reqs, 'w') as f:
            pass

    if os.path.getsize(ruta_reqs) == 0:
        print(f"{Fore.YELLOW}El archivo {ruta_reqs} está vacío. Analizando importaciones...")
        imports = analizar_imports(ruta_modulo)
        with open(ruta_reqs, 'w') as f:
            for imp in imports:
                f.write(f"{imp}\n")

    print(f"{Fore.YELLOW}Validando dependencias en {ruta_reqs}...")
    validar_dependencias(ruta_reqs)

    print(f"{Fore.YELLOW}Instalando dependencias desde {ruta_reqs}...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', ruta_reqs])
        print(f"{Fore.GREEN}Dependencias instaladas correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al instalar dependencias del módulo: {e}")
        traceback.print_exc()
        print(f"{Fore.YELLOW}Intentando cargar el módulo a pesar del error en la instalación de dependencias...")
