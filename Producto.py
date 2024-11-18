import json
import requests

class Producto:
    def __init__(self, id, name, description, price, category, inventory, compatible_vehicles=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.inventory = inventory
        self.compatible_vehicles = compatible_vehicles if compatible_vehicles is not None else []

    def show(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category": self.category,
            "inventory": self.inventory,
            "compatible_vehicles": self.compatible_vehicles
        }

class GestionProductos:
    def __init__(self):
        self.productos = []
        self.cargar_productos()

    def cargar_productos(self):
        try:
            with open("productos.json", "r") as f:
                productos_data = json.load(f)
                for producto_data in productos_data:
                    producto = Producto(
                        id=producto_data["id"],
                        name=producto_data["name"],
                        description=producto_data["description"],
                        price=producto_data["price"],
                        category=producto_data["category"],
                        inventory=producto_data["inventory"],
                        compatible_vehicles=producto_data.get("compatible_vehicles", [])
                    )
                    self.productos.append(producto)
        except FileNotFoundError:
            print("Archivo no encontrado. Cargando productos desde la API...")
            self.cargar_productos_desde_api()
        except Exception as e:
            print(f"Error al cargar productos desde el archivo: {e}")
            self.cargar_productos_desde_api()

    def cargar_productos_desde_api(self):  #Importarse todos los productos de la API
        try:
            response = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/products.json")
            response.raise_for_status()
            productos_data = response.json()
            for producto_data in productos_data:
                producto = Producto(
                    id=producto_data["id"],
                    name=producto_data["name"],
                    description=producto_data["description"],
                    price=producto_data["price"],
                    category=producto_data["category"],
                    inventory=producto_data["inventory"],
                    compatible_vehicles=producto_data.get("compatible_vehicles", [])
                )
                self.productos.append(producto)
        except requests.exceptions.RequestException as e: # Esto es para indicarle al usuario que hay algun error que hace que no se puedan importar datos de la API
            print(f"Error al cargar los productos desde la API: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def guardar_productos(self):
        with open("productos.json", "w") as f:
            json.dump([producto.show() for producto in self.productos], f, indent=4)

    def agregar_producto(self):
        name = input("Ingrese el nombre del producto: ")
        description = input("Ingrese la descripción del producto: ")
        
        while True:
            precio_input = input("Ingrese el precio del producto: ")
            try:
                price = float(precio_input.replace(",", "."))
                break
            except ValueError:
                print("Error... Por favor, ingrese un precio válido (use '.' como separador decimal).")

        category = input("Ingrese la categoría del producto: ")
        inventory = int(input("Ingrese la cantidad en inventario: "))
        compatible_vehicles = input("Ingrese los vehículos compatibles (separados por comas): ").split(',')

        producto = Producto(
            id=len(self.productos) + 1,
            name=name,
            description=description,
            price=price,
            category=category,
            inventory=inventory,
            compatible_vehicles=[vehiculo.strip() for vehiculo in compatible_vehicles]
        )
        self.productos.append(producto)
        self.guardar_productos()
        print("Producto agregado exitosamente.")

    def buscar_producto(self, name_producto):
        for producto in self.productos:
            if producto.name.lower() == name_producto.lower():
                return producto
        return None

    def modificar_producto(self):
        id_producto = int(input("Ingrese el ID del producto a modificar: "))
        for producto in self.productos:
            if producto.id == id_producto:
                print("Producto encontrado:")
                print(f"ID: {producto.id}, Nombre: {producto.name}, Descripción: {producto.description}, Precio: {producto.price}, Categoría: {producto.category}, Inventario: {producto.inventory}, Vehículos compatibles: {', '.join(producto.compatible_vehicles)}")
                
                # Modificar los atributos del producto
                producto.name = input("Ingrese el nuevo nombre del producto (deje vacío para no modificar): ") or producto.name
                producto.description = input("Ingrese la nueva descripción (deje vacío para no modificar): ") or producto.description
                while True:
                    precio_input = input("Ingrese el nuevo precio (deje vacío para no modificar): ")
                    if precio_input == "":
                        break
                    try:
                        producto.price = float(precio_input.replace(",", "."))
                        break
                    except ValueError:
                        print("Error... Por favor, ingrese un precio válido (use '.' como separador decimal).")
                
                producto.category = input("Ingrese la nueva categoría (deje vacío para no modificar): ") or producto.category
                inventory_input = input("Ingrese la nueva cantidad en inventario (deje vacío para no modificar): ")
                if inventory_input != "":
                    producto.inventory = int(inventory_input)
                
                compatible_vehicles_input = input("Ingrese los nuevos vehículos compatibles (separados por comas, deje vacío para no modificar): ")
                if compatible_vehicles_input != "":
                    producto.compatible_vehicles = [vehiculo.strip() for vehiculo in compatible_vehicles_input.split(',')]
                
                self.guardar_productos()
                print("Producto modificado exitosamente.")
                return
        
        print("Producto no encontrado.")

    def eliminar_producto(self):
        id_producto = int(input("Ingrese el ID del producto a eliminar: "))
        for i, producto in enumerate(self.productos):
            if producto.id == id_producto:
                del self.productos[i]
                self.guardar_productos()
                print("Producto eliminado exitosamente.")
                return
        
        print("Producto no encontrado.")

#Mneu de productos
def menu_gestion_productos(gestion_productos):
    while True:
        print("\n--- Menú de Gestión de Productos ---")
        print("1. Agregar Producto")
        print("2. Buscar Producto")
        print("3. Modificar Producto")
        print("4. Eliminar Producto")
        print("5. Mostrar Todos los Productos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestion_productos.agregar_producto()
        elif opcion == "2":
            nombre_producto = input("Ingrese el nombre del producto a buscar: ")
            producto = gestion_productos.buscar_producto(nombre_producto)
            if producto:
                print(producto.show())
            else:
                print("Producto no encontrado.")
        elif opcion == "3":
            gestion_productos.modificar_producto()
        elif opcion == "4":
            gestion_productos.eliminar_producto()
        elif opcion == "5":
            if gestion_productos.productos:
                for producto in gestion_productos.productos:
                    print(producto.show())
                    print("-" * 30)
            else:
                print("No hay productos registrados.")
        elif opcion == "6":
            print("Gracias por usar el sistema de gestión de productos.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    gestion_productos = GestionProductos()
    menu_gestion_productos(gestion_productos)