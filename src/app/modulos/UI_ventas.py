import customtkinter as ctk

class UIVentas:
    def __init__(self, frame):
        self.frame = frame
        self.draw_ui()

        
    def draw_ui(self):
        self.header()
        self.centro() 
        self.footer()
    
    #-------- Funciones para los botones del footer --------
    def cobrar(self):
        pass
    def nuevo(self):
        pass
    def eliminar(self):
        pass
    def pago_tarjeta(self):
        pass
    def pago_efectivo(self):
        pass
    
    #-------- Funciones para crear la interfaz de ventas --------
    def header(self):
        self.header = ctk.CTkFrame(self.frame)
        self.header.pack(padx=(0,1), pady =(1,1),fill="both", expand=False,)
        
        header_frame = ctk.CTkFrame(self.header, height=50, fg_color="#2c3e50")
        header_frame.pack(fill="x", padx=10, pady=10)
        header_label = ctk.CTkLabel(header_frame, text="Ventas", font=("Arial", 24), text_color="white")
        header_label.pack(pady=(2,2))

        # Crear entrada de búsqueda
        self.frame_busqueda = ctk.CTkFrame(self.header)
        self.frame_busqueda.pack(fill="x", padx=1, pady=(0, 1))
        
        self.entry_busqueda = ctk.CTkEntry(self.frame_busqueda, placeholder_text="Buscar por nombre o ID")
        self.entry_busqueda.pack(expand=True, fill="x", side="left", padx=(0, 10), pady=(1,1))
        
        # Crear botón de búsqueda
        self.btn_buscar = ctk.CTkButton(self.frame_busqueda, text="ENTER - Agregar Producto", width=40, height=25)
        self.btn_buscar.pack(side="right", padx=(0, 1), pady=(1,1))

    #-------- Función para crear el centro de ventas (tabla) -------- 
    def centro(self):
        self.centro = ctk.CTkFrame(self.frame)
        self.centro.pack(fill="both", expand=True, padx=1, pady=1)
        
            # Tabla de productos
        HEADERS = ['ID', 'Descripcion', 'Cantidad', 'Precio', 'Stock']

        CONFIG_COLUMNAS = {
            "ID":          {"width": 70,  "anchor": "center", "weight": 0},
            "Descripcion": {"width": 500, "anchor": "w",      "weight": 1},
            "Cantidad":    {"width": 50,  "anchor": "center", "weight": 0},
            "Precio":      {"width": 50,  "anchor": "center", "weight": 0},
            "Stock":       {"width": 50,  "anchor": "center", "weight": 0},
        }

        self.header_frame = ctk.CTkFrame(self.centro, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=1, pady=1)

        for col, header in enumerate(HEADERS):

            col_frame = ctk.CTkFrame(
                self.header_frame,
                fg_color="#1f538d",
                corner_radius=5
            )
            col_frame.grid(row=0, column=col, padx=1, pady=1, sticky="ew")

            config = CONFIG_COLUMNAS[header]

            lbl = ctk.CTkLabel(
                col_frame,
                text=header,
                font=("Arial", 12, "bold"),
                text_color="white",
                height=20,
                width=config["width"],
                anchor=config["anchor"]
            )
            lbl.grid(row=0, column=0, padx=10, pady=5)

            self.header_frame.grid_columnconfigure(col, weight=config["weight"])


            
    #-------- Función para crear el footer de ventas (botones) --------
    def footer(self):
        self.footer = ctk.CTkFrame(self.frame,
                                   border_width=1, border_color="gray", fg_color="transparent")
        self.footer.pack(padx=(1,1), pady=(1,1), fill="both", expand=False)
        
        cobrar_frame = ctk.CTkFrame(self.footer, fg_color="transparent")
        cobrar_frame.pack(side="right", padx=(0, 1), pady=(1,1), fill="both", expand=False)
        
        # ---- BOTÓN COBRAR (especial) ----
        btn_cobrar = ctk.CTkButton(
            cobrar_frame,
            text="Cobrar (F1)",
            width=220,
            height=110,
            fg_color="green",
            font=("Segoe UI", 18, "bold"),
            command=self.cobrar
        )
        btn_cobrar.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.botones = {"Cobrar (F1)": btn_cobrar}
        
        BOTONES = [
            ("Eliminar (Del)", self.eliminar, None),
            ("Nuevo (F2)", self.nuevo, "red"),
            ("Tarjeta (F3)", self.pago_tarjeta, None),
            ("Efectivo (F4)", self.pago_efectivo, None),
            ]
        filas = []

        for i, (texto, comando, color) in enumerate(BOTONES):

            # Crear un frame nuevo cada 2 botones
            if i % 2 == 0:
                fila = ctk.CTkFrame(self.footer, fg_color="transparent")
                fila.pack(side="top", anchor="e", pady=3)
                filas.append(fila)

            btn = ctk.CTkButton(
                fila,
                text=texto,
                width=140,
                height=42,
                fg_color=color,
                command=comando
            )

            btn.pack(side="left", padx=5, pady=5)
            self.botones[texto] = btn

