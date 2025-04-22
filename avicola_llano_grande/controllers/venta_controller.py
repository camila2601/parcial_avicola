# controllers/venta_controller.py
from db import stock_collection
from datetime import datetime

def realizar_venta(data):
    tipo = data.get('tipo')
    tamano = data.get('tamano')
    cliente = data.get('cliente')  # NATURAL o JURIDICO
    cantidad = int(data.get('cantidad'))

    if cliente == "NATURAL":
        huevos_por_unidad = 12
        precio_unitario = 5000
        iva_porcentaje = 0
    else:
        huevos_por_unidad = 30
        precio_unitario = 12000
        iva_porcentaje = 0.19

    huevos_necesarios = cantidad * huevos_por_unidad
    filtro = {'tipo': tipo, 'tamano': tamano}
    stock = stock_collection.find_one(filtro)

    if not stock or stock['cantidad'] < huevos_necesarios:
        return None, "No hay suficiente stock para esta venta."

    # Calcular precios
    subtotal = cantidad * precio_unitario
    iva = int(subtotal * iva_porcentaje)
    total = subtotal + iva

    # Actualizar stock
    nuevo_stock = stock['cantidad'] - huevos_necesarios
    stock_collection.update_one(filtro, {'$set': {'cantidad': nuevo_stock}})

    # Generar factura .txt
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"factura_{fecha}.txt"
    with open(nombre_archivo, 'w') as f:
        f.write("╔══════════════════════════════════════╗\n")
        f.write("║      AVÍCOLA LLANO GRANDE S.A.S      ║\n")
        f.write("╠══════════════════════════════════════╣\n")
        f.write(f"║ Fecha: {fecha:<30}║\n")
        f.write(f"║ Cliente: {cliente:<29}║\n")
        f.write(f"║ Tipo: {tipo:<33}║\n")
        f.write(f"║ Tamaño: {tamano:<31}║\n")
        f.write(f"║ Cantidad: {cantidad} ({huevos_necesarios} huevos)       ║\n")
        f.write("╠══════════════════════════════════════╣\n")
        f.write(f"║ Subtotal: ${subtotal:<24}║\n")
        f.write(f"║ IVA: ${iva:<30}║\n")
        f.write(f"║ TOTAL: ${total:<27}║\n")
        f.write("╚══════════════════════════════════════╝\n")

    return nombre_archivo, "Venta realizada con éxito. Factura generada."
