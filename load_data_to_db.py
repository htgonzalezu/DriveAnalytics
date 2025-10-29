"""
Script para cargar datos de ejemplo a la base de datos usando la función de limpieza
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
print("CARGA DE DATOS A LA BASE DE DATOS")
print("=" * 70)

# Leer el archivo CSV de ejemplo
df_original = pd.read_csv('/home/santixo/Dev/DriveAnalytics/ejemplo_vehiculos.csv')

print(f"\n1. Leyendo archivo CSV...")
print(f"   - Filas originales: {len(df_original)}")
print(f"   - Columnas originales: {len(df_original.columns)}")

# Limpiar y normalizar
print(f"\n2. Limpiando y normalizando datos...")
df_clean = clean_and_normalize_data(df_original)
print(f"   - Filas después de limpieza: {len(df_clean)}")
print(f"   - Filas removidas: {len(df_original) - len(df_clean)}")

# Verificar cuántos registros ya existen
print(f"\n3. Estado actual de la base de datos:")
existing_count = DimVehiculo.objects.count()
print(f"   - Registros existentes: {existing_count}")

# Subir los datos a la base de datos
print(f"\n4. Subiendo datos a la base de datos...")
uploaded_count = 0
updated_count = 0
error_count = 0
errors = []

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
                error_msg = f"Fila {index + 1}: {str(e)}"
                errors.append(error_msg)
                print(f"   ✗ Error: {error_msg}")
    
    print(f"\n5. RESUMEN DE CARGA:")
    print(f"   - Nuevos registros creados: {uploaded_count}")
    print(f"   - Registros actualizados: {updated_count}")
    print(f"   - Errores: {error_count}")
    print(f"   - Total en base de datos: {DimVehiculo.objects.count()}")
    
    if errors:
        print(f"\n6. ERRORES ENCONTRADOS:")
        for error in errors:
            print(f"   - {error}")
    
    # Mostrar algunos registros de la base de datos
    print(f"\n7. MUESTRA DE REGISTROS EN BASE DE DATOS:")
    vehiculos = DimVehiculo.objects.all()[:10]
    for v in vehiculos:
        print(f"   - ID {v.id_vehiculo}: {v.marca} {v.modelo} ({v.year}) - {v.estado} - ${v.precio}")
    
    print("\n" + "=" * 70)
    print("CARGA COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    
except Exception as e:
    print(f"\n✗ ERROR CRÍTICO: {str(e)}")
    print("=" * 70)
