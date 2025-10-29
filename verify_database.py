"""
Script para verificar todos los datos en la base de datos
"""
import sys
import os
import django

sys.path.append('/home/santixo/Dev/DriveAnalytics')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'driveanalytics.settings')
django.setup()

from driveanalyticsApp.models import DimVehiculo

print("=" * 80)
print("VERIFICACIÓN DE DATOS EN LA BASE DE DATOS")
print("=" * 80)

vehiculos = DimVehiculo.objects.all().order_by('id_vehiculo')
total = vehiculos.count()

print(f"\nTotal de vehículos en la base de datos: {total}\n")

print(f"{'ID':^5} | {'Marca':^15} | {'Modelo':^15} | {'Año':^4} | {'Tipo':^12} | {'Precio':^12} | {'Estado':^18}")
print("-" * 110)

for v in vehiculos:
    print(f"{v.id_vehiculo:^5} | {v.marca:^15} | {v.modelo:^15} | {v.year:^4} | {v.tipo:^12} | ${v.precio:>10,.2f} | {v.estado:^18}")

print("-" * 110)
print(f"\nEstadísticas:")
print(f"  - Total registros: {total}")
print(f"  - Marcas únicas: {DimVehiculo.objects.values('marca').distinct().count()}")
print(f"  - Tipos únicos: {DimVehiculo.objects.values('tipo').distinct().count()}")
print(f"  - Estados únicos: {DimVehiculo.objects.values('estado').distinct().count()}")

print("\nDistribución por estado:")
from django.db.models import Count
estados = DimVehiculo.objects.values('estado').annotate(count=Count('estado')).order_by('-count')
for estado in estados:
    print(f"  - {estado['estado']}: {estado['count']} vehículos")

print("\nDistribución por tipo:")
tipos = DimVehiculo.objects.values('tipo').annotate(count=Count('tipo')).order_by('-count')
for tipo in tipos:
    print(f"  - {tipo['tipo']}: {tipo['count']} vehículos")

print("\n" + "=" * 80)
print("✓ VERIFICACIÓN COMPLETADA")
print("=" * 80)
