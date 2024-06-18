import socket
import tkinter as tk
from datetime import datetime
from time import sleep
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

now = datetime.now()

# Configurar opciones para mantener la sesión actual de Chrome
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Crear la ventana principal
master = tk.Tk()
master.title("Whatsapp Bot")
width = 500
height = 700
canvas1 = tk.Canvas(master, width=width, height=height, relief='raised', bg='white')
canvas1.pack()

# Dibujar líneas en el canvas
canvas1.create_line(width / 2, 0, width / 2, height, dash=(4, 2))
canvas1.create_line(0, height / 2, width, height / 2, dash=(4, 2))

# Calcular la posición del centro
cx = canvas1.canvasx(width / 2)
cy = canvas1.canvasy(height / 2)
cid = canvas1.find_closest(cx, cy)[0]
canvas1.itemconfigure(cid, fill="blue")

# Cargar la imagen gif
current_directory = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_directory, 'images', 'GZd3Pv.png')

try:
    gif1 = tk.PhotoImage(file=image_path)
    canvas1.create_image(width / 2, height / 2, image=gif1)
except tk.TclError as e:
    print(f"Error al cargar la imagen: {e}")

# Funciones de selección
def blueSelection(event=None):
    l1 = tk.Label(master, text="Enter the Message ", bg="blue")
    l2 = tk.Label(master, text="How many messages do you want to send?", bg="blue")
    l3 = tk.Label(master, text="Enter the Phone Number ", bg="blue")

    canvas1.create_window(100, 250, window=l1)
    canvas1.create_window(150, 290, window=l2)
    canvas1.create_window(100, 330, window=l3)

    e1 = tk.Entry(master)
    e2 = tk.Entry(master)
    e3 = tk.Entry(master)

    canvas1.create_window(400, 250, window=e1)
    canvas1.create_window(400, 290, window=e2)
    canvas1.create_window(400, 330, window=e3)

    def Driver():
        message_text = e1.get()
        no_of_message = e2.get()
        phone_number = e3.get()

        if not message_text or not no_of_message or not phone_number:
            m1 = tk.Label(master, text="ERROR : Please fill the blanks.", fg="red", bg="black")
            canvas1.create_window(250, 140, window=m1)
            m1.after(5000, m1.destroy)
            return

        try:
            no_of_message = int(no_of_message)
            phone_number = int(phone_number)
        except ValueError:
            m1 = tk.Label(master, text="ERROR : Please enter valid numbers.", fg="red", bg="black")
            canvas1.create_window(250, 170, window=m1)
            m1.after(5000, m1.destroy)
            return

        if len(str(phone_number)) < 9:
            m1 = tk.Label(master, text="ERROR : Please enter minimum 9 digits for Phone Number.", fg="red", bg="black")
            canvas1.create_window(250, 200, window=m1)
            m1.after(5000, m1.destroy)
            return

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get("http://web.whatsapp.com")
        sleep(15)  # Tiempo para escanear el código QR

        def element_presence(driver, by, xpath, time):
            element_present = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(driver, time).until(element_present)

        def is_connected():
            try:
                socket.create_connection(("www.google.com", 80))
                return True
            except:
                return False

        def send_whatsapp_msg(driver, phone_no, text, no):
            sleep(2)
            driver.get(f"https://web.whatsapp.com/send?phone={phone_no}&source=&data=#")
            try:
                element_presence(driver, By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div', 30)
                txt_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div')
                for _ in range(no):
                    txt_box.send_keys(text)
                    txt_box.send_keys("\n")
            except Exception as e:
                print(f"Error: {e}")
                print(f"Invalid Phone Number: {phone_no}")

        try:
            send_whatsapp_msg(driver, phone_number, message_text, no_of_message)
        except Exception as e:
            if not is_connected():
                print("No internet connection.")
            print(f"Failed to send message: {e}")

    c1 = tk.Button(text='Send', command=Driver, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
    canvas1.create_window(250, 380, window=c1)

# Vinculación de eventos para diferentes selecciones
ch = tk.Label(master, text="Send Message X Times", fg="white", bg="lightblue")
ch.bind("<Button-1>", blueSelection)
ch.config(font=('helvetica', 14))
canvas1.create_window(120, 270, window=ch)

# Otros eventos de selección pueden ser definidos de manera similar

master.mainloop()
