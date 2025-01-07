import pandas as pd
import csv

 
def ejecutar():
 # Cargar el archivo original
 archivo_original = input("archivo.csv : ")
 destino = input("destino.csv : ") 

 # Extraer nombres completos
 nombres_completos = []
 perfiles = []
 
 with open(archivo_original, 'r', encoding='utf-8-sig') as file:
     for linea in file:
        partes = linea.split(' ')
        if len(partes) >= 2:
            nombre_completo = partes[0] + ' ' + partes[1]  # Asumir que los dos primeros son el nombre completo
            nombres_completos.append(nombre_completo)
            # Extraer el enlace que sigue a 'URL :'
            if 'URL :' in linea:
                url_index = linea.index('URL :') + len('URL :')
                perfil = linea[url_index:].strip().split(' ')[0]  # Obtener el enlace
                perfiles.append(perfil)
       
 # Eliminar duplicados
 nombres_completos = list(set(nombres_completos))
 perfiles = list(set(perfiles))

 # Crear un nuevo archivo con los nombres completos y los perfiles
 
 nombres_df = pd.DataFrame({'Nombres': nombres_completos, 'Perfil': perfiles})
 nombres_df.to_csv(destino, index=False)
 print(f'Archivo con nombres y perfiles creado: {destino}')     
 

 

if __name__ == "__main__":
    ejecutar()
    

    