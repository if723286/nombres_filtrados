import streamlit as st
import pandas as pd
from io import BytesIO

# Título de la aplicación
st.title("Filtrar Base de Datos de Alumnos")

# Subir los archivos
st.subheader("Sube los archivos Excel")
uploaded_file_db = st.file_uploader("Sube la base de datos de alumnos", type=["xlsx"])
uploaded_file_filter = st.file_uploader("Sube el archivo con los nombres a filtrar", type=["xlsx"])

if uploaded_file_db and uploaded_file_filter:
    # Cargar los datos
    try:
        # Leer los archivos Excel
        db_data = pd.read_excel(uploaded_file_db)
        filter_data = pd.read_excel(uploaded_file_filter)

        # Mostrar las primeras filas de los datos
        st.subheader("Vista previa de la base de datos:")
        st.write(db_data.head())

        st.subheader("Vista previa del archivo de nombres:")
        st.write(filter_data.head())

        # Asegurarse de que los archivos tienen las columnas necesarias
        if "Nombre" in db_data.columns and "Nombre" in filter_data.columns:
            # Convertir los nombres a minúsculas para ignorar las diferencias de mayúsculas y minúsculas
            db_data["Nombre"] = db_data["Nombre"].str.lower()
            filter_data["Nombre"] = filter_data["Nombre"].str.lower()

            # Filtrar la base de datos
            filtered_data = db_data[db_data["Nombre"].isin(filter_data["Nombre"])]

            # Mostrar los resultados
            st.subheader("Resultados filtrados:")
            st.write(filtered_data)

            # Función para convertir el DataFrame a Excel
            def convert_df(df):
                # Crear un buffer en memoria para almacenar el archivo Excel
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                buffer.seek(0)
                return buffer

            # Convertir los datos filtrados a un archivo Excel
            result_file = convert_df(filtered_data)

            # Crear el botón de descarga
            st.subheader("Descargar los resultados:")
            st.download_button(
                label="Descargar Excel",
                data=result_file,
                file_name="filtered_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.error("Asegúrate de que ambos archivos tienen una columna llamada 'Nombre'.")
    except Exception as e:
        st.error(f"Error al procesar los archivos: {e}")
else:
    st.info("Por favor, sube ambos archivos Excel para continuar.")



