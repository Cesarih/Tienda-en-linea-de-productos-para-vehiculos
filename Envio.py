import json
from datetime import datetime
from Cliente import GestionClientes

class Envio:
    def __init__(self, orden_compra, servicio_envio, motorizado, costo, fecha):
        self.orden_compra = orden_compra
        self.servicio_envio = servicio_envio
        self.motorizado = motorizado  # Puede ser None si no es delivery por moto
        self.costo = costo
        self.fecha = fecha

    def __str__(self):
        motorizado_info = f"\nMotorizado: {self.motorizado}" if self.motorizado else "\nMotorizado: No aplica"
        return (f"Orden de Compra: {self.orden_compra}\n"
                f"Servicio de Envío: {self.servicio_envio}\n"
                f"{motorizado_info}\n"
                f"Costo del Servicio: {self.costo}\n"
                f"Fecha: {self.fecha.strftime('%Y-%m-%d')}")

class GestionEnvios:
    def __init__(self, archivo='envios.json'):
        self.envios = []
        self.archivo = archivo
        self.cargar_envios()

    def cargar_envios(self):
        """Carga los envíos desde el archivo JSON al iniciar la clase."""
        try:
            with open(self.archivo, 'r') as f:
                self.envios = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.envios = []  # Si el archivo no existe o está vacío, se inicializa una lista vacía

    def guardar_envios(self):
        """Guarda los envíos en el archivo JSON."""
        with open(self.archivo, 'w') as f:
            json.dump(self.envios, f, default=str, indent=4)

    def registrar_envio(self):
        orden_compra = input("Ingrese el número de orden de compra: ")
        servicio_envio = input("Ingrese el servicio de envío (e.g. Zoom, Delivery por moto): ")
        
        motorizado = None
        if "delivery" in servicio_envio.lower():
            nombre_motorizado = input("Ingrese el nombre del motorizado: ")
            telefono_motorizado = input("Ingrese el teléfono del motorizado: ")
            motorizado = {'nombre': nombre_motorizado, 'telefono': telefono_motorizado}

        costo = float(input("Ingrese el costo del servicio: "))
        fecha_str = input("Ingrese la fecha del envío (YYYY-MM-DD): ")
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')

        envio = {
            'orden_compra': orden_compra,
            'servicio_envio': servicio_envio,
            'motorizado': motorizado,
            'costo': costo,
            'fecha': fecha.strftime('%Y-%m-%d')
        }
        
        self.envios.append(envio)
        self.guardar_envios()  # Guardar en el archivo JSON
        print("Envío registrado exitosamente.")

    def eliminar_envio(self):
        if not self.envios:
            print("No hay envíos registrados para eliminar.")
            return
        
        self.mostrar_envios()  # Muestra los envíos para que el usuario elija
        try:
            indice = int(input("Ingrese el número del envío que desea eliminar: ")) - 1
            
            if 0 <= indice < len(self.envios):
                envio_eliminado = self.envios.pop(indice)
                self.guardar_envios()  # Guarda los cambios en el archivo
                print("Envío eliminado exitosamente.")
                print(f"Envío eliminado: {envio_eliminado}")
            else:
                print("Número de envío no válido.")
        except ValueError:
            print("Entrada no válida. Debe ingresar un número.")

    def buscar_envios(self, cliente=None, fecha=None):
        resultados = []
        for envio in self.envios:
            if (cliente is None or envio['orden_compra'] == cliente.cedula_rif) and \
               (fecha is None or datetime.strptime(envio['fecha'], '%Y-%m-%d').date() == fecha):
                resultados.append(envio)
        return resultados

    def mostrar_envios(self):
        if not self.envios:
            print("No hay envíos registrados.")
        else:
            for i, envio in enumerate(self.envios, start=1):
                print(f"Envío {i}:")
                print(envio)
                print("-" * 30)

# Menu de envios
def menu_gestion_envios(gestion_envios, gestion_clientes):
    while True:
        print("\n--Gestion de Envíos--")
        print("1. Registrar envío")
        print("2. Buscar envíos")
        print("3. Mostrar todos los envíos")
        print("4. Eliminar envío")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            gestion_envios.registrar_envio()
        elif opcion == "2":
            print("Filtros de búsqueda:")
            cliente_rif = input("Ingrese la cédula o RIF del cliente (deje vacío para omitir): ")
            fecha_str = input("Ingrese la fecha del envío (YYYY-MM-DD) (deje vacío para omitir): ")

            cliente = gestion_clientes.buscar_cliente(cliente_rif) if cliente_rif else None
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date() if fecha_str else None
            
            resultados = gestion_envios.buscar_envios(cliente, fecha)
            if resultados:
                for envio in resultados:
                    print(envio)
                    print("-" * 30)
            else:
                print("No se encontraron envíos que coincidan con los criterios de búsqueda.")
        elif opcion == "3":
            gestion_envios.mostrar_envios()
        elif opcion == "4":
            gestion_envios.eliminar_envio()
        elif opcion == "5":
            print("Gracias por usar el sistema de gestión de envíos.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    gestion_clientes = GestionClientes() 
    gestion_envios = GestionEnvios()

    menu_gestion_envios(gestion_envios, gestion_clientes)