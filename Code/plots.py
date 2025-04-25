import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


def boxplot(df, jugador, variable, jugador_col="player"):
    
    """
    Muestra un BoxPlot con todos los jugadores, destacando el jugador que se quiere analizar. A la derecha del BoxPlot se muestra el percentil del jugador

    Argumentos:
    df: Data Frame donde cada fila representa las stats de un jugador
    jugador: jugador que se quiere destacar en el boxplot
    variable: nombre de la variable que se quiere mostrar
    jugador_col: nombre de la columna que contiene los nombres de los jugadores

    """

    if jugador not in df[jugador_col].values:
        raise ValueError(f"El jugador '{jugador}' no está en la columna '{jugador_col}'.")

    
    

    fig = go.Figure()

    # Boxplot
    fig.add_trace(go.Box(
    x=df[variable],
    y=[0]*len(df),
    orientation='h',
    boxpoints=False,     # No muestra puntos
    fillcolor='rgba(255, 100, 100, 0.2)',
    line=dict(color='rgba(255,100,100,0.8)'),
    hoverinfo='skip',    # Desactiva hover
    showlegend=False
))

    fig.update_layout(
    xaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=False, ticks='', hoverformat=False),
    yaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=False,ticks='', hoverformat=False),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=10, r=10, t=10, b=10)
)
    
    #Añadir los puntos personalizados
    fig.add_trace(go.Scatter(
        x=df[variable],
        y=[0]*len(df),
        mode='markers',
        marker=dict(
            color='orange',
            size=4,
            opacity=0.8
        ),
        customdata=df[['player']],
        hovertemplate="Jugador: %{customdata[0]}<br>" + f"{variable}: " + "%{x:.2f}<extra></extra>",
        showlegend=False
    ))

    # Marcar un jugador destacado
    highlighted = df[df['player'] == jugador]
    fig.add_trace(go.Scatter(
        x=highlighted[variable],
        y=[0],
        mode='markers',
        marker=dict(
            color='crimson',
            size=8,
            line=dict(color='black', width=1)
        ),
        customdata=highlighted[['player']],
        hovertemplate="Jugador: %{customdata[0]}<br>" + f"{variable}: " + "%{x:.2f}<extra></extra>",
        showlegend=False
    ))
    
    fig.update_layout(
    yaxis=dict(visible=False)  # en vez de múltiples flags
        )
    return fig


