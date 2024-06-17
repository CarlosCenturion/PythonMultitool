from colorama import init, Fore, Style

init(autoreset=True)

def convertir_longitud(valor, from_unit, to_unit):
    conversiones = {
        'metros_kilometros': valor / 1000,
        'kilometros_millas': valor * 0.621371,
        'millas_metros': valor * 1609.34
    }
    return conversiones.get(f"{from_unit}_{to_unit}")

def convertir_peso(valor, from_unit, to_unit):
    conversiones = {
        'gramos_kilogramos': valor / 1000,
        'kilogramos_libras': valor * 2.20462,
        'libras_gramos': valor * 453.592
    }
    return conversiones.get(f"{from_unit}_{to_unit}")

def convertir_volumen(valor, from_unit, to_unit):
    conversiones = {
        'mililitros_litros': valor / 1000,
        'litros_galones': valor * 0.264172,
        'galones_mililitros': valor * 3785.41
    }
    return conversiones.get(f"{from_unit}_{to_unit}")

def ejecutar():
    while True:
        print(f"\n{Fore.GREEN}Conversor de Unidades")
        print(f"{Fore.BLUE}1. Convertir Longitud")
        print(f"{Fore.BLUE}2. Convertir Peso")
        print(f"{Fore.BLUE}3. Convertir Volumen")
        print(f"{Fore.BLUE}4. Salir")
        eleccion = input(f"{Fore.YELLOW}Selecciona una opción: ")

        if eleccion == "1":
            valor = float(input("Valor: "))
            print(f"{Fore.CYAN}1. Metros a Kilómetros")
            print(f"{Fore.CYAN}2. Kilómetros a Millas")
            print(f"{Fore.CYAN}3. Millas a Metros")
            subeleccion = input(f"{Fore.YELLOW}Selecciona una opción: ")
            if subeleccion == "1":
                resultado = convertir_longitud(valor, 'metros', 'kilometros')
                print(f"{Fore.CYAN}{valor} metros son {resultado} kilómetros")
            elif subeleccion == "2":
                resultado = convertir_longitud(valor, 'kilometros', 'millas')
                print(f"{Fore.CYAN}{valor} kilómetros son {resultado} millas")
            elif subeleccion == "3":
                resultado = convertir_longitud(valor, 'millas', 'metros')
                print(f"{Fore.CYAN}{valor} millas son {resultado} metros")
            else:
                print(f"{Fore.RED}Opción no válida.")

        elif eleccion == "2":
            valor = float(input("Valor: "))
            print(f"{Fore.CYAN}1. Gramos a Kilogramos")
            print(f"{Fore.CYAN}2. Kilogramos a Libras")
            print(f"{Fore.CYAN}3. Libras a Gramos")
            subeleccion = input(f"{Fore.YELLOW}Selecciona una opción: ")
            if subeleccion == "1":
                resultado = convertir_peso(valor, 'gramos', 'kilogramos')
                print(f"{Fore.CYAN}{valor} gramos son {resultado} kilogramos")
            elif subeleccion == "2":
                resultado = convertir_peso(valor, 'kilogramos', 'libras')
                print(f"{Fore.CYAN}{valor} kilogramos son {resultado} libras")
            elif subeleccion == "3":
                resultado = convertir_peso(valor, 'libras', 'gramos')
                print(f"{Fore.CYAN}{valor} libras son {resultado} gramos")
            else:
                print(f"{Fore.RED}Opción no válida.")

        elif eleccion == "3":
            valor = float(input("Valor: "))
            print(f"{Fore.CYAN}1. Mililitros a Litros")
            print(f"{Fore.CYAN}2. Litros a Galones")
            print(f"{Fore.CYAN}3. Galones a Mililitros")
            subeleccion = input(f"{Fore.YELLOW}Selecciona una opción: ")
            if subeleccion == "1":
                resultado = convertir_volumen(valor, 'mililitros', 'litros')
                print(f"{Fore.CYAN}{valor} mililitros son {resultado} litros")
            elif subeleccion == "2":
                resultado = convertir_volumen(valor, 'litros', 'galones')
                print(f"{Fore.CYAN}{valor} litros son {resultado} galones")
            elif subeleccion == "3":
                resultado = convertir_volumen(valor, 'galones', 'mililitros')
                print(f"{Fore.CYAN}{valor} galones son {resultado} mililitros")
            else:
                print(f"{Fore.RED}Opción no válida.")

        elif eleccion == "4":
            break
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    ejecutar()
