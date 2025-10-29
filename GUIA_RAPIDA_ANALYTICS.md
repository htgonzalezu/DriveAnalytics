# 🚀 Guía Rápida - Dashboard de Análisis

## 📊 Acceso al Dashboard

### Opción 1: Desde la Página Principal
1. Ir a `http://localhost:8000/`
2. Hacer clic en el botón **"📈 Análisis y Gráficos"**

### Opción 2: Desde la Lista de Vehículos
1. Ir a `http://localhost:8000/vehiculos/`
2. Hacer clic en el botón **"📊 Ver Análisis"**

### Opción 3: URL Directa
- Acceder directamente a: `http://localhost:8000/analytics/`

---

## 🎯 ¿Qué Encontrarás?

### 📈 8 Gráficos Interactivos
1. **Top 10 Marcas** - Las marcas más populares en tu inventario
2. **Distribución por Tipo** - Porcentajes de SUVs, Sedanes, etc.
3. **Estado del Inventario** - Disponibles, vendidos, en mantenimiento
4. **Vehículos por Año** - Tendencia temporal del inventario
5. **Distribución de Precios** - Rangos de precio del inventario
6. **Distribución por Cilindraje** - Preferencias de motor
7. **Valor Total por Marca** - Capital invertido por marca
8. **Precio Promedio por Tipo** - Comparación de precios

### 💡 4 KPIs Principales
- Total de Vehículos
- Valor Total del Inventario
- Precio Promedio
- Precio Máximo

### 📦 Análisis de Inventario
- Cards con información detallada por estado
- Cantidad, valor y porcentaje

### 💎 Top 10 Vehículos Más Valiosos
- Tabla con los vehículos premium

---

## 🔄 Iniciar el Servidor

```bash
# Activar entorno virtual (si usas uno)
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Ejecutar el servidor
python manage.py runserver

# Acceder a:
# http://localhost:8000/analytics/
```

---

## ⚠️ Requisitos

- ✅ Django instalado
- ✅ Base de datos configurada
- ✅ Datos de vehículos cargados
- ✅ Conexión a internet (para Chart.js desde CDN)

---

## 📱 Funcionalidades

### Interactividad
- Hover sobre gráficos para ver detalles
- Tooltips con información completa
- Formato automático de moneda

### Navegación
- Botones para ir a Inicio y Lista de Vehículos
- Diseño responsive para móviles y tablets

### Sin Datos
- Si no hay datos, muestra mensaje amigable
- Link directo para cargar datos

---

## 🎨 Características Técnicas

### Frontend
- HTML5 + CSS3
- JavaScript vanilla
- Chart.js 4.x
- Diseño responsive

### Backend
- Django 5.2.7
- Consultas optimizadas con ORM
- Agregaciones eficientes

### Rendimiento
- Caché de datos
- Gráficos renderizados en cliente
- Sin dependencias pesadas

---

## 📊 Ejemplo de Uso

1. **Cargar Datos**
   ```
   Inicio → Cargar Archivo → Upload
   ```

2. **Ver Análisis**
   ```
   Inicio → Análisis y Gráficos
   ```

3. **Interpretar Gráficos**
   - Identifica tendencias
   - Toma decisiones de compra
   - Optimiza inventario

---

## 🆘 Solución de Problemas

### No aparecen gráficos
- ✅ Verificar que hay datos en la BD
- ✅ Revisar consola del navegador
- ✅ Verificar conexión a internet

### Error 404
- ✅ Verificar que el servidor está corriendo
- ✅ Revisar la URL
- ✅ Verificar que las URLs están configuradas

### Datos no actualizados
- ✅ Recargar la página (F5)
- ✅ Verificar los datos en la BD
- ✅ Revisar la vista `analytics()`

---

## 📞 Navegación del Sistema

```
┌─────────────────────────────────────┐
│         Inicio (/)                  │
│                                     │
│  ┌──────────────┐  ┌──────────────┐│
│  │   Cargar     │  │  Análisis    ││
│  │   Datos      │  │  Gráficos    ││
│  └──────────────┘  └──────────────┘│
│                                     │
│  ┌──────────────┐                  │
│  │  Lista de    │                  │
│  │  Vehículos   │                  │
│  └──────────────┘                  │
└─────────────────────────────────────┘
```

---

## 🎯 Casos de Uso Recomendados

### Para Gerentes
- Revisar KPIs diariamente
- Identificar tendencias de venta
- Planificar compras

### Para Vendedores
- Ver inventario disponible
- Conocer precios promedio
- Identificar vehículos premium

### Para Análisis
- Generar reportes
- Identificar oportunidades
- Optimizar stock

---

**¡Listo para usar!** 🚀

Última actualización: 27 de Octubre, 2025
