# controllers/stock_controller.py
from db import stock_collection

def registrar_huevos(data):
    tipo = data.get('tipo')        # ROJO o BLANCO
    tamano = data.get('tamano')    # A, AA, B, EXTRA
    cubetas = int(data.get('cubetas'))

    if cubetas <= 0:
        return "La cantidad de cubetas debe ser mayor que cero."

    unidades = cubetas * 30  # Cada cubeta tiene 30 huevos

    # Buscar si ya existe ese tipo y tamaño en stock
    filtro = {'tipo': tipo, 'tamano': tamano}
    existente = stock_collection.find_one(filtro)

    if existente:
        # Si existe, actualizamos la cantidad
        nueva_cantidad = existente['cantidad'] + unidades
        stock_collection.update_one(filtro, {'$set': {'cantidad': nueva_cantidad}})
        return f"Stock actualizado: ahora hay {nueva_cantidad} huevos de tipo {tipo} tamaño {tamano}."
    else:
        # Si no existe, lo insertamos
        nuevo_registro = {
            'tipo': tipo,
            'tamano': tamano,
            'cantidad': unidades
        }
        stock_collection.insert_one(nuevo_registro)
        return f"Nuevo registro agregado: {unidades} huevos de tipo {tipo} tamaño {tamano}."
def obtener_stock():
    stock = list(stock_collection.find({}, {'_id': 0}))  # Excluye el campo '_id'
    return stock
