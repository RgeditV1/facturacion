import customtkinter as ctk

class Ventas:
    def __init__(self, frame):
        self.frame = frame
        self.draw_ui()

        
    def draw_ui(self):
        self.header()
        self.centro() 
               
    def header(self):
        self.header = ctk.CTkFrame(self.frame)
        self.header.pack(padx=(0,1), pady =(1,1),fill="both", expand=False,)
        
        # Crear entrada de búsqueda
        self.frame_busqueda = ctk.CTkFrame(self.header)
        self.frame_busqueda.pack(fill="x", padx=10, pady=10)
        
        self.entry_busqueda = ctk.CTkEntry(self.frame_busqueda, placeholder_text="Buscar por nombre o ID")
        self.entry_busqueda.pack(expand=True, fill="x", side="left", padx=(0, 10))
        
        # Crear botón de búsqueda
        self.btn_buscar = ctk.CTkButton(self.frame_busqueda, text="ENTER - Agregar Producto", width=40, height=40)
        self.btn_buscar.pack(side="right")
        
        # Crear botone de accione
        self.frame_acciones = ctk.CTkFrame(self.header)
        self.frame_acciones.pack(fill="x", padx=10, pady=(0, 10))
        
        self.btn_buscar = ctk.CTkButton(self.frame_acciones, text="F1 - Buscar", width=40, height=25)
        self.btn_buscar.pack(side="left", padx=(0, 10))
        
        self.btn_eliminar = ctk.CTkButton(self.frame_acciones, text="Del - Eliminar", width=40, height=25)
        self.btn_eliminar.pack(side="left", padx=(0, 10))
        
    def centro(self):
        self.centro = ctk.CTkFrame(self.frame, border_width=1, border_color="gray")
        self.centro.pack(fill="both", expand=True, padx=1, pady=1)