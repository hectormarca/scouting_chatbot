import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
    boxpoints=False,     # ❌ No muestra puntos
    fillcolor='rgba(255, 100, 100, 0.2)',
    line=dict(color='rgba(255,100,100,0.8)'),
    hoverinfo='skip',    # ❌ Desactiva hover
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
    
    if comparation == 'mean':

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
            name='Promedio'
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
            showlegend=True
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
                "font": {"size": 28, "color": "crimson"}
            },
            title={
                "text": f"<span style='font-size:14px;color:gray'><b>Perc. {variable}</b></span>",
            },
            domain={"x": [0, 1], "y": [0, 1]}
            
        )
    
    return fig

def comparative_report(df, variables, player, jugador_col='player'):

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
        horizontal_spacing=0.03,
        vertical_spacing=0.08,
        subplot_titles=["", "", "<b style='color:crimson'>Comparación Rendimiento Ofensivo</b>",
                        "", "",
                        "", "","<b style='color:crimson'>Comparación Rendimiento Creación</b>",
                        "", ""],
        column_titles = ["",f"<b style='color:crimson'>Situación de {player} respecto del resto de jugadores</b>",""]
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
    fig_of = radar_chart(data_scaled, player, vars_ofensivas)
    for trace in fig_of.data:
        dashboard.add_trace(trace, row=1, col=3)

    # Radar defensivo en filas 3-4
    fig_def = radar_chart(data_scaled, player, vars_defensivas)
    for trace in fig_def.data:
        dashboard.add_trace(trace, row=3, col=3)

    
    dashboard.update_layout(
        template='simple_white',
        showlegend=True,
        paper_bgcolor='rgba(240, 248, 255, 0.6)',  # fondo pastel claro
        plot_bgcolor='rgba(255, 255, 255, 0.0)',
        font=dict(family="Arial", color="black"),
        title=dict(
            text=f"Informe de Rendimiento de {player}. Comparación con el resto de jugadores",
            font=dict(size=24, color="crimson"),
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



data = pd.read_csv("Data/aggregated_data.csv", sep=";", encoding = "UTF-8")
data = data[(data['minutes']>1000) & (data['position']!='Goalkeeper')]
vars = ['Pases', 'Shot_Assist', 'Assist', 'Centros_Area',
       'Porc_Pase', 'Regates_Int', 'Regates_Comp', 'Recuperaciones',
       'Despejes', 'Perdidas', 'Errores', 'Tiros', 'xG_per_90', 'Goles']

data_scaled = data.copy()
data_scaled = data_scaled[vars + ['player','position']]

min_vals = data_scaled[vars].min()
max_vals = data_scaled[vars].max()
data_scaled[vars] = (data_scaled[vars] - min_vals) / (max_vals - min_vals)

fig = comparative_report(data, ['xG_per_90', 'Porc_Pase', 'Regates_Int', 'Perdidas'],'Leroy Sané')
fig.show()