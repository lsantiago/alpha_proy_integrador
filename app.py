import streamlit as st
import pandas as pd
import altair as alt
import io
from fpdf import FPDF
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import warnings

# Suppress fpdf warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, 'Reporte de Datos', new_x='LMARGIN', new_y='NEXT', align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', new_x='RIGHT', new_y='TOP', align='C')

def convert_altair_to_matplotlib(chart_data, x_axis, y_axis, color_axis=None):
    """
    Convierte datos de Altair a un gráfico matplotlib para incluir en PDF
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if color_axis and color_axis != "(Ninguno)":
        # Gráfico con colores por categoría
        if chart_data[color_axis].dtype in ['object', 'category']:
            unique_vals = chart_data[color_axis].unique()
            colors = plt.cm.Set3(range(len(unique_vals)))
            for i, val in enumerate(unique_vals):
                mask = chart_data[color_axis] == val
                ax.scatter(chart_data[mask][x_axis], chart_data[mask][y_axis], 
                          c=[colors[i]], label=str(val), alpha=0.7, s=50)
            ax.legend()
        else:
            # Colorear por valores numéricos
            scatter = ax.scatter(chart_data[x_axis], chart_data[y_axis], 
                               c=chart_data[color_axis], cmap='viridis', alpha=0.7, s=50)
            plt.colorbar(scatter, ax=ax, label=color_axis)
    else:
        # Gráfico simple sin colores
        ax.scatter(chart_data[x_axis], chart_data[y_axis], alpha=0.7, s=50)
    
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title('Gráfico de Dispersión....')
    ax.grid(True, alpha=0.3)
    
    # Guardar en buffer
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer

def create_pdf_report(df, chart_data, x_axis, y_axis, color_axis, stats):
    pdf = PDF()
    pdf.add_page()

    # Título de la tabla de datos
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'Tabla de Datos', new_x='LMARGIN', new_y='NEXT', align='L')
    pdf.set_font('Helvetica', '', 9)

    # Cabecera de la tabla
    cols = df.columns[:6]  # Limitar a 6 columnas para que quepa en la página
    col_width = (pdf.w - 20) / len(cols)
    
    for col in cols:
        pdf.cell(col_width, 8, str(col)[:15], border=1, new_x='RIGHT', new_y='TOP')
    pdf.ln()

    # Contenido de la tabla (solo primeras 15 filas)
    for index, row in df.head(15).iterrows():
        for col in cols:
            cell_value = str(row[col])[:15] if pd.notna(row[col]) else ''
            pdf.cell(col_width, 8, cell_value, border=1, new_x='RIGHT', new_y='TOP')
        pdf.ln()

    # Nueva página para el gráfico
    pdf.add_page()

    # Gráfico
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'Gráfico de Dispersión', new_x='LMARGIN', new_y='NEXT', align='L')
    
    try:
        # Convertir gráfico de Altair a matplotlib
        chart_img = convert_altair_to_matplotlib(chart_data, x_axis, y_axis, color_axis)
        
        # Crear archivo temporal para la imagen
        temp_img_path = 'temp_chart.png'
        with open(temp_img_path, 'wb') as f:
            f.write(chart_img.getvalue())
        
        pdf.image(temp_img_path, x=10, y=None, w=190)
        
        # Limpiar archivo temporal
        import os
        os.remove(temp_img_path)
        
    except Exception as e:
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 10, f'No se pudo generar el gráfico: {str(e)}', new_x='LMARGIN', new_y='NEXT', align='L')

    # Estadísticas
    pdf.ln(20)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'Estadísticas Descriptivas', new_x='LMARGIN', new_y='NEXT', align='L')
    pdf.set_font('Helvetica', '', 9)
    
    # Procesar estadísticas de manera más controlada
    numeric_cols = stats.columns[:4]  # Limitar columnas para que quepa
    
    # Encabezados de estadísticas
    pdf.cell(30, 8, 'Estadística', border=1, new_x='RIGHT', new_y='TOP')
    for col in numeric_cols:
        pdf.cell(35, 8, str(col)[:10], border=1, new_x='RIGHT', new_y='TOP')
    pdf.ln()
    
    # Filas de estadísticas
    for stat_name in ['count', 'mean', 'std', 'min', 'max']:
        if stat_name in stats.index:
            pdf.cell(30, 8, stat_name, border=1, new_x='RIGHT', new_y='TOP')
            for col in numeric_cols:
                value = stats.loc[stat_name, col]
                if pd.notna(value):
                    if isinstance(value, (int, float)):
                        formatted_value = f"{value:.2f}"
                    else:
                        formatted_value = str(value)[:8]
                else:
                    formatted_value = "N/A"
                pdf.cell(35, 8, formatted_value, border=1, new_x='RIGHT', new_y='TOP')
            pdf.ln()

    return bytes(pdf.output())

# Configuración de la página
st.set_page_config(page_title="Visualizador de Datos", layout="wide")

st.title("Visualizador de Datos y Generador de Reportes PDF")

# Información sobre dependencias
with st.expander("Información sobre dependencias"):
    st.write("""
    Para usar esta aplicación correctamente, asegúrate de tener instaladas las siguientes dependencias:
    
    ```bash
    pip install streamlit pandas altair fpdf2 matplotlib
    ```
    
    **Nota:** Esta versión usa matplotlib para generar gráficos en PDF, evitando problemas de compatibilidad.
    """)

# Carga de archivo
uploaded_file = st.file_uploader("Seleccione un archivo CSV", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("Datos del archivo CSV:")
        st.dataframe(df)

        st.divider()

        st.header("Opciones del Gráfico Dinámico")

        # Opciones dinámicas
        columns = df.columns.tolist()
        
        # Filtrar solo columnas numéricas para ejes X e Y
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        if not numeric_columns:
            st.error("El archivo CSV debe contener al menos una columna numérica.")
            st.stop()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            x_axis = st.selectbox("Seleccione el eje X", numeric_columns, index=0)
        with col2:
            y_axis = st.selectbox("Seleccione el eje Y", numeric_columns, index=min(1, len(numeric_columns)-1))
        with col3:
            color_axis = st.selectbox("Colorear por", ["(Ninguno)"] + columns)

        # Crear el gráfico interactivo con Altair
        color_encoding = alt.value('steelblue')  # Color por defecto
        if color_axis != "(Ninguno)":
            if df[color_axis].dtype in ['object', 'category']:
                color_encoding = alt.Color(color_axis, scale=alt.Scale(scheme='category10'))
            else:
                color_encoding = alt.Color(color_axis, scale=alt.Scale(scheme='viridis'))

        chart = alt.Chart(df).mark_point(size=100).encode(
            x=alt.X(x_axis, type='quantitative'),
            y=alt.Y(y_axis, type='quantitative'),
            tooltip=columns,
            color=color_encoding
        ).interactive().properties(
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)

        # Calcular estadísticas solo para columnas numéricas
        numeric_df = df.select_dtypes(include=['number'])
        stats = numeric_df.describe()

        # Botón de descarga de PDF
        if st.button("Generar Reporte PDF"):
            with st.spinner("Generando PDF..."):
                try:
                    pdf_bytes = create_pdf_report(df, df, x_axis, y_axis, color_axis, stats)
                    st.download_button(
                        label="Descargar Reporte en PDF",
                        data=pdf_bytes,
                        file_name="reporte.pdf",
                        mime="application/pdf"
                    )
                    st.success("PDF generado exitosamente!")
                except Exception as e:
                    st.error(f"Error al generar PDF: {e}")

        st.divider()

        # Mostrar datos estadísticos
        st.header("Estadísticas de los Datos")
        st.write(stats)

    except Exception as e:
        st.error(f"Se produjo un error: {e}")
        st.write("Asegúrate de que el archivo CSV esté correctamente formateado.")
