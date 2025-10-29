# 🚗 DriveAnalytics - Sistema de Limpieza y Carga de Datos

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)](https://www.djangoproject.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.3.3-orange.svg)](https://pandas.pydata.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue.svg)](https://www.postgresql.org/)

Sistema completo de análisis de datos de vehículos con capacidades de limpieza, transformación y normalización de datos desde archivos CSV y Excel.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Documentación](#-documentación)
- [Ejemplos](#-ejemplos)
- [Pruebas](#-pruebas)
- [Contribuir](#-contribuir)

---

## ✨ Características

### 🧹 Limpieza Automática de Datos
- ✅ Eliminación de filas vacías y duplicados
- ✅ Normalización de nombres de columnas
- ✅ Mapeo automático español/inglés
- ✅ Corrección de valores inválidos

### 🔄 Transformación y Normalización
- ✅ Validación de tipos de datos
- ✅ Normalización de texto (Title Case)
- ✅ Validación de rangos numéricos
- ✅ Conversión de fechas
- ✅ Mapeo de categorías

### 💾 Carga a Base de Datos
- ✅ Update or Create (evita duplicados)
- ✅ Transacciones atómicas
- ✅ Manejo de errores por fila
- ✅ Estadísticas detalladas

### 📊 Soporte de Formatos
- ✅ CSV (múltiples encodings)
- ✅ Excel (.xlsx, .xls)
- ✅ Respuestas JSON

---

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/santihern16/DriveAnalytics.git
cd DriveAnalytics
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `.env` con:
```env
DATABASE=nombre_db
USER_SQL=usuario
PASSWORD=contraseña
HOST=localhost
PORT=5432
```

### 5. Ejecutar migraciones
```bash
python manage.py migrate
```

### 6. Iniciar servidor
```bash
python manage.py runserver
```

---

## 💻 Uso

### Via Web (Endpoint)

```bash
POST /upload/
Content-Type: multipart/form-data
file: vehiculos.csv
```

**Respuesta:**
```json
{
    "success": true,
    "message": "Archivo procesado exitosamente.",
    "statistics": {
        "original_rows": 15,
        "cleaned_rows": 15,
        "uploaded_count": 6,
        "updated_count": 9,
        "error_count": 0,
        "total_in_database": 25
    }
}
```

### Via Scripts Python

```bash
# Probar limpieza de datos
python test_data_cleaning.py

# Cargar CSV a base de datos
python load_data_to_db.py

# Cargar Excel a base de datos
python load_excel_to_db.py

# Verificar datos en base de datos
python verify_database.py

# Demostración completa del sistema
python demo_completa.py
```

### Programáticamente

```python
from driveanalyticsApp.views import clean_and_normalize_data
import pandas as pd

# Leer archivo
df = pd.read_csv('vehiculos.csv')

# Limpiar y normalizar
df_clean = clean_and_normalize_data(df)

# Procesar datos limpios
print(df_clean)
```

---

## 📁 Estructura del Proyecto

```
DriveAnalytics/
├── 📄 manage.py                        # Django management
├── 📄 requirements.txt                 # Dependencias
├── 📄 db.sqlite3                       # DB local (desarrollo)
│
├── 📂 driveanalytics/                  # Configuración Django
│   ├── settings.py                     # Configuración
│   ├── urls.py                         # URLs principales
│   └── wsgi.py                         # WSGI config
│
├── 📂 driveanalyticsApp/               # Aplicación principal
│   ├── 📄 models.py                    # Modelo DimVehiculo
│   ├── 📄 views.py                     # ⭐ Lógica de limpieza y carga
│   ├── 📄 urls.py                      # URLs de la app
│   ├── 📄 admin.py                     # Admin de Django
│   └── 📂 templates/                   # Templates HTML
│       ├── index.html
│       └── vehiculos.html
│
├── 📂 db_connection/                   # Conexiones a DB
│   ├── bodegadedatos_pi.py
│   └── testcon.py
│
├── 📊 ejemplo_vehiculos.csv            # Datos de prueba CSV
├── 📊 ejemplo_vehiculos.xlsx           # Datos de prueba Excel
│
├── 🧪 test_data_cleaning.py           # Test de limpieza
├── 🧪 load_data_to_db.py              # Carga CSV → DB
├── 🧪 load_excel_to_db.py             # Carga Excel → DB
├── 🧪 verify_database.py              # Verificación de datos
├── 🧪 demo_completa.py                # Demo completa
├── 🧪 create_excel_example.py         # Generador Excel
│
└── 📚 Documentación/
    ├── DATA_CLEANING_README.md        # Guía técnica
    ├── IMPLEMENTACION_COMPLETA.md     # Resumen implementación
    └── RESUMEN_VISUAL.md              # Resumen visual
```

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [DATA_CLEANING_README.md](DATA_CLEANING_README.md) | Guía técnica completa del sistema de limpieza |
| [IMPLEMENTACION_COMPLETA.md](IMPLEMENTACION_COMPLETA.md) | Resumen detallado de la implementación |
| [RESUMEN_VISUAL.md](RESUMEN_VISUAL.md) | Resumen visual con tablas y estadísticas |

---

## 🎯 Ejemplos

### Formato de Archivo CSV

```csv
id_vehiculo,marca,modelo,year,tipo,cilindraje,estado,fecha_registro,precio
1,Toyota,Corolla,2020,Sedan,1800,Disponible,2020-01-15,25000.50
2,Honda,Civic,2021,Sedan,2000,Disponible,2021-03-20,28000
3,Ford,Mustang,2019,Coupe,5000,Vendido,2019-06-10,45000.75
```

### Columnas Soportadas

| Español | Inglés | Tipo | Requerido |
|---------|--------|------|-----------|
| id_vehiculo | id | Entero | ✅ |
| marca | brand | Texto | ✅ |
| modelo | model | Texto | ✅ |
| year / año | year | Entero | ✅ |
| tipo | type | Texto | ✅ |
| cilindraje | engine_size | Entero | ✅ |
| estado | status | Texto | ✅ |
| fecha_registro | registration_date | Fecha | ✅ |
| precio | price | Decimal | ✅ |

### Transformaciones Automáticas

| Entrada | Salida | Transformación |
|---------|--------|----------------|
| `"  TOYOTA  "` | `"Toyota"` | Normalización |
| `"invalid_year"` | `2025` | Año actual |
| `-1600` | `0` | Corrección negativo |
| `"Available"` | `"Disponible"` | Mapeo ES/EN |
| `"sedan"` | `"Sedán"` | Normalización |

---

## 🧪 Pruebas

### Ejecutar todas las pruebas

```bash
# Test de limpieza
python test_data_cleaning.py

# Test de carga CSV
python load_data_to_db.py

# Test de carga Excel
python load_excel_to_db.py

# Verificación final
python verify_database.py

# Demo completa
python demo_completa.py
```

### Resultados Esperados

```
✓ 25 registros cargados
✓ 0 errores críticos
✓ 100% datos normalizados
✓ 21 marcas únicas
✓ 5 tipos de vehículos
```

---

## 🔧 Tecnologías

- **Backend**: Django 5.2.7
- **Base de Datos**: PostgreSQL
- **Procesamiento de Datos**: Pandas 2.3.3, NumPy 2.3.3
- **Excel**: OpenPyXL 3.1.5
- **Python**: 3.12

---

## 📊 Estadísticas del Proyecto

- **Líneas de código**: ~500+ (limpieza y carga)
- **Transformaciones**: 25+ tipos diferentes
- **Formatos soportados**: CSV, Excel
- **Encodings**: UTF-8, Latin-1, ISO-8859-1
- **Tests**: 5 scripts completos
- **Documentación**: 3 archivos detallados

---

## 🎓 Capacidades Destacadas

1. **Robustez**: Maneja datos inconsistentes automáticamente
2. **Flexibilidad**: Soporta múltiples formatos y idiomas
3. **Seguridad**: Transacciones atómicas con rollback
4. **Transparencia**: Estadísticas detalladas de cada operación
5. **Escalabilidad**: Preparado para grandes volúmenes de datos

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**Santiago Hernández**
- GitHub: [@santihern16](https://github.com/santihern16)
- Proyecto: DriveAnalytics

---

## 📞 Soporte

Para problemas o consultas:
- Revisar la [documentación](DATA_CLEANING_README.md)
- Abrir un [Issue](https://github.com/santihern16/DriveAnalytics/issues)
- Contactar al equipo de desarrollo

---

## 🎉 Agradecimientos

- Equipo de Django por el excelente framework
- Pandas por las herramientas de procesamiento de datos
- PostgreSQL por la base de datos robusta

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!**

---

*Última actualización: Octubre 16, 2025*
