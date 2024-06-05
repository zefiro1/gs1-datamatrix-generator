import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import segno
import tempfile
import os
import re
from PIL import Image, ImageTk

GS = '\x1d'

# Funciones para formatear datos
def format_gs1_data(pc, sn, lote, cad, nhrn):
    prefix_map = {
        "PC": "01",    # GTIN
        "SN": "21",    # Serial Number
        "LOTE": "10",  # Batch/Lot Number
        "CAD": "17",   # Expiration Date
        "NHRN": "712"  # NHRN
    }
    
    if pc.startswith("0847000"):
        ordered_data = [
            ("PC", pc),
            ("CAD", cad),
            ("LOTE", lote),
            ("SN", sn),
            ("NHRN", nhrn)
        ]
    else:
        ordered_data = [
            ("PC", pc),
            ("LOTE", lote),
            ("CAD", cad),
            ("SN", sn),
            ("NHRN", nhrn)
        ]

    formatted_data = ""
    for prefix, data in ordered_data:
        if data:
            if (pc.startswith("0847000") and prefix in ["SN", "NHRN"]) or (not pc.startswith("0847000") and prefix not in ["LOTE", "SN"]):
                formatted_data += GS
            formatted_data += prefix_map[prefix] + data
    
    if formatted_data.startswith(GS):
        formatted_data = formatted_data[1:]
    
    return formatted_data

def format_ppn_data(pc, lote, cad, sn):
    formatted_data = f"[)>069N{pc}1T{lote}D{cad}S{sn}"
    return formatted_data

# Función para generar el DataMatrix
def generate_gs1_datamatrix(data):
    return segno.make(data)

# Función para generar y mostrar el DataMatrix
def generate_and_display_data_matrix(pc, sn, lote, cad, nhrn, code_type, image_label):
    # Formatear la fecha de expiración
    cad = re.sub(r'(\d{2})/(\d{2})/(\d{2})', r'\3\2\1', cad)
    
    if code_type == "GS1":
        formatted_data = format_gs1_data(pc, sn, lote, cad, nhrn)
    else:  # PPN
        formatted_data = format_ppn_data(pc, lote, cad, sn)
    
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

# Clase para gestionar la interfaz de usuario
class DataMatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador GS1/PPN Data Matrix")
        
        self.create_widgets()
        
    def create_widgets(self):
        code_type_label = ttk.Label(self.root, text="Code Type:")
        code_type_label.grid(row=0, column=0, sticky="w")
        self.code_type = ttk.Combobox(self.root, values=["GS1", "PPN"])
        self.code_type.grid(row=0, column=1)
        self.code_type.current(0)

        pc_label = ttk.Label(self.root, text="Product Code (PC):")
        pc_label.grid(row=1, column=0, sticky="w")
        self.pc_entry = ttk.Entry(self.root)
        self.pc_entry.grid(row=1, column=1)

        sn_label = ttk.Label(self.root, text="Serial Number (SN):")
        sn_label.grid(row=2, column=0, sticky="w")
        self.sn_entry = ttk.Entry(self.root)
        self.sn_entry.grid(row=2, column=1)

        lote_label = ttk.Label(self.root, text="Lote (Batch):")
        lote_label.grid(row=3, column=0, sticky="w")
        self.lote_entry = ttk.Entry(self.root)
        self.lote_entry.grid(row=3, column=1)

        cad_label = ttk.Label(self.root, text="Exp Date (CAD):")
        cad_label.grid(row=4, column=0, sticky="w")
        self.cad_entry = ttk.Entry(self.root)
        self.cad_entry.grid(row=4, column=1)

        nhrn_label = ttk.Label(self.root, text="National Code (NHRN):")
        nhrn_label.grid(row=5, column=0, sticky="w")
        self.nhrn_entry = ttk.Entry(self.root)
        self.nhrn_entry.grid(row=5, column=1)

        generate_button = ttk.Button(self.root, text="Generate", command=self.generate_and_display)
        generate_button.grid(row=7, column=0, columnspan=4, pady=10)

        download_button = ttk.Button(self.root, text="Download", command=self.download_datamatrix)
        download_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.image_label = ttk.Label(self.root)
        self.image_label.grid(row=9, column=0, columnspan=2)
        
    def generate_and_display(self):
        pc = self.pc_entry.get()
        sn = self.sn_entry.get()
        lote = self.lote_entry.get()
        cad = self.cad_entry.get()
        nhrn = self.nhrn_entry.get()
        
        generate_and_display_data_matrix(pc, sn, lote, cad, nhrn, self.code_type.get(), self.image_label)
        
    def download_datamatrix(self):
        pc = self.pc_entry.get()
        sn = self.sn_entry.get()
        lote = self.lote_entry.get()
        cad = self.cad_entry.get()
        nhrn = self.nhrn_entry.get()
        
        # Formatear la fecha de expiración
        cad = re.sub(r'(\d{2})/(\d{2})/(\d{2})', r'\3\2\1', cad)
        
        if self.code_type.get() == "GS1":
            formatted_data = format_gs1_data(pc, sn, lote, cad, nhrn)
        else:  # PPN
            formatted_data = format_ppn_data(pc, lote, cad, sn)
        
        # Generar el DataMatrix
        dm = generate_gs1_datamatrix(formatted_data)
        
        # Abrir el cuadro de diálogo para seleccionar la ubicación de guardado
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        
        # Guardar el DataMatrix en la ubicación seleccionada
        if file_path:
            dm.save(file_path, scale=5, border=2)

# Crear la ventana principal
root = tk.Tk()
app = DataMatrixApp(root)
root.mainloop()

