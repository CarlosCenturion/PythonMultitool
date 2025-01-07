import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from collections import Counter
import math
import matplotlib.pyplot as plt

# Función para obtener la distribución esperada de Benford
def benford_distribution():
    return [math.log10(1 + 1 / d) for d in range(1, 10)]

# Filtrar transacciones según la Ley de Benford
def filter_by_benford(transactions):
    # Obtener el primer dígito de cada transacción
    first_digits = [int(str(int(x)).lstrip("0")[0]) for x in transactions if x > 0]
    digit_counts = Counter(first_digits)
    total = sum(digit_counts.values())
    
    # Calcular la frecuencia observada
    observed_frequencies = np.array([digit_counts[d] / total for d in range(1, 10)])
    expected_frequencies = np.array(benford_distribution())
    
    # Comparar frecuencias observadas con las esperadas
    return np.abs(observed_frequencies - expected_frequencies) > 0.05  # Umbral ajustable

# Crear y entrenar un modelo Autoencoder
def train_autoencoder(X_train):
    input_dim = X_train.shape[1]
    encoding_dim = input_dim // 2
    
    # Definir el modelo de Autoencoder
    input_layer = Input(shape=(input_dim,))
    encoded = Dense(encoding_dim, activation="relu")(input_layer)
    decoded = Dense(input_dim, activation="sigmoid")(encoded)
    
    autoencoder = Model(inputs=input_layer, outputs=decoded)
    autoencoder.compile(optimizer="adam", loss="mse")
    
    # Entrenar el modelo
    autoencoder.fit(X_train, X_train, epochs=50, batch_size=32, shuffle=True, validation_split=0.1)
    return autoencoder

# Detectar anomalías con el Autoencoder
def detect_anomalies(autoencoder, X_test, threshold):
    reconstructions = autoencoder.predict(X_test)
    test_loss = np.mean(np.square(reconstructions - X_test), axis=1)
    return test_loss > threshold

# Función principal del script
def ejecutar():
    # Cargar los datos de ejemplo
    df_transactions = pd.DataFrame({"monto": [2150, 13500, 7000, 99, 1250, 34000, 4321, 8765, 10000, 555, 123, 340, 789, 1400]})
    transactions = df_transactions["monto"].values
    
    # Filtrar por la Ley de Benford
    benford_anomalies = filter_by_benford(transactions)
    
    # Preprocesamiento: escalar los datos
    scaler = MinMaxScaler()
    transactions_scaled = scaler.fit_transform(df_transactions)
    
    # Dividir los datos en entrenamiento y prueba
    X_train, X_test = transactions_scaled[:10], transactions_scaled[10:]
    
    # Entrenar el Autoencoder con datos de entrenamiento
    autoencoder = train_autoencoder(X_train)
    
    # Calcular el umbral para detección de anomalías
    train_reconstructions = autoencoder.predict(X_train)
    train_loss = np.mean(np.square(train_reconstructions - X_train), axis=1)
    threshold = np.mean(train_loss) + 2 * np.std(train_loss)
    print(f"Umbral de detección de anomalías: {threshold}")
    
    # Detectar anomalías en el conjunto de prueba usando el Autoencoder
    autoencoder_anomalies = detect_anomalies(autoencoder, X_test, threshold)
    
    # Mostrar resultados
    suspicious_transactions = np.where(benford_anomalies & autoencoder_anomalies)
    print("Transacciones sospechosas detectadas:", suspicious_transactions[0])

    # Visualizar el error de reconstrucción
    plt.hist(train_loss, bins=50, color='blue', alpha=0.7)
    plt.axvline(threshold, color='red', linestyle='dashed', linewidth=2)
    plt.xlabel("Error de Reconstrucción")
    plt.ylabel("Frecuencia")
    plt.title("Distribución del Error de Reconstrucción en el Conjunto de Entrenamiento")
    plt.show()

# Ejecutar el script
if __name__ == "__main__":
    ejecutar()
