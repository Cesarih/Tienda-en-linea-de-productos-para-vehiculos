import json

class Cliente:
    def __init__(self, nombre, apellido, cedula_rif, correo_electronico, direccion_envio, telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula_rif = cedula_rif
        self.correo_electronico = correo_electronico
        self.direccion_envio = direccion_envio
        self.telefono = telefono

    def show(self):
        return f"Nombre: {self.nombre} {self.apellido}\nCédula/RIF: {self.cedula_rif}\nCorreo electrónico: {self.correo_electronico}\nDirección de envío: {self.direccion_envio}\nTeléfono: {self.telefono}"

class ClienteJuridico(Cliente):
    def __init__(self, razon_social, cedula_rif, correo_electronico, direccion_envio, telefono, nombre_contacto, telefono_contacto, correo_contacto):
        super().__init__("", "", cedula_rif, correo_electronico, direccion_envio, telefono)
        self.razon_social = razon_social
        self.nombre_contacto = nombre_contacto
        self.telefono_contacto = telefono_contacto
        self.correo_contacto = correo_contacto

    def show(self):
        return f"Razón Social: {self.razon_social}\nCédula/RIF: {self.cedula_rif}\nCorreo electrónico: {self.correo_electronico}\nDirección de envío: {self.direccion_envio}\nTeléfono: {self.telefono}\nNombre de contacto: {self.nombre_contacto}\nTeléfono de contacto: {self.telefono_contacto}\nCorreo de contacto: {self.correo_contacto}"

class GestionClientes:
    def __init__(self):
        self.clientes = []
        self.cargar_clientes()  # Cargar clientes al iniciar

    def registrar_cliente(self):
        tipo_cliente = input("Ingrese el tipo de cliente (Natural/Jurídico): ").lower()
        if tipo_cliente == "natural":
            nombre = input("Ingrese el nombre del cliente: ")
            apellido = input("Ingrese el apellido del cliente: ")
            cedula_rif = input("Ingrese la cédula o RIF del cliente: ")
            correo_electronico = input("Ingrese el correo electrónico del cliente: ")
            direccion_envio = input("Ingrese la dirección de envío del cliente: ")
            telefono = input("Ingrese el número de teléfono del cliente: ")
            
            cliente = Cliente(nombre, apellido, cedula_rif, correo_electronico, direccion_envio, telefono)
            self.clientes.append(cliente)
            self.guardar_clientes()  # Guardar clientes naturales después de registrar
            print("Cliente natural registrado exitosamente.")
        
        elif tipo_cliente == "jurídico":
            razon_social = input("Ingrese la razón social de la empresa: ")
            cedula_rif = input("Ingrese el RIF de la empresa: ")
            correo_electronico = input("Ingrese el correo electrónico de la empresa: ")
            direccion_envio = input("Ingrese la dirección de envío de la empresa: ")
            telefono = input("Ingrese el número de teléfono de la empresa: ")
            nombre_contacto = input("Ingrese el nombre del contacto: ")
            telefono_contacto = input("Ingrese el teléfono del contacto: ")
            correo_contacto = input("Ingrese el correo electrónico del contacto: ")
            
            cliente = ClienteJuridico(razon_social, cedula_rif, correo_electronico, direccion_envio, telefono, nombre_contacto, telefono_contacto, correo_contacto)
            self.clientes.append(cliente)
            self.guardar_clientes()  # Guardar clientes juridicos después de registrar
            print("Cliente jurídico registrado exitosamente.")
        
        else:
            print("Tipo de cliente no válido. Por favor, ingrese 'Natural' o 'Jurídico'.")

    def buscar_cliente(self, cedula_rif=None, correo_electronico=None):
        for cliente in self.clientes:
            if cliente.cedula_rif == cedula_rif or cliente.correo_electronico == correo_electronico:
                return cliente
        return None

    def mostrar_clientes(self):
        if not self.clientes:
            print("No hay clientes registrados.")
        else:
            for cliente in self.clientes:
                print(cliente.show())
                print("-" * 30)

    def editar_cliente(self, cedula_rif):
        cliente = self.buscar_cliente(cedula_rif=cedula_rif)
        if cliente:
            print("\nDatos actuales del cliente:")
            print(cliente.show())
            print("\nIngrese los nuevos datos (presione Enter para mantener el valor actual):")
            
            # Obtener nuevos datos o mantener los actuales
            nuevo_nombre = input(f"Nuevo nombre [{cliente.nombre}]: ") or cliente.nombre
            nuevo_apellido = input(f"Nuevo apellido [{cliente.apellido}]: ") or cliente.apellido
            nuevo_correo = input(f"Nuevo correo electrónico [{cliente.correo_electronico}]: ") or cliente.correo_electronico
            nueva_direccion = input(f"Nueva dirección de envío [{cliente.direccion_envio}]: ") or cliente.direccion_envio
            nuevo_telefono = input(f"Nuevo teléfono [{cliente.telefono}]: ") or cliente.telefono

            # Actualizar los datos
            cliente.nombre = nuevo_nombre
            cliente.apellido = nuevo_apellido
            cliente.correo_electronico = nuevo_correo
            cliente.direccion_envio = nueva_direccion
            cliente.telefono = nuevo_telefono

            # Si es cliente jurídico, actualizar datos adicionales
            if isinstance(cliente, ClienteJuridico):
                nuevo_nombre_contacto = input(f"Nuevo nombre de contacto [{cliente.nombre_contacto}]: ") or cliente.nombre_contacto
                nuevo_telefono_contacto = input(f"Nuevo teléfono de contacto [{cliente.telefono_contacto}]: ") or cliente.telefono_contacto
                nuevo_correo_contacto = input(f"Nuevo correo de contacto [{cliente.correo_contacto}]: ") or cliente.correo_contacto
                
                cliente.nombre_contacto = nuevo_nombre_contacto
                cliente.telefono_contacto = nuevo_telefono_contacto
                cliente.correo_contacto = nuevo_correo_contacto

            self.guardar_clientes()  # Guardar cambios después de editar
            print("Cliente actualizado exitosamente.")
        else:
            print("Cliente no encontrado.")

    def eliminar_cliente(self, cedula_rif):
        cliente = self.buscar_cliente(cedula_rif)
        if cliente:
            self.clientes.remove(cliente)
            self.guardar_clientes()  # Guardar cambios después de eliminar
            print("Cliente eliminado exitosamente.")
        else:
            print("Cliente no encontrado.")

    def guardar_clientes(self):
        with open('clientes.json', 'w', encoding='utf-8') as f:
            json.dump([cliente.__dict__ for cliente in self.clientes], f, ensure_ascii=False, indent=4)

    def cargar_clientes(self):
        try:
            with open('clientes.json', 'r', encoding='utf-8') as f:
                clientes_data = json.load(f)
                self.clientes = []
                for data in clientes_data:
                    if 'razon_social' in data:  # Cliente Jurídico
                        cliente = ClienteJuridico(
                            razon_social=data['razon_social'],
                            cedula_rif=data['cedula_rif'],
                            correo_electronico=data['correo_electronico'],
                            direccion_envio=data['direccion_envio'],
                            telefono=data['telefono'],
                            nombre_contacto=data.get('nombre_contacto', ''),  # En este caso utilice .get() para evitar un KeyError
                            telefono_contacto=data.get('telefono_contacto', ''),
                            correo_contacto=data.get('correo_contacto', '')
                        )
                    else:  # Cliente Natural
                        cliente = Cliente(
                            nombre=data.get('nombre', ''),
                            apellido=data.get('apellido', ''),
                            cedula_rif=data['cedula_rif'],
                            correo_electronico=data['correo_electronico'],
                            direccion_envio=data['direccion_envio'],
                            telefono=data['telefono']
                        )
                    self.clientes.append(cliente)
        except FileNotFoundError:
            self.clientes = []
            
# Menu de los clientes
def menu_gestion_clientes(gestion):
    while True:
        print("\n1. Registrar cliente")
        print("2. Buscar cliente")
        print("3. Mostrar todos los clientes")
        print("4. Editar cliente")
        print("5. Eliminar cliente")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            gestion.registrar_cliente()
        elif opcion == "2":
            cedula_rif = input("Ingrese la cédula o RIF del cliente a buscar: ")
            cliente = gestion.buscar_cliente(cedula_rif)
            if cliente:
                print(cliente.show())
            else:
                print("Cliente no encontrado.")
        elif opcion == "3":
            gestion.mostrar_clientes()
        elif opcion == "4":
            cedula_rif = input("Ingrese la cédula o RIF del cliente a editar: ")
            gestion.editar_cliente(cedula_rif)
        elif opcion == "5":
            cedula_rif = input("Ingrese la cédula o RIF del cliente a eliminar: ")
            confirmacion = input("¿Está seguro que desea eliminar este cliente? (s/n): ").lower()
            if confirmacion == 's':
                gestion.eliminar_cliente(cedula_rif)
            else:
                print("Operación cancelada.")
        elif opcion == "6":
            print("Gracias por usar el sistema de gestión de clientes.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    gestion_clientes = GestionClientes()
    menu_gestion_clientes(gestion_clientes)



