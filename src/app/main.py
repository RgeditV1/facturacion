import customtkinter as ctk
from modulos.UI_ventas import UIVentas

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema De Facturacion E Inventario A&L")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.draw_ui()

    def draw_ui(self):
        root = ctk.CTkFrame(self, fg_color="transparent")
        root.pack(pady=2, padx=2, fill="both", expand=True)

        menu_frame = ctk.CTkFrame(root, border_width=1, border_color="gray")
        menu_frame.pack(side="left", fill="y")

        content_frame = ctk.CTkFrame(root, border_width=1, border_color="gray")
        content_frame.pack(side="right", fill="both", expand=True)

        self.pestañas = {}
        self.botones = {}
        self.boton_activo = None
        
        # Lista de tuplas: (nombre, módulo/clase o None)
        pestañas_config = [
            ("Ventas", UIVentas),
            ("Inventario", None),  # Cambiar None por tu clase cuando la tengas
            ("Productos", None),
            ("Corte", None),
            ("Reportes", None),
            ("Configuracion", None),
            ("Salir", None)
        ]

        # Crear botones y frames dinámicamente
        for nombre, modulo_clase in pestañas_config:
            btn = ctk.CTkButton(
                menu_frame,
                text=nombre,
                command=lambda n=nombre: self.mostrar_pestaña(n)
            )
            btn.pack(pady=10, padx=10, fill="x")
            self.botones[nombre] = btn

            # Crear frame para la pestaña
            frame = ctk.CTkFrame(content_frame)
            self.pestañas[nombre] = frame
            
            # Instanciar el módulo si existe
            if modulo_clase is not None and nombre != "Salir":
                modulo_clase(frame)

        self.mostrar_pestaña("Ventas")


        #Switch modo Oscuro
        switch = ctk.CTkSwitch(menu_frame, text="🌙 Modo Oscuro", command=self.toggle_dark_mode)
        switch.pack(side="bottom", pady=10, padx=10)


    def toggle_dark_mode(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    def mostrar_pestaña(self, nombre):
        if nombre == "Salir":
            self.destroy()
            return

        # Ocultar todas las pestañas
        for frame in self.pestañas.values():
            frame.pack_forget()

        # Reactivar botón anterior
        if self.boton_activo:
            self.botones[self.boton_activo].configure(state="normal")

        # Mostrar pestaña actual
        self.pestañas[nombre].pack(fill="both", expand=True)

        # Desactivar botón actual
        self.botones[nombre].configure(state="disabled")
        self.boton_activo = nombre


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
