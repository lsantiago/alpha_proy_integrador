# Visualizador de Datos y Generador de Reportes PDF

Una aplicación web interactiva construida con Streamlit que permite cargar archivos CSV, crear visualizaciones dinámicas y generar reportes en PDF con gráficos y estadísticas descriptivas.

## 🚀 Características

- **Carga de archivos CSV**: Interfaz simple para cargar y visualizar datos
- **Gráficos interactivos**: Visualizaciones de dispersión personalizables con Altair
- **Generación de PDF**: Reportes automáticos con tablas, gráficos y estadísticas
- **Análisis estadístico**: Estadísticas descriptivas automáticas de datos numéricos
- **Interfaz intuitiva**: Diseño limpio y fácil de usar

## 📋 Requisitos

### Dependencias de Python

```bash
pip install streamlit pandas altair fpdf2 matplotlib
```

### Versiones recomendadas

- Python 3.8+
- streamlit >= 1.28.0
- pandas >= 1.5.0
- altair >= 5.0.0
- fpdf2 >= 2.7.0
- matplotlib >= 3.6.0

## 🛠️ Instalación

1. **Clona o descarga el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd visualizador-datos
   ```

2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```
   
   O instala manualmente:
   ```bash
   pip install streamlit pandas altair fpdf2 matplotlib
   ```

3. **Ejecuta la aplicación**
   ```bash
   streamlit run app.py
   ```

4. **Abre el navegador** y ve a `http://localhost:8501`

## 📖 Uso

### Carga de datos

1. Haz clic en "Seleccione un archivo CSV" 
2. Selecciona tu archivo CSV desde tu computadora
3. Los datos se mostrarán automáticamente en una tabla interactiva

### Creación de gráficos

1. **Selecciona el eje X**: Elige una columna numérica para el eje horizontal
2. **Selecciona el eje Y**: Elige una columna numérica para el eje vertical  
3. **Colorear por** (opcional): Selecciona una columna para colorear los puntos
   - Columnas categóricas: Colores discretos por categoría
   - Columnas numéricas: Gradiente de colores continuo

### Generación de reportes PDF

1. Configura tu gráfico como desees
2. Haz clic en "Generar Reporte PDF"
3. Descarga el archivo PDF generado

El reporte incluye:
- Tabla de datos (primeras 15 filas, máximo 6 columnas)
- Gráfico de dispersión
- Estadísticas descriptivas

## 📊 Tipos de datos soportados

### Formatos de archivo
- **CSV**: Archivos separados por comas con codificación UTF-8

### Tipos de columnas
- **Numéricas**: int64, float64 (para ejes X e Y)
- **Categóricas**: object, string (para colorear)
- **Mixtas**: Combinación de ambos tipos

### Requisitos del CSV
- Debe contener al menos una columna numérica
- Formato estándar con headers en la primera fila
- Separador de comas (,)

## 🔧 Funcionalidades técnicas

### Componentes principales

**Visualización interactiva**
- Gráficos de dispersión con zoom y pan
- Tooltips informativos
- Escalas automáticas
- Esquemas de colores adaptativos

**Generación de PDF**
- Conversión automática de Altair a matplotlib
- Tablas formateadas con bordes
- Gráficos de alta resolución (300 DPI)
- Paginación automática

**Análisis estadístico**
- Media, desviación estándar, mínimo, máximo
- Conteo de valores válidos
- Solo para columnas numéricas

### Manejo de errores

La aplicación incluye manejo robusto de errores para:
- Archivos CSV malformados
- Datos faltantes o inválidos
- Errores en la generación de gráficos
- Problemas en la creación de PDF

## 📁 Estructura del proyecto

```
├── app.py                 # Archivo principal de la aplicación
├── requirements.txt       # Dependencias de Python
├── README.md             # Este archivo
└── temp_chart.png        # Archivo temporal (se crea y elimina automáticamente)
```

## ⚠️ Limitaciones conocidas

- **Tamaño de archivo**: Archivos muy grandes (>100MB) pueden ser lentos
- **Columnas en PDF**: Máximo 6 columnas en la tabla del reporte
- **Filas en PDF**: Máximo 15 filas en la tabla del reporte
- **Tipos de gráfico**: Solo gráficos de dispersión disponibles

## 🐛 Resolución de problemas

### Error: "No se pudo generar el gráfico"
- Verifica que las columnas seleccionadas contengan datos numéricos válidos
- Asegúrate de que no hay valores NaN en las columnas de los ejes

### Error: "El archivo CSV debe contener al menos una columna numérica"
- Verifica que tu CSV tenga columnas con números
- Revisa que los números no estén formateados como texto

### Error en la instalación de dependencias
```bash
# Actualiza pip primero
pip install --upgrade pip

# Instala las dependencias una por una
pip install streamlit
pip install pandas
pip install altair
pip install fpdf2
pip install matplotlib
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa la sección de "Resolución de problemas" 
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema

## 🔄 Actualizaciones futuras

Funcionalidades planeadas:
- Soporte para más tipos de gráficos (barras, líneas, histogramas)
- Export a Excel además de PDF
- Filtros interactivos de datos
- Más opciones de personalización de gráficos
- Soporte para archivos Excel (.xlsx)
