import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Dashboard Financiero", layout="wide")

# Función para cargar los datos
@st.cache_data
def load_data():
    # Cargamos los datos del CSV proporcionado
    df = pd.read_csv('datos_limpios.csv')
    return df

# Cargar los datos
df = load_data()

# Función para aplicar filtros
def apply_filters(df, industrias, paises, empresas, tamanios):
    if industrias:
        df = df[df['Industria'].isin(industrias)]
    if paises:
        df = df[df['Pais'].isin(paises)]
    if empresas:
        df = df[df['Empresa_ID'].isin(empresas)]
    if tamanios:
        df = df[df['Tamano_Empresa'].isin(tamanios)]
    return df

# Barra lateral para filtros
st.sidebar.header("Filtros")

# Filtro de industria
industrias = st.sidebar.multiselect(
    "Selecciona industrias",
    options=df['Industria'].unique(),
    default=[]
)

# Filtro de país
paises = st.sidebar.multiselect(
    "Selecciona países",
    options=df['Pais'].unique(),
    default=[]
)

# Filtro de empresa
empresas = st.sidebar.multiselect(
    "Selecciona empresas",
    options=df['Empresa_ID'].unique(),
    default=[]
)

# Filtro de tamaño de empresa
tamanios = st.sidebar.multiselect(
    "Selecciona tamaños de empresa",
    options=df['Tamano_Empresa'].unique(),
    default=[]
)

# Aplicar filtros
df_filtered = apply_filters(df, industrias, paises, empresas, tamanios)

# Contenido principal
st.title("Dashboard Financiero")

# Mostrar mensaje sobre los filtros aplicados
st.write(f"Mostrando datos para {len(df_filtered)} empresas")

# Mostrar ratios financieros
st.header("Ratios Financieros")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Ratio de Liquidez Promedio", f"{df_filtered['Ratio_de_Liquidez'].mean():.2f}")

with col2:
    st.metric("Ratio Deuda a Patrimonio Promedio", f"{df_filtered['Ratio_Deuda_a_Patrimonio'].mean():.2f}")

with col3:
    st.metric("Cobertura de Gastos Financieros Promedio", f"{df_filtered['Cobertura_Gastos_Financieros'].mean():.2f}")

# Visualizaciones
st.header("Visualizaciones")

# Gráfico de barras para comparar ratios entre empresas
fig_barras = px.bar(df_filtered, x='Empresa_ID', y=['Ratio_de_Liquidez', 'Ratio_Deuda_a_Patrimonio', 'Cobertura_Gastos_Financieros'], 
                    title="Comparación de Ratios por Empresa", barmode='group')
st.plotly_chart(fig_barras, use_container_width=True)

# Gráfico de dispersión para ver relaciones entre ratios
fig_scatter = px.scatter(df_filtered, x='Ratio_de_Liquidez', y='Ratio_Deuda_a_Patrimonio', 
                         size='Cobertura_Gastos_Financieros', color='Industria', 
                         hover_name='Empresa_ID', 
                         title="Relación entre Ratio de Liquidez y Ratio Deuda a Patrimonio")
st.plotly_chart(fig_scatter, use_container_width=True)

# Gráfico circular para mostrar la distribución por industria
fig_pie = px.pie(df_filtered, names='Industria', title="Distribución por Industria")
st.plotly_chart(fig_pie, use_container_width=True)

# Gráfico de caja para mostrar la distribución de los ratios por país
fig_box = px.box(df_filtered, x='Pais', y=['Ratio_de_Liquidez', 'Ratio_Deuda_a_Patrimonio', 'Cobertura_Gastos_Financieros'], 
                 title="Distribución de Ratios por País")
st.plotly_chart(fig_box, use_container_width=True)

# Añadir un botón de descarga
csv = df_filtered.to_csv(index=False)
st.download_button(
    label="Descargar datos filtrados como CSV",
    data=csv,
    file_name="datos_financieros_filtrados.csv",
    mime="text/csv",
)