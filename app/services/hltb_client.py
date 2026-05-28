"""Cliente de consulta para las duraciones de videojuegos en HowLongToBeat.

Utiliza la librería especializada 'howlongtobeatpy' para realizar búsquedas
y extraer estimaciones de horas de juego basadas en datos de la comunidad.
"""
__author__ = "Alejandro Cortés"
__date__ = "2026-25-24"

from howlongtobeatpy import HowLongToBeat
import requests

def get_playtime(game_name: str) -> dict:
    """Busca un juego en HLTB y devuelve sus tiempos principales en un diccionario.

    Realiza un análisis de similitud de texto sobre los resultados para extraer
    el título más representativo y mitigar respuestas vacías o caídas de red.

    Args:
        game_name (str): Nombre textual del videojuego a buscar.

    Returns:
        dict: Diccionario con las claves 'promedio', 'historia', 'extra' y 'completo'.
            Si el juego no es localizado o hay un fallo de red, todos los campos
            se devuelven con el valor centinela "S/D" (Sin Datos).
    """

    default_data = {"promedio": "S/D", "historia": "S/D", "extra": "S/D", "completo": "S/D"}

    try:
        # Realiza la búsqueda en la plataforma
        results = HowLongToBeat().search(game_name)

        if not results:
            return default_data

        # El mejor resultado (el más relevante) suele ser el primero
        best_result = max(results, key=lambda element: element.similarity)

        return {
            "promedio": best_result.all_styles,
            "historia": best_result.main_story,
            "extra": best_result.main_extra,
            "completo": best_result.completionist,
        }
    except requests.exceptions.RequestException as err_red:
        print(f"[HLTB/Red] Error en la solicitud para '{game_name}': {err_red}")
        return default_data