def radar_chart(df, player, variables, comparation = 'mean', jugador_col="player"):

    """
    Muestra un RadarPlot comparando las stats de un jugador con una media o con otro jugador a elegir.

    Argumentos:
    df: Data Frame donde cada fila representa las stats de un jugador. Preferiblemente escalado con las variables entre 0 y 1.
    jugador: nombre del jugador que se quiere analizar
    variables: lista con el nombre de las variables que se quiere mostrar
    comparation: nombre del jugador con el que comparar. Por defecto, se calcula la media de todos los datos de entrada
    jugador_col: nombre de la columna que contiene los nombres de los jugadores
    """


    if player not in df[jugador_col].values:
        raise ValueError(f"El jugador '{player}' no está disponible.")
    
    if comparation == 'position':
        
        position = df[df[jugador_col] == player]['position'].values[0]
        stats_jugador1 = df[df[jugador_col] == player][variables].values.flatten().tolist()
        stats_jugador2 = df[df['position']==position][variables].mean().tolist()
            # Cierre del radar chart (repetir el primer valor al final)
        stats_jugador1 += [stats_jugador1[0]]
        stats_jugador2 += [stats_jugador2[0]]
        categorias = variables + [variables[0]]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
        r=stats_jugador1,
        theta=categorias,
        fill='toself',
        line=dict(color='crimson'),
        fillcolor='rgba(220, 20, 60, 0.4)',
        name=player
    ))

        fig.add_trace(go.Scatterpolar(
            r=stats_jugador2,
            theta=categorias,
            fill='toself',
            line=dict(color='orange'),
            fillcolor='rgba(255, 165, 0, 0.4)',
            name=f'Promedio {position}'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    linewidth=1,
                    gridcolor="lightgray",
                    range=[0, 1]
                )
            ),
            showlegend=False
        )

        return fig
    
    elif comparation == 'mean':

        stats_jugador1 = df[df[jugador_col] == player][variables].values.flatten().tolist()
        stats_jugador2 = df[variables].mean().tolist()
            # Cierre del radar chart (repetir el primer valor al final)
        stats_jugador1 += [stats_jugador1[0]]
        stats_jugador2 += [stats_jugador2[0]]
        categorias = variables + [variables[0]]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
        r=stats_jugador1,
        theta=categorias,
        fill='toself',
        line=dict(color='crimson'),
        fillcolor='rgba(220, 20, 60, 0.4)',
        name=player
    ))

        fig.add_trace(go.Scatterpolar(
            r=stats_jugador2,
            theta=categorias,
            fill='toself',
            line=dict(color='orange'),
            fillcolor='rgba(255, 165, 0, 0.4)',
            name='Promedio General'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    linewidth=1,
                    gridcolor="lightgray",
                    range=[0, 1]
                )
            ),
            showlegend=False
        )

        return fig


    elif comparation not in df[jugador_col].values:

        raise ValueError(f"El jugador '{comparation}' no está disponible.")
    
    else:

        stats_jugador1 = df[df[jugador_col] == player][variables].values.flatten().tolist()
        stats_jugador2 = df[df[jugador_col] == comparation][variables].values.flatten().tolist()
            # Cierre del radar chart (repetir el primer valor al final)
        stats_jugador1 += [stats_jugador1[0]]
        stats_jugador2 += [stats_jugador2[0]]
        categorias = variables + [variables[0]]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
        r=stats_jugador1,
        theta=categorias,
        fill='toself',
        line=dict(color='crimson'),
        fillcolor='rgba(220, 20, 60, 0.4)',
        name=player
    ))

        fig.add_trace(go.Scatterpolar(
            r=stats_jugador2,
            theta=categorias,
            fill='toself',
            line=dict(color='orange'),
            fillcolor='rgba(255, 165, 0, 0.4)',
            name=comparation
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    linewidth=1,
                    gridcolor="lightgray",
                    range=[0, 1],
                    tickfont=dict(size=10)
                ),
                angularaxis=dict(
                    tickfont=dict(size=10)
                )
            ),
            showlegend=True,
            margin=dict(t=60, b=20, l=20, r=20)
        )

        return fig

def indicator(variable, value):

    fig = go.Indicator(
            mode="number",
            value=value,  # tu percentil como valor
            number={
                "suffix": "%",
                "font": {"size": 20, "color": "crimson" ,"family":"Montserrat Bold, Montserrat, sans-serif"}
            },
            title={
                "text": f"<span style='font-size:11px;color:gray'><b>Perc. {variable}</b></span>",
            },
            domain={"x": [0, 1], "y": [0, 1]}
            
        )
    
    return fig

def indicator_total(value):

    fig = go.Indicator(
            mode="number",
            value=value,  # tu percentil como valor
            number={
                "font": {"size": 28, "color": "crimson", "family":"Montserrat, sans-serif"}
            },
            title={
                "text": f"<span style='font-size:14px;color:gray'><b>Total temporada</b></span>",
            },
            domain={"x": [0, 1], "y": [0, 1]}
            
        )
    
    return fig

