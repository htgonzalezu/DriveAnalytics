from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import DimVehiculo
import pandas as pd
import numpy as np
from datetime import datetime
from django.db import transaction
from django.db.models import Count, Sum, Avg, Max, Min, Q
from decimal import Decimal
import json
import io

# Create your views here.

def index(request):
    return render(request, 'index.html')

def lista_vehiculos(request):
    vehiculos = DimVehiculo.objects.all()
    return render(request, 'vehiculos.html', {'vehiculos': vehiculos})

def clean_and_normalize_data(df):
    """
    Limpia, transforma y normaliza los datos del DataFrame
    """
    # Crear una copia del DataFrame para no modificar el original
    df_clean = df.copy()

    # 1. LIMPIEZA DE DATOS

    # Eliminar filas completamente vacías
    df_clean = df_clean.dropna(how='all')

    # Eliminar duplicados basados en todas las columnas
    df_clean = df_clean.drop_duplicates()

    # Normalizar nombres de columnas (minúsculas, sin espacios)
    df_clean.columns = df_clean.columns.str.strip().str.lower().str.replace(' ', '_')

    # Mapeo de columnas esperadas
    column_mapping = {
        'id': 'id_vehiculo',
        'id_vehiculo': 'id_vehiculo',
        'brand': 'marca',
        'marca': 'marca',
        'model': 'modelo',
        'modelo': 'modelo',
        'year': 'year',
        'año': 'year',
        'type': 'tipo',
        'tipo': 'tipo',
        'engine_size': 'cilindraje',
        'cilindraje': 'cilindraje',
        'status': 'estado',
        'estado': 'estado',
        'registration_date': 'fecha_registro',
        'fecha_registro': 'fecha_registro',
        'price': 'precio',
        'precio': 'precio'
    }

    # Renombrar columnas según el mapeo
    df_clean = df_clean.rename(columns=column_mapping)

    # 2. TRANSFORMACIÓN Y NORMALIZACIÓN DE DATOS

    # ID Vehículo: asegurar que sea entero
    if 'id_vehiculo' in df_clean.columns:
        df_clean['id_vehiculo'] = pd.to_numeric(df_clean['id_vehiculo'], errors='coerce')
        df_clean = df_clean.dropna(subset=['id_vehiculo'])
        df_clean['id_vehiculo'] = df_clean['id_vehiculo'].astype(int)

    # Marca: limpiar y normalizar texto
    if 'marca' in df_clean.columns:
        df_clean['marca'] = df_clean['marca'].astype(str).str.strip().str.title()
        df_clean['marca'] = df_clean['marca'].replace(['Nan', 'None', ''], np.nan)
        df_clean['marca'] = df_clean['marca'].fillna('Desconocido')
        # Limitar longitud a 50 caracteres
        df_clean['marca'] = df_clean['marca'].str[:50]

    # Modelo: limpiar y normalizar texto
    if 'modelo' in df_clean.columns:
        df_clean['modelo'] = df_clean['modelo'].astype(str).str.strip().str.title()
        df_clean['modelo'] = df_clean['modelo'].replace(['Nan', 'None', ''], np.nan)
        df_clean['modelo'] = df_clean['modelo'].fillna('Desconocido')
        df_clean['modelo'] = df_clean['modelo'].str[:50]

    # Year: validar rango de años razonable
    if 'year' in df_clean.columns:
        df_clean['year'] = pd.to_numeric(df_clean['year'], errors='coerce')
        current_year = datetime.now().year
        # Filtrar años entre 1900 y año actual + 1
        df_clean['year'] = df_clean['year'].apply(
            lambda x: x if (1900 <= x <= current_year + 1) else current_year if pd.notna(x) else current_year
        )
        df_clean['year'] = df_clean['year'].astype(int)

    # Tipo: normalizar categorías
    if 'tipo' in df_clean.columns:
        df_clean['tipo'] = df_clean['tipo'].astype(str).str.strip().str.title()
        df_clean['tipo'] = df_clean['tipo'].replace(['Nan', 'None', ''], np.nan)
        # Mapear tipos comunes
        tipo_mapping = {
            'Sedan': 'Sedán',
            'Suv': 'SUV',
            'Pickup': 'Pickup',
            'Camioneta': 'Pickup',
            'Hatchback': 'Hatchback',
            'Coupe': 'Coupé',
            'Convertible': 'Convertible',
            'Van': 'Van',
            'Minivan': 'Minivan'
        }
        df_clean['tipo'] = df_clean['tipo'].replace(tipo_mapping)
        df_clean['tipo'] = df_clean['tipo'].fillna('Otro')
        df_clean['tipo'] = df_clean['tipo'].str[:50]

    # Cilindraje: asegurar que sea entero positivo
    if 'cilindraje' in df_clean.columns:
        df_clean['cilindraje'] = pd.to_numeric(df_clean['cilindraje'], errors='coerce')
        df_clean['cilindraje'] = df_clean['cilindraje'].fillna(0)
        df_clean['cilindraje'] = df_clean['cilindraje'].apply(lambda x: max(0, int(x)))

    # Estado: normalizar estados
    if 'estado' in df_clean.columns:
        df_clean['estado'] = df_clean['estado'].astype(str).str.strip().str.title()
        df_clean['estado'] = df_clean['estado'].replace(['Nan', 'None', ''], np.nan)
        # Mapear estados comunes
        estado_mapping = {
            'Disponible': 'Disponible',
            'Available': 'Disponible',
            'Vendido': 'Vendido',
            'Sold': 'Vendido',
            'En Mantenimiento': 'En Mantenimiento',
            'Maintenance': 'En Mantenimiento',
            'Reservado': 'Reservado',
            'Reserved': 'Reservado'
        }
        df_clean['estado'] = df_clean['estado'].replace(estado_mapping)
        df_clean['estado'] = df_clean['estado'].fillna('Disponible')
        df_clean['estado'] = df_clean['estado'].str[:20]

    # Fecha de registro: convertir a formato de fecha
    if 'fecha_registro' in df_clean.columns:
        df_clean['fecha_registro'] = pd.to_datetime(df_clean['fecha_registro'], errors='coerce')
        # Si la fecha es nula o inválida, usar fecha actual
        df_clean['fecha_registro'] = df_clean['fecha_registro'].fillna(pd.Timestamp.now())
        # Convertir a formato de fecha (sin hora)
        df_clean['fecha_registro'] = df_clean['fecha_registro'].dt.date

    # Precio: asegurar que sea decimal positivo
    if 'precio' in df_clean.columns:
        df_clean['precio'] = pd.to_numeric(df_clean['precio'], errors='coerce')
        df_clean['precio'] = df_clean['precio'].fillna(0)
        df_clean['precio'] = df_clean['precio'].apply(lambda x: max(0, round(x, 2)))

    # 3. VALIDACIÓN FINAL

    # Asegurar que todas las columnas requeridas existan
    required_columns = ['id_vehiculo', 'marca', 'modelo', 'year', 'tipo',
                       'cilindraje', 'estado', 'fecha_registro', 'precio']

    for col in required_columns:
        if col not in df_clean.columns:
            # Asignar valores por defecto según el tipo de columna
            if col == 'id_vehiculo':
                df_clean[col] = range(1, len(df_clean) + 1)
            elif col in ['marca', 'modelo', 'tipo', 'estado']:
                df_clean[col] = 'Desconocido' if col != 'estado' else 'Disponible'
            elif col in ['year', 'cilindraje']:
                df_clean[col] = 0
            elif col == 'fecha_registro':
                df_clean[col] = datetime.now().date()
            elif col == 'precio':
                df_clean[col] = 0.0

    # Seleccionar solo las columnas necesarias
    df_clean = df_clean[required_columns]

    # Eliminar filas con ID duplicado (mantener la primera)
    df_clean = df_clean.drop_duplicates(subset=['id_vehiculo'], keep='first')

    return df_clean


