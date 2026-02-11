# main_window.py
import customtkinter as ctk
from tkinter import messagebox
from CTkMessagebox import CTkMessagebox
from modulos.UI_ventas import UIVentas
from modulos.UI_inventario import UIInventario

class MainWindow(ctk.CTk):
    """
    Ventana principal simplificada:
    - Uso exclusivo de pack.
    - Pestañas instanciadas perezosamente.
    - Botón 'Salir' fijo abajo.
    - Emojis como iconos de texto en botones del menú.
    """

    def __init__(self):
        super().__init__()
        self.title("Sistema De Facturacion E Inventario A&L")
        self.geometry("1000x600")
        self.resizable(False, False)

        # Estructuras
        self._frames = {}        # frame por pestaña
        self._instances = {}     # instancia del módulo por pestaña
        self._buttons = {}       # botones del menú
        self._active = None

        # Config: (nombre, clase, emoji)
        self._tabs = [
            ("Ventas", UIVentas, "🧾"),
            ("Inventario", UIInventario, "📦"),
            ("Productos", None, "📋"),
            ("Corte", None, "✂️"),
            ("Reportes", None, "📊"),
            ("Configuracion", None, "⚙️"),
        ]

        self._build_ui()
        self.show_tab("Ventas")

    # -----------------------
    # Construcción UI
    # -----------------------
    def _build_ui(self):
        root = ctk.CTkFrame(self, fg_color="transparent")
        root.pack(fill="both", expand=True, padx=6, pady=6)

        menu = ctk.CTkFrame(root, border_width=1, border_color="gray")
        menu.pack(side="left", fill="y")

        content = ctk.CTkFrame(root, border_width=1, border_color="gray")
        content.pack(side="right", fill="both", expand=True)

        self._menu = menu
        self._content = content

        # Logo
        ctk.CTkLabel(menu, text="A&L", font=("Arial", 18, "bold")).pack(pady=(12,6), padx=8)

        # Crear botones y frames (no instanciamos módulos aún)
        for name, cls, emoji in self._tabs:
            text = f"{emoji}  {name}"
            btn = ctk.CTkButton(menu, text=text, width=160, anchor="w",
                                command=lambda n=name: self.show_tab(n))
            btn.pack(pady=6, padx=8, fill="x")
            self._buttons[name] = btn

            frame = ctk.CTkFrame(self._content, fg_color="transparent")
            self._frames[name] = frame
            self._instances[name] = None

        # Separador
        ctk.CTkFrame(menu, height=1, fg_color="gray").pack(fill="x", padx=8, pady=(6,6))

        # Dark mode switch (above exit)
        ctk.CTkSwitch(menu, text="🌙 Modo Oscuro", command=self._toggle_dark).pack(side="bottom", pady=(60,6), padx=8)

        # Salir fijo abajo
        btn_exit = ctk.CTkButton(menu, text="⏻  Salir", fg_color="#b22222", hover_color="#a11a1a", command=self._on_exit)
        btn_exit.pack(side="bottom", pady=12, padx=8, fill="x")
        self._buttons["Salir"] = btn_exit

        # Atajos
        self.bind_all("<Control-q>", lambda e: self._on_exit())

    # -----------------------
    # Acciones globales
    # -----------------------
    def _toggle_dark(self):
        ctk.set_appearance_mode("Light" if ctk.get_appearance_mode() == "Dark" else "Dark")


    def _on_exit(self, event=None):
        """
        Confirmación de salida y cierre seguro de la ventana principal.
        Acepta un event opcional para poder enlazar con bind_all.
        """
        # askyesno devuelve True si el usuario confirma
        if messagebox.askyesno("Salir", "¿Deseas salir de la aplicación?"):
            try:
                # Primero intentamos salir del mainloop (seguro)
                self.quit()
            except Exception:
                pass
            try:
                # Luego destruimos la ventana y todos sus widgets
                self.destroy()
            except Exception:
                # En casos extremos forzamos cierre del toplevel
                try:
                    self.winfo_toplevel().destroy()
                except Exception:
                    pass

    # -----------------------
    # Gestión de pestañas (lazy load)
    # -----------------------
    def show_tab(self, name):
        # Manejo especial Salir
        if name == "Salir":
            self._on_exit()
            return

        # Ocultar todos los frames
        for f in self._frames.values():
            f.pack_forget()

        # Reactivar botón anterior y restaurar estilo
        if self._active:
            prev = self._buttons.get(self._active)
            if prev:
                prev.configure(state="normal")
                try:
                    prev.configure(fg_color=None, text_color=None)
                except Exception:
                    pass

        # Instanciar módulo si aplica (lazy)
        cls = {n: c for n, c, _ in self._tabs}.get(name)
        if cls is not None and self._instances.get(name) is None:
            try:
                self._instances[name] = cls(self._frames[name])
            except Exception as e:
                CTkMessagebox(title="Error", message=f"No se pudo cargar {name}:\n{e}", icon="cancel", option_1="OK")
                self._instances[name] = None

        # Mostrar frame
        frame = self._frames[name]
        frame.pack(fill="both", expand=True)

        # Desactivar y marcar botón actual
        btn = self._buttons.get(name)
        if btn:
            btn.configure(state="disabled")
            try:
                btn.configure(fg_color="#2c3e50", text_color="white")
            except Exception:
                pass

        self._active = name

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