def comparative_report(df, variables, player, jugador_col='player', comp="mean"):

    if len(variables) !=4:
        raise ValueError(f"El nº de variables para mostrar en el informe es de 4")
    
    specs = [
    [{'type': 'indicator'}, {'type': 'xy'}, {'type': 'polar', 'rowspan': 2}],  # Radar 1 ocupa fila 1-2
    [{'type': 'indicator'}, {'type': 'xy'}, None],
    [{'type': 'indicator'}, {'type': 'xy'}, {'type': 'polar', 'rowspan': 2}],  # Radar 2 ocupa fila 3-4
    [{'type': 'indicator'}, {'type': 'xy'}, None]
]



    dashboard = make_subplots(
        rows=4, cols=3,
        column_widths=[0.05, 0.6, 0.35],
        row_heights=[0.25]*4,
        specs=specs,
        horizontal_spacing=0.08,
        vertical_spacing=0.08,
        subplot_titles=["", "", "<b style='color:crimson'>Comparación Rendimiento Ofensivo</b>",
                        "", "",
                        "", "","<b style='color:crimson'>Comparación Rendimiento Creación</b>",
                        "", ""],
        column_titles = ["",f"<b style='color:crimson'>Situación respecto del resto de jugadores</b>",""]
    ) 

    for num, var in enumerate(variables):

        #Añadir los boxplots
        fig = boxplot(df, player, var)
        for trace in fig.data:
            dashboard.add_trace(trace, row = num+1, col=2)
        
        
        # Anotación de los KPI (percentil)
        kpi_percentil = df.loc[df[jugador_col] == player, f'{var}_perc'].values[0]
        
        dashboard.add_trace(indicator(var,kpi_percentil), row = num+1, col=1)

    for i in range(4):
        dashboard.update_yaxes(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            showline=True,
            ticks='',
            row=i+1,
            col=2
        )

    vars = ['Pases', 'Shot_Assist', 'Assist', 'Centros_Area',
       'Porc_Pase', 'Regates_Int', 'Regates_Comp', 'Recuperaciones',
       'Despejes', 'Perdidas', 'Errores', 'Tiros', 'xG_per_90', 'Goles']
    
    vars_ofensivas = ['Pases', 'Shot_Assist', 'Assist','Tiros', 'xG_per_90', 'Goles']
    vars_defensivas = ['Regates_Int', 'Regates_Comp',  'Centros_Area','Porc_Pase', 'Pases']


    data_scaled = df.copy()
    data_scaled = data_scaled[vars + ['player','position']]

    min_vals = data_scaled[vars].min()
    max_vals = data_scaled[vars].max()
    data_scaled[vars] = (data_scaled[vars] - min_vals) / (max_vals - min_vals)

    # Radar ofensivo en filas 1-2
    fig_of = radar_chart(data_scaled, player, vars_ofensivas, comparation=comp)
    for trace in fig_of.data:
        dashboard.add_trace(trace, row=1, col=3)

    # Radar defensivo en filas 3-4
    fig_def = radar_chart(data_scaled, player, vars_defensivas, comparation=comp)
    for trace in fig_def.data:
        dashboard.add_trace(trace, row=3, col=3)

    
    dashboard.update_layout(
        template='simple_white',
        width=1000, height=800,
        showlegend=False,
        paper_bgcolor='rgba(240, 248, 255, 0.6)',  # fondo pastel claro
        plot_bgcolor='rgba(255, 255, 255, 0.0)',
        font=dict(family="Montserrat, sans-serif", color="black"),
        title=dict(
            text=f"Informe de Rendimiento de {player}.<br>Comparación con el resto de jugadores",
            font=dict(size=18, color="crimson", family="Montserrat, sans-serif"),
            x=0.5,
            xanchor='center'
        ),
        polar=dict(
            bgcolor='rgba(255,255,255,0)',
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                showline=True,
                showgrid=True,
                gridcolor="lightgray",
                gridwidth=1,
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=10)
            )
        ),
        polar2=dict(
            bgcolor='rgba(255,255,255,0)',
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                showline=True,
                showgrid=True,
                gridcolor="lightgray",
                gridwidth=1,
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=10)
            )
        )
    )

    return dashboard


