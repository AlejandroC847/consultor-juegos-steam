"""Ejecución Principal. Punto de Entrada del Consultor de Bibliotecas.

Coordina la inicialización de la interfaz gráfica, el sistema de persistencia 
local y la ejecución segura de peticiones asíncronas pesadas mediante hilos.
"""
__author__ = "Alejandro Cortés"
__date__ = "2026-25-23"

import threading
import app.games_manager as games_manager
import gui

def background_process(manager: games_manager.GameManager, ui_window: gui.ConsultorApp):
    """Descarga, procesa y almacena la biblioteca de juegos.

    Función diseñada para ejecutarse en un hilo ('Thread') independiente.
    Usa un callback interno para que el gestor del juego se comunique con la interfaz.

    Args:
        gestor (GestorJuegos): Instancia lógica de procesamiento del archivo caché.
        ventana (AplicacionConsultor): Instancia de interfaz gráfica basada en CustomTkinter.
    """

    def progress_status(current: int, total: int, name: str):
        """Modifica la etiqueta de estatus con los valores de juego actual, juegos totales y nombre.

        Args:
            current (int): Número actual de juegos procesados.
            total (int): Número total de juegos.
            name (str): Nombre del juego actual.
        """

        ui_window.label_status.configure(text = f"Procesando Juego {current}/{total}: {name}")
        ui_window.update_idletasks()

    success = manager.update_and_save_library(progress_status = progress_status)

    if success:
        # Una vez guardado el JSON, la interfaz redibuja las tarjetas
        ui_window.label_status.configure(text="Sincronización con Steam completada.")
        ui_window.render_list()
    else:
        ui_window.show_error("Error al sincronizar con la API de Steam.")

def main():
    """Ejecución inicial del programa.
    
    Gestiona la instanciacion de GestorJuegos, AplicacionConsultor, inicia la recuperación de
    registros locales y el despliegue de un hilo de ejecución secundaria para la descarga de datos.
    """

    manager = games_manager.GameManager()
    main_window = gui.ConsultorApp(manager)

    success_cache = manager.load_local_json()

    if success_cache:
        # Si la caché cargó bien, la GUI se encarga de avisar y dibujar
        main_window.label_status.configure(text="Mostrando datos locales. Actualizando...")
        main_window.render_list()
    else:
        # Primera ejecución o caché borrada
        main_window.label_status.configure(
            text="No se encontraron datos locales. Descargando por primera vez..."
        )

    # Hilo de ejecución secundaria
    threading. Thread(
        target=background_process, args=(manager, main_window), daemon=True
    ).start()

    main_window.mainloop()

# =============================================
# Ejecución Principal
# =============================================
if __name__ == "__main__":
    main()
