import pandas as pd
import plotly.graph_objects as go

def boxplot_with_percentil(df, jugador, variable, jugador_col="player"):
    """
    Boxplot horizontal personalizado con jugador destacado y estilo visual refinado.
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
    
    # 2. Añadir los puntos personalizados
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

    # 3. Opcional: marcar un jugador destacado
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


