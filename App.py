from Producto import GestionProductos, menu_gestion_productos
from Cliente import GestionClientes, menu_gestion_clientes
from Pago import GestionPagos, menu_gestion_pagos
from Venta import SistemaVentas, menu_sistema_ventas
from Envio import GestionEnvios, menu_gestion_envios
from Estadistica import Estadisticas

class App:
    def mostrar_menu_principal(self):
        gestion_productos = GestionProductos()
        gestion_clientes = GestionClientes()
        gestion_pagos = GestionPagos()
        gestion_envios = GestionEnvios()
        sistema_ventas = SistemaVentas(gestion_clientes, gestion_productos, gestion_envios)

        while True:
            print("\n--- Menú Principal ---")
            print("1. Gestión de Productos")
            print("2. Gestión de Clientes")
            print("3. Gestión de Pagos")
            print("4. Gestión de Ventas")
            print("5. Gestión de Envíos")
            print("6. Estadísticas")
            print("0. Salir")
        
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                menu_gestion_productos(gestion_productos)

            elif opcion == '2':
                menu_gestion_clientes(gestion_clientes)

            elif opcion == '3':
                menu_gestion_pagos(gestion_pagos, gestion_clientes)

            elif opcion == '4':
                menu_sistema_ventas(sistema_ventas)
                
            elif opcion == '5':
                menu_gestion_envios(gestion_envios, gestion_clientes)

            elif opcion == '6':
                self.mostrar_estadisticas()

            elif opcion == '0':
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def mostrar_estadisticas(self):
        estadisticas = Estadisticas()

        # Mostrar estadísticas en la consola
        print("Ventas Totales por Día:")
        print(estadisticas.ventas_totales('dia'))

        print("\nProductos Más Vendidos:")
        print(estadisticas.productos_mas_vendidos())

        print("\nClientes Más Frecuentes:")
        print(estadisticas.clientes_mas_frecuentes())

        print("\nPagos Totales por Día:")
        print(estadisticas.pagos_totales('dia'))

        print("\nEnvíos Totales por Día:")
        print(estadisticas.envios_totales('dia'))

        # Graficar estadísticas
        estadisticas.graficar_ventas('mes')
        estadisticas.graficar_pagos('mes')
        estadisticas.graficar_envios('mes')