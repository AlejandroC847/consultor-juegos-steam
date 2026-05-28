"""Módulo encargado de la interfaz grafica del programa (GUI) basada en CustomTkinter.

La clase AplicacionConsultor se encarga de mostrar la interfaz de la lista de juegos en secuencia
por medio de elementos interactivos que permiten visualizar y ordenar la biblioteca cargada desde
la caché local o mediante peticiones a las APIs externas. 
"""
__author__ = "Alejandro Cortés"
__date__ = "2026-05-24"

import os
import sys
from pathlib import Path
import customtkinter as ctk

# Solucionar TclError en ciertos entornos de Windows
ruta_base_python = Path(sys.base_prefix)
ruta_tcl = ruta_base_python / "tcl" / "tcl8.6"
ruta_tk = ruta_base_python / "tcl" / "tk8.6"
os.environ["TCL_LIBRARY"] = str(ruta_tcl)
os.environ["TK_LIBRARY"] = str(ruta_tk)

# Configuración visual global de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ConsultorApp(ctk.CTk):
    """Interfaz gráfica principal para el Consultor de la Biblioteca de Juegos.

    Esta clase hereda de `customtkinter.CTk` y gestiona la ventana principal, la
    organización de los componentes visuales (como filtros, botones y el contenedor
    desplazable de juegos) y la interacción directa con el usuario. Coordina las
    llamadas al gestor lógico para actualizar y ordenar las tarjetas en pantalla.
    """

    def __init__(self, manager):
        """Inicializa la ventana principal de la interfaz y le asocia el controlador lógico.

        Args:
            manager (GameManager): Instancia lógica de persistencia y procesamiento 
        """

        super().__init__()

        self.title("Biblioteca de Juegos")
        self.geometry("750x600")

        self.manager = manager

        self.create_ui()

    def create_ui(self)-> None:
        """Construye y empaqueta la estructura de la interfaz gráfica de usuario.

        Inicializa los componentes visuales estáticos de la aplicación, como
        los paneles de navegación (Frames), botones de acción, menús desplegables
        (Combobox) y el contenedor con barra de desplazamiento (ScrollableFrame) 
        donde se desplegarán los juegos. Además, vincula los eventos de los widgets 
        con sus respectivos métodos manejadores (callbacks).
        """

        # Título Principal
        self.main_title = ctk.CTkLabel(
            self, text="Biblioteca de Juegos", font=ctk.CTkFont(size=24, weight="bold")
            )
        self.main_title.pack(pady=20)

        # Contenedor de Controles
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.pack(pady=10, fill="x")

        # Menú Desplegable (Criterio)
        self.order_label = ctk.CTkLabel(self.controls_frame, text="Ordenar por:")
        self.order_label.pack(side="left", padx=10, pady=10)

        self.option_menu = ctk.CTkOptionMenu(
            self.controls_frame,
            values=["Alfabético", "Por logros", "Por tiempo"],
            command=self.change_order
        )
        self.option_menu.set("Alfabético")
        self.option_menu.pack(side="left", padx=10, pady=10)

        # Botón Invertir Orden
        self.invert_button = ctk.CTkButton(
            self.controls_frame,
            text="Orden: A-Z / Mayor a Menor",
            command=self.invert_sorting
        )
        self.invert_button.pack(side="right", padx=10, pady=10)

        # Estado de carga / información
        self.label_status = ctk.CTkLabel(
            self, text="Cargando biblioteca...", font=ctk.CTkFont(size=12)
            )
        self.label_status.pack(pady=5)

        # Marco Desplazable para los juegos
        self.games_frame = ctk.CTkScrollableFrame(self, width=700, height=400)
        self.games_frame.pack(pady=10, fill="both", expand=True, padx=20)

    def render_list(self) -> None:
        """Limpia el contenedor visual y muestra los juegos en su orden actual.

        Sincroniza la interfaz gráfica con el estado interno de los datos de los juegos.
        Primero elimina todos los widgets hijos dentro de `self.frame_juegos` para evitar
        duplicados, solicita al gestor que reordene la lista en memoria y finalmente
        muestra cada juego con sus respectivas estadísticas en pantalla.
        """
        # Esperar a que termine de dibujar cosas pendientes
        self.update_idletasks()

        # Limpiar elementos anteriores en el frame
        for widget in self.games_frame.winfo_children():
            widget.destroy()

        self.manager.sort_game_list()

        # Dibujar cada juego como una fila/tarjeta
        for j in self.manager.games:
            row_frame = ctk.CTkFrame(self.games_frame)
            row_frame.pack(fill="x", pady=4, padx=5)

            # Nombre del Juego
            lbl_name = ctk.CTkLabel(
                row_frame, text=j["nombre"], font=ctk.CTkFont(weight="bold"), anchor="w"
            )
            lbl_name.pack(side="left", padx=15, pady=10, fill="x", expand=True)

            # Formateo de estadísticas (Tiempo jugado, logros, HLTB)
            tiempo_val = j['horas_jugadas']
            time_text = f"{tiempo_val} hrs"

            achievements_val = j['logros_porcentaje']
            achievements_text = f"{achievements_val}%" if achievements_val != "N/A" else "N/A"

            hltb_val = j['duracion_hltb']
            hltb_text = f"{hltb_val}%" if hltb_val != "S/D" else "S/D"

            # Construcción del string para la etiqueta
            text_stats = (
                f"Tiempo: {time_text} | "
                f"Logros: {achievements_text} | "
                f"Duración HLTB: {hltb_text}"
            )

            # Actualización de etiqueta
            lbl_stats = ctk.CTkLabel(row_frame, text=text_stats, font=ctk.CTkFont(size=11))
            lbl_stats.pack(side="right", padx=15, pady=10)

    def change_order(self, new_parameter: str) -> None:
        """Manejador de evento para cambiar el criterio de ordenamiento de los juegos.

        Actualiza la configuración del criterio de orden en el gestor de datos y
        fuerza una actualización visual completa de la lista de juegos expuesta.

        Args:
            new_parameter (str): El nuevo nombre del criterio seleccionado en el
                menú desplegable ("Alfabético", "Por logros", "Por tiempo").
        """
        self.manager.sorting_parameter = new_parameter
        self.render_list()

    def invert_sorting(self) -> None:
        """Manejador de evento para alternar la dirección del ordenamiento (Asc/Desc).

        Invierte el estado booleano de dirección en el gestor de datos, actualiza
        el texto del botón interactivo para reflejar el estado actual y fuerza la
        reconstrucción visual de la lista con la nueva orientación.
        """

        self.manager.ascending_order = not self.manager.ascending_order

        if self.manager.ascending_order:
            self.invert_button.configure(text="Orden: Ascendente / A-Z")
        else:
            self.invert_button.configure(text="Orden: Descendente / Z-A")
        self.render_list()

    def show_error(self, message: str )-> None:
        """Despliega un mensaje de error crítico visible en el panel de estado.

        Modifica las propiedades de texto y color de la etiqueta de notificación
        principal de la interfaz para alertar al usuario de fallos en internet o datos.

        Args:
            message (str): Texto descriptivo del error que se desea proyectar.
        """
        self.label_status.configure(text=message, text_color="red")
