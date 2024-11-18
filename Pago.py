from datetime import datetime
from Cliente import GestionClientes, Cliente 
import json

class Pago:
    def __init__(self, cliente, monto, moneda, tipo_pago, fecha):
        self.cliente = cliente
        self.monto = monto
        self.moneda = moneda
        self.tipo_pago = tipo_pago
        self.fecha = fecha

    def __str__(self):
        # Verificar si el cliente es jurídico y mostrar su razón social, ya que no poseen nombre ni apellido porque es una empresa
        if hasattr(self.cliente, 'razon_social') and self.cliente.razon_social:
            cliente_info = self.cliente.razon_social
        else:
            cliente_info = f"{self.cliente.nombre} {self.cliente.apellido}"

        return (f"Cliente: {cliente_info}\n"
                f"Monto: {self.monto} {self.moneda}\n"
                f"Tipo de Pago: {self.tipo_pago}\n"
                f"Fecha: {self.fecha.strftime('%Y-%m-%d')}")
    
class GestionPagos:
    def __init__(self, archivo='pagos.json'):
        self.pagos = []
        self.archivo = archivo
        self.cargar_pagos()

    def cargar_pagos(self):
        """Carga los pagos desde el archivo JSON al iniciar la clase."""
        try:
            with open(self.archivo, 'r') as f:
                pagos_data = json.load(f)
                for pago_data in pagos_data:
                    cliente_data = pago_data.get('cliente', {})
                    # Verifica que las claves necesarias existan
                    if 'nombre' in cliente_data and 'apellido' in cliente_data and 'cedula_rif' in cliente_data:
                        cliente = Cliente(
                            nombre=cliente_data['nombre'],
                            apellido=cliente_data['apellido'],
                            cedula_rif=cliente_data['cedula_rif'],
                            correo_electronico=cliente_data.get('correo_electronico', ''),
                            direccion_envio=cliente_data.get('direccion_envio', ''),
                            telefono=cliente_data.get('telefono', '')
                        )
                    else:
                        print("Datos del cliente incompletos. Se omitirá este pago.")
                        continue  # Salta este pago si faltan datos del cliente

                    monto = pago_data.get('monto', 0)
                    moneda = pago_data.get('moneda', 'No especificado')
                    tipo_pago = pago_data.get('tipo_pago', 'No especificado')
                    fecha_str = pago_data.get('fecha', None)

                    if fecha_str:
                        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
                    else:
                        print("Fecha no válida. Se omitirá este pago.")
                        continue

                    self.pagos.append(Pago(cliente, monto, moneda, tipo_pago, fecha))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al cargar los pagos: {e}")
            self.pagos = []  

    def guardar_pagos(self):
        #Guarda los pagos en el archivo JSON
        pagos_data = []
        for pago in self.pagos:
            cliente_data = {
                'cedula_rif': pago.cliente.cedula_rif,
                'correo_electronico': pago.cliente.correo_electronico,
                'direccion_envio': pago.cliente.direccion_envio,
                'telefono': pago.cliente.telefono
            }
        
           
            if hasattr(pago.cliente, 'razon_social') and pago.cliente.razon_social:
                cliente_data['razon_social'] = pago.cliente.razon_social
            else:
                cliente_data['nombre'] = pago.cliente.nombre
                cliente_data['apellido'] = pago.cliente.apellido
        
            pagos_data.append({
                'cliente': cliente_data,
                'monto': pago.monto, 
                'moneda': pago.moneda,
                'tipo_pago': pago.tipo_pago,
                'fecha': pago.fecha.strftime('%Y-%m-%d')
            })
    
        with open(self.archivo, 'w') as f:
            json.dump(pagos_data, f, indent=4)

    def registrar_pago(self, cliente):
        monto = float(input("Ingrese el monto del pago: "))
        moneda = input("Ingrese la moneda del pago (Bolivares/Divisas): ").strip().lower()

        # Selección del tipo de pago según la moneda
        if moneda == "bolivares":
            print("Seleccione el tipo de pago:")
            print("1. Punto de venta")
            print("2. Pago móvil")
            print("3. Transferencia")
            tipo_pago_opcion = input("Seleccione una opción (1/2/3): ")
            if tipo_pago_opcion == "1":
                tipo_pago = "Punto de venta"
            elif tipo_pago_opcion == "2":
                tipo_pago = "Pago móvil"
            elif tipo_pago_opcion == "3":
                tipo_pago = "Transferencia"
            else:
                print("Opción no válida. Se registrará como 'No especificado'.")
                tipo_pago = "No especificado"
        elif moneda == "divisas":
            print("Seleccione el tipo de pago:")
            print("1. Zelle")
            print("2. PayPal")
            print("3. Efectivo")
            tipo_pago_opcion = input("Seleccione una opción (1/2/3): ")
            if tipo_pago_opcion == "1":
                tipo_pago = "Zelle"
            elif tipo_pago_opcion == "2":
                tipo_pago = "PayPal"
            elif tipo_pago_opcion == "3":
                tipo_pago = "Efectivo"
            else:
                print("Opción no válida. Se registrará como 'No especificado'.")
                tipo_pago = "No especificado"
        else:
            print("Moneda no válida. Se registrará como 'No especificado'")
            tipo_pago = "No especificado"

        fecha_str = input("Ingrese la fecha del pago (YYYY-MM-DD): ")
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')

        pago = Pago(cliente, monto, moneda, tipo_pago, fecha)
        self.pagos.append(pago)
        self.guardar_pagos()  # Guardar el pago en el archivo JSON
        print("Pago registrado exitosamente.")

    def eliminar_pago(self):
        """Elimina un pago específico basado en la fecha y el monto."""
        fecha_str = input("Ingrese la fecha del pago a eliminar (YYYY-MM-DD): ")
        monto = float(input("Ingrese el monto del pago a eliminar: "))
        
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        pago_a_eliminar = None
        
        for pago in self.pagos:
            if pago.fecha.date() == fecha.date() and pago.monto == monto:
                pago_a_eliminar = pago
                break
        
        if pago_a_eliminar:
            self.pagos.remove(pago_a_eliminar)
            self.guardar_pagos()  # Guardar los cambios en el archivo JSON
            print("Pago eliminado exitosamente.")
        else:
            print("No se encontró un pago con la fecha y monto especificados.")

    def buscar_pagos(self, cliente=None, fecha=None, tipo_pago=None, moneda=None):
        resultados = []
        for pago in self.pagos:
            if (cliente is None or pago.cliente == cliente) and \
               (fecha is None or pago.fecha.date() == fecha) and \
               (tipo_pago is None or pago.tipo_pago.lower() == tipo_pago.lower()) and \
               (moneda is None or pago.moneda.lower() == moneda.lower()):
                resultados.append(pago)
        return resultados

    def mostrar_pagos(self):
        if not self.pagos:
            print("No hay pagos registrados.")
        else:
            for pago in self.pagos:
                print(pago)
                print("-" * 30)

