"""Paquete de servicios y clientes de comunicación con APIs externas.

Centraliza los módulos encargados de realizar peticiones de red hacia las
plataformas de Valve/Steam y el sitio de métricas HowLongToBeat.
"""

from .base_client import BasePlatformClient
from .steam_api import SteamAPIClient
from .hltb_client import get_playtime

# Expone las clases y funciones al exterior del paquete
__all__ = ["BasePlatformClient", "SteamAPIClient", "get_playtime"]
