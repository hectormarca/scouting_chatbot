import pandas as pd
import plotly.graph_objects as go

def barra_con_bola(jugadores, valores, titulo="Estadísticas por jugador", color="#1f77b4"):
    """
    Crea un gráfico de barras verticales con una bola al final de cada barra.
    
    jugadores: lista de nombres (categorías en eje X)
    valores: lista de valores numéricos (altura de cada barra)
    color: color de barra y bola
    """
    fig = go.Figure()

    # Barras finas (usamos scatter como líneas verticales)
    for i, (x, y) in enumerate(zip(jugadores, valores)):
        fig.add_trace(go.Scatter(
            x=[x, x],
            y=[0, y],
            mode="lines",
            line=dict(color=color, width=4),
            showlegend=False
        ))

    # Bolas al final
    fig.add_trace(go.Scatter(
        x=jugadores,
        y=valores,
        mode="markers+text",
        marker=dict(size=16, color=color, line=dict(width=1, color="white")),
        text=[f"{v}" for v in valores],
        textposition="top center",
        showlegend=False
    ))

    fig.update_layout(
        title=titulo,
        xaxis_title="Jugador",
        yaxis_title="Valor",
        template="simple_white",
        margin=dict(t=60, b=40),
        height=500
    )

    return fig

