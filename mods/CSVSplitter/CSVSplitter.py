import pandas as pd
import os

def split_csv(file_path, max_rows=100):
    # Crear el directorio si no existe
    output_dir = os.path.expanduser('~/Descargas/CSVSplitter')
    os.makedirs(output_dir, exist_ok=True)
    # Leer el archivo CSV
    df = pd.read_csv(file_path)
    # Calcular el número de archivos necesarios
    num_files = (len(df) // max_rows) + 1
    # Crear archivos más pequeños
    for i in range(num_files):
        start_row = i * max_rows
        end_row = start_row + max_rows
        df_chunk = df.iloc[start_row:end_row]
        df_chunk.to_csv(os.path.join(output_dir, f'output_part_{i + 1}.csv'), index=False)

# Ejemplo de uso
# split_csv('input_file.csv')

def ejecutar():
    split_csv(input(f"ingrese el path del archivo csv"))