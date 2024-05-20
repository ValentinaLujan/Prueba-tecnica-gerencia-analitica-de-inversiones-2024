import dash
from dash import dcc, html
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objs as go

# Conexión con la base de datos
engine = create_engine('postgresql://postgres:12345678@localhost:5432/Inversiones')

#Querys
query_portafolio_cliente = """
SELECT 
    h.id_sistema_cliente AS cliente_id,
    COUNT(*) AS total_transacciones,
    SUM(h.aba) AS suma_aba,
    AVG(h.aba) AS promedio_aba
FROM 
    historico_aba_macroactivos h
WHERE 
    h.id_sistema_cliente IS NOT NULL
GROUP BY 
    h.id_sistema_cliente
ORDER BY 
    total_transacciones DESC;
"""

query_a_m_cliente = """
SELECT 
	COALESCE(id_sistema_cliente, 'sin cliente') as id_sistema_cliente, 
    ROUND(COUNT(macroactivo) * 100.0 / (SELECT COUNT(*) FROM historico_aba_macroactivos) , 2) as porcentaje_macro,  
    ROUND(COUNT(cod_activo) * 100.0 / (SELECT COUNT(*) FROM historico_aba_macroactivos), 2) as porcentaje_activo 
FROM 
    historico_aba_macroactivos 
GROUP BY 
    id_sistema_cliente;"""

query_activo = """
WITH conteo_activos AS (
    SELECT 
        cod_activo,
        COUNT(*) AS total_activos
    FROM 
        portafolio_clientes
    GROUP BY 
        cod_activo
),
total_total_activos AS (
    SELECT 
        SUM(total_activos) AS suma_total_activos
    FROM 
        conteo_activos
)
SELECT 
    c.cod_activo,
    a.activo,
    c.total_activos,
    ROUND((c.total_activos / (SELECT suma_total_activos FROM total_total_activos)) * 100, 2) AS porcentaje_total
FROM 
    conteo_activos c
JOIN 
    catalogo_activos a ON c.cod_activo = a.cod_activo
ORDER BY 
    porcentaje_total DESC;"""

query_macroactivo = """ 
WITH conteo_macroactivos AS (
    SELECT 
        macroactivo,
        COUNT(*) AS total_macroactivos
    FROM 
        portafolio_clientes
    GROUP BY 
        macroactivo
),
total_total_macroactivos AS (
    SELECT 
        SUM(total_macroactivos) AS suma_total_macroactivos
    FROM 
        conteo_macroactivos
)
SELECT 
    c.macroactivo,
    c.total_macroactivos,
    ROUND((c.total_macroactivos / (SELECT suma_total_macroactivos FROM total_total_macroactivos)) * 100, 2) AS porcentaje_total
FROM 
    conteo_macroactivos c
ORDER BY 
    porcentaje_total DESC;"""

query_portafolio_banca = """
SELECT 
    h.cod_banca,
    cb.banca,
    COUNT(*) AS total_transacciones,
    SUM(h.aba) AS suma_aba,
    AVG(h.aba) AS promedio_aba
FROM 
    historico_aba_macroactivos h
JOIN 
    catalogo_banca cb ON h.cod_banca = cb.cod_banca
GROUP BY 
    h.cod_banca, cb.banca
ORDER BY 
    total_transacciones DESC;"""

query_m_banca = """ SELECT 
    cb.banca,
    hm.cod_banca, 
    ROUND(COUNT(hm.macroactivo) * 100.0 / (SELECT COUNT(*) FROM historico_aba_macroactivos) , 2) as porcentaje_macro
FROM
    historico_aba_macroactivos hm
JOIN
    catalogo_banca cb ON hm.cod_banca = cb.cod_banca
GROUP BY 
    hm.cod_banca,
    cb.banca;"""

query_portafolio_perfil_riesgo =  """
SELECT 
    h.cod_perfil_riesgo,
    p.perfil_riesgo,
    COUNT(*) AS total_transacciones,
    SUM(h.aba) AS suma_aba,
    AVG(h.aba) AS promedio_aba
FROM 
    historico_aba_macroactivos h
JOIN 
    cat_perfil_riesgo p ON h.cod_perfil_riesgo = p.cod_perfil_riesgo
GROUP BY 
    h.cod_perfil_riesgo, p.perfil_riesgo
ORDER BY 
    total_transacciones DESC;"""

