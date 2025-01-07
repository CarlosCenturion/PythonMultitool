import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import urllib.request
import os

# Descargar los archivos necesarios para YOLOv4
def descargar_archivo(url, nombre_archivo):
    urllib.request.urlretrieve(url, nombre_archivo)

# Descargar los archivos de YOLOv4 si no existen
archivos_yolo = {
    'config': ('yolov4.cfg', 'https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg'),
    'weights': ('yolov4.weights', 'https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights'),
    'classes': ('coco.names', 'https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names')
}

for nombre_archivo, (archivo, url) in archivos_yolo.items():
    if not os.path.exists(archivo):
        print(f"Descargando {archivo}...")
        descargar_archivo(url, archivo)

# Cargar el modelo YOLOv4
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

def analizar_imagen(imagen):
    altura, ancho, _ = imagen.shape
    blob = cv2.dnn.blobFromImage(imagen, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * ancho)
                center_y = int(detection[1] * altura)
                w = int(detection[2] * ancho)
                h = int(detection[3] * altura)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    objetos_detectados = {}

    for i in range(len(boxes)):
        if i in indexes:
            label = str(classes[class_ids[i]])
            objetos_detectados[label] = objetos_detectados.get(label, 0) + 1
            # Dibujar el rectángulo y la etiqueta en la imagen
            x, y, w, h = boxes[i]
            cv2.rectangle(imagen, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(imagen, f"{label}: {confidences[i]:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    resultado = "Objetos detectados en la imagen:\n"
    for objeto, cantidad in objetos_detectados.items():
        resultado += f"- {objeto}: {cantidad}\n"

    return resultado, imagen

class AnalizarImagenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Imagen con YOLOv4")
        
        self.label = tk.Label(root, text="Selecciona una imagen para analizar")
        self.label.pack(pady=20)
        
        self.boton = tk.Button(root, text="Seleccionar Imagen", command=self.seleccionar_imagen)
        self.boton.pack(pady=10)
        
    def seleccionar_imagen(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if file_path:
            try:
                imagen = cv2.imread(file_path)
                if imagen is None:
                    raise ValueError("No se pudo cargar la imagen")
                
                resultado, imagen_analizada = analizar_imagen(imagen)
                messagebox.showinfo("Resultado del Análisis", resultado)
                
                # Mostrar la imagen
                imagen_pil = Image.fromarray(cv2.cvtColor(imagen_analizada, cv2.COLOR_BGR2RGB))
                imagen_pil.thumbnail((600, 600))  # Redimensionar la imagen manteniendo la proporción
                imagen_tk = ImageTk.PhotoImage(imagen_pil)
                self.label.config(image=imagen_tk)
                self.label.image = imagen_tk
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar la imagen: {str(e)}")


def ejecutar():
    root = tk.Tk()
    app = AnalizarImagenApp(root)
    root.mainloop()

if __name__ == "__main__":
    ejecutar()