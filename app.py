# app.py
import sys
import io
from flask import Flask, render_template, request, redirect, url_for, flash
from avicola_llano_grande.controllers.stock_controller import registrar_huevos, obtener_stock
from avicola_llano_grande.controllers.venta_controller import realizar_venta
from db import stock_collection

# Configurar la codificación predeterminada como UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__, template_folder='avicola_llano_grande/templates')
app.secret_key = 'clave_secreta_para_flask'  # Necesaria para usar mensajes flash

# Prueba de conexión a la base de datos al iniciar la aplicación
try:
    stock_collection.find_one()
    print("Conexión a la base de datos exitosa.")
except Exception as e:
    print(f"Error al conectar con la base de datos: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        data = request.form
        mensaje = registrar_huevos(data)
        flash(mensaje)
        return redirect(url_for('registro'))
    return render_template('registro.html')

@app.route('/venta', methods=['GET', 'POST'])
def venta():
    mensaje = None
    archivo = None
    try:
        if request.method == 'POST':
            data = request.form
            archivo, mensaje = realizar_venta(data)
            flash(mensaje)
    except Exception as e:
        print(f"Error en la ruta /venta: {e}")
        flash("Ocurrió un error al procesar la venta.")
    return render_template('venta.html', mensaje=mensaje, archivo=archivo)

@app.route('/stock')
def ver_stock():
    stock = obtener_stock()
    return render_template('stock.html', stock=stock)

if __name__ == '__main__':
    app.run(debug=True)
