from db import stock_collection
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def realizar_venta(data):
    tipo = data.get('tipo')  # ROJO o BLANCO
    tamano = data.get('tamano')  # A, AA, B, EXTRA
    cliente = data.get('cliente')  # NATURAL o JURIDICO
    unidad = data.get('unidad')  # DOCENA o CUBETA
    cantidad = int(data.get('cantidad'))

    # Tabla de precios por cubeta
    precios_cubeta = {
        "ROJO": {
            "A": 12000,
            "AA": 13500,
            "B": 11000,
            "EXTRA": 15000
        },
        "BLANCO": {
            "A": 10000,
            "AA": 11500,
            "B": 9500,
            "EXTRA": 14000
        }
    }

    # Verificar si el tipo y tamaño son válidos
    if tipo not in precios_cubeta or tamano not in precios_cubeta[tipo]:
        return None, "Tipo o tamaño de huevo inválido."

    # Obtener el precio unitario según la tabla
    precio_unitario = precios_cubeta[tipo][tamano]

    # Ajustar el precio si es por docena
    if unidad == "DOCENA":
        precio_unitario = precio_unitario // 2  # La docena es la mitad del precio de la cubeta

    # Calcular huevos necesarios
    huevos_por_unidad = 12 if unidad == "DOCENA" else 30
    huevos_necesarios = cantidad * huevos_por_unidad

    # Verificar stock
    filtro = {'tipo': tipo, 'tamano': tamano}
    stock = stock_collection.find_one(filtro)

    if not stock or stock['cantidad'] < huevos_necesarios:
        return None, "No hay suficiente stock para esta venta."

    # Calcular precios
    subtotal = cantidad * precio_unitario
    iva_porcentaje = 0.19 if cliente == "JURIDICO" else 0
    iva = int(subtotal * iva_porcentaje)
    total = subtotal + iva

    # Actualizar stock
    nuevo_stock = stock['cantidad'] - huevos_necesarios
    stock_collection.update_one(filtro, {'$set': {'cantidad': nuevo_stock}})

    # Crear carpeta 'facturas' si no existe
    if not os.path.exists('facturas'):
        os.makedirs('facturas')

    # Generar nombres de archivos
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_txt = f"facturas/factura_{fecha}.txt"
    nombre_pdf = f"facturas/factura_{fecha}.pdf"

    # Factura en TXT
    with open(nombre_txt, 'w', encoding='utf-8') as f:
        f.write("AVÍCOLA LLANO GRANDE S.A.S\n")
        f.write("Factura de venta\n")
        f.write(f"Fecha: {fecha}\n")
        f.write(f"Cliente: {cliente}\n")
        f.write(f"Tipo de huevo: {tipo}\n")
        f.write(f"Tamaño: {tamano}\n")
        f.write(f"Unidad: {unidad}\n")
        f.write(f"Cantidad: {cantidad} ({huevos_necesarios} huevos)\n")
        f.write(f"Subtotal: ${subtotal}\n")
        f.write(f"IVA: ${iva}\n")
        f.write(f"TOTAL: ${total}\n")
        f.write("\n")
        f.write("     (\\_/)\n")
        f.write("    ( 'x' )\n")
        f.write("    c(\")_(\")\n")
        f.write("     /   \\\n")
        f.write("    /     \\\n")
        f.write("   (       )\n")
        f.write("    \\_____/\n")

    # Factura en PDF
    c = canvas.Canvas(nombre_pdf, pagesize=letter)
    text = c.beginText(50, 750)
    text.setFont("Helvetica", 12)
    text.textLine("AVÍCOLA LLANO GRANDE S.A.S")
    text.textLine("Factura de venta")
    text.textLine(f"Fecha: {fecha}")
    text.textLine(f"Cliente: {cliente}")
    text.textLine(f"Tipo de huevo: {tipo}")
    text.textLine(f"Tamaño: {tamano}")
    text.textLine(f"Unidad: {unidad}")
    text.textLine(f"Cantidad: {cantidad} ({huevos_necesarios} huevos)")
    text.textLine(f"Subtotal: ${subtotal}")
    text.textLine(f"IVA: ${iva}")
    text.textLine(f"TOTAL: ${total}")
    c.drawText(text)
    c.save()

    return f"factura_{fecha}.pdf", f"factura_{fecha}.txt", "Venta realizada con éxito. Factura generada en PDF y TXT."
