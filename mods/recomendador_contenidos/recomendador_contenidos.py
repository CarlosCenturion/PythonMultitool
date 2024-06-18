import os
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from colorama import init, Fore, Style

init(autoreset=True)

def cargar_datos():
    # Simulación de datos de usuario
    ratings_dict = {
        "item": [1, 2, 3, 1, 2, 3],
        "user": [9, 32, 2, 45, 27, 2],
        "rating": [3, 2, 4, 3, 4, 1],
    }
    return pd.DataFrame(ratings_dict)

def entrenar_modelo(datos):
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(datos[['user', 'item', 'rating']], reader)
    trainset, testset = train_test_split(data, test_size=0.25)
    algo = SVD()
    algo.fit(trainset)
    return algo, testset

def hacer_recomendaciones(modelo, user_id, num_recommendations=5):
    items = range(1, 100)  # Suponiendo que hay 100 items
    recomendaciones = []
    for item_id in items:
        if len(recomendaciones) >= num_recommendations:
            break
        rating = modelo.predict(user_id, item_id).est
        recomendaciones.append((item_id, rating))
    recomendaciones.sort(key=lambda x: x[1], reverse=True)
    return recomendaciones[:num_recommendations]

def ejecutar():
    datos = cargar_datos()
    modelo, testset = entrenar_modelo(datos)
    
    while True:
        print(f"\n{Fore.GREEN}Recomendador de Contenidos")
        print(f"{Fore.BLUE}1. Obtener Recomendaciones")
        print(f"{Fore.BLUE}2. Salir")
        eleccion = input(f"{Fore.YELLOW}Selecciona una opción: ")

        if eleccion == "1":
            user_id = int(input("ID de Usuario: "))
            recomendaciones = hacer_recomendaciones(modelo, user_id)
            print(f"{Fore.CYAN}Recomendaciones para el usuario {user_id}:")
            for item_id, rating in recomendaciones:
                print(f"{Fore.WHITE}Item {item_id}: Predicción de Rating {rating:.2f}")
        elif eleccion == "2":
            break
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    ejecutar()
