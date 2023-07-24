import os
import qrcode
import random
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def generar_codigo_rastreo():
    return str(random.randint(1000000, 9999999))

nombre_cliente = input("Ingrese el nombre del cliente: ")
direccion_cliente = input("Ingrese la direccion del cliente: ")
correo_cliente = input("Ingrese el correo del cliente: ")

productos = []
while True:
    nombre_producto = input("Ingrese el nombre del producto o fin para terminar ")
    if nombre_producto.lower() == 'fin':
        break

    cantidad = int(input(f"Ingrese la cantidad de '{nombre_producto}': "))
    precio_unitario = float(input(f"Ingrese el precio unitario de '{nombre_producto}': "))

    costo_producto = cantidad * precio_unitario
    productos.append((nombre_producto, cantidad, precio_unitario, costo_producto))

total_costo = sum(costo_producto for _, _, _, costo_producto in productos)


fecha_actual = datetime.now()
fecha_entrega = fecha_actual + timedelta(days=5)

codigo_rastreo = generar_codigo_rastreo()

informacion_qr = f"Código de Rastreo: {codigo_rastreo}\nFecha de Entrega: {fecha_entrega.strftime('%Y-%m-%d')}"
qr_code = qrcode.make(informacion_qr)

ruta_guardado = "C:/Users/Lenovo/Desktop/ticket_1/"
if not os.path.exists(ruta_guardado):
    os.makedirs(ruta_guardado)

nombre_imagen = os.path.join(ruta_guardado, "miQr.png")
qr_code.save(nombre_imagen)

nombre_pdf = os.path.join(ruta_guardado, "ticket_compra.pdf")
c = canvas.Canvas(nombre_pdf + 'examen.pdf', pagesize=A4)

c.setFont('Helvetica-Bold', 18)
c.drawString(210, 740, "Datos del Cliente ")
c.setFont('Helvetica', 14)
c.drawString(70,720,"-------------------------------------------------------------------------------------------")
c.drawString(50, 700, "NOMBRE: ")
c.drawString(400, 700, f" {nombre_cliente}")
c.drawString(50, 680, "DIRECCION: ")
c.drawString(400, 680, f" {direccion_cliente}")
c.drawString(50, 660, "CORREO ELECTRONICO: ")
c.drawString(400, 660, f" {correo_cliente}")

c.drawString(400,800, "Comprobante de pago")
c.drawString(400,780, f"{codigo_rastreo}")


ruta_imagen = "C:/Users/Lenovo/Desktop/ticket_1/logo_mp.png"

x = 0
y = 750

ancho_imagen = 200 
alto_imagen = 100

c.drawImage(ruta_imagen, x,y, ancho_imagen, alto_imagen)

c.setFont('Helvetica-Bold',18)
c.drawString(190,600, "Datos de los productos ")
c.setFont('Helvetica', 14)
c.drawString(70,580,"-------------------------------------------------------------------------------------------")

y_pos = 560

for nombre_producto,cantidad, precio_unitario,costo_producto in productos:
    
    c.drawString(50, y_pos, f"NOMBRE PRODUCTO: {nombre_producto}")
    c.drawString(400, y_pos, f"CANTIDAD: {cantidad}")
    c.drawString(50, y_pos - 20, f"PRECIO UNITARIO: ${precio_unitario:.2f}")
    c.drawString(400, y_pos - 20, f"COSTO: ${costo_producto:.2f}")
    y_pos -= 50

c.setFont('Helvetica-Bold', 14)
c.drawString(50, y_pos - 30, "Costo total: ")

c.setFont('Helvetica', 14)
c.drawString(400, y_pos - 30, f"${total_costo:.2f}")

x_qr = A4[0] / 2 - qr_code.size[0]/6
y_qr = y_pos -200

c.drawImage(nombre_imagen, x_qr, y_qr, qr_code.size[0]/3, qr_code.size[1]/3)
c.save()

print("archivos generados y guardados en: ",ruta_guardado)