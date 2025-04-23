# app.py
import sys
import io
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
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
    archivo_pdf = None
    archivo_txt = None
    try:
        if request.method == 'POST':
            data = request.form
            archivo_pdf, archivo_txt, mensaje = realizar_venta(data)  # Retorna ambos archivos
            flash(mensaje)
    except Exception as e:
        print(f"Error en la ruta /venta: {e}")
        flash("Ocurrió un error al procesar la venta.")
    return render_template('venta.html', mensaje=mensaje, archivo_pdf=archivo_pdf, archivo_txt=archivo_txt)

@app.route('/stock')
def ver_stock():
    stock = obtener_stock()
    return render_template('stock.html', stock=stock)

@app.route('/factura/<nombre>')
def descargar_factura(nombre):
    try:
        # Asegúrate de que el archivo exista en la carpeta 'facturas'
        return send_file(f"facturas/{nombre}", as_attachment=False)  # Cambia `as_attachment` a `False` para verlo en el navegador
    except FileNotFoundError:
        flash("El archivo solicitado no existe.")
        return redirect(url_for('venta'))

if __name__ == '__main__':
    app.run(debug=True)
