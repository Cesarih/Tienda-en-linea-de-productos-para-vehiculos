import json
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt

class Estadisticas:
    def __init__(self, archivo_ventas='ventas.json', archivo_pagos='pagos.json', archivo_envios='envios.json'):
        self.archivo_ventas = archivo_ventas
        self.archivo_pagos = archivo_pagos
        self.archivo_envios = archivo_envios
        self.ventas = []
        self.pagos = []
        self.envios = []
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos de ventas, pagos y envíos desde los archivos JSON."""
        try:
            with open(self.archivo_ventas, 'r', encoding='utf-8') as f:
                self.ventas = json.load(f)
        except FileNotFoundError:
            print("Archivo de ventas no encontrado.")
            self.ventas = []

        try:
            with open(self.archivo_pagos, 'r', encoding='utf-8') as f:
                self.pagos = json.load(f)
        except FileNotFoundError:
            print("Archivo de pagos no encontrado.")
            self.pagos = []

        try:
            with open(self.archivo_envios, 'r', encoding='utf-8') as f:
                self.envios = json.load(f)
        except FileNotFoundError:
            print("Archivo de envíos no encontrado.")
            self.envios = []

    def ventas_totales(self, periodo='dia'):
        """Calcula las ventas totales por día, semana, mes o año."""
        totales = Counter()
        for venta in self.ventas:
            fecha = datetime.strptime(venta['fecha'], '%Y-%m-%d')
            if periodo == 'dia':
                clave = fecha.date()
            elif periodo == 'semana':
                clave = fecha.strftime('%Y-%U')  # Año y número de semana
            elif periodo == 'mes':
                clave = fecha.strftime('%Y-%m')  # Año y mes
            elif periodo == 'año':
                clave = fecha.year
            else:
                raise ValueError("Periodo no válido.")
            totales[clave] += venta['totales']['total']
        return totales

    def productos_mas_vendidos(self):
        """Devuelve los productos más vendidos."""
        productos = Counter()
        for venta in self.ventas:
            for producto, cantidad in venta['productos']:
                productos[producto] += cantidad
        return productos.most_common(10)  # Devuelve los 10 más vendidos

    def clientes_mas_frecuentes(self):
        """Devuelve los clientes más frecuentes."""
        clientes = Counter()
        for venta in self.ventas:
            clientes[venta['cliente']['cedula_rif']] += 1
        return clientes.most_common(10)  # Devuelve los 10 más frecuentes

    def pagos_totales(self, periodo='dia'):
        """Calcula los pagos totales por día, semana, mes o año."""
        totales = Counter()
        for pago in self.pagos:
            fecha = datetime.strptime(pago['fecha'], '%Y-%m-%d')
            if periodo == 'dia':
                clave = fecha.date()
            elif periodo == 'semana':
                clave = fecha.strftime('%Y-%U')
            elif periodo == 'mes':
                clave = fecha.strftime('%Y-%m')
            elif periodo == 'año':
                clave = fecha.year
            else:
                raise ValueError("Periodo no válido.")
            totales[clave] += pago['monto']
        return totales

    def envios_totales(self, periodo='dia'):
        """Calcula los envíos totales por día, semana, mes o año."""
        totales = Counter()
        for envio in self.envios:
            fecha = datetime.strptime(envio['fecha'], '%Y-%m-%d')
            if periodo == 'dia':
                clave = fecha.date()
            elif periodo == 'semana':
                clave = fecha.strftime('%Y-%U')
            elif periodo == 'mes':
                clave = fecha.strftime('%Y-%m')
            elif periodo == 'año':
                clave = fecha.year
            else:
                raise ValueError("Periodo no válido.")
            totales[clave] += 1  # Contamos el número de envíos
        return totales

    def graficar_ventas(self, periodo='dia'):
        """Genera un gráfico de las ventas totales por periodo."""
        totales = self.ventas_totales(periodo)
        fechas = list(totales.keys())
        valores = list(totales.values())

        plt.figure(figsize=(10, 5))
        plt.bar(fechas, valores, color='blue')
        plt.title(f'Ventas Totales por {periodo.capitalize()}')
        plt.xlabel(periodo.capitalize())
        plt.ylabel('Total de Ventas')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def graficar_pagos(self, periodo='dia'):
        """Genera un gráfico de los pagos totales por periodo."""
        totales = self.pagos_totales(periodo)
        fechas = list(totales.keys())
        valores = list(totales.values())

        plt.figure(figsize=(10, 5))
        plt.bar(fechas, valores, color='green')
        plt.title(f'Pagos Totales por {periodo.capitalize()}')
        plt.xlabel(periodo.capitalize())
        plt.ylabel('Total de Pagos')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def graficar_envios(self, periodo='dia'):
        """Genera un gráfico de los envíos totales por periodo."""
        totales = self.envios_totales(periodo)
        fechas = list(totales.keys())
        valores = list(totales.values())

        plt.figure(figsize=(10, 5))
        plt.bar(fechas, valores, color='orange')
        plt.title(f'Envíos Totales por {periodo.capitalize()}')
        plt.xlabel(periodo.capitalize())
        plt.ylabel('Total de Envíos')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

#Menu de las estadisticas
if __name__ == "__main__":
    estadisticas = Estadisticas()
    
    # Generar y mostrar estadísticas
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