query_m_portafolio_de_riesgo = """
SELECT 
    cpr.perfil_riesgo,
    hm.cod_perfil_riesgo, 
    ROUND(COUNT(hm.macroactivo) * 100.0 / (SELECT COUNT(*) FROM historico_aba_macroactivos) , 2) as porcentaje_macro
FROM
    historico_aba_macroactivos hm
JOIN
    cat_perfil_riesgo cpr ON hm.cod_perfil_riesgo = cpr.cod_perfil_riesgo
GROUP BY 
    hm.cod_perfil_riesgo,
    cpr.perfil_riesgo;"""

query_aba_evolucion = """
SELECT 
    DATE_TRUNC('month', DATE(h.ingestion_year || '-' || h.ingestion_month || '-01')) AS mes,
    AVG(h.aba) AS aba_promedio
FROM 
    historico_aba_macroactivos h
WHERE 
    DATE(ingestion_date) BETWEEN '2023-01-01' AND '2024-12-31'
GROUP BY 
    mes
ORDER BY 
    mes;
"""

# Lectura de las tablas como DataFrames
df_portafolio_cliente = pd.read_sql(query_portafolio_cliente, engine)
df_m_a_portafolio_cliente = pd.read_sql(query_a_m_cliente, engine)
df_macroactivo = pd.read_sql(query_macroactivo, engine)
df_activo = pd.read_sql(query_activo, engine)
df_portafolio_banca = pd.read_sql(query_portafolio_banca, engine)
df_m_a_portafolio_banca = pd.read_sql(query_m_banca, engine)
df_portafolio_perfil_riesgo = pd.read_sql(query_portafolio_perfil_riesgo, engine)
df_m_a_portafolio_perfil_riesgo = pd.read_sql(query_m_portafolio_de_riesgo, engine)
df_aba_evolucion = pd.read_sql(query_aba_evolucion, engine)

# Creación de la app en dash
app_name = 'dash-postgresqledataplot'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Gerencia analítica de inversiones 2024'

# Creación de las graficas
trace_portafolio_cliente= go.Pie(labels=df_portafolio_cliente.cliente_id, values=df_portafolio_cliente.total_transacciones, name='Total de transacciones por cliente')
trace_cliente_macro = go.Pie(labels=df_m_a_portafolio_cliente.id_sistema_cliente, values=df_m_a_portafolio_cliente.porcentaje_macro, name='Porcentaje Macroactivo')
trace_cliente_activo = go.Pie(labels=df_m_a_portafolio_cliente.id_sistema_cliente, values=df_m_a_portafolio_cliente.porcentaje_activo, name='Porcentaje Activo')
trace_macroactivo = go.Pie(labels=df_macroactivo.macroactivo, values=df_macroactivo.porcentaje_total, name='Porcentaje macroactivo')
trace_activo =  go.Pie(labels=df_activo.activo, values=df_activo.porcentaje_total, name='Porcentaje activos')
trace_portafolio_banca = go.Bar(x=df_portafolio_banca.banca, y=df_portafolio_banca.promedio_aba, name='Portafolio banca', marker=dict(color=['#fb6f92', '#ff8fab', '#ffb3c6', '#ffc2d1', '#ffe5ec']))
trace_m_portafolio_banca = go.Bar(x=df_m_a_portafolio_banca.banca, y=df_m_a_portafolio_banca.porcentaje_macro, name='Porcentaje de macroactivos en portafolio banca', marker=dict(color=['#fb6f92', '#ff8fab', '#ffb3c6', '#ffc2d1', '#ffe5ec']))
trace_perfil_riesgo = go.Bar(x=df_portafolio_perfil_riesgo.perfil_riesgo, y=df_portafolio_perfil_riesgo.promedio_aba, name='Portafolio perfil de riesgo', marker=dict(color=['#318CE7', '#6aa9e9', '#98c3ed', '#afcdea']))
trace_m_perfil_riesgo = go.Bar(x=df_m_a_portafolio_perfil_riesgo.perfil_riesgo, y=df_m_a_portafolio_perfil_riesgo.porcentaje_macro, name='Porcentaje de macroactivos en portafolio perfil de riesgo', marker=dict(color=['#318CE7', '#6aa9e9', '#98c3ed', '#afcdea']))
trace_aba = go.Bar(x=df_aba_evolucion.mes, y=df_aba_evolucion.aba_promedio, name='Evolución ABA', marker=dict(color=['#4A148C', '#6A1B9A', '#7B1FA2', '#8E24AA', '#9C27B0', '#AB47BC', '#BA68C8', '#CE93D8']))

