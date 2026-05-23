# Consultor de Juegos

Una aplicación de escritorio para gestionar, analizar y organizar tu biblioteca
de Steam, enriquecida con datos de tiempo de juego reales.

## Objetivo

Ofrecer una interfaz visual e intuitiva para que el usuario explore sus juegos
de Steam, permitiendo ordenamientos avanzados por logros, orden alfabético y
duración estimada de juego.

## Características Principales

- **Integración con Steam:** Conexión mediante la API oficial para recuperar
la biblioteca del usuario.
- **Tiempos de Juego Reales:** Raspado/Integración con datos de duración
(estilo HowLongToBeat).
- **Filtros Avanzados:** Ordenamiento por orden alfabético, porcentaje de
logros completados y horas de juego.
- **Interfaz Moderna:** Diseñada con CustomTkinter para un aspecto limpio y
modo oscuro nativo.

## Tecnologías

- Python 3.12+
- CustomTkinter (UI)
- Requests / Steam Web API
- BeautifulSoup4 / API (para datos de duración)

## Progreso del Proyecto

- [x] Módulo 0: Inicialización del proyecto
- [x] Módulo 1: Configuración Inicial e Interfaz Base (CustomTkinter)
- [x] Módulo 2: Conexión y Autenticación con la API de Steam
- [ ] Módulo 3: Integración de Datos de Duración (HowLongToBeat)
- [x] Módulo 4: Sistema de Filtros y Ordenamiento
- [ ] Módulo 5: Pruebas Unitarias y Optimización
