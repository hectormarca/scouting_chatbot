import pandas as pd
from difflib import get_close_matches
import json
import re

def union_events(df_list):

    result = pd.DataFrame()

    for df in df_list:

        result = pd.concat(result, df, ignore_index=True)

    return result

def filter_by_player(df, player, player_column='player'):

    df_filtered = df[df[player_column]==player]
    return df_filtered

def buscar_similares(df, columna, valor, n=10, umbral=0.5):
    """
    Devuelve los elementos más similares a `valor` en una columna del DataFrame.

    Parámetros:
    - df: DataFrame de entrada
    - columna: nombre de la columna donde buscar
    - valor: string a comparar
    - n: número máximo de resultados
    - umbral: valor mínimo de similitud (entre 0 y 1)

    Retorna:
    - Lista con los elementos más similares
    """
    elementos = df[columna].dropna().astype(str).unique()
    similares = get_close_matches(valor, elementos, n=n, cutoff=umbral)
    return similares

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