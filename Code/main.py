import plots.py as plots
import transformations.py as transf
import pandas as pd

agg_data = pd.read_parquet(agg_data_path)
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
