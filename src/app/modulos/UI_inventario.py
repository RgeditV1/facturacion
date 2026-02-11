import customtkinter as ctk
from .core.inventario import Inventario
from tkinter import ttk
from CTkMessagebox import CTkMessagebox

class UIInventario:
    def __init__(self, frame):
        self.main_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=1, pady=1)
        self.inventario = Inventario()
        self.draw_ui()

    def show_info(self, text):
        pass
    def show_warning(self, text):
        CTkMessagebox(title="Error", message=text,
                          icon="warning", option_1="!ok")
    def show_error(self, text):
        pass

    def buscar_producto(self, event=None):
        query = self.entry_busqueda.get().strip()
        if not query: #query == ""
            self.show_warning("Barra de busqueda vacia")
            return
        for item in self.tabla.get_children():
            valores = self.tabla.item(item, "values")
            if query.lower() in str(valores[0]).lower() or query.lower() in str(valores[1]).lower():
                self.tabla.selection_set(item)
                self.tabla.see(item)
                break

    def agregar_producto(self):
        producto_id = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        precio = self.entry_precio.get().strip()

        if not producto_id or not nombre:
            self.show_warning("Debe ingresar un nombre e ID")
            return
        if not cantidad.isdigit():
            self.show_warning("La cantidad debe ser un número")
            return

        # Si el producto ya existe en inventario y tiene precio, lo usamos
        if producto_id in self.inventario.productos and precio.strip() == "":
            precio_final = self.inventario.productos[producto_id]["precio"]
        else:
            precio_final = float(precio)
            if not precio.replace('.', '', 1).isdigit():
                self.show_warning("Debe ingresar un precio válido para productos nuevos")
                return
            precio_final = float(precio)

        # Guardar en inventario
        self.inventario.agregar_producto(producto_id, nombre, int(cantidad), precio_final)
        self.actualizar_tabla()

        # Limpiar los entrys después de agregar
        self.entry_id.delete(0, "end")
        self.entry_nombre.delete(0, "end")
        self.entry_cantidad.delete(0, "end")
        self.entry_precio.delete(0, "end")


    def borrar_producto(self, event=None):
        seleccion = self.tabla.selection()
        for item in seleccion:
            valores = self.tabla.item(item, "values")
            producto_id = valores[0]
            self.inventario.eliminar_producto(producto_id)
        self.actualizar_tabla()

    def draw_ui(self):
        self.header()
        self.crear_tabla()
        self.actualizar_tabla()

    def header(self):
        header_frame = ctk.CTkFrame(self.main_frame, height=50, fg_color="#2c3e50")
        header_frame.pack(fill="x", padx=10, pady=10)
        header_label = ctk.CTkLabel(header_frame, text="Inventario", font=("Arial", 24), text_color="white")
        header_label.pack(pady=(2,2))

        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.pack(fill="x", padx=10, pady=10)

        # ID
        ctk.CTkLabel(form_frame, text="ID").grid(row=0, column=0, padx=(0,5), pady=5, sticky="e")
        self.entry_id = ctk.CTkEntry(form_frame, width=120)
        self.entry_id.grid(row=0, column=1, padx=(0,10), pady=5, sticky="w")

        # Nombre (más ancho)
        ctk.CTkLabel(form_frame, text="Nombre").grid(row=0, column=2, padx=(0,5), pady=5, sticky="e")
        self.entry_nombre = ctk.CTkEntry(form_frame, width=300)   # ✅ más ancho
        self.entry_nombre.grid(row=0, column=3, padx=(0,10), pady=5, sticky="w")

        # Cantidad
        ctk.CTkLabel(form_frame, text="Cantidad").grid(row=1, column=0, padx=(0,5), pady=5, sticky="e")
        self.entry_cantidad = ctk.CTkEntry(form_frame, width=120)
        self.entry_cantidad.grid(row=1, column=1, padx=(0,10), pady=5, sticky="w")

        # Precio
        ctk.CTkLabel(form_frame, text="Precio").grid(row=1, column=2, padx=(0,5), pady=5, sticky="e")
        self.entry_precio = ctk.CTkEntry(form_frame, width=120)
        self.entry_precio.grid(row=1, column=3, padx=(0,10), pady=5, sticky="w")

        # Barra de búsqueda
        self.entry_busqueda = ctk.CTkEntry(form_frame, placeholder_text="Buscar por ID o Nombre", width=250)
        self.entry_busqueda.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.entry_busqueda.bind("<Return>", self.buscar_producto)
        
        # Frame para los botones
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky="w")

        # Botón Buscar
        self.btn_buscar = ctk.CTkButton(buttons_frame, text="Buscar", command=self.buscar_producto, width=80)
        self.btn_buscar.pack(side="left", padx=5)

        # Botón Agregar
        self.btn_agregar = ctk.CTkButton(buttons_frame, text="Agregar", command=self.agregar_producto, width=80)
        self.btn_agregar.pack(side="left", padx=5)

        # Botón Borrar
        self.btn_borrar = ctk.CTkButton(buttons_frame, text="Borrar", command=self.borrar_producto, width=80)
        self.btn_borrar.pack(side="left", padx=5)



    def crear_tabla(self):
        columnas = ("ID", "Descripción", "Cantidad", "Precio")
        self.tabla = ttk.Treeview(self.main_frame, columns=columnas, show="headings")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        for col in columnas:
            self.tabla.heading(col, text=col, command=lambda c=col: self.ordenar_por(c, False))
            self.tabla.column(col, width=120)

        # Atajo de teclado para borrar con Supr
        self.tabla.bind("<Delete>", self.borrar_producto)
        self.tabla.bind("<BackSpace>", self.borrar_producto)

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for producto_id, datos in self.inventario.productos.items():
            cantidad_fmt = f"{datos['cantidad']:,}"          # separador de miles
            precio_fmt = f"{datos['precio']:,.2f}"           # separador de miles y 2 decimales
            self.tabla.insert("", "end", values=(producto_id, datos['nombre'], cantidad_fmt, precio_fmt))

    def ordenar_por(self, col, descendente):
        datos = [(self.tabla.set(k, col), k) for k in self.tabla.get_children("")]
        if col in ("Cantidad", "Precio"):
            datos = [(float(valor), k) for valor, k in datos]
        datos.sort(reverse=descendente)
        for index, (val, k) in enumerate(datos):
            self.tabla.move(k, "", index)
        self.tabla.heading(col, command=lambda: self.ordenar_por(col, not descendente))
