from colorama import Fore, Style

def mostrar_logo():    
    logo = f"""
{Fore.RED}
 _____________________________________________
|  _   _               _ ____  _              |
| | | | | __ _ _ __ __| |  _ \| | __ _ _   _  |
| | |_| |/ _` | '__/ _` | |_) | |/ _` | | | | |
| {Fore.GREEN}|  _  | (_| | | | (_| |  __/| | (_| | |_| | | 
| |_| |_|\__,_|_|  \__,_|_|   |_|\__,_|\__, | |
| {Fore.YELLOW}Multitool by Carlos Ezequiel Centurión{Fore.GREEN}|___/ |  
|_____________________________________________|                                                                  
{Style.RESET_ALL}    
   """
    print(logo)




def mostrar_submenu(nombre_modulo):
    print(f"")
    print(f"{Fore.MAGENTA}Selecciona una opción para {nombre_modulo.capitalize()}:")
    print(f"")
    print(f"{Fore.MAGENTA}1. Ejecutar Módulo")
    print(f"{Fore.MAGENTA}2. Información del Módulo")
    print(f"{Fore.MAGENTA}3. Editar Módulo")
    print(f"{Fore.MAGENTA}4. Eliminar Módulo")
    print(f"{Fore.MAGENTA}5. Volver al Menú Principal")
    print(f"")
