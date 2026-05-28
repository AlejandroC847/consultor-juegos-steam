"""Módulo base abstracto para clientes de plataformas de videojuegos.

Proporciona una interfaz estructurada y herramientas de comunicación HTTP
reutilizables para asegurar un comportamiento homogéneo entre distintas tiendas.
"""
__author__ = "Alejandro Cortés"
__date__ = "2026-25-27"

from abc import ABC, abstractmethod
import requests


class BasePlatformClient(ABC):
    """Clase base abstracta que define las reglas y herramientas de red

    para cualquier cliente de tienda de videojuegos.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.timeout = 10

    def _submit_request(self, endpoint: str, params: dict = None) -> dict:
        """Método interno que todas las subclases usarán para conectarse a internet.

        Centraliza el manejo de excepciones de red de la librería 'requests'
        para evitar caídas catastróficas del programa ante fallos de conexión.

        Args:
            endpoint (str): Ruta relativa del servicio web al que se desea consultar.
            params (dict, opcional): Parámetros de consulta (Query Parameters) para la URL.

        Returns:
            dict: Diccionario con la respuesta JSON parseada. Retorna un diccionario
                vacío `{}` si ocurre un error HTTP o de conectividad.
        """

        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[Red/BaseCliente] Error crítico: {e}")
            return {}

    @abstractmethod
    def get_game_list(self) -> list[dict]:
        """Debe retornar una lista estandarizada de diccionarios de juegos.

        Cada subclase hija (Steam, Epic, etc.) debe implementar obligatoriamente
        su propia lógica de consulta y formateo de datos.

        Returns:
            list[dict]: Lista de diccionarios que representan la colección de juegos.
        """
