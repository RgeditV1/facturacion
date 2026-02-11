# core/inventario.py
from pathlib import Path
import json

class Inventario:
    """
    Clase simple para manejar inventario en memoria y persistir en JSON.
    Claves internas usadas:
      - 'nombre'
      - 'cantidad'
      - 'precio'           (precio de venta unitario)
      - 'precio_costo'     (precio de compra)
      - 'precio_mayoreo'   (precio al por mayor)
    """

    def __init__(self, ruta_datos: str = "data/inventario.json"):
        self.productos = {}
        self.ruta = Path(ruta_datos)
        self.cargar_inventario()

    def agregar_producto(self, producto_id, producto_nombre,
                         cantidad, precio, precio_compra=None,
                         precio_mayoreo=None):
        """
        Agrega o actualiza un producto.
        - Si existe, suma la cantidad y actualiza precios si se proporcionan (None = no cambiar).
        - Si no existe, crea la entrada con los valores dados (si precio_compra o precio_mayoreo son None, se guardan como None).
        """
        if producto_id in self.productos:
            p = self.productos[producto_id]
            p['cantidad'] = p.get('cantidad', 0) + int(cantidad)
            # Actualizar precio de venta si se proporcionó (puede ser 0.0)
            if precio is not None:
                p['precio'] = float(precio)
            # Actualizar precio de compra si se proporcionó (None = no cambiar)
            if precio_compra is not None:
                p['precio_costo'] = float(precio_compra)
            # Actualizar precio mayoreo si se proporcionó
            if precio_mayoreo is not None:
                p['precio_mayoreo'] = float(precio_mayoreo)
        else:
            self.productos[producto_id] = {
                'nombre': producto_nombre,
                'cantidad': int(cantidad),
                'precio': float(precio) if precio is not None else 0.0,
                'precio_costo': float(precio_compra) if precio_compra is not None else None,
                'precio_mayoreo': float(precio_mayoreo) if precio_mayoreo is not None else None
            }
        self.guardar_inventario()

    def eliminar_producto(self, producto_id, cantidad=None):
        """
        Si cantidad es None o >= cantidad actual, elimina el producto.
        Si cantidad es menor, resta la cantidad.
        """
        if producto_id in self.productos:
            if cantidad is None or self.productos[producto_id]['cantidad'] <= cantidad:
                del self.productos[producto_id]
            else:
                self.productos[producto_id]['cantidad'] -= int(cantidad)
            self.guardar_inventario()

    def cargar_inventario(self):
        if not self.ruta.exists():
            return
        try:
            with open(self.ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Asegurar tipos correctos y nombres de claves (compatibilidad con versiones previas)
                normalized = {}
                for pid, d in data.items():
                    normalized[pid] = {
                        'nombre': d.get('nombre', ''),
                        'cantidad': int(d.get('cantidad', 0)),
                        # soportar claves antiguas 'precio de compra' / 'precio al por mayor'
                        'precio': float(d.get('precio', d.get('precio', 0.0))),
                        'precio_costo': (float(d.get('precio_costo')) if d.get('precio_costo') is not None
                                         else (float(d.get('precio de compra')) if d.get('precio de compra') is not None else None)),
                        'precio_mayoreo': (float(d.get('precio_mayoreo')) if d.get('precio_mayoreo') is not None
                                           else (float(d.get('precio al por mayor')) if d.get('precio al por mayor') is not None else None))
                    }
                self.productos = normalized
        except Exception:
            # Si falla la carga, dejamos productos vacío (no interrumpir la UI)
            self.productos = {}

    def guardar_inventario(self):
        try:
            self.ruta.parent.mkdir(parents=True, exist_ok=True)
            with open(self.ruta, 'w', encoding='utf-8') as f:
                json.dump(self.productos, f, indent=4, ensure_ascii=False)
        except Exception:
            # No interrumpir la aplicación si falla el guardado
            pass
