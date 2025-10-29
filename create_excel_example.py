"""
Script para crear un archivo Excel de ejemplo
"""
import pandas as pd

# Datos de ejemplo
data = {
    'id_vehiculo': [16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
    'marca': ['Jeep', 'DODGE', '  Ford  ', 'toyota', 'Chevrolet', 'Ram', 'GMC', 'Cadillac', 'Lincoln', 'Buick'],
    'modelo': ['Wrangler', 'CHARGER', 'F-150', 'tacoma', 'Silverado', '1500', 'Sierra', 'Escalade', 'Navigator', 'Enclave'],
    'year': [2022, 2021, 2023, '2024', 2020, 2022, 2021, 2023, 2022, 2020],
    'tipo': ['SUV', 'sedan', 'Pickup', 'pickup', 'Pickup', 'Pickup', 'Pickup', 'SUV', 'SUV', 'SUV'],
    'cilindraje': [3600, 3600, 5000, 3500, 6200, 5700, 6200, 6200, 3500, 3600],
    'estado': ['Disponible', 'disponible', 'Available', 'Sold', 'Disponible', 'Reservado', 'Disponible', 'Disponible', 'Vendido', 'Disponible'],
    'fecha_registro': ['2022-03-15', '2021-07-20', '2023-01-10', '2024-02-14', '2020-09-05', '2022-11-22', '2021-08-30', '2023-04-18', '2022-06-12', '2020-10-25'],
    'precio': [45000, 38000.50, 55000, 42000, 48000.75, 52000, 49000.99, 89000, 78000.25, 46000]
}

df = pd.DataFrame(data)

# Guardar como Excel
output_file = '/home/santixo/Dev/DriveAnalytics/ejemplo_vehiculos.xlsx'
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"Archivo Excel creado exitosamente: {output_file}")
print(f"\nDatos guardados:")
print(df)