# Menu de pagos
def menu_gestion_pagos(gestion_pagos, gestion_clientes):
    while True:
        print("\n1. Registrar pago")
        print("2. Buscar pagos")
        print("3. Mostrar todos los pagos")
        print("4. Eliminar pago")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            cedula_rif = input("Ingrese la cédula o RIF del cliente que realizó el pago: ")
            cliente = gestion_clientes.buscar_cliente(cedula_rif)
            if cliente:
                gestion_pagos.registrar_pago(cliente)
            else:
                print("Cliente no encontrado.")
        elif opcion == "2":
            print("Filtros de búsqueda:")
            cliente_rif = input("Ingrese la cédula o RIF del cliente (deje vacío para omitir): ")
            fecha_str = input("Ingrese la fecha del pago (YYYY-MM-DD) (deje vacío para omitir): ")
            tipo_pago = input("Ingrese el tipo de pago (deje vacío para omitir): ")
            moneda = input("Ingrese la moneda del pago (deje vacío para omitir): ")

            cliente = gestion_clientes.buscar_cliente(cliente_rif) if cliente_rif else None
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date() if fecha_str else None
            
            resultados = gestion_pagos.buscar_pagos(cliente, fecha, tipo_pago, moneda)
            if resultados:
                for pago in resultados:
                    print(pago)
                    print("-" * 30)
            else:
                print("No se encontraron pagos que coincidan con los criterios de búsqueda.")
        elif opcion == "3":
            gestion_pagos.mostrar_pagos()
        elif opcion == "4":
            gestion_pagos.eliminar_pago() 
        elif opcion == "5":
            print("Gracias por usar el sistema de gestión de pagos.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")


if __name__ == "__main__":
    gestion_clientes = GestionClientes()  
    gestion_pagos = GestionPagos()  

    menu_gestion_pagos(gestion_pagos, gestion_clientes)