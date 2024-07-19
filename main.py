import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import segno
import tempfile
import os
import re
from PIL import Image, ImageTk, ImageOps

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

# Función para invertir la imagen
def invert_image(image_path):
    img = Image.open(image_path)
    inverted_image = ImageOps.invert(img.convert("L")).convert("1")
    return inverted_image

# Función para generar y mostrar el DataMatrix
def generate_and_display_data_matrix(pc, sn, lote, cad, nhrn, code_type, image_label, inverted):
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
    
    if inverted:
        img = invert_image(filename)
    else:
        img = Image.open(filename)
    
    # Redimensionar la imagen a 200x200
    img_resized = img.resize((200, 200), Image.Resampling.LANCZOS)

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
        self.root.geometry("400x600")
        
        self.always_on_top_var = tk.BooleanVar(value=True)  # Variable para el checkbox
        self.root.attributes("-topmost", self.always_on_top_var.get())
        
        self.create_widgets()
        
    def create_widgets(self):
        # Crear un frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Crear un frame para los controles
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=(0, 20))
        
        # Etiqueta y combobox para el tipo de código
        code_type_label = ttk.Label(control_frame, text="Code Type:")
        code_type_label.grid(row=0, column=0, padx=(0, 10), sticky="w")
        self.code_type = ttk.Combobox(control_frame, values=["GS1", "PPN"], width=10)
        self.code_type.grid(row=0, column=1)
        self.code_type.current(0)

        # Etiquetas y entradas para los datos del código
        pc_label = ttk.Label(control_frame, text="Product Code (PC):")
        pc_label.grid(row=1, column=0, padx=(0, 10), pady=(10, 0), sticky="w")
        self.pc_entry = ttk.Entry(control_frame)
        self.pc_entry.grid(row=1, column=1, pady=(10, 0))

        sn_label = ttk.Label(control_frame, text="Serial Number (SN):")
        sn_label.grid(row=2, column=0, padx=(0, 10), pady=(10, 0), sticky="w")
        self.sn_entry = ttk.Entry(control_frame)
        self.sn_entry.grid(row=2, column=1, pady=(10, 0))

        lote_label = ttk.Label(control_frame, text="Lote (Batch):")
        lote_label.grid(row=3, column=0, padx=(0, 10), pady=(10, 0), sticky="w")
        self.lote_entry = ttk.Entry(control_frame)
        self.lote_entry.grid(row=3, column=1, pady=(10, 0))

        cad_label = ttk.Label(control_frame, text="Exp Date (CAD):")
        cad_label.grid(row=4, column=0, padx=(0, 10), pady=(10, 0), sticky="w")
        self.cad_entry = ttk.Entry(control_frame)
        self.cad_entry.grid(row=4, column=1, pady=(10, 0))

        nhrn_label = ttk.Label(control_frame, text="National Code (NHRN):")
        nhrn_label.grid(row=5, column=0, padx=(0, 10), pady=(10, 0), sticky="w")
        self.nhrn_entry = ttk.Entry(control_frame)
        self.nhrn_entry.grid(row=5, column=1, pady=(10, 0))

        # Checkbox para invertir el Data Matrix
        self.inverted_var = tk.BooleanVar()
        inverted_checkbox = ttk.Checkbutton(control_frame, text="Invert Data Matrix", variable=self.inverted_var)
        inverted_checkbox.grid(row=6, column=0, columnspan=2, pady=(10, 0), sticky="w")

        # Checkbox para mantener siempre en primer plano
        always_on_top_checkbox = ttk.Checkbutton(control_frame, text="Always on Top", variable=self.always_on_top_var, command=self.toggle_always_on_top)
        always_on_top_checkbox.grid(row=7, column=0, columnspan=2, pady=(10, 0), sticky="w")
        
        # Botones para generar y descargar el Data Matrix
        generate_button = ttk.Button(control_frame, text="Generate", command=self.generate_and_display)
        generate_button.grid(row=8, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        download_button = ttk.Button(control_frame, text="Download", command=self.download_datamatrix)
        download_button.grid(row=9, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        # Etiqueta para mostrar la imagen del Data Matrix
        self.image_label = ttk.Label(main_frame)
        self.image_label.pack(pady=(20, 0))      
    def toggle_always_on_top(self):
        self.root.attributes("-topmost", self.always_on_top_var.get())
    def generate_and_display(self):
        pc = self.pc_entry.get()
        sn = self.sn_entry.get()
        lote = self.lote_entry.get()
        cad = self.cad_entry.get()
        nhrn = self.nhrn_entry.get()
        inverted = self.inverted_var.get()
        
        generate_and_display_data_matrix(pc, sn, lote, cad, nhrn, self.code_type.get(), self.image_label, inverted)
        
    def download_datamatrix(self):
        pc = self.pc_entry.get()
        sn = self.sn_entry.get()
        lote = self.lote_entry.get()
        cad = self.cad_entry.get()
        nhrn = self.nhrn_entry.get()
        inverted = self.inverted_var.get()
        
        # Formatear la fecha de expiración
        cad = re.sub(r'(\d{2})/(\d{2})/(\d{2})', r'\3\2\1', cad)
        
        if self.code_type.get() == "GS1":
            formatted_data = format_gs1_data(pc, sn, lote, cad, nhrn)
        else:  # PPN
            formatted_data = format_ppn_data(pc, lote, cad, sn)
        
        # Generar el DataMatrix
        dm = generate_gs1_datamatrix(formatted_data)
        
        # Guardar el DataMatrix en un archivo temporal
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            filename = temp_file.name
            dm.save(temp_file)

        if inverted:
            img = invert_image(filename)
        else:
            img = Image.open(filename)
        
        # Abrir el cuadro de diálogo para seleccionar la ubicación de guardado
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        
        # Guardar el DataMatrix en la ubicación seleccionada
        if file_path:
            img.save(file_path, format="PNG", dpi=(800, 800))

        # Eliminar el archivo temporal
        os.remove(filename)

# Crear la ventana principal
root = tk.Tk()
app = DataMatrixApp(root)
root.mainloop()

