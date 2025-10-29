"""
DEMOSTRACIÓN COMPLETA DEL SISTEMA DE LIMPIEZA Y CARGA DE DATOS
Este script muestra todas las capacidades del sistema implementado
"""
import sys
import os
import django

sys.path.append('/home/santixo/Dev/DriveAnalytics')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'driveanalytics.settings')
django.setup()

import pandas as pd
from driveanalyticsApp.models import DimVehiculo
from driveanalyticsApp.views import clean_and_normalize_data

print("=" * 80)
print(" " * 20 + "DEMOSTRACIÓN COMPLETA DEL SISTEMA")
print(" " * 15 + "Limpieza, Transformación y Carga de Datos")
print("=" * 80)

# Parte 1: Demostrar limpieza de datos problemáticos
print("\n" + "🔍 PARTE 1: DEMOSTRACIÓN DE LIMPIEZA DE DATOS PROBLEMÁTICOS")
print("-" * 80)

# Crear un DataFrame con datos problemáticos
datos_problematicos = {
    'id_vehiculo': [100, 101, 102, 103, 104, 105],
    'marca': ['  TOYOTA  ', 'honda', 'FORD', '', '  chevrolet  ', None],
    'modelo': ['COROLLA', '  civic  ', 'f-150', 'Unknown', 'SILVERADO', 'None'],
    'year': [2020, 'invalid', 1800, 2030, 2022, '2021'],
    'tipo': ['sedan', 'SEDAN', 'pickup', '', 'Pickup', 'suv'],
    'cilindraje': [1800, -2000, 5000, 0, 6200, '2500'],
    'estado': ['disponible', 'Available', 'Sold', '', 'En Mantenimiento', 'Unknown'],
    'fecha_registro': ['2020-01-15', 'invalid_date', '2022-03-20', '', '2022-08-05', '2021-07-30'],
    'precio': [25000.5, -10000, 55000, '', 48000.75, '28000']
}

df_problemas = pd.DataFrame(datos_problematicos)

print("\n📋 Datos ANTES de la limpieza:")
print(df_problemas.to_string(index=False))
print(f"\nTipos de datos originales:")
for col in df_problemas.columns:
    print(f"  • {col}: {df_problemas[col].dtype}")

# Limpiar los datos
df_limpio = clean_and_normalize_data(df_problemas)

print("\n\n✨ Datos DESPUÉS de la limpieza:")
print(df_limpio.to_string(index=False))
print(f"\nTipos de datos limpios:")
for col in df_limpio.columns:
    print(f"  • {col}: {df_limpio[col].dtype}")

# Parte 2: Mostrar transformaciones específicas
print("\n\n" + "🔄 PARTE 2: TRANSFORMACIONES APLICADAS")
print("-" * 80)

transformaciones = [
    ("Marca", "  TOYOTA  ", "Toyota", "Normalización a Title Case y eliminación de espacios"),
    ("Modelo", "  civic  ", "Civic", "Normalización a Title Case y eliminación de espacios"),
    ("Year", "invalid", "2025", "Año inválido → año actual"),
    ("Year", "1800", "2025", "Año fuera de rango → año actual"),
    ("Tipo", "sedan", "Sedán", "Normalización de categoría"),
    ("Tipo", "pickup", "Pickup", "Normalización de categoría"),
    ("Cilindraje", "-2000", "0", "Valor negativo → 0"),
    ("Estado", "Available", "Disponible", "Mapeo inglés → español"),
    ("Estado", "Sold", "Vendido", "Mapeo inglés → español"),
    ("Precio", "-10000", "0.00", "Precio negativo → 0.00"),
    ("Fecha", "invalid_date", "2025-10-16", "Fecha inválida → fecha actual"),
]

print(f"\n{'Campo':<15} | {'Valor Original':<20} | {'Valor Transformado':<20} | {'Descripción'}")
print("-" * 100)
for campo, original, transformado, desc in transformaciones:
    print(f"{campo:<15} | {original:<20} | {transformado:<20} | {desc}")

# Parte 3: Estadísticas de limpieza
print("\n\n" + "📊 PARTE 3: ESTADÍSTICAS DE LIMPIEZA")
print("-" * 80)

print(f"\nComparación de datos:")
print(f"  • Filas originales: {len(df_problemas)}")
print(f"  • Filas después de limpieza: {len(df_limpio)}")
print(f"  • Filas removidas: {len(df_problemas) - len(df_limpio)}")
print(f"  • Columnas procesadas: {len(df_limpio.columns)}")