app.layout = html.Div(children=[
    html.H1("Total de transacciones por cliente", style={'textAlign': 'center'}),
    dcc.Graph(
        id='Portafolio-Clientes-Relacion-entre-el-total-de-transacciones-y-el-promedio-de-ABA',
        figure={'data': [trace_portafolio_cliente],
                'layout':go.Layout(showlegend= True)
        }
    ),

    html.Div([
        html.Div([
            html.H1("Porcentaje macroactivos por cliente", style={'textAlign': 'center'}),
            dcc.Graph(
                id='portafolio-macro-cliente',
                figure={'data': [trace_cliente_macro],
                        'layout': go.Layout(showlegend=True)
                }
            )
        ], className='six columns'),  # Divide en 6 columnas

        html.Div([
            html.H1("Porcentaje activos por cliente", style={'textAlign': 'center'}),
            dcc.Graph(
                id='Portafolio-activo-cliente',
                figure={'data': [trace_cliente_activo],
                        'layout': go.Layout(showlegend=True)
                }
            )
        ], className='six columns')  # Divide en 6 columnas
    ], className='row'),  # Divide en una fila

    html.Div([
        html.Div([
            html.H1("Portafolio banca", style={'textAlign': 'center'}),
            dcc.Graph(
                id='portafolio-banca',
                figure={'data': [trace_portafolio_banca],
                        'layout': go.Layout(barmode='stack', xaxis_title='Banca', yaxis_title='Promedio ABA')
                }
            )
        ], className='six columns'),  # Divide en 6 columnas

        html.Div([
            html.H1("Porcentaje de macroactivos", style={'textAlign': 'center'}),
            dcc.Graph(
                id='portafolio-banca-macro',
                figure={'data': [trace_m_portafolio_banca],
                        'layout': go.Layout(barmode='stack', xaxis_title='Banca', yaxis_title='Porcentaje macroactivos')
                }
            )
        ], className='six columns')  # Divide en 6 columnas
    ], className='row'),  # Divide en una fila

    html.Div([
        html.Div([
            html.H1("Portafolio perfil de riesgo", style={'textAlign': 'center'}),
            dcc.Graph(
                id='p-perfil-riesgo',
                figure={'data': [trace_perfil_riesgo],
                        'layout': go.Layout(barmode='stack', xaxis_title='Perfil de riesgo', yaxis_title='Promedio ABA')
                }
            )
        ], className='six columns'),  # Divide en 6 columnas

        html.Div([
            html.H1("Porcentaje de macroactivos por perfil de riesgo", style={'textAlign': 'center'}),
            dcc.Graph(
                id='p-perfil-riesgo-macro',
                figure={'data': [trace_m_perfil_riesgo],
                        'layout': go.Layout(barmode='stack', xaxis_title='Perfil de riesgo', yaxis_title='Porcentaje macroactivos')
                }
            )
        ], className='six columns')  # Divide en 6 columnas
    ], className='row'),  # Divide en una fila

    html.H1("Evolución mes a mes del ABA (Activos Bajo Administración) promedio", style={'textAlign': 'center'}),
    dcc.Graph(
        id='evolucion_ABA',
        figure={'data': [trace_aba],
                'layout': go.Layout(barmode='stack', xaxis_title='Mes', yaxis_title='Promedio ABA')
        }
    ),

    html.H1("Porcentaje de macroactivos", style={'textAlign': 'center'}),
    dcc.Graph(
        id='porcentaje-macroactivos',
        figure={'data': [trace_macroactivo],
                'layout': go.Layout(showlegend=True)
        }
    ),

    html.H1("Porcentaje de activos", style={'textAlign': 'center'}),
    dcc.Graph(
        id='porcentaje-activos',
        figure={'data': [trace_activo],
                'layout': go.Layout(showlegend=True)
        }
    ),
], className="container")


if __name__ == '__main__':
    app.run_server(debug=True)
