import plots
import transformations as transf
import pandas as pd
import gradio as gr
from openai import OpenAI
import os
from dotenv import load_dotenv
import ast


# Cargar variables de entorno (para poder acceder al token de la API)
load_dotenv()
# Obtener el token de la API de DeepSeek
api_token = os.getenv('API_TOKEN')
# Configurar tu API key de OpenAI (puede estar en una variable de entorno)
client = OpenAI(api_key=api_token, base_url="https://api.deepseek.com")

# Cargar datos
agg_data = pd.read_parquet('/workspaces/scouting_chatbot/Data/aggregated_data.parquet', engine = 'pyarrow')
event_data = pd.read_parquet('/workspaces/scouting_chatbot/Data/eventing_data.parquet', engine = 'pyarrow')

# Función de NLP para interpretar la pregunta
#Configuramos para que la respuesta sea un JSON con la metadata para realizar los informes
def interpretar_pregunta(pregunta, historial):
    prompt = f"""
Dispones en las variables agg_data y event_data de los siguientes conjuntos de datos con información sobre futbolistas:

agg_data
Información agregada de toda la temporada a nivel de jugador, cada fila representa un futbolista. El DataFrame contiene las siguientes columnas:

- player: nombre del jugador
- minutes: minutos que ha jugado en toda la temporada
- Pases: pases que ha dado por 90 minutos
- Shot_Assist: pases que ha dado y que han precedido a un tiro del compañero que ha recibido el pase por 90 minutos
- Assist: asistencias de gol que da por 90 minutos
- Centros_Area: centros al área que realiza por 90 minutos
- Porc_Pase: porcentaje de acierto en el pase durante la temporada
- Regates_Int: regates intentados por el jugador cada 90 minutos
- Regates_Comp: regates completados con éxito por el jugador cada 90 minutos
- Recuperaciones: recuperaciones de balón realizadas cada 90 minutos
- Despejes: despejes realizados cada 90 minutos
- Perdidas: pérdidas de balón cada 90 minutos
- Errores: errores que propician un tiro al equipo contrario cada 90 minutos
- Tiros: tiros que realiza el jugador cada 90 minutos
- xG_per_90: expected goals que genera el jugador cada 90 minutos
- Goles: goles anotados cada 90 minutos
- position: posición del jugador
- Pases_perc: percentil que ocupa el jugador en la categoría de pases realizados
- Shot_Assist_perc: percentil que ocupa el jugador en la categoría de pases que propician un tiro
- Assist_perc: percentil que ocupa el jugador en la categoría de asistencias de gol
- Centros_Area_perc: percentil que ocupa el jugador en la categoría de centros al área
- Porc_Pase_perc: percentil que ocupa el jugador en la categoría de porcentaje de acierto en el pase
- Regates_Int_perc: percentil que ocupa el jugador en la categoría de regates intentados
- Regates_Comp_perc: percentil que ocupa el jugador en la categoría de regates completados
- Recuperaciones_perc: percentil que ocupa el jugador en la categoría de recuperaciones
- Despejes_perc: percentil que ocupa el jugador en la categoría de despejes
- Tiros_perc: percentil que ocupa el jugador en la categoría de tiros
- xG_per_90_perc: percentil que ocupa el jugador en la categoría de expected goals generados
- Goles_perc: percentil que ocupa el jugador en la categoría de goles
- Perdidas_perc: percentil que ocupa el jugador en la categoría de pérdidas
- Errores_perc: percentil que ocupa el jugador en la categoría de errores

event_data
Recoge todo el eventing data de la temporada 2015/2016, cada fila representa un evento en un partido. El DataFrame contiene las siguientes columnas:

- id: identificador del evento
- minute: minuto del partido en que tuvo lugar el evento
- type: tipo de evento. Sus posibles valores son ['Dribble', 'Carry', 'Ball Recovery', 'Interception', 'Clearance', 'Dispossessed', 'Error', 'Pass', 'Shot']
- play_pattern: tipo de jugada en la que se realiza el evento. Sus posibles	valores son ['Regular Play', 'From Counter', 'From Goal Kick', 'From Throw In', 'From Free Kick', 'From Keeper', 'Other', 'From Kick Off', 'From Corner']
- team: equipo al que pertenece el jugador que protagoniza el evento
- player: jugador que protagoniza el evento
- position: posición del jugador que protagoniza el evento
- match_id: identificador del partido en el que ocurre el evento
- dribble_outcome: resultado del regate, solo aplica a eventos de tipo 'Dribble'. Sus posibles valores son ['Incomplete', 'Complete']
- dribble_overrun: Booleano, solo aplica a eventos de tipo 'Dribble'. Added when a dribble goes past the original defender into the possession of another player
- match_day: jornada de liga en la que tuvo lugar el partido
- x: coordenadas del eje X donde tuvo lugar el evento. Rango de 0-120
- y: coordenadas del eje Y donde tuvo lugar el evento. Rango de 0-80
- pass_length: solo aplica a eventos de tipo 'Pass'. Longitud del pase
- pass_height: solo aplica a eventos de tipo 'Pass'. Altura del pase, puede tomar los valores ['Ground Pass', 'High Pass', 'Low Pass']
- pass_type: solo aplica a eventos de tipo 'Pass'. Tipo de pase, puede tomar los valores ['Kick Off', 'Recovery', 'Throw-in', 'Free Kick', 'Corner', 'Interception', 'Goal Kick']
- pass_switch: solo aplica a eventos de tipo 'Pass'. Booleano que indica si el pase es un cambio de orientación
- pass_through_ball: solo aplica a eventos de tipo 'Pass'. Booleano que indica si el pase es un pase entre líneas
- pass_cross: solo aplica a eventos de tipo 'Pass'. Booleano que indica si el pase es un centro al área
- pass_shot_assist: solo aplica a eventos de tipo 'Pass'. Booleano que indica si el pase es una asistencia de tiro
- pass_goal_assist: solo aplica a eventos de tipo 'Pass'. Booleano que indica si el pase es una asistencia de gol
- pass_cut_back: solo aplica a eventos de tipo 'Pass'. Booleano que indica si el pase es un pase atrás desde línea de fondo
- shot_statsbomb_xg: solo aplica a eventos de tipo 'Shot'. Indica el expected goal generado por el tiro
- shot_end_location: solo aplica a eventos de tipo 'Shot'. Array con las coordenadas finales del tiro
- shot_type: solo aplica a eventos de tipo 'Shot'. Tipo de tiro, puede tomar los valores ['Open Play', 'Free Kick', 'Penalty', 'Corner']
- shot_outcome: solo aplica a eventos de tipo 'Shot'. Resultado del tiro, puede tomar los valores ['Goal', 'Blocked', 'Saved', 'Off T', 'Wayward', 'Post', 'Saved Off Target', 'Saved to Post']
- shot_first_time: solo aplica a eventos de tipo 'Shot'. Booleano que indica si el tiro fue al primer toque
- shot_body_part: solo aplica a eventos de tipo 'Shot'. Parte del cuerpo con la que se realizó en tiro, puede tomar los valores ['Right Foot', 'Left Foot', 'Head', 'Other']
- shot_aerial_won: solo aplica a eventos de tipo 'Shot'. Booleano que indica si el tiro se realizó al ganar un duelo aéreo
- shot_follows_dribble: solo aplica a eventos de tipo 'Shot'. Booleano que indica si el jugador realizó el tiro después de completar un regate



Tienes que extraer la siguiente información sobre la siguiente pregunta acerca de un jugador de fútbol: "{pregunta}"

Devuelve en formato JSON la siguiente información
- "report_type": tipo de informe a realizar, entre "comparative" o "individual". Si no se especifica, el informe será "comparative"
- "player_name": jugador sobre el que construir el importe (basado en la siguiente lista de jugadores disponibles: {agg_data['player'].unique().tolist()})
- "player_position": valor de la columna 'position' del jugador
- "variables": variables a mostrar en el informe si es de tipo "comparative". Si no este elemento puede ir vacío. Tiene que se una lista de 4 columnas presentes en ['Pases', 'Shot_Assist','Assist','Centros_Area','Porc_Pase','Regates_Int','Regates_Comp','Recuperaciones','Despejes','Perdidas','Errores','Tiros','xG_per_90','Goles'].
Si el usuario no especifica nada, tomará el valor ["Goles","Assist","Regates_Comp","Recuperaciones"]
- "comparation": con quien se va a comparar el jugador. Puede tomar los valores "mean", "position" si se quiere comparar con los jugadores de su misma posición o cualquier valor de {agg_data['player'].unique().tolist()} si se quiere comparar con un jugador en concreto
- "filter_config": Te pido que devuelvas 5 objetos de tipo diccionario con exactamente 1 par clave/valor. Cada par clave/valor debe seguir estas reglas:
La clave debe ser un nombre de columna de event_data (es decir, uno de los valores listados en {event_data.columns.tolist()}).
El valor de cada clave será una lista con dos elementos: El valor para filtrar (Este valor debe ser uno de los valores presentes en la columna seleccionada.) y el operador de comparación (que debe ser uno de los siguientes: '==', '>=', '<=', '>', o '<').
La lista debe tener siempre 5 diccionarios. Si no se especifica nada, la respuesta debe tomar el siguiente valor predeterminado: [{{"type": ["Shot", '==']}}, {{"type": ["Pass", '==']}}, {{"type": ["Dribble", '==']}}, {{"type": ["Ball Recovery", '==']}}, {{"type": ["Clearance", '==']}}]
- "event_plot_column": lista donde el primer elemento es una columna de event_data ({event_data.columns.tolist()}) y el segundo elemento el valor a utilizar de esa columna. Por defecto ["type", "Shot"]
- "event_color_column": nombre de columna de event data ({event_data.columns.tolist()}) que se va a utilizar para colorear un gráfico. Por defecto None

Teniendo en cuenta que anteriormente ya te han preguntado lo siguiente {historial}.

Output example:
{{"report_type": "comparative", "player_position": "FW", "player_name": "Lionel Andrés Messi Cuccittini", "variables": ["Goles","Assist","Regates_Comp","Recuperaciones"], "comparation":"mean", "filter_config": {{"type": ["Shot", '=='],"type": ["Pass", '=='], "type": ["Dribble", '=='], "type": ["Ball Recovery", '=='], "type": ["Clearance", '==']}}, "event_plot_column": "minute", "event_color_column": None}}
"""



    response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "Eres un scout/analista de fútbol cuya principal misión es diseñar informes de jugadores a partir de sus datos y estadísticas de los partidos"},
        {"role": "user", "content": prompt},
    ],
    stream=False)

    try:
        return transf.extraer_json_de_respuesta(response.choices[0].message.content)
    except:
        return None