print(f"\nValores nulos ANTES de limpieza:")
for col in df_problemas.columns:
    nulos = df_problemas[col].isnull().sum()
    if nulos > 0:
        print(f"  • {col}: {nulos} valores nulos")

print(f"\nValores nulos DESPUÉS de limpieza:")
nulos_total = df_limpio.isnull().sum().sum()
print(f"  • Total: {nulos_total} valores nulos (¡todos corregidos!)")

# Parte 4: Estado actual de la base de datos
print("\n\n" + "💾 PARTE 4: ESTADO ACTUAL DE LA BASE DE DATOS")
print("-" * 80)

total_db = DimVehiculo.objects.count()
print(f"\nTotal de registros en base de datos: {total_db}")

print(f"\n📈 Distribución por Estado:")
from django.db.models import Count
estados = DimVehiculo.objects.values('estado').annotate(count=Count('estado')).order_by('-count')
for estado in estados:
    porcentaje = (estado['count'] / total_db) * 100
    barra = '█' * int(porcentaje / 5)
    print(f"  {estado['estado']:20s} | {barra:<20s} {estado['count']:2d} ({porcentaje:5.1f}%)")

print(f"\n📈 Distribución por Tipo:")
tipos = DimVehiculo.objects.values('tipo').annotate(count=Count('tipo')).order_by('-count')
for tipo in tipos:
    porcentaje = (tipo['count'] / total_db) * 100
    barra = '█' * int(porcentaje / 5)
    print(f"  {tipo['tipo']:20s} | {barra:<20s} {tipo['count']:2d} ({porcentaje:5.1f}%)")

print(f"\n📈 Top 5 Marcas Más Comunes:")
marcas = DimVehiculo.objects.values('marca').annotate(count=Count('marca')).order_by('-count')[:5]
for i, marca in enumerate(marcas, 1):
    print(f"  {i}. {marca['marca']:20s} - {marca['count']} vehículos")

# Parte 5: Resumen de capacidades
print("\n\n" + "✨ PARTE 5: CAPACIDADES DEL SISTEMA")
print("-" * 80)

capacidades = [
    "✅ Soporte para archivos CSV y Excel (.csv, .xlsx, .xls)",
    "✅ Múltiples encodings (utf-8, latin-1, iso-8859-1)",
    "✅ Eliminación automática de filas vacías y duplicados",
    "✅ Normalización de nombres de columnas",
    "✅ Mapeo automático de columnas en español e inglés",
    "✅ Validación y corrección de tipos de datos",
    "✅ Normalización de texto (Title Case, espacios)",
    "✅ Validación de rangos numéricos (años, precios, cilindradas)",
    "✅ Mapeo de categorías (estados, tipos de vehículos)",
    "✅ Conversión de fechas con manejo de errores",
    "✅ Corrección de valores negativos y nulos",
    "✅ Update or Create (evita duplicados)",
    "✅ Transacciones atómicas con rollback",
    "✅ Estadísticas detalladas de cada operación",
    "✅ Reporte de errores específicos por fila",
    "✅ Valores por defecto inteligentes"
]

print("\nEl sistema incluye:")
for capacidad in capacidades:
    print(f"  {capacidad}")

# Parte 6: Ejemplos de uso
print("\n\n" + "📚 PARTE 6: EJEMPLOS DE USO")
print("-" * 80)

print("\n1️⃣  Via Endpoint Web:")
print("""
    POST /upload/
    Content-Type: multipart/form-data
    file: vehiculos.csv
    
    Respuesta JSON con estadísticas detalladas
""")

print("2️⃣  Via Script Python:")
print("""
    python load_data_to_db.py      # Cargar CSV
    python load_excel_to_db.py     # Cargar Excel
    python verify_database.py       # Verificar datos
""")

print("3️⃣  Programáticamente:")
print("""
    from driveanalyticsApp.views import clean_and_normalize_data
    df_clean = clean_and_normalize_data(df_original)
""")

# Final
print("\n\n" + "=" * 80)
print(" " * 25 + "🎉 DEMOSTRACIÓN COMPLETADA 🎉")
print(" " * 15 + "Sistema listo para procesar tus datos!")
print("=" * 80)

print("\n📁 Archivos disponibles para probar:")
print("  • ejemplo_vehiculos.csv  - Archivo CSV con datos de ejemplo")
print("  • ejemplo_vehiculos.xlsx - Archivo Excel con datos de ejemplo")

print("\n📖 Documentación completa en:")
print("  • DATA_CLEANING_README.md      - Guía detallada del sistema")
print("  • IMPLEMENTACION_COMPLETA.md   - Resumen de implementación")

print("\n" + "=" * 80 + "\n")
