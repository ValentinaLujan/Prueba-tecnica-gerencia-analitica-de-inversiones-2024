import pandas as pd
from sqlalchemy import create_engine

# Configurar la conexión a PostgreSQL
# IMPORTANTE: En esta parte se debe agregar la configuración de usuario antes de ejecutar
engine = create_engine('postgresql://usuario:contraseña@localhost:5432/Inversiones')

# Cargar y poblar datos en las tablas
def cargar_datos():
    # Cargar CSVs en dataframes con la libreria pandas
    cat_perfil_riesgo = pd.read_csv(r'data\cat_perfil_riesgo.csv')
    catalogo_activos = pd.read_csv(r'data\catalogo_activos.csv')
    catalogo_banca = pd.read_csv(r'data\catalogo_banca.csv')
    historico_aba_macroactivos = pd.read_csv(r'data\historico_aba_macroactivos.csv')

    # Poblar tablas
    cat_perfil_riesgo.to_sql('cat_perfil_riesgo', engine, if_exists='append', index=False)
    catalogo_activos.to_sql('catalogo_activos', engine, if_exists='append', index=False)
    catalogo_banca.to_sql('catalogo_banca', engine, if_exists='append', index=False)

    historico_aba_macroactivos = historico_aba_macroactivos.replace('', None) #Ajustar espacios vacios con la palabra reservada
    historico_aba_macroactivos = historico_aba_macroactivos.replace('None', None) #Ajustar espacios con la palabra 'None' para que sean tomados como nulos
    historico_aba_macroactivos.to_sql('historico_aba_macroactivos', engine, if_exists='append', index=False)

#Entry point
if __name__ == '__main__':
    cargar_datos()
    print("Datos cargados exitosamente.")
