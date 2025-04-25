import plots
import transformations as transf
import pandas as pd
import gradio as gr
import plotly.express as px
from openai import OpenAI
import os
from openai import AsyncOpenAI
import json
import re

def extraer_json_de_respuesta(respuesta):
    # Buscar cualquier contenido entre llaves {...}
    match = re.search(r'\{.*\}', respuesta, re.DOTALL)
    if match:
        json_text = match.group()
        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            return None
    return None


# Configurar tu API key de OpenAI (puede estar en una variable de entorno)
client = OpenAI(api_key="sk-6528ca292910466e95b9e352d21fe79a", base_url="https://api.deepseek.com")
#os.getenv("OPENAI_API_KEY") or


# Cargar datos
agg_data = pd.read_parquet('/workspaces/scouting_chatbot/Data/aggregated_data.parquet', engine = 'pyarrow')

# Función de NLP para interpretar la pregunta
def interpretar_pregunta(pregunta):
    prompt = f"""
Extract the following information about the next football question: "{pregunta}"

Return in JSON format the following:
- "jugador": player to build a report of (based on the following available players: {agg_data['player'].unique().tolist()})
- "metrica": one of the following ["Gls", "xG", "Ast"]
- "modo": one of ["compare", "show", "list"] according to the type of action

Output example:
{{"jugador": "Haaland", "metrica": "Gls", "modo": "compare"}}
"""



    response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a football scouting"},
        {"role": "user", "content": prompt},
    ],
    stream=False)

    try:
        return extraer_json_de_respuesta(response.choices[0].message.content)
    except:
        return None

# Función principal del asistente
def responder(pregunta, history):
    info = interpretar_pregunta(pregunta)

    if info is None:
        return "No pude interpretar bien tu pregunta. ¿Puedes reformularla?", None

    jugadores = info["jugador"]
    metrica = info["metrica"]
    modo = info["modo"]

    fig = plots.comparative_report(agg_data, ['Shot_Assist', 'Assist', 'Regates_Comp', 'Goles'] , jugadores)

    return  gr.Plot(fig)

# Lanzar la app
chat = gr.ChatInterface(
    fn=responder,
    title="Asistente de Fútbol ⚽",
    description="Pide informes sobre el rendimiento de un jugador en la temporada 2015/2016. Todos los datos son extraídos de StatsBomb"
).launch(debug=True)




'''
event_data = pd.read_parquet(event_data_path)

agg_data_gk = pd.read_parquet(agg_data_gk_path)
event_data_gk = pd.read_parquet(event_data_gk_path)

if metadata['report_type'] == 'comparative' and metadata['player_position'] <> 'GK':

  report = plots.comparative_report(agg_data, metadata['variables'], metadata['player_name'])

elif metadata['report_type'] == 'individual' and metadata['player_position'] <> 'GK':

  event_data_filtered = transf.filter_by_player(event_data, metadata['player_name'])
  report = plots.individual_report(event_data_filtered, metadata['player_name'], metadata['filter_config'], metadata['event_plot_column'], metadata['event_color_column'])

elif metadata['report_type'] == 'comparative' and metadata['player_position'] == 'GK':

  report = plots.comparative_report(agg_data_gk, metadata['variables'], metadata['player_name'])

elif metadata['report_type'] == 'individual' and metadata['player_position'] == 'GK':

  print('El análisis individual de porteros todavía no está disponible')

else:

  RaiseValueError(f'El informe de tipo {metadata['report_type']} para jugadores que juegan de {metadata['player_position']} no está disponible')
'''
