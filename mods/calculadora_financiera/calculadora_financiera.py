import math
import requests
from colorama import init, Fore, Style

init(autoreset=True)

def calcular_interes_simple(principal, tasa, tiempo):
    return principal * (tasa / 100) * tiempo

def calcular_interes_compuesto(principal, tasa, tiempo, n):
    return principal * (1 + (tasa / 100) / n) ** (n * tiempo) - principal

def calcular_prestamo(principal, tasa, tiempo):
    tasa_mensual = tasa / 100 / 12
    pagos = tiempo * 12
    pago_mensual = principal * tasa_mensual / (1 - (1 + tasa_mensual) ** -pagos)
    total_pagado = pago_mensual * pagos
    total_interes = total_pagado - principal
    return pago_mensual, total_pagado, total_interes

def calcular_ahorros(monto_mensual, tasa, tiempo):
    tasa_mensual = tasa / 100 / 12
    meses = tiempo * 12
    total_ahorrado = monto_mensual * (((1 + tasa_mensual) ** meses - 1) / tasa_mensual) * (1 + tasa_mensual)
    return total_ahorrado

def convertir_monedas(cantidad, from_currency, to_currency):
    api_url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(api_url)
    if response.status_code == 200:
        rates = response.json().get('rates')
        if rates and to_currency in rates:
            tasa_conversion = rates[to_currency]
            return cantidad * tasa_conversion
    return None

def ejecutar():
    while True:
        print(f"\n{Fore.GREEN}Calculadora Financiera")
        print(f"{Fore.BLUE}1. Calcular Interés Simple")
        print(f"{Fore.BLUE}2. Calcular Interés Compuesto")
        print(f"{Fore.BLUE}3. Calcular Préstamo")
        print(f"{Fore.BLUE}4. Calcular Ahorros")
        print(f"{Fore.BLUE}5. Convertir Monedas")
        print(f"{Fore.BLUE}6. Salir")
        eleccion = input(f"{Fore.YELLOW}Selecciona una opción: ")

        if eleccion == "1":
            principal = float(input("Principal: "))
            tasa = float(input("Tasa de interés (%): "))
            tiempo = float(input("Tiempo (años): "))
            interes = calcular_interes_simple(principal, tasa, tiempo)
            print(f"{Fore.CYAN}Interés Simple: {Fore.WHITE}{interes}")

        elif eleccion == "2":
            principal = float(input("Principal: "))
            tasa = float(input("Tasa de interés (%): "))
            tiempo = float(input("Tiempo (años): "))
            n = int(input("Número de veces que se capitaliza por año: "))
            interes = calcular_interes_compuesto(principal, tasa, tiempo, n)
            print(f"{Fore.CYAN}Interés Compuesto: {Fore.WHITE}{interes}")

        elif eleccion == "3":
            principal = float(input("Principal del préstamo: "))
            tasa = float(input("Tasa de interés (%): "))
            tiempo = float(input("Tiempo (años): "))
            pago_mensual, total_pagado, total_interes = calcular_prestamo(principal, tasa, tiempo)
            print(f"{Fore.CYAN}Pago Mensual: {Fore.WHITE}{pago_mensual}")
            print(f"{Fore.CYAN}Total Pagado: {Fore.WHITE}{total_pagado}")
            print(f"{Fore.CYAN}Total de Interés Pagado: {Fore.WHITE}{total_interes}")

        elif eleccion == "4":
            monto_mensual = float(input("Monto mensual ahorrado: "))
            tasa = float(input("Tasa de interés (%): "))
            tiempo = float(input("Tiempo (años): "))
            total_ahorrado = calcular_ahorros(monto_mensual, tasa, tiempo)
            print(f"{Fore.CYAN}Total Ahorrado: {Fore.WHITE}{total_ahorrado}")

        elif eleccion == "5":
            cantidad = float(input("Cantidad a convertir: "))
            from_currency = input("Moneda de origen (ej. USD): ").upper()
            to_currency = input("Moneda de destino (ej. EUR): ").upper()
            convertido = convertir_monedas(cantidad, from_currency, to_currency)
            if convertido:
                print(f"{Fore.CYAN}{cantidad} {from_currency} {Fore.WHITE}equivale a {Fore.CYAN}{convertido} {to_currency}")
            else:
                print(f"{Fore.RED}No se pudo realizar la conversión. Por favor, intenta de nuevo.")

        elif eleccion == "6":
            break
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    ejecutar()
