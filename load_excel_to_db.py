"""
Script para cargar datos desde un archivo Excel a la base de datos
"""
import sys
import os
import django

# Configurar el entorno de Django
sys.path.append('/home/santixo/Dev/DriveAnalytics')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'driveanalytics.settings')
django.setup()

import pandas as pd
from driveanalyticsApp.models import DimVehiculo
from driveanalyticsApp.views import clean_and_normalize_data
from django.db import transaction

print("=" * 70)
print("CARGA DE DATOS DESDE ARCHIVO EXCEL")
print("=" * 70)

# Leer el archivo Excel
excel_file = '/home/santixo/Dev/DriveAnalytics/ejemplo_vehiculos.xlsx'
df_original = pd.read_excel(excel_file)

print(f"\n1. Leyendo archivo Excel: {excel_file}")
print(f"   - Filas originales: {len(df_original)}")
print(f"   - Columnas originales: {len(df_original.columns)}")
print(f"\n   Primeras 5 filas:")
print(df_original.head())

# Limpiar y normalizar
print(f"\n2. Limpiando y normalizando datos...")
df_clean = clean_and_normalize_data(df_original)
print(f"   - Filas después de limpieza: {len(df_clean)}")
print(f"   - Filas removidas: {len(df_original) - len(df_clean)}")
print(f"\n   Datos limpios (primeras 5 filas):")
print(df_clean.head())

# Estado actual de la base de datos
print(f"\n3. Estado actual de la base de datos:")
existing_count = DimVehiculo.objects.count()
print(f"   - Registros existentes antes de la carga: {existing_count}")

# Subir los datos
print(f"\n4. Subiendo datos a la base de datos...")
uploaded_count = 0
updated_count = 0
error_count = 0

try:
    with transaction.atomic():
        for index, row in df_clean.iterrows():
            try:
                vehiculo, created = DimVehiculo.objects.update_or_create(
                    id_vehiculo=row['id_vehiculo'],
                    defaults={
                        'marca': row['marca'],
                        'modelo': row['modelo'],
                        'year': row['year'],
                        'tipo': row['tipo'],
                        'cilindraje': row['cilindraje'],
                        'estado': row['estado'],
                        'fecha_registro': row['fecha_registro'],
                        'precio': row['precio']
                    }
                )
                
                if created:
                    uploaded_count += 1
                    print(f"   ✓ Creado: {vehiculo.marca} {vehiculo.modelo} (ID: {vehiculo.id_vehiculo})")
                else:
                    updated_count += 1
                    print(f"   ↻ Actualizado: {vehiculo.marca} {vehiculo.modelo} (ID: {vehiculo.id_vehiculo})")
                    
            except Exception as e:
                error_count += 1
                print(f"   ✗ Error en fila {index + 1}: {str(e)}")
    
    print(f"\n5. RESUMEN DE CARGA:")
    print(f"   - Archivo procesado: {os.path.basename(excel_file)}")
    print(f"   - Nuevos registros creados: {uploaded_count}")
    print(f"   - Registros actualizados: {updated_count}")
    print(f"   - Errores: {error_count}")
    print(f"   - Total en base de datos: {DimVehiculo.objects.count()}")
    
    # Mostrar vehículos recién agregados
    print(f"\n6. VEHÍCULOS RECIÉN AGREGADOS/ACTUALIZADOS:")
    ids = df_clean['id_vehiculo'].tolist()
    vehiculos_nuevos = DimVehiculo.objects.filter(id_vehiculo__in=ids).order_by('id_vehiculo')
    
    for v in vehiculos_nuevos:
        print(f"   ID {v.id_vehiculo:3d} | {v.marca:15s} | {v.modelo:15s} | {v.year} | {v.tipo:10s} | ${v.precio:>10,.2f} | {v.estado}")
    
    print("\n" + "=" * 70)
    print("✓ CARGA DESDE EXCEL COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    
except Exception as e:
    print(f"\n✗ ERROR CRÍTICO: {str(e)}")
    print("=" * 70)
