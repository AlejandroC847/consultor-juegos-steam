"""Cliente especializado para la API Web de Valve/Steam.

Módulo encargado de gestionar la autenticación por llaves privadas y procesar
los endpoints específicos del perfil del usuario (juegos en biblioteca y logros).
"""

__author__ = "Alejandro Cortés"
__date__ = "2026-25-27"

import os

from .base_client import BasePlatformClient
from dotenv import load_dotenv

class SteamAPIClient(BasePlatformClient):
    """Cliente de comunicación directa con los servicios web de Steam.

    Hereda la infraestructura de peticiones seguras de `BasePlatformClient`
    y consume las credenciales del entorno local.
    """

    def __init__(self):
        """Inicializa el cliente configurando la URL base y cargando el entorno .env."""

        super().__init__(base_url="https://api.steampowered.com")
        load_dotenv()
        self.api_key = os.getenv("STEAM_API_KEY")
        self.steam_id = os.getenv("STEAM_ID")

    def _are_credentials_valid(self)-> bool:
        """Verifica que las credenciales del archivo .env estén cargadas.

        Returns:
            bool: True si las variables existen y tienen contenido; False en caso contrario.
        """

        if not self.api_key or not self.steam_id:
            print("❌ ERROR CRÍTICO: No se encontraron las credenciales en el archivo .env")
            return False
        return True

    def get_game_list(self) -> list[dict]:
        """Obtiene la lista de juegos pertenecientes a la cuenta de Steam configurada.

        Consulta el servicio 'GetOwnedGames' inyectando parámetros de conversión.

        Returns:
            list[dict]: Lista con los diccionarios crudos de los juegos proporcionados
                por la API de Valve. Devuelve una lista vacía `[]` si ocurre un error.
        """

        if not self._are_credentials_valid():
            return []

        params = {
            "key": self.api_key,
            "steamid": self.steam_id,
            "include_appinfo": 1,
            "format": "json", # Innecesario, por defecto ya es json
            "include_played_free_games": 1,
            "include_free_sub": 1
        }

        data = self._submit_request(
            "/IPlayerService/GetOwnedGames/v1/", params=params
        )

        # Aquí limpias el JSON y devuelves tu lista estandarizada
        return data.get("response", {}).get("games", [])

    def get_achievement_rate(self, appid: int) -> float | str:
        """Calcula el porcentaje de progreso de logros de un juego específico.

        Realiza la consulta para el identificador del juego dado y computa la relación
        entre logros totales y logros desbloqueados por el usuario (`achieved == 1`).

        Args:
            appid (int): Identificador único del videojuego en Steam.

        Returns:
            float: Porcentaje numérico de avance redondeado a un decimal (ej. 45.2).
            str: Retorna "N/A" si el juego no posee logros o el perfil es privado, 
                y "S/D" si las credenciales base fallan.
        """

        if not self._are_credentials_valid():
            return "S/D"

        params = {"key": self.api_key, "steamid": self.steam_id, "appid": appid}
        data = self._submit_request("/ISteamUserStats/GetPlayerAchievements/v1/", params=params)

        if "playerstats" not in data or "achievements" not in data["playerstats"]:
            return "N/A"

        achievements = data["playerstats"]["achievements"]
        total = len(achievements)

        if total == 0:
            return "N/A"

        try:
            achieved = sum(1 for ach in achievements if ach.get("achieved") == 1)
            return round((achieved / total) * 100, 1)

        except (TypeError, KeyError) as err:
            print(f"[STEAMAPI] Estructura interna de logros corrupta para el appid {appid}: {err}")
            return "N/A"
        except ZeroDivisionError:
            return "N/A"
