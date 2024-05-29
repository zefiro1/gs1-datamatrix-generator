import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import segno
import tempfile
import os
import re
from PIL import Image, ImageTk

GS = '\x1d'

def format_gs1_data(pc, sn, lote, cad, nhrn):
    prefix_map = {
        "PC": "01",    # GTIN
        "SN": "21",    # Serial Number
        "LOTE": "10",  # Batch/Lot Number
        "CAD": "17",   # Expiration Date
        "NHRN": "712" # NHRN
    }
    
    formatted_data = ""
    
    ordered_data = [
        ("PC", pc),
        ("LOTE", lote),
        ("CAD", cad),
        ("SN", sn),
        ("NHRN", nhrn)
    ]
    
    for prefix, data in ordered_data:
        if data:
            if prefix != "LOTE" and prefix != "SN":
                formatted_data += GS
            formatted_data += prefix_map[prefix] + data
    
    if formatted_data.startswith(GS):
        formatted_data = formatted_data[1:]
    
    return formatted_data

def generate_gs1_datamatrix(data):
    return segno.make(data)

def generate_and_display():
    pc = pc_entry.get()
    sn = sn_entry.get()
    lote = lote_entry.get()
    cad = cad_entry.get()
    nhrn = nhrn_entry.get()
    
    # Formatear la fecha de expiración
    cad = re.sub(r'(\d{2})/(\d{2})/(\d{2})', r'\3\2\1', cad)
    
    formatted_data = format_gs1_data(pc, sn, lote, cad, nhrn)
    
    # Generar el DataMatrix
    dm = generate_gs1_datamatrix(formatted_data)
    
    # Guardar el DataMatrix en un archivo temporal
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        filename = temp_file.name
        dm.save(temp_file)

    # Redimensionar la imagen a 200x200
    img = Image.open(filename)
    img_resized = img.resize((200, 200), Image.ANTIALIAS)

    # Mostrar la imagen en la GUI
    img_tk = ImageTk.PhotoImage(img_resized)
    image_label.config(image=img_tk)
    image_label.image = img_tk

    # Eliminar el archivo temporal
    os.remove(filename)

def download_datamatrix():
    pc = pc_entry.get()
    sn = sn_entry.get()
    lote = lote_entry.get()
    cad = cad_entry.get()
    nhrn = nhrn_entry.get()
    
    # Formatear la fecha de expiración
    cad = re.sub(r'(\d{2})/(\d{2})/(\d{2})', r'\3\2\1', cad)
    
    formatted_data = format_gs1_data(pc, sn, lote, cad, nhrn)
    
    # Generar el DataMatrix
    dm = generate_gs1_datamatrix(formatted_data)
    
    # Abrir el cuadro de diálogo para seleccionar la ubicación de guardado
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    
    # Guardar el DataMatrix en la ubicación seleccionada
    if file_path:
        dm.save(file_path, scale=5, border=2)



# Crear la ventana principal
root = tk.Tk()
root.title("Generador GS1 Data Matrix")

# Crear y colocar los widgets
pc_label = ttk.Label(root, text="Product Code (PC):")
pc_label.grid(row=0, column=0, sticky="w")
pc_entry = ttk.Entry(root)
pc_entry.grid(row=0, column=1)

sn_label = ttk.Label(root, text="Serial Number (SN):")
sn_label.grid(row=1, column=0, sticky="w")
sn_entry = ttk.Entry(root)
sn_entry.grid(row=1, column=1)

lote_label = ttk.Label(root, text="Lote (Batch):")
lote_label.grid(row=2, column=0, sticky="w")
lote_entry = ttk.Entry(root)
lote_entry.grid(row=2, column=1)

cad_label = ttk.Label(root, text="Exp Date (CAD):")
cad_label.grid(row=3, column=0, sticky="w")
cad_entry = ttk.Entry(root)
cad_entry.grid(row=3, column=1)

nhrn_label = ttk.Label(root, text="National Code (NHRN):")
nhrn_label.grid(row=4, column=0, sticky="w")
nhrn_entry = ttk.Entry(root)
nhrn_entry.grid(row=4, column=1)

generate_button = ttk.Button(root, text="Generate", command=generate_and_display)
generate_button.grid(row=5, column=0, columnspan=4, pady=10)

download_button = ttk.Button(root, text="Download", command=download_datamatrix)
download_button.grid(row=6, column=0, columnspan=2, pady=10)

# Etiqueta para mostrar la imagen
image_label = ttk.Label(root)
image_label.grid(row=7, column=0, columnspan=2)

root.mainloop()