# Función principal del asistente
#A partir del JSON de metadatos que devuelve la llamada a la API de Deepseek generamos el informe que ha pedido el usuario
def responder(pregunta, history):
    
    texto = ''
    if history:
        
        ultimas = min(len(history), 5)
        
        for i in range(1, ultimas+1):
          texto += f"La respuesta anterior {i} del bot fue: '{history[-i][0]}'"

    #Generamos el JSON de metadatos
    info = interpretar_pregunta(pregunta, texto)

    if info is None:
        return "No pude interpretar bien tu pregunta. ¿Puedes reformularla?"

    #Guardamos el jugador sobre el que se ha pedido el informe
    jugadores = info["player_name"]

    #Si el jugador está disponible en los datos
    if jugadores in agg_data.player.tolist():

      #Elaboramos el informe, ya sea individual o comparativo
      if info["report_type"]=="comparative":

        fig = plots.comparative_report(agg_data, info["variables"] , jugadores, comp = info['comparation'])
      
      elif info["report_type"]=="individual":

        event_data_filtered = event_data[event_data['player'] == jugadores]
        fig = plots.individual_report(event_data_filtered, jugadores, info['filter_config'], info['event_plot_column'], info['event_color_column'])

      else:
         
         return f'El tipo de informe {info["report_type"]} no está disponible todavía. Puedes pedir informes individuales o comparativos'
      
      return  gr.Plot(fig)
    
    #Si no encontramos el jugador, mostramos posibles coincidencias de jugadores con nombres parecidos
    else:
        
        similares_names = transf.buscar_similares(agg_data, 'player', jugadores)
        similares_table = agg_data[agg_data['player'].isin(similares_names)][['player','position']]
        return f"Lo siento, no encuentro al jugador que me has pedido. He encontrado los siguientes nombres similares:\n {similares_table.to_string(index=False, header=False)}"



# Lanzar la app
chat = gr.ChatInterface(
    fn=responder,
    title="Asistente de Scouting. Informes comparativos e individuales de jugadores de las 5 grandes ligas",
    description="Asistente para diseñar informes sobre el rendimiento de un jugador en la temporada 2015/2016. Todos los datos son extraídos de StatsBomb." \
    "Actualmente, están disponibles informes comparativos (se muestra a un jugador elegido respecto al resto) o individuales (progreso del jugador elegido a lo largo de la temporada)." \
    "El asistente es capaz de modificar los informes para mostrar las variables requeridas por el usuario. Para los informes individuales, se muestran siempre 4 variables entre: Pases, Shot_Assist, Assist, Centros_Area, Porc_Pase, Regates_Int, Regates_Comp, Recuperaciones, Despejes, Perdidas, Errores, Tiros, xG_per_90, Goles. " \
    "También permite cambiar contra quién se compara el jugador en los gráficos de radar, si contra la media de todos los jugadores, contra la media de los jugadores de su posición o contra un jugador en concreto."
).launch(debug=True, share=True)




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
