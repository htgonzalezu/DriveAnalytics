# Sistema de Limpieza y Carga de Datos - DriveAnalytics

## Descripción

Este sistema procesa archivos CSV y Excel con datos de vehículos, aplicando limpieza, transformación y normalización de datos usando pandas, para finalmente subirlos a la base de datos PostgreSQL.

## Características Principales

### 1. Limpieza de Datos

- **Eliminación de filas vacías**: Remueve filas completamente vacías
- **Eliminación de duplicados**: Identifica y elimina registros duplicados
- **Normalización de nombres de columnas**: Convierte a minúsculas, elimina espacios
- **Mapeo automático de columnas**: Soporta nombres en inglés y español

### 2. Transformación y Normalización

#### ID Vehículo
- Convierte a número entero
- Elimina valores no numéricos
- Genera IDs automáticos si faltan

#### Marca y Modelo
- Normaliza texto (Title Case)
- Limita longitud a 50 caracteres
- Reemplaza valores nulos por "Desconocido"
- Elimina espacios en blanco extras

#### Año (Year)
- Valida rango entre 1900 y año actual + 1
- Convierte valores inválidos al año actual
- Asegura tipo entero

#### Tipo de Vehículo
- Normaliza categorías comunes:
  - Sedan → Sedán
  - SUV → SUV
  - Pickup/Camioneta → Pickup
  - Hatchback → Hatchback
  - Coupe → Coupé
  - etc.
- Valores desconocidos → "Otro"

#### Cilindraje
- Convierte a número entero
- Asegura valores positivos (mínimo 0)
- Valores negativos o inválidos → 0

#### Estado
- Mapea estados en inglés y español:
  - Available/Disponible → Disponible
  - Sold/Vendido → Vendido
  - Maintenance/En Mantenimiento → En Mantenimiento
  - Reserved/Reservado → Reservado
- Valor por defecto: "Disponible"

#### Fecha de Registro
- Convierte a formato de fecha válido
- Fechas inválidas → fecha actual
- Formato: YYYY-MM-DD

#### Precio
- Convierte a decimal con 2 decimales
- Asegura valores positivos (mínimo 0)
- Precios negativos → 0.00

### 3. Carga a Base de Datos

- **Update or Create**: Actualiza registros existentes o crea nuevos
- **Transacciones atómicas**: Garantiza integridad de datos
- **Manejo de errores**: Captura y reporta errores por fila
- **Estadísticas detalladas**: Muestra resumen de operaciones

## Uso

### Endpoint de Carga

```python
POST /upload/
```

**Parámetros:**
- `file`: Archivo CSV o Excel (.csv, .xlsx, .xls)

**Respuesta JSON:**
```json
{
    "success": true,
    "message": "Archivo procesado exitosamente.",
    "statistics": {
        "original_rows": 15,
        "original_columns": 9,
        "cleaned_rows": 15,
        "removed_rows": 0,
        "uploaded_count": 6,
        "updated_count": 9,
        "error_count": 0,
        "total_in_database": 15
    }
}
```

### Formato de Archivo CSV

```csv
id_vehiculo,marca,modelo,year,tipo,cilindraje,estado,fecha_registro,precio
1,Toyota,Corolla,2020,Sedan,1800,Disponible,2020-01-15,25000.50
2,Honda,Civic,2021,Sedan,2000,Disponible,2021-03-20,28000
```

### Columnas Soportadas

El sistema acepta nombres de columnas en inglés o español:

| Español | Inglés | Tipo | Requerido |
|---------|--------|------|-----------|
| id_vehiculo | id | Entero | Sí |
| marca | brand | Texto | Sí |
| modelo | model | Texto | Sí |
| year / año | year | Entero | Sí |
| tipo | type | Texto | Sí |
| cilindraje | engine_size | Entero | Sí |
| estado | status | Texto | Sí |
| fecha_registro | registration_date | Fecha | Sí |
| precio | price | Decimal | Sí |

## Scripts de Prueba

### 1. Prueba de Limpieza de Datos

```bash
python test_data_cleaning.py
```

Muestra:
- Datos originales vs. limpios
- Tipos de datos antes y después
- Valores nulos
- Estadísticas descriptivas
- Valores únicos en categorías

### 2. Carga de Datos a Base de Datos

```bash
python load_data_to_db.py
```

Realiza:
- Lectura del archivo CSV
- Limpieza y normalización
- Carga a base de datos
- Reporte de resultados

## Ejemplos de Transformaciones

### Ejemplo 1: Normalización de Texto
```
Entrada:  "  honda  " → Salida: "Honda"
Entrada:  "TOYOTA"   → Salida: "Toyota"
```

### Ejemplo 2: Validación de Año
```
Entrada:  "invalid_year" → Salida: 2025 (año actual)
Entrada:  "2030"         → Salida: 2025 (año actual, fuera de rango)
```

### Ejemplo 3: Normalización de Estado
```
Entrada:  "disponible"   → Salida: "Disponible"
Entrada:  "Available"    → Salida: "Disponible"
Entrada:  "Unknown"      → Salida: "Unknown" (se mantiene si no está mapeado)
```

### Ejemplo 4: Corrección de Valores Negativos
```
Cilindraje: -1600 → 0
Precio:     -5000 → 0.00
```

## Dependencias

```
pandas>=2.3.3
openpyxl>=3.1.5
Django>=5.2.7
psycopg2-binary>=2.9.10
numpy>=2.3.3
```

## Instalación de Dependencias

```bash
pip install -r requirements.txt
```

## Estructura del Código

```
driveanalyticsApp/
├── views.py                    # Lógica de limpieza y carga
│   ├── clean_and_normalize_data()  # Función de limpieza
│   └── upload_file()               # Endpoint de carga
├── models.py                   # Modelo DimVehiculo
└── urls.py                     # Rutas

Scripts de prueba:
├── test_data_cleaning.py      # Prueba de limpieza
├── load_data_to_db.py         # Carga a base de datos
└── ejemplo_vehiculos.csv      # Datos de ejemplo
```

## Manejo de Errores

El sistema captura y reporta errores específicos por fila:

1. **Errores de conversión de tipos**: Se aplican valores por defecto
2. **Valores fuera de rango**: Se normalizan automáticamente
3. **Errores de base de datos**: Se reportan con detalles
4. **Transacciones fallidas**: Se hace rollback automático

## Mejores Prácticas

1. **Verificar formato de archivo**: Solo CSV y Excel son soportados
2. **Incluir encabezados**: Primera fila debe contener nombres de columnas
3. **Revisar estadísticas**: Analizar el reporte de limpieza
4. **Validar datos críticos**: Especialmente IDs y precios
5. **Hacer respaldos**: Antes de cargas masivas

## Ventajas del Sistema

✅ **Automático**: No requiere preparación manual de datos  
✅ **Robusto**: Maneja múltiples formatos y errores  
✅ **Normalizado**: Garantiza consistencia en los datos  
✅ **Reportes**: Estadísticas detalladas de cada operación  
✅ **Seguro**: Transacciones atómicas y manejo de errores  
✅ **Flexible**: Soporta múltiples idiomas y formatos  

## Soporte

Para problemas o consultas, revisar los logs de errores en la respuesta JSON del endpoint.
