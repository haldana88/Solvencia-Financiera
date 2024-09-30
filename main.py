import openai
import pandas as pd
import plotly.express as px
import streamlit as st

# Título del Dashboard
st.title("Análisis Financiero de Empresas")

# Cargar datos desde GitHub
url = "https://raw.githubusercontent.com/haldana88/Solvencia-Financiera/main/datos_limpios.csv"
@st.cache_data
def cargar_datos():
    return pd.read_csv(url)

datos = cargar_datos()

# Barra lateral para filtros
st.sidebar.header("Filtros")
industria = st.sidebar.multiselect(
    "Selecciona la Industria:",
    options=datos["Industria"].unique(),
    default=datos["Industria"].unique()
)

pais = st.sidebar.multiselect(
    "Selecciona el País:",
    options=datos["Pais"].unique(),
    default=datos["Pais"].unique()
)

tamano_empresa = st.sidebar.multiselect(
    "Selecciona el Tamaño de la Empresa:",
    options=datos["Tamano_Empresa"].unique(),
    default=datos["Tamano_Empresa"].unique()
)

# Filtrar datos
datos_filtrados = datos[
    (datos["Industria"].isin(industria)) &
    (datos["Pais"].isin(pais)) &
    (datos["Tamano_Empresa"].isin(tamano_empresa))
]

# Mostrar datos filtrados
st.write("### Datos Filtrados:")
st.dataframe(datos_filtrados)

st.markdown('---') # Barra Horizontal

# Descripción de los ratios
st.write("""
### Descripción de Ratios:

- **Ratio de Liquidez:** Muestra la capacidad de la empresa para cubrir sus obligaciones a corto plazo con sus activos circulantes.
- **Ratio Deuda a Patrimonio:** Indica la proporción de deuda total que tiene la empresa en comparación con su patrimonio neto.
- **Cobertura de Gastos Financieros:** Refleja la capacidad de la empresa para pagar sus gastos financieros con los ingresos totales generados.
""")

# Graficar indicadores clave
st.write("### Indicadores Financieros por Empresa")

fig_liquidez = px.bar(
    datos_filtrados, 
    x="Empresa_ID", 
    y="Ratio_de_Liquidez", 
    color="Industria", 
    title="Ratio de Liquidez por Empresa",
    color_discrete_sequence=px.colors.qualitative.Bold
)
st.plotly_chart(fig_liquidez)

fig_deuda = px.bar(
    datos_filtrados, 
    x="Empresa_ID", 
    y="Ratio_Deuda_a_Patrimonio", 
    color="Industria", 
    title="Ratio Deuda a Patrimonio por Empresa",
    color_discrete_sequence=px.colors.qualitative.Bold
)
st.plotly_chart(fig_deuda)

fig_cobertura = px.bar(
    datos_filtrados, 
    x="Empresa_ID", 
    y="Cobertura_Gastos_Financieros", 
    color="Industria", 
    title="Cobertura de Gastos Financieros por Empresa",
    color_discrete_sequence=px.colors.qualitative.Bold
)
st.plotly_chart(fig_cobertura)


st.markdown('---')


# Acceder a la API key desde secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Instanciar el cliente de OpenAI
client = openai.OpenAI(api_key=openai_api_key)


def obtener_respuesta(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Ajusta el modelo según lo que necesites
        messages=[
            {
                "role":
                "system",
                "content":
                """
            Eres un financiero amigable que trabaja para la aseguradora patito, eres experto en el área de solvencia,
            entonces vas a responder todo desde la perspectiva de la aseguradora. Contesta siempre en español
            en un máximo de 50 palabras.
            """
            },  #Solo podemos personalizar la parte de content
            {
                "role": "user",
                "content": prompt
            }
        ])
    output = response.choices[0].message.content
    return output


# Ejemplo de uso
prompt_user = st.text_area("Ingresa tu pregunta: ")
output = obtener_respuesta(prompt_user)

# Obtener la respuesta del modelo
output_modelo = obtener_respuesta(prompt_user)

# Mostrar la respuesta del modelo
st.write(output_modelo)