def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        try:
            # Detectar el tipo de archivo y leer con pandas
            file_extension = uploaded_file.name.split('.')[-1].lower()

            if file_extension == 'csv':
                # Intentar con diferentes encodings comunes
                try:
                    df = pd.read_csv(uploaded_file, encoding='utf-8')
                except UnicodeDecodeError:
                    uploaded_file.seek(0)  # Reiniciar el puntero del archivo
                    try:
                        df = pd.read_csv(uploaded_file, encoding='latin-1')
                    except:
                        uploaded_file.seek(0)
                        df = pd.read_csv(uploaded_file, encoding='iso-8859-1')

            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(uploaded_file)
            else:
                context = {
                    'success': False,
                    'error': 'Formato de archivo no soportado. Use CSV o Excel (.xlsx, .xls)'
                }
                return render(request, 'upload_result.html', context)

            # Información del archivo original
            original_rows = len(df)
            original_columns = len(df.columns)

            # Limpiar y normalizar los datos
            df_clean = clean_and_normalize_data(df)

            # Información después de la limpieza
            cleaned_rows = len(df_clean)
            removed_rows = original_rows - cleaned_rows

            # Subir los datos a la base de datos
            uploaded_count = 0
            updated_count = 0
            error_count = 0
            errors = []

            with transaction.atomic():
                for index, row in df_clean.iterrows():
                    try:
                        # Intentar actualizar si existe, o crear si no existe
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
                        else:
                            updated_count += 1

                    except Exception as e:
                        error_count += 1
                        errors.append(f"Fila {index + 1}: {str(e)}")

            # Preparar contexto para la plantilla
            context = {
                'success': True,
                'message': f'Archivo procesado exitosamente.',
                'filename': uploaded_file.name,
                'statistics': {
                    'original_rows': original_rows,
                    'original_columns': original_columns,
                    'cleaned_rows': cleaned_rows,
                    'removed_rows': removed_rows,
                    'uploaded_count': uploaded_count,
                    'updated_count': updated_count,
                    'error_count': error_count,
                    'total_in_database': DimVehiculo.objects.count()
                }
            }

            if errors and len(errors) <= 10:  # Mostrar máximo 10 errores
                context['errors'] = errors
            elif errors:
                context['errors'] = errors[:10]
                context['more_errors'] = len(errors) - 10

            return render(request, 'upload_result.html', context)

        except Exception as e:
            context = {
                'success': False,
                'error': f'Error al procesar el archivo: {str(e)}'
            }
            return render(request, 'upload_result.html', context)

    context = {
        'success': False,
        'error': 'No se ha subido ningún archivo.'
    }
    return render(request, 'upload_result.html', context)

    #Change from Zed editor