def barchart_eventing(df, event,jornada_col='match_day', color='crimson'):
    """
    Genera un gráfico de barras con la distribución de eventos por jornada.

    Parámetros:
        df (pd.DataFrame): dataframe ya filtrado al evento y jugadores deseados deseado
        event: Nombre del evento que se va a mostrar
        jornada_col (str): nombre de la columna que indica la jornada
        color (str): color base para barras y puntos
    """
    # Agrupar por jornada
    counts = df[jornada_col].value_counts().sort_index()
    jornadas = counts.index.tolist()
    valores = counts.values.tolist()

    hovertemplate = (
        "Jornada: %{x}<br>"
        f"{event}:"+" %{y}<extra></extra>"
    )

    bar = go.Bar(
        x=jornadas,
        y=valores,
        marker_color=color,
        opacity=0.3,
        width=0.4,
        showlegend=False,
        hovertemplate=hovertemplate
    )

    dots = go.Scatter(
        x=jornadas,
        y=valores,
        mode='markers',
        marker=dict(color=color, size=7),
        showlegend=False,
        hovertemplate=hovertemplate
    )

    fig = go.Figure(data=[bar, dots])

    # Estética del gráfico
    fig.update_layout(
        template='simple_white',
        margin=dict(l=40, r=20, t=40, b=40),
        xaxis_title='Jornada',
        yaxis_title='',
        xaxis=dict(tickmode='linear', tick0=1, dtick=1, range=[0.5, max(jornadas)+0.5]),
        yaxis=dict(range=[0, max(valores) + 1]),
        height=300,
        width=600,
        title=dict(
            text=f"{event} por jornada",
            x=0.5,
            font=dict(size=16, color=color)
        )
    )

    return fig


def draw_eventing_data(df, x_col='x', y_col='y', color_col=None):
    """
    Dibuja un campo de fútbol en orientación vertical y grafica eventos.

    Args:
        df (pd.DataFrame): DataFrame con los datos de eventos.
        x_col (str): Nombre de la columna para coordenada X.
        y_col (str): Nombre de la columna para coordenada Y.
        color_col (str, optional): Nombre de la columna para usar como color. Default es None.

    Returns:
        go.Figure: Objeto Plotly con el campo y eventos.
    """
    # Crear la figura
    fig = go.Figure()

    # Dimensiones del campo
    field_length = 120
    field_width = 80
    # Graficar los eventos
    if color_col:
        # Si la variable es categórica
        unique_categories = df[color_col].dropna().unique()
        palette = px.colors.qualitative.Set2  # o Set1, Dark2, Plotly, etc.
        color_map = {cat: palette[i % len(palette)] for i, cat in enumerate(unique_categories)}

        for category in unique_categories:
            sub_df = df[df[color_col] == category]
            fig.add_trace(go.Scatter(
                x=sub_df[y_col],
                y=sub_df[x_col],
                mode='markers',
                marker=dict(color=color_map[category], size=8),
                name=str(category)
            ))
    else:
        fig.add_trace(go.Scatter(
            x=df[y_col],
            y=df[x_col],
            mode='markers',
            marker=dict(color='crimson', size=6),
            name='Eventos'
        ))


    return fig

def filter_event_data(df, filtros):

    for col, (val, op) in filtros.items():
            if op == '==':
                df = df[df[col] == val]
            elif op == '!=':
                df = df[df[col] != val]
            elif op == '>':
                df = df[df[col] > val]
            elif op == '>=':
                df = df[df[col] >= val]
            elif op == '<':
                df = df[df[col] < val]
            elif op == '<=':
                df = df[df[col] <= val]
            else:
                raise ValueError(f"Operador no soportado: {op}")
    return df
  
