import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

def analizar_imagen(imagen):
    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    # Detectar bordes usando Canny
    bordes = cv2.Canny(gris, 100, 200)
    
    # Contar el número de bordes detectados
    num_bordes = np.sum(bordes > 0)
    
    # Detectar círculos usando Hough Circle Transform
    circulos = cv2.HoughCircles(gris, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    
    num_circulos = 0 if circulos is None else len(circulos[0])
    
    return f"La imagen contiene aproximadamente {num_bordes} píxeles de borde y {num_circulos} círculos detectados."

class AnalizarImagenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Imagen")
        
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
                
                resultado = analizar_imagen(imagen)
                messagebox.showinfo("Resultado del Análisis", resultado)
                
                # Mostrar la imagen
                imagen_pil = Image.fromarray(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
                imagen_pil = imagen_pil.resize((300, 300), Image.LANCZOS)  # Redimensionar la imagen
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