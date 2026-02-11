from pathlib import Path
import json

class Inventario:
    def __init__(self):
        self.productos = {}
        self.cargar_inventario()

    def agregar_producto(self, producto_id, producto_nombre, cantidad, precio):
        if producto_id in self.productos:
            self.productos[producto_id]['cantidad'] += cantidad
            self.productos[producto_id]['precio'] = precio
        else:
            self.productos[producto_id] = {
                'nombre': producto_nombre,
                'cantidad': cantidad,
                'precio': precio
            }
        self.guardar_inventario()
    
    def eliminar_producto(self, producto_id, cantidad=None):
        if producto_id in self.productos:
            if cantidad is None or self.productos[producto_id]['cantidad'] <= cantidad:
                del self.productos[producto_id]
            else:
                self.productos[producto_id]['cantidad'] -= cantidad
            self.guardar_inventario()

    def cargar_inventario(self):
        ruta = Path('data/inventario.json')
        if not ruta.exists():
            return
        try:
            with open(ruta, 'r') as f:
                self.productos = json.load(f)
        except Exception:
            pass

    def guardar_inventario(self):
        try:
            Path('data').mkdir(exist_ok=True)
            with open('data/inventario.json', 'w') as f:
                json.dump(self.productos, f, indent=4)
        except Exception:
            pass
