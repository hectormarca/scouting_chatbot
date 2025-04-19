import pandas as pd
import plotly.graph_objects as go

def boxplot_with_percentil(df, jugador, variable, jugador_col="player"):
    
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

    valor_jugador = df.loc[df[jugador_col] == jugador, variable].values[0]
    kpi_percentil = df.loc[df[jugador_col] == jugador, f'{variable}_perc'].values[0]

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

    # Estilo visual
    fig.update_layout(
        height=120,
        margin=dict(l=20, r=10, t=10, b=10),
        template='simple_white',
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, domain=[0.025, 1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )

    # Anotación del KPI (percentil)
    fig.add_annotation(
        xref='paper', yref='paper',
        x=0, y=0.5,
        text=f"<b style='font-size:14px;'>Perc. \n{variable}</b><br><span style='font-size:16px; color:#e74c3c;'><b>{kpi_percentil:.0f}%</b></span>",
        showarrow=False,
        align='center',
        font=dict(size=14, color='gray'),
        bordercolor='white',
        bgcolor='white'
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
            showlegend=True,
            title=dict(
        text=f'Rendimiento de {player} frente al promedio',
        x=0.5,  # Centrado horizontalmente
        xanchor='center'
    )
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
                    range=[0, 1]
                )
            ),
            showlegend=True,
            title=dict(
        text=f'Comparativa entre {player} y {comparation}',
        x=0.5,  # Centrado horizontalmente
        xanchor='center'
    )
        )

        return fig
