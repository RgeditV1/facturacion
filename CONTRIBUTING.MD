# Contributing

Gracias por tu interés en contribuir a este sistema de facturación POS.

El objetivo es mantener un código **claro, modular y fácil de mantener**.

---

## Reglas generales

* Mantén el código simple y legible
* No mezclar lógica de negocio con la interfaz gráfica
* Sigue la estructura del proyecto
* Un cambio por commit

---

## Convenciones del proyecto

### Nombres de archivos

* Interfaces gráficas: `UI_<modulo>.py`
* Lógica de negocio: dentro de `core/`

Ejemplos:

* `UI_ventas.py`
* `ventas_logic.py`

---

### Separación de responsabilidades

**UI**

* Botones
* Layout
* Eventos

**Core**

* Cálculos
* Validaciones
* Reglas de negocio

La UI **no debe** contener lógica compleja.

---

## Estilo de código

* Usar snake_case
* Evitar duplicación de código
* Preferir diccionarios de configuración
* Comentarios claros cuando sea necesario

---

## Commits

Formato recomendado:

```text
feat: agregar validación de stock
fix: corregir cálculo de total
refactor: separar lógica de ventas
```

---

## Pull Requests

Antes de enviar un PR:

1. Verifica que el código funciona
2. Asegúrate de no romper la UI existente
3. Explica claramente el cambio

---

## Reporte de errores

Incluye:

* Descripción clara del problema
* Pasos para reproducirlo
* Mensaje de error si existe

---

## Filosofía del proyecto

Este POS prioriza:

* Claridad sobre complejidad
* Mantenimiento a largo plazo
* Evolución progresiva

Gracias por contribuir.
