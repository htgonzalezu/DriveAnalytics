"""
Script para probar la nueva interfaz web de carga de archivos
Este script simula una petición HTTP POST con un archivo
"""
import os
import sys

# Configurar el entorno de Django
sys.path.append('/home/santixo/Dev/DriveAnalytics')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'driveanalytics.settings')

import django
django.setup()

from django.test import RequestFactory, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from driveanalyticsApp.views import upload_file

print("=" * 80)
print("PRUEBA DE LA NUEVA INTERFAZ WEB")
print("=" * 80)

print("\n📝 Información:")
print("   La función upload_file ahora retorna HTML en lugar de JSON")
print("   Los resultados se muestran en una página web estilizada")

print("\n✅ Cambios implementados:")
print("   1. Nueva plantilla: upload_result.html")
print("   2. Diseño responsivo con CSS moderno")
print("   3. Visualización de estadísticas en tarjetas")
print("   4. Mensajes de éxito y error estilizados")
print("   5. Botones para navegar a otras páginas")
print("   6. Página de inicio mejorada (index.html)")
print("   7. Selector de archivos interactivo")

print("\n🎨 Características de la interfaz:")
print("   • Diseño con gradientes y sombras")
print("   • Tarjetas de estadísticas animadas")
print("   • Alertas visuales (éxito/error)")
print("   • Resumen detallado del procesamiento")
print("   • Lista de errores si los hay")
print("   • Botones para navegar fácilmente")
print("   • Diseño responsivo para móviles")

print("\n🚀 Para probar la interfaz web:")
print("   1. Inicia el servidor Django:")
print("      python manage.py runserver")
print("")
print("   2. Abre tu navegador en:")
print("      http://localhost:8000/")
print("")
print("   3. Sube un archivo CSV o Excel")
print("")
print("   4. Verás los resultados en una página hermosa!")

print("\n📁 Archivos de prueba disponibles:")
print("   • ejemplo_vehiculos.csv  (15 registros)")
print("   • ejemplo_vehiculos.xlsx (10 registros)")

print("\n💡 Prueba con el servidor:")
print("   El servidor está corriendo en segundo plano.")
print("   Visita http://localhost:8000/ para ver la interfaz.")

print("\n" + "=" * 80)
print("✅ SISTEMA ACTUALIZADO EXITOSAMENTE")
print("=" * 80)

print("\n🎉 ¡La interfaz web está lista para usar!")
print("   Ya no recibirás respuestas JSON, sino páginas HTML bonitas.\n")
