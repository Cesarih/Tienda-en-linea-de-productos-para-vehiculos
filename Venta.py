from datetime import datetime
import json
from Cliente import ClienteJuridico, Cliente, GestionClientes
from Producto import GestionProductos
from Envio import GestionEnvios

class Venta:
    def __init__(self, cliente, productos, cantidades, metodo_pago, tipo_moneda, tipo_credito=None, fecha=None):
        self.cliente = cliente
        self.productos = productos
        self.cantidades = cantidades
        self.metodo_pago = metodo_pago
        self.tipo_moneda = tipo_moneda
        self.tipo_credito = tipo_credito  # Puede ser 'contado' o 'credito'
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d")  # Usar la fecha proporcionada o la actual
        self.factura = self.generar_factura()

    def calcular_totales(self):
        subtotal = sum(p.price * c for p, c in zip(self.productos, self.cantidades))
        descuento = 0

        # Aplicar descuento del 5% si es cliente jurídico y paga de contado
        if isinstance(self.cliente, ClienteJuridico) and self.tipo_credito == 'contado':
            descuento = subtotal * 0.05

        subtotal -= descuento
        iva = subtotal * 0.16

        # Aplicar IGTF solo si el método de pago es en divisas
        if self.tipo_moneda == 'divisas' and self.metodo_pago in ['zelle', 'paypal', 'efectivo']:
            igtf = subtotal * 0.03
        else:
            igtf = 0

        total = subtotal + iva + igtf

        return {
            'subtotal': subtotal,
            'descuentos': descuento,
            'iva': iva,
            'igtf': igtf,
            'total': total
        }

    def generar_factura(self):
        totales = self.calcular_totales()
        factura = {
            'cliente': {
                'razon_social' if isinstance(self.cliente, ClienteJuridico) else 'nombre': self.cliente.razon_social if isinstance(self.cliente, ClienteJuridico) else self.cliente.nombre,
                'cedula_rif': self.cliente.cedula_rif,
                'tipo': self.cliente.__class__.__name__
            },
            'productos': [(p.name, c) for p, c in zip(self.productos, self.cantidades)],
            'metodo_pago': self.metodo_pago,
            'tipo_moneda': self.tipo_moneda,
            'tipo_credito': self.tipo_credito,
            'fecha': self.fecha,
            'totales': totales  #ESTO DE LOS TOTALES ES LA SUMA DEL IVA, IGTF, DESCUENTO, ETC.... QUE TERMINA DANTO EL PRECIO TOTAL.
        }
        return factura

