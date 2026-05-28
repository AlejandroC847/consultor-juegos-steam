"""Módulo de gestión de persistencia de registros locales de la biblioteca.

Manipula, almacena y procesa el archivo JSON de la caché local. Permite ordenar, escribir o leer
las listas de juegos que necesita la interfaz gráfica.
"""
__author__ = "Alejandro Cortés"
__date__ = "2026-05-24"

import json
from pathlib import Path
from typing import Callable
from services.steam_api import SteamAPIClient
from services.hltb_client import get_playtime

class GameManager():
    """Contiene la manipulación de datos en crudo de los registros en el disco.

    Gestiona el ciclo de vida del archivo JSON local, coordina las consultas de las APIs de
    terceros para actualizar los registros y los ordena.
    """

    def __init__(self):
        """Inicializa  las rutas de almacenamiento local y los sub-clientes.
        
        Inicializa las estructuras de datos principales en vacío
        y define los criterios predeterminados para el ordenamiento de la GUI.
        """

        current_path = Path(__file__).resolve()
        root_path = current_path.parent.parent
        self.data_folder = root_path / "data"

        # La primera vez se crea la carpeta para que exista
        self.data_folder.mkdir(parents=True, exist_ok=True)
        self.json_file = self.data_folder / "steam_games.json"

        self.steam_client = SteamAPIClient()

        #Lista de juegos y criterios de ordenamiento.
        self.games = []
        self.ascending_order = True
        self.sorting_parameter = "Alfabético"

    def load_local_json(self):
        """Lee el archivo caché local de juegos en formato JSON.

        Verifica de la existencia física del archivo en disco. Si el archivo está presente y
        estructurado adecuadamente, traslada los datos hacia la variable de la coleccion en memoria.

        Returns:
            bool: True si el archivo existe y fue decodificado exitosamente.
                False si el archivo no existia, si desaparece inesperadamente,
                si está vacio o con errores de sintaxis.
        """

        if self.json_file.exists():
            try:
                with open(self.json_file, "r", encoding="utf-8") as f:
                    self.games = json.load(f)
                return True #Había datos locales
            except FileNotFoundError:
                # El archivo desaparece inesperadamente
                self.games = []
                return False  # Error al leer el archivo
            except json.JSONDecodeError:
                # Archivo vacio o con errores de sintaxis
                print(f"El archivo {self.json_file.name} está corrupto o mal formateado.")
                self.games = []
                return False  # Error al leer el archivo

        self.games = []
        return False  # El archivo ni siquiera existía (primera ejecución)

    def sort_game_list(self):
        """Ordena la lista de juegos según el criterio de ordenamiento y dirección configurados.

        Modifica la lista `self.games`. Maneja de forma segura los datos faltantes ("N/A", "S/D").

        Criterios soportados:
            - "Alfabético": Ordena por el nombre del juego (case-insensitive).
            - "Por logros": Ordena por porcentaje de logros completados.
            - "Por tiempo": Ordena por la duración estimada de HowLongToBeat.
        """

        if not self.games:
            return

        if self.sorting_parameter == "Alfabético":
            self.games.sort(key=lambda x: x["nombre"].lower(), reverse=not self.ascending_order)

        elif self.sorting_parameter == "Por logros":
            def llave_logros(x):
                val = x["logros_porcentaje"]
                return (0 if self.ascending_order else -1, -1) if val == "N/A" else (1, val)
            self.games.sort(key=llave_logros, reverse=not self.ascending_order)

        elif self.sorting_parameter == "Por tiempo":
            def llave_tiempo(x):
                val = x["duracion_hltb"]
                return (0 if self.ascending_order else -1, -1) if val == "S/D" else (1, val)
            self.games.sort(key=llave_tiempo, reverse=not self.ascending_order)

    def update_and_save_library(self, progress_status: Callable = None):
        """Sincroniza la biblioteca de juegos desde internet y la persiste en el disco.

        Método diseñado para ejecutarse en un hilo secundario por su alta carga operativa.
        Consulta la lista dejuegos desde el 'steam_client' y obtiene de manera secuencial el
        porcentaje de logros y las horas estimadas de duración del título. Al terminar actualiza
        la memoria y sobreescribe el JSON local de caché.

        Args:
            progress_status (Callable, optional): Funció de callback de la GUI para notificar
            el avance del procesamiento en tiempo real. Por defecto es None.

        Returns:
            bool: True si el proceso para consultar, procesar y escribir se realizo existosamente.
                False si la API devolvió datos vacíos o si ocurrieron errores de tipado o disco.
        """

        try:
            # Se llama a la API usando el cliente interno
            api_games = self.steam_client.get_game_list()

            if not api_games:
                print(
                    "[Gestor] No se pudieron obtener juegos de la API. Manteniendo datos locales."
                )
                return False

            new_games = []

            total_games = len(api_games)
            for index, game in enumerate(api_games):
                name = game.get("name", "Juego Desconocido")
                appid = game.get("appid")
                minutes_played = game.get("playtime_forever", 0)
                hours_played = round(minutes_played / 60, 1)

                # Notificar progreso en la interfaz
                if progress_status:
                    progress_status(index + 1, total_games, name)

                # Obtener logros y duraciones
                achievement_rate = self.steam_client.get_achievement_rate(appid)
                playtime = get_playtime(name)["promedio"]

                new_games.append({
                    "nombre": name,
                    "appid": appid,
                    "horas_jugadas": hours_played,
                    "logros_porcentaje": achievement_rate,
                    "duracion_hltb": playtime
                })

            # Actualizar la lista en memoria del programa
            self.games = new_games

            # Guardar físicamente en el archivo steam_games.json
            with open(self.json_file, "w", encoding="utf-8") as f:
                json.dump(self.games, f, indent=4, ensure_ascii=False)

            print(f"[Gestor] Éxito: Sincronizados y guardados {len(self.games)} juegos en caché.")
            return True

        except (TypeError, AttributeError) as err_datos:
            print("[Gestor/Datos] Estructura de datos corrupta en la "
                    f"respuesta de la API: {err_datos}"
            )
            return False

        except IOError as err_disco:
            print(f"[Gestor/Datos] Error crítico al escribir en el archivo JSON: {err_disco}")
            return False