def individual_report(df, player, filtro_config, columna_evento, columna_color):
    """
    Genera un dashboard de eventos individuales.

    Args:
        df (pd.DataFrame): Eventing data completo
        filtro_config (list[dict]): Lista de 5 diccionarios. Cada diccionario contiene:
            {
                'filtros': dict de filtros a aplicar (columna: (valor, operador))
            }
            operador puede ser: '==', '!=', '>', '>=', '<', '<='

        columna_evento (tuple): Par (columna, valor) para filtrar eventos en draw_eventing_data
        columna_color (str): Nombre de la columna para colorear draw_eventing_data

    Returns:
        go.Figure: Dashboard con 3 columnas:
            - Indicador de total de eventos (col 1)
            - Barchart por jornada (col 2)
            - Campo con eventos (col 3)
    """
    if len(filtro_config) != 5:
        raise ValueError("Se requieren exactamente 5 configuraciones de filtro.")

    specs = [
    [{'type': 'indicator'}, {'type': 'xy'}, {'type': 'xy', 'rowspan': 5}],  # Radar 1 ocupa fila 1-2
    [{'type': 'indicator'}, {'type': 'xy'}, None],
    [{'type': 'indicator'}, {'type': 'xy'}, None],
    [{'type': 'indicator'}, {'type': 'xy'}, None],
    [{'type': 'indicator'}, {'type': 'xy'}, None]
]

    titulos = [f"<b style='color:crimson; font-size:15px'>Progresión de {" ".join([f"{v}" for k, (v, op) in config.items()])} de la temporada</b>" for config in filtro_config]
    dashboard = make_subplots(
        rows=5, cols=3,
        column_widths=[0.05, 0.45, 0.5],
        row_heights=[0.2] * 5,
        specs=specs,
        horizontal_spacing=0.04,
        vertical_spacing=0.06,
        column_titles = ["", "", f"<b style='color:crimson; font-size:19px'>Distribución de {columna_evento[1]} de la temporada</b>"],
        subplot_titles = ["", titulos[0], "",
                          "", titulos[1],
                          "", titulos[2], 
                          "", titulos[3],
                          "", titulos[4]]
    )

    for i, config in enumerate(filtro_config):

  
        df_filtrado = filter_event_data(df, config)

        total_eventos = len(df_filtrado)

        nombre_evento = " ".join([f"{v}" for k, (v, op) in config.items()])

        dashboard.add_trace(indicator_total(total_eventos), row=i + 1, col=1)

        # Barchart
        bar = barchart_eventing(df_filtrado, nombre_evento)
        for trace in bar.data:
            dashboard.add_trace(trace, row=i + 1, col=2)

        if i == 4:
            # Campo con eventos (último solo)
            columna_evento_col, columna_evento_val = columna_evento
            df_eventing = df[df[columna_evento_col] == columna_evento_val]
            campo = draw_eventing_data(df_eventing, color_col=columna_color)
            campo.update_layout(
                xaxis=dict(range=[-5, 85], showgrid=False),
                yaxis=dict(range=[-5, 125], showgrid=False)
            )
            for trace in campo.data:
                dashboard.add_trace(trace, row=1, col=3)
    
    dashboard.add_layout_image(
    dict(
        source="https://raw.githubusercontent.com/hectormarca/scouting_chatbot/refs/heads/main/Code/Plantilla%20Campo%20Futbol%20Negro.jpg",
        xref="x2",  # ejes x del segundo gráfico
        yref="y2",  # ejes y del segundo gráfico
        x=-5,        # coordenada x (ajústala según el gráfico)
        y=125,        # coordenada y (ajústala según el gráfico)
        sizex=90,    # tamaño horizontal de la imagen
        sizey=130,    # tamaño vertical de la imagen
        xanchor="left",
        yanchor="top",
        layer="below",  # poner detrás de las trazas
        sizing="stretch"  # para que se adapte
    )
)
    
    dashboard.update_xaxes(range=[-5, 85], row=1, col=3)
    dashboard.update_yaxes(range=[-5, 125], row=1, col=3)
    
    dashboard.update_layout(
        template='simple_white',
        showlegend=True,
        paper_bgcolor='rgba(240, 248, 255, 0.6)',  # fondo pastel claro
        plot_bgcolor='rgba(255, 255, 255, 0.0)',
        font=dict(family="Lato"	, color="black"),
        title=dict(
            text=f"Informe de Rendimiento de {player}. Evolución de la temporada",
            font=dict(size=30, color="crimson", family="Montserrat, sans-serif"),
            x=0.5,
            xanchor='center'
        )
    )

    return dashboard