class SistemaVentas:
    def __init__(self, gestion_clientes, gestion_productos, gestion_envios):
        self.gestion_clientes = gestion_clientes
        self.gestion_productos = gestion_productos
        self.gestion_envios = gestion_envios
        self.ventas = []
        self.archivo_ventas = 'ventas.json'
        self.cargar_ventas()

    def cargar_ventas(self):
        try:
            with open(self.archivo_ventas, 'r', encoding='utf-8') as f:
                ventas_data = json.load(f)
                for venta_data in ventas_data:
                    if venta_data['cliente']['tipo'] == 'ClienteJuridico':
                        cliente = ClienteJuridico(
                            razon_social=venta_data['cliente']['razon_social'],
                            cedula_rif=venta_data['cliente']['cedula_rif'],
                            correo_electronico=venta_data['cliente'].get('correo_electronico', None),
                            direccion_envio=venta_data['cliente'].get('direccion_envio', None),
                            telefono=venta_data['cliente'].get('telefono', None),
                            nombre_contacto=venta_data['cliente'].get('nombre_contacto', None),
                            telefono_contacto=venta_data['cliente'].get('telefono_contacto', None),
                            correo_contacto=venta_data['cliente'].get('correo_contacto', None)
                        )
                    else:
                        cliente = Cliente(
                            nombre=venta_data['cliente']['nombre'],
                            apellido=venta_data['cliente']['apellido'],
                            cedula_rif=venta_data['cliente']['cedula_rif'],
                            correo_electronico=venta_data['cliente'].get('correo_electronico', None),
                            direccion_envio=venta_data['cliente'].get('direccion_envio', None),
                            telefono=venta_data['cliente'].get('telefono', None)
                        )
                
                    # Crear la venta
                    productos = []
                    cantidades = []
                
                    for producto_data in venta_data['productos']:
                        nombre_producto = producto_data[0]
                        cantidad = producto_data[1]
                    
                        # Buscar el objeto del producto en el sistema
                        producto = self.gestion_productos.buscar_producto(nombre_producto)
                        if producto is not None:
                            productos.append(producto)  # Agregar el objeto del producto
                            cantidades.append(cantidad)  # Agregar la cantidad
                        else:
                            print(f"Producto no encontrado: {nombre_producto}")

                    # Crear la venta solo si se encontraron todos los productos
                    if len(productos) == len(venta_data['productos']):
                        venta = Venta(
                            cliente,
                            productos,
                            cantidades,
                            venta_data['metodo_pago'],
                            venta_data['tipo_moneda'],
                            venta_data.get('tipo_credito', None),
                            fecha=venta_data['fecha']
                        )
                        self.ventas.append(venta.factura)
                    else:
                        print(f"Venta no registrada debido a productos no encontrados para el cliente: {cliente.cedula_rif}")
        except FileNotFoundError:
            print("No se encontró el archivo de ventas. Se creará uno nuevo.")
        except json.JSONDecodeError:
            print("Error al decodificar el archivo de ventas. Asegúrese de que el formato sea correcto.")
        except Exception as e:
            print(f"Error al cargar ventas: {e}")

    def guardar_ventas(self):
        try:
            with open(self.archivo_ventas, 'w', encoding='utf-8') as f:
                json.dump(self.ventas, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar ventas: {e}")

    def registrar_venta(self):
        print("Registro de Venta")
        cedula_rif = input("Ingrese la cédula o RIF del cliente: ")
        cliente = self.gestion_clientes.buscar_cliente(cedula_rif)

        if not cliente:
            print("Cliente no encontrado.")
            return

        productos = []
        cantidades = []
        while True:
            nombre_producto = input("Ingrese el nombre del producto (o 'fin' para terminar): ")
            if nombre_producto.lower() == 'fin':
                break
            producto = self.gestion_productos.buscar_producto(nombre_producto)
            if not producto:
                print("Producto no encontrado.")
                continue
            cantidad = int(input(f"Ingrese la cantidad de {producto.name}: "))
            productos.append(producto)
            cantidades.append(cantidad)

        # Selección de tipo de moneda
        tipo_moneda = input("Seleccione el tipo de moneda (1) Divisas (2) Bolívares: ")
        if tipo_moneda == '1':
            tipo_moneda = 'divisas'
            metodo_pago = input("Seleccione el método de pago (efectivo, zelle, paypal): ")
        elif tipo_moneda == '2':
            tipo_moneda = 'bolivares'
            metodo_pago = input("Ingrese el método de pago (punto de venta, pago móvil, transferencia): ")
        else:
            print("Opción no válida.")
            return

        # Determinar si el cliente es jurídico o natural
        tipo_credito = None
        if isinstance(cliente, ClienteJuridico):
            tipo_credito = input("Seleccione el tipo de pago (1) Contado (2) Crédito: ")
            if tipo_credito == '1':
                tipo_credito = 'contado'
            elif tipo_credito == '2':
                tipo_credito = 'credito'
            else:
                print("Opción no válida.")
                return
        elif isinstance(cliente, Cliente):  # Cliente natural
            tipo_credito = 'contado'  # Solo puede pagar al contado

        # Crear la venta
        venta = Venta(cliente, productos, cantidades, metodo_pago, tipo_moneda, tipo_credito)
        self.ventas.append(venta.factura)  # Agregar la factura de la venta a la lista de ventas

        # Guardar las ventas en el archivo JSON
        self.guardar_ventas()

        # Registrar el envío
        self.gestion_envios.registrar_envio()

        # Mostrar la factura generada
        print("Factura generada:")
        print(json.dumps(venta.factura, indent=4, ensure_ascii=False))

    def ver_ventas(self):
        if not self.ventas:
            print("No hay ventas registradas.")
            return
        
        print("Ventas registradas:")
        for i, venta in enumerate(self.ventas, start=1):
            print(f"\nVenta {i}:")
            print(json.dumps(venta, indent=4, ensure_ascii=False))

    def buscar_ventas(self):
        criterio = input("Buscar por (1) Cliente o (2) Fecha: ")
        if criterio == '1':
            cedula_rif = input("Ingrese la cédula o RIF del cliente: ")
            ventas_encontradas = [venta for venta in self.ventas if venta['cliente']['cedula_rif'] == cedula_rif]
            if not ventas_encontradas:
                print("No se encontraron ventas para el cliente especificado.")
            else:
                for venta in ventas_encontradas:
                    print(json.dumps(venta, indent=4, ensure_ascii=False))
        
        elif criterio == '2':
            fecha_str = input("Ingrese la fecha de la venta (YYYY-MM-DD): ")
            ventas_encontradas = [venta for venta in self.ventas if venta['fecha'] == fecha_str]
            if not ventas_encontradas:
                print("No se encontraron ventas para la fecha especificada.")
            else:
                for venta in ventas_encontradas:
                    print(json.dumps(venta, indent=4, ensure_ascii=False))
        else:
            print("Opción no válida.")

    def eliminar_venta(self):
        self.ver_ventas()
        indice = int(input("Ingrese el número de la venta que desea eliminar: ")) - 1
        if 0 <= indice < len(self.ventas):
            venta_eliminada = self.ventas.pop(indice)
            self.guardar_ventas()  
            print("Venta eliminada exitosamente.")
            print(f"Venta eliminada: {json.dumps(venta_eliminada, indent=4, ensure_ascii=False)}")
        else:
            print("Número de venta no válido.")

#Menu de ventas
def menu_sistema_ventas(sistema_ventas):
    while True:
        print("\nSistema de Ventas") 
        print("1. Registrar Venta")
        print("2. Ver Ventas")
        print("3. Buscar Ventas")
        print("4. Eliminar Venta") 
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            sistema_ventas.registrar_venta()
        elif opcion == "2":
            sistema_ventas.ver_ventas()
        elif opcion == "3":
            sistema_ventas.buscar_ventas()
        elif opcion == "4":
            sistema_ventas.eliminar_venta() 
        elif opcion == "5":
            print("Gracias por usar el sistema de ventas.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    gestion_clientes = GestionClientes()
    gestion_productos = GestionProductos()
    gestion_envios = GestionEnvios()
    
    sistema_ventas = SistemaVentas(gestion_clientes, gestion_productos, gestion_envios)

    menu_sistema_ventas(sistema_ventas)