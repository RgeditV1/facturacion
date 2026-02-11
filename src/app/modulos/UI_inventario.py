# ui_inventario.py
import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from .core.inventario import Inventario  # Asegúrate de que la ruta sea correcta

class UIInventario:
    def __init__(self, frame):
        # Frame principal donde se dibuja todo
        self.main_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=1, pady=1)

        self.inventario = Inventario()
        self.entries = {}  # diccionario para referencias a Entry por nombre
        self._sort_column = None
        self._sort_desc = False

        # Scrollbars (se crean en crear_tabla)
        self._v_scroll = None
        self._h_scroll = None

        self._draw_ui()

    # -----------------------
    # Mensajería
    # -----------------------
    def show_info(self, text):
        CTkMessagebox(title="Info", message=text, icon="info", option_1="OK")

    def show_warning(self, text):
        CTkMessagebox(title="Atención", message=text, icon="warning", option_1="OK")

    def show_error(self, text):
        CTkMessagebox(title="Error", message=text, icon="cancel", option_1="OK")

    # -----------------------
    # Utilidades de parsing
    # -----------------------
    def _parse_number_flexible(self, s):
        """
        Convierte una cadena numérica que puede usar '.' o ',' como separadores de miles
        y ',' o '.' como separador decimal, a float.
        Devuelve float o None si no es convertible.
        """
        if s is None:
            return None
        s = str(s).strip().replace(" ", "")
        if s == "":
            return None

        allowed = set("0123456789.,-")
        if any(ch not in allowed for ch in s):
            return None

        negative = False
        if s.startswith("-"):
            negative = True
            s = s[1:]

        if "." in s and "," in s:
            last_dot = s.rfind(".")
            last_comma = s.rfind(",")
            if last_comma > last_dot:
                s = s.replace(".", "")
                s = s.replace(",", ".")
            else:
                s = s.replace(",", "")
        else:
            if "," in s:
                if s.count(",") > 1:
                    s = s.replace(",", "")
                else:
                    parts = s.split(",")
                    if len(parts[1]) == 3:
                        s = s.replace(",", "")
                    else:
                        s = s.replace(",", ".")
            elif "." in s:
                if s.count(".") > 1:
                    s = s.replace(".", "")
                else:
                    parts = s.split(".")
                    if len(parts[1]) == 3:
                        s = s.replace(".", "")

        try:
            val = float(s)
            return -val if negative else val
        except ValueError:
            return None

    # -----------------------
    # Búsqueda
    # -----------------------
    def buscar_producto(self, event=None):
        query = self.entry_busqueda.get().strip()
        if not query:
            self.show_warning("Barra de búsqueda vacía")
            return
        for item in self.tabla.get_children():
            valores = self.tabla.item(item, "values")
            if query.lower() in str(valores[0]).lower() or query.lower() in str(valores[1]).lower():
                self.tabla.selection_set(item)
                self.tabla.see(item)
                return
        self.show_info("No se encontró ningún producto con esa búsqueda")

    # -----------------------
    # Agregar / Borrar
    # -----------------------
    def agregar_producto(self):
        producto_id = self.entries['ID'].get().strip()
        nombre = self.entries['Nombre'].get().strip()
        cantidad_raw = self.entries['Cantidad'].get().strip()
        precio_raw = self.entries['Precio'].get().strip()
        precio_costo_raw = self.entries['Precio costo'].get().strip()
        precio_mayoreo_raw = self.entries['Precio mayoreo'].get().strip()

        if not producto_id or not nombre:
            self.show_warning("Debe ingresar un ID y un Nombre")
            return

        if not cantidad_raw.isdigit():
            self.show_warning("La cantidad debe ser un número entero")
            return
        cantidad = int(cantidad_raw)

        precio = self._parse_number_flexible(precio_raw)
        precio_costo = self._parse_number_flexible(precio_costo_raw)
        precio_mayoreo = self._parse_number_flexible(precio_mayoreo_raw)

        # Si el producto ya existe y no se ingresó precio nuevo, conservar el anterior
        if producto_id in self.inventario.productos and precio is None:
            precio_final = self.inventario.productos[producto_id].get("precio", 0.0)
        else:
            if precio is None:
                self.show_warning("Debe ingresar un precio válido para productos nuevos o dejar vacío para conservar el precio existente")
                return
            precio_final = precio

        # Llamada a Inventario con los campos de precio de compra y mayoreo
        self.inventario.agregar_producto(
            producto_id,
            nombre,
            cantidad,
            precio_final,
            precio_compra=precio_costo,
            precio_mayoreo=precio_mayoreo
        )

        self.actualizar_tabla()

        # Limpiar los entrys después de agregar
        for key in ("ID", "Nombre", "Cantidad", "Precio", "Precio costo", "Precio mayoreo"):
            self.entries[key].delete(0, "end")

        self.show_info("Producto agregado/actualizado correctamente")

    def borrar_producto(self, event=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            self.show_warning("No hay productos seleccionados para borrar")
            return
        for item in seleccion:
            valores = self.tabla.item(item, "values")
            producto_id = valores[0]
            self.inventario.eliminar_producto(producto_id)
        self.actualizar_tabla()
        self.show_info("Producto(s) eliminado(s)")

    # -----------------------
    # UI: dibujado
    # -----------------------
    def _draw_ui(self):
        self.header()
        self.crear_tabla()
        self.actualizar_tabla()

    def header(self):
        # Encabezado
        header_frame = ctk.CTkFrame(self.main_frame, height=50, fg_color="#2c3e50")
        header_frame.pack(fill="x", padx=10, pady=10)
        header_label = ctk.CTkLabel(header_frame, text="Inventario", font=("Arial", 24), text_color="white")
        header_label.pack(pady=(2,2))

        # Frame principal del formulario
        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.pack(fill="x", padx=10, pady=10)

        # --- Fila 1: ID y Nombre (definidos explícitamente porque Nombre es más ancho) ---
        row1 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row1.pack(fill="x", pady=5)

        ctk.CTkLabel(row1, text="ID", width=100).pack(side="left", padx=(0,5))
        self.entries['ID'] = ctk.CTkEntry(row1, width=120)
        self.entries['ID'].pack(side="left", padx=(0,15))

        ctk.CTkLabel(row1, text="Nombre", width=100).pack(side="left", padx=(0,5))
        self.entries['Nombre'] = ctk.CTkEntry(row1, width=300)
        self.entries['Nombre'].pack(side="left", padx=(0,15))

        # --- Filas siguientes: dos campos por fila generados con un for ---
        campos = [
            ("Cantidad", 120),
            ("Precio", 120),
            ("Precio costo", 120),
            ("Precio mayoreo", 120),
        ]

        for i in range(0, len(campos), 2):
            row = ctk.CTkFrame(form_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)

            label_text, entry_width = campos[i]
            ctk.CTkLabel(row, text=label_text, width=100).pack(side="left", padx=(0,5))
            entry = ctk.CTkEntry(row, width=entry_width)
            entry.pack(side="left", padx=(0,15))
            self.entries[label_text] = entry

            if i + 1 < len(campos):
                label_text2, entry_width2 = campos[i + 1]
                ctk.CTkLabel(row, text=label_text2, width=100).pack(side="left", padx=(20,5))
                entry2 = ctk.CTkEntry(row, width=entry_width2)
                entry2.pack(side="left", padx=(0,15))
                self.entries[label_text2] = entry2

        # --- Fila de búsqueda y botones ---
        row3 = ctk.CTkFrame(form_frame, fg_color="transparent")
        row3.pack(fill="x", pady=10)

        self.entry_busqueda = ctk.CTkEntry(row3, placeholder_text="Buscar por ID o Nombre", width=250)
        self.entry_busqueda.pack(side="left", padx=(0,15))
        self.entry_busqueda.bind("<Return>", self.buscar_producto)

        self.btn_buscar = ctk.CTkButton(row3, text="Buscar", command=self.buscar_producto, width=80)
        self.btn_buscar.pack(side="left", padx=5)

        self.btn_agregar = ctk.CTkButton(row3, text="Agregar", command=self.agregar_producto, width=80)
        self.btn_agregar.pack(side="left", padx=5)

        self.btn_borrar = ctk.CTkButton(row3, text="Borrar", command=self.borrar_producto, width=80)
        self.btn_borrar.pack(side="left", padx=5)

    # -----------------------
    # Tabla y scrollbars dinámicas
    # -----------------------
    def crear_tabla(self):
        columnas = ("ID", "Descripción", "Cantidad", "Precio", "Precio costo", "Precio mayoreo")
        tabla_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")
        self.tabla.pack(fill="both", expand=True, side="top")

        # Guardamos estado de orden
        self._sort_column = None
        self._sort_desc = False

        def make_heading(col, text, width, anchor="w"):
            self.tabla.heading(col, text=text, command=lambda c=col: self.ordenar_por(c, None))
            self.tabla.column(col, width=width, anchor=anchor)

        make_heading("ID", "ID", 100, anchor="center")
        make_heading("Descripción", "Descripción", 260, anchor="w")
        make_heading("Cantidad", "Cantidad", 100, anchor="center")
        make_heading("Precio", "Precio", 120, anchor="e")
        make_heading("Precio costo", "Precio costo", 120, anchor="e")
        make_heading("Precio mayoreo", "Precio mayoreo", 140, anchor="e")

        # Scrollbars (creadas pero no empaquetadas hasta que se necesiten)
        self._v_scroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self._h_scroll = ttk.Scrollbar(tabla_frame, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=self._v_scroll.set, xscrollcommand=self._h_scroll.set)

        # Bind para actualizar scrollbars al redimensionar
        self.tabla.bind("<Configure>", lambda e: self._update_scrollbars_visibility())
        # Atajos de teclado para borrar
        self.tabla.bind("<Delete>", self.borrar_producto)
        self.tabla.bind("<BackSpace>", self.borrar_producto)

    def _update_scrollbars_visibility(self):
        """
        Muestra u oculta las scrollbars según si el contenido excede el área visible.
        """
        self.tabla.update_idletasks()

        items = self.tabla.get_children()
        # Si no hay items, ocultar ambas
        if not items:
            if self._v_scroll.winfo_ismapped():
                self._v_scroll.pack_forget()
            if self._h_scroll.winfo_ismapped():
                self._h_scroll.pack_forget()
            return

        # Vertical: comprobamos si el último item queda fuera del área visible
        last_item = items[-1]
        bbox = self.tabla.bbox(last_item)
        need_v = False
        if bbox:
            x, y, w, h = bbox
            if y + h > self.tabla.winfo_height():
                need_v = True
        else:
            need_v = True

        # Horizontal: sumamos anchos de columnas y comparamos con ancho visible
        total_col_width = sum(self.tabla.column(c, option="width") for c in self.tabla["columns"])
        need_h = total_col_width > self.tabla.winfo_width()

        # Mostrar u ocultar vertical
        if need_v:
            if not self._v_scroll.winfo_ismapped():
                self._v_scroll.pack(side="right", fill="y")
        else:
            if self._v_scroll.winfo_ismapped():
                self._v_scroll.pack_forget()

        # Mostrar u ocultar horizontal
        if need_h:
            if not self._h_scroll.winfo_ismapped():
                self._h_scroll.pack(side="bottom", fill="x")
        else:
            if self._h_scroll.winfo_ismapped():
                self._h_scroll.pack_forget()

    # -----------------------
    # Actualizar tabla (preserva orden actual)
    # -----------------------
    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for producto_id, datos in self.inventario.productos.items():
            cantidad_val = datos.get('cantidad', 0)
            precio_val = datos.get('precio', 0.0)
            precio_costo_val = datos.get('precio_costo', None)
            precio_mayoreo_val = datos.get('precio_mayoreo', None)

            cantidad_fmt = f"{int(cantidad_val):,}"
            precio_fmt = f"{float(precio_val):,.2f}" if precio_val is not None else ""
            precio_costo_fmt = f"{float(precio_costo_val):,.2f}" if precio_costo_val is not None else ""
            precio_mayoreo_fmt = f"{float(precio_mayoreo_val):,.2f}" if precio_mayoreo_val is not None else ""

            self.tabla.insert("", "end", values=(
                producto_id,
                datos.get('nombre', ''),
                cantidad_fmt,
                precio_fmt,
                precio_costo_fmt,
                precio_mayoreo_fmt
            ))

        # Actualizamos geometría y scrollbars
        self.tabla.update_idletasks()
        self._update_scrollbars_visibility()

        # Reaplicar orden si ya había una columna ordenada
        if self._sort_column:
            # Llamamos a ordenar_por con descendente actual para reaplicar
            self.ordenar_por(self._sort_column, self._sort_desc)

    # -----------------------
    # Ordenamiento con icono
    # -----------------------
    def ordenar_por(self, col, descendente=None):
        numeric_cols = {"Cantidad", "Precio", "Precio costo", "Precio mayoreo"}

        if descendente is None:
            if self._sort_column == col:
                self._sort_desc = not self._sort_desc
            else:
                self._sort_column = col
                self._sort_desc = False
        else:
            self._sort_column = col
            self._sort_desc = descendente

        items = self.tabla.get_children("")
        datos = []
        for k in items:
            raw = self.tabla.set(k, col)
            if col in numeric_cols:
                def safe_float(v):
                    try:
                        s = str(v).strip().replace(" ", "").replace("$", "").replace("€", "")
                        s = s.replace(",", "")
                        return float(s) if s != "" else 0.0
                    except Exception:
                        return 0.0
                key = safe_float(raw)
            else:
                key = str(raw).lower()
            datos.append((key, k))

        datos.sort(reverse=self._sort_desc, key=lambda x: x[0])

        for index, (_, k) in enumerate(datos):
            self.tabla.move(k, "", index)

        # Actualizar encabezados: limpiar y poner flecha en la activa
        for col_name in self.tabla["columns"]:
            base_text = col_name
            self.tabla.heading(col_name, text=base_text, command=lambda c=col_name: self.ordenar_por(c, None))

        arrow = " ▼" if self._sort_desc else " ▲"
        active_text = self._sort_column + arrow
        self.tabla.heading(self._sort_column, text=active_text, command=lambda c=self._sort_column: self.ordenar_por(c, None))