def analytics(request):
    """
    Vista para mostrar análisis y gráficos de los datos de vehículos
    """
    # Obtener todos los vehículos
    vehiculos = DimVehiculo.objects.all()
    total_vehiculos = vehiculos.count()
    
    if total_vehiculos == 0:
        context = {
            'no_data': True,
            'message': 'No hay datos disponibles para generar gráficos. Por favor, cargue datos primero.'
        }
        return render(request, 'analytics.html', context)
    
    # 1. ANÁLISIS POR MARCA (Top 10)
    marcas_data = list(
        vehiculos.values('marca')
        .annotate(
            cantidad=Count('id_vehiculo'),
            valor_total=Sum('precio'),
            precio_promedio=Avg('precio')
        )
        .order_by('-cantidad')[:10]
    )
    
    # 2. ANÁLISIS POR TIPO DE VEHÍCULO
    tipos_data = list(
        vehiculos.values('tipo')
        .annotate(
            cantidad=Count('id_vehiculo'),
            valor_total=Sum('precio'),
            precio_promedio=Avg('precio')
        )
        .order_by('-cantidad')
    )
    
    # 3. ANÁLISIS POR ESTADO
    estados_data = list(
        vehiculos.values('estado')
        .annotate(
            cantidad=Count('id_vehiculo'),
            valor_total=Sum('precio')
        )
        .order_by('-cantidad')
    )
    
    # 4. DISTRIBUCIÓN POR AÑO (últimos 15 años)
    current_year = datetime.now().year
    years_data = list(
        vehiculos.filter(year__gte=current_year - 15)
        .values('year')
        .annotate(
            cantidad=Count('id_vehiculo'),
            precio_promedio=Avg('precio')
        )
        .order_by('year')
    )
    
    # 5. ANÁLISIS DE PRECIOS
    precios_stats = vehiculos.aggregate(
        precio_minimo=Min('precio'),
        precio_maximo=Max('precio'),
        precio_promedio=Avg('precio'),
        precio_total=Sum('precio')
    )
    
    # Distribución de precios por rangos
    rangos_precio = [
        {'rango': '0-10K', 'min': 0, 'max': 10000},
        {'rango': '10K-20K', 'min': 10000, 'max': 20000},
        {'rango': '20K-30K', 'min': 20000, 'max': 30000},
        {'rango': '30K-50K', 'min': 30000, 'max': 50000},
        {'rango': '50K+', 'min': 50000, 'max': 999999999},
    ]
    
    rangos_data = []
    for rango in rangos_precio:
        count = vehiculos.filter(
            precio__gte=rango['min'],
            precio__lt=rango['max']
        ).count()
        rangos_data.append({
            'rango': rango['rango'],
            'cantidad': count
        })
    
    # 6. TOP 10 MODELOS MÁS VALIOSOS
    modelos_valiosos = list(
        vehiculos.values('marca', 'modelo', 'year')
        .annotate(precio_max=Max('precio'))
        .order_by('-precio_max')[:10]
    )
    
    # 7. INVENTARIO POR ESTADO Y VALOR
    inventario_estado = []
    for estado in estados_data:
        inventario_estado.append({
            'estado': estado['estado'],
            'cantidad': estado['cantidad'],
            'valor_total': float(estado['valor_total']) if estado['valor_total'] else 0,
            'porcentaje': round((estado['cantidad'] / total_vehiculos) * 100, 1)
        })
    
    # 8. ANÁLISIS DE CILINDRAJE
    cilindraje_ranges = [
        {'rango': '< 1500cc', 'min': 0, 'max': 1500},
        {'rango': '1500-2000cc', 'min': 1500, 'max': 2000},
        {'rango': '2000-3000cc', 'min': 2000, 'max': 3000},
        {'rango': '3000cc+', 'min': 3000, 'max': 999999},
    ]
    
    cilindraje_data = []
    for rango in cilindraje_ranges:
        count = vehiculos.filter(
            cilindraje__gte=rango['min'],
            cilindraje__lt=rango['max']
        ).count()
        avg_price = vehiculos.filter(
            cilindraje__gte=rango['min'],
            cilindraje__lt=rango['max']
        ).aggregate(Avg('precio'))['precio__avg']
        
        cilindraje_data.append({
            'rango': rango['rango'],
            'cantidad': count,
            'precio_promedio': float(avg_price) if avg_price else 0
        })
    
    # Convertir Decimal a float para JSON
    for item in marcas_data:
        if item['valor_total']:
            item['valor_total'] = float(item['valor_total'])
        if item['precio_promedio']:
            item['precio_promedio'] = float(item['precio_promedio'])
    
    for item in tipos_data:
        if item['valor_total']:
            item['valor_total'] = float(item['valor_total'])
        if item['precio_promedio']:
            item['precio_promedio'] = float(item['precio_promedio'])
    
    for item in estados_data:
        if item['valor_total']:
            item['valor_total'] = float(item['valor_total'])
    
    for item in years_data:
        if item['precio_promedio']:
            item['precio_promedio'] = float(item['precio_promedio'])
    
    for item in modelos_valiosos:
        if item['precio_max']:
            item['precio_max'] = float(item['precio_max'])
    
    # Convertir stats a float
    precios_stats = {
        'precio_minimo': float(precios_stats['precio_minimo']) if precios_stats['precio_minimo'] else 0,
        'precio_maximo': float(precios_stats['precio_maximo']) if precios_stats['precio_maximo'] else 0,
        'precio_promedio': float(precios_stats['precio_promedio']) if precios_stats['precio_promedio'] else 0,
        'precio_total': float(precios_stats['precio_total']) if precios_stats['precio_total'] else 0,
    }
    
    context = {
        'no_data': False,
        'total_vehiculos': total_vehiculos,
        'marcas_data': json.dumps(marcas_data),
        'tipos_data': json.dumps(tipos_data),
        'estados_data': json.dumps(estados_data),
        'years_data': json.dumps(years_data),
        'rangos_data': json.dumps(rangos_data),
        'cilindraje_data': json.dumps(cilindraje_data),
        'modelos_valiosos': modelos_valiosos,
        'inventario_estado': inventario_estado,
        'precios_stats': precios_stats,
    }
    
    return render(request, 'analytics.html', context)
