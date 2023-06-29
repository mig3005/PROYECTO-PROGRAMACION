import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gdown
import os

#Título
st.title('Casos Positivos de Covid-19 en el Perú')
st.subheader("Miembros del equipo")
st.markdown("""
- Isabel Muñoz
- Enzo Baltazar
- Joel Huillca
- Stephany Samanez
- Lucero de la Cruz
- Leonardo Plasencia
""")
st.markdown("""
---
La información contenida en esta página web permite acceder al Dataset “Casos positivos por COVID-19” 
elaborado por el Ministerio de Salud (MINSA) del Perú. Este ha registrado el monitoreo diario de los 
casos positivos de covid-19 confirmados con cualquier tipo de prueba hasta el día 23 de mayo de 2022. 
Cada registro es equivalente a una persona, así como su sexo, edad y distintos niveles de ubicación geográfica: 
departamento, provincia y distrito. 

Fuente de datos: (https://www.datosabiertos.gob.pe/dataset/casos-positivos-por-covid-19-ministerio-de-salud-minsa)

---
""")
st.markdown("""
Para poder visualizar la información de una zona geográfica en específico del Perú, seleccione el nombre de un departamento, provincia y distrito.
""")

#Lectura de datos desde CSV
#id = 1op-iq0XhBXBQOPlagCPE9TzFsFkkNVjQ
if not os.path.exists('downloads'):
  os.makedirs('downloads')

@st.experimental_memo
def download_data():
  #https://drive.google.com/uc?id=
  url = "https://drive.google.com/uc?id=1op-iq0XhBXBQOPlagCPE9TzFsFkkNVjQ"
  output = "downloads/data.csv"
  gdown.download(url,output,quiet = False)
  
download_data()
df = pd.read_csv("downloads/data.csv", sep = ";", parse_dates = ["FECHA_CORTE","FECHA_RESULTADO"])
#Simplificacion del dataset (retiro de columnas)
df = df.drop(columns = ["FECHA_CORTE","FECHA_RESULTADO","UBIGEO","id_persona"])

#Sistema de filtros

#Construccion del set/list de departamentos (Valores unicos sin NA)
set_departamentos = np.sort(df['DEPARTAMENTO'].dropna().unique())
#Seleccion del departamento
opcion_departamento = st.selectbox('Selecciona un departamento', set_departamentos)
df_departamentos = df[df['DEPARTAMENTO'] == opcion_departamento]
num_filas = len(df_departamentos.axes[0]) 

#Construccion del set/list de provincias (Valores unicos sin NA)
set_provincias = np.sort(df_departamentos['PROVINCIA'].dropna().unique())
#Seleccion de la provincia
opcion_provincia = st.selectbox('Selecciona una provincia', set_provincias)
df_provincias = df_departamentos[df_departamentos['PROVINCIA'] == opcion_provincia]
num_filas = len(df_provincias.axes[0]) 

#Construccion del set/list de distritos (Valores unicos sin NA)
set_distritos = np.sort(df_departamentos['DISTRITO'].dropna().unique())
#Seleccion de la distrito
opcion_distrito = st.selectbox('Selecciona un distrito', set_distritos)
df_distritos = df_departamentos[df_departamentos['DISTRITO'] == opcion_distrito]
num_filas = len(df_distritos.axes[0]) 

st.write('Numero de registros:', num_filas)

#Gráficas

#Gráfica de pie de METODODX
df_metododx = df_distritos.METODODX.value_counts()
df_metododx = pd.DataFrame(df_metododx)
df_metododx = df_metododx.reset_index()  
df_metododx.columns = ['METODODX', 'Total']

fig1, ax1 = plt.subplots()
ax1.pie(df_metododx['Total'], labels=df_metododx['METODODX'], autopct='%1.1f%%')
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.write('Distribución por METODODX:')
st.pyplot(fig1)

#Gráfica de barras de SEXO
df_SEXO = df_distritos.SEXO.value_counts()
st.write('Distribución por SEXO:')
st.bar_chart(df_SEXO)

#Gráfica de barras de EDAD
df_edad = df_distritos.EDAD.value_counts()
st.write('Distribución por EDAD:')
st.bar_chart(df_edad)
