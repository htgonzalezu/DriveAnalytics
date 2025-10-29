"""
Script de prueba para verificar la limpieza y normalización de datos
"""
import sys
import os
import django

# Configurar el entorno de Django
sys.path.append('/home/santixo/Dev/DriveAnalytics')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'driveanalytics.settings')
django.setup()

import pandas as pd
from driveanalyticsApp.views import clean_and_normalize_data

# Leer el archivo CSV de ejemplo
print("=" * 70)
print("PRUEBA DE LIMPIEZA Y NORMALIZACIÓN DE DATOS")
print("=" * 70)

df_original = pd.read_csv('/home/santixo/Dev/DriveAnalytics/ejemplo_vehiculos.csv')

print("\n1. DATOS ORIGINALES:")
print(f"   - Filas: {len(df_original)}")
print(f"   - Columnas: {len(df_original.columns)}")
print(f"\n{df_original.head(10)}")

print("\n2. INFORMACIÓN DE TIPOS DE DATOS ORIGINALES:")
print(df_original.dtypes)

print("\n3. DATOS CON PROBLEMAS:")
print(f"   - Valores nulos por columna:")
print(df_original.isnull().sum())

# Limpiar y normalizar
df_clean = clean_and_normalize_data(df_original)

print("\n4. DATOS DESPUÉS DE LA LIMPIEZA:")
print(f"   - Filas: {len(df_clean)}")
print(f"   - Columnas: {len(df_clean.columns)}")
print(f"   - Filas eliminadas: {len(df_original) - len(df_clean)}")
print(f"\n{df_clean.head(15)}")

print("\n5. INFORMACIÓN DE TIPOS DE DATOS LIMPIOS:")
print(df_clean.dtypes)

print("\n6. VERIFICACIÓN DE LIMPIEZA:")
print(f"   - Valores nulos después de limpieza:")
print(df_clean.isnull().sum())

print("\n7. ESTADÍSTICAS DE LOS DATOS LIMPIOS:")
print(df_clean.describe())

print("\n8. VALORES ÚNICOS EN COLUMNAS CATEGÓRICAS:")
print(f"   - Marcas únicas: {df_clean['marca'].nunique()}")
print(f"     {df_clean['marca'].unique()}")
print(f"   - Tipos únicos: {df_clean['tipo'].nunique()}")
print(f"     {df_clean['tipo'].unique()}")
print(f"   - Estados únicos: {df_clean['estado'].nunique()}")
print(f"     {df_clean['estado'].unique()}")

print("\n9. RANGOS DE VALORES NUMÉRICOS:")
print(f"   - Año: {df_clean['year'].min()} - {df_clean['year'].max()}")
print(f"   - Cilindraje: {df_clean['cilindraje'].min()} - {df_clean['cilindraje'].max()}")
print(f"   - Precio: ${df_clean['precio'].min():,.2f} - ${df_clean['precio'].max():,.2f}")

print("\n" + "=" * 70)
print("PRUEBA COMPLETADA EXITOSAMENTE")
print("=" * 70)
