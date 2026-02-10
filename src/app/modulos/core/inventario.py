from pathlib import Path
import json

class Inventario:
    def __init__(self):
        self.productos = {}
        # Intentamos cargar los datos en cuanto se crea la instancia
        self.cargar_inventario()

    def agregar_producto(self, producto_id, producto_nombre, cantidad):
        if producto_id in self.productos:
            self.productos[producto_id]['cantidad'] += cantidad
        else:
            self.productos[producto_id] = {'nombre': producto_nombre, 'cantidad': cantidad}
        # Guardamos automáticamente tras cambios
        self.guardar_inventario()
    
    def eliminar_producto(self, producto_id, cantidad=None):
        if producto_id in self.productos:
            if cantidad is None or self.productos[producto_id]['cantidad'] <= cantidad:
                del self.productos[producto_id]
            else:
                self.productos[producto_id]['cantidad'] -= cantidad
            self.guardar_inventario()
        else:
            print(f"Producto con ID {producto_id} no encontrado.")

    def cargar_inventario(self):
        ruta = Path('data/inventario.json')
        if not ruta.exists():
            return # Si no existe, self.productos se queda vacío

        try:
            with open(ruta, 'r') as f:
                self.productos = json.load(f)
            print("Inventario cargado con éxito.")
        except Exception as e:
            print(f"Error al cargar: {e}")

    def guardar_inventario(self):
        try:
            Path('data').mkdir(exist_ok=True)
            # USAMOS 'w' para sobrescribir el archivo con la versión más reciente del diccionario
            with open('data/inventario.json', 'w') as f:
                json.dump(self.productos, f, indent=4)
        except Exception as e:
            print(f"Error al guardar: {e}")