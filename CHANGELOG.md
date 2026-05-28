# Changelog

---

Todos los cambios notables en este proyecto serán documentados en este archivo
de acuerdo a los estándares de [Keep a Changelog](https://keepachangelog.com/es-ES/).

---

## [1.0.0] - 2026-05-28

### Added

- Integración con la plataforma **HowLongToBeat** mediante la librería
`howlongtobeatpy` para estimar horas de juego de forma automática.
- Arquitectura basada en el patrón de diseño **MVC (Modelo-Vista-Controlador)**
de forma híbrida mediante los módulos independientes `game_manager.py` y `gui.py`.
- Creación del paquete encapsulado `services/` con una
**Clase Base Abstracta** (`BasePlatformClient`) para normalizar
futuras implementaciones de otras tiendas de videojuegos.

### Changed

- **Refactorización modular masiva:** Se fragmentó el script monolítico original
distribuyendo la lógica de persistencia local en el backend y el renderizado
interactivo en la vista.
- Homologación y traducción de funciones internas al ingles para mejorar la
consistencia y mantenibilidad del repositorio.

### Removed

- Archivo unitario y monolítico de ejecución `app_steam.py` debido a la migración
total hacia la nueva arquitectura orientada a objetos y modular.

### Security

- Delegación de credenciales sensibles externas (`Steam API Key` y `Steam ID`)
hacia variables de entorno locales mediante un archivo `.env`, mitigando riesgos
de exposición en el repositorio público.

---

## [0.1.0] - 2026-05-23

### Added

- Implementación inicial de lógica del proyecto
- Consulta a la API de Steam para descarga de datos
- Creacion de interfaz grafica de usuario con CustomTkinter

---

## [0.0.1] - 2026-05-22

### Added

- Estructura base del proyecto con entorno virtual.
- Documentación inicial (`README.md` y `CHANGELOG.md`).
