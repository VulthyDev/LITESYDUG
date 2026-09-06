# =========================================================
# LITESYDUG
# =========================================================

VERSION_APP = "v0.1.0"
#puro import aca xdXd
from settings_window import SettingsWindow
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

import random
import threading
import os

from player import Player
from library import Library
from settings import Settings
from hotkeys import HotkeyManager
from tray import TrayManager
from assets import Assets


# =========================================================
# PALETA Y2K / RETRO
# =========================================================

COLOR_FONDO = "#080c14"
COLOR_PANEL = "#101827"
COLOR_PANEL_2 = "#121d30"
COLOR_PANEL_INTERNO = "#08111f"

COLOR_BOTON = "#18243a"
COLOR_BOTON_HOVER = "#263a5c"

COLOR_ACENTO = "#7957ff"
COLOR_ACENTO_CLARO = "#a88cff"

COLOR_CYAN = "#38d9ff"
COLOR_ROSA = "#ff4da6"

COLOR_TEXTO = "#f4f7ff"
COLOR_TEXTO_SECUNDARIO = "#8e9ab0"

COLOR_BORDE = "#293854"
COLOR_LISTA = "#070e1a"


# =========================================================
# OBJETOS
# =========================================================

player = Player()
library = Library()
assets = Assets()

config = Settings()
datos_config = config.cargar()
iniciar_minimizado = datos_config.get(
    "iniciar_minimizado",
    False
)

iniciar_mini = datos_config.get(
    "iniciar_mini",
    False
)

cerrar_a_bandeja = datos_config.get(
    "cerrar_a_bandeja",
    True
)

recordar_ultima_carpeta = datos_config.get(
    "recordar_ultima_carpeta",
    True
)
hotkey_manager = HotkeyManager()
colores_ajustes = {
    "fondo": COLOR_FONDO,
    "panel": COLOR_PANEL,
    "panel_2": COLOR_PANEL_2,
    "panel_interno": COLOR_PANEL_INTERNO,
    "boton": COLOR_BOTON,
    "boton_hover": COLOR_BOTON_HOVER,
    "acento": COLOR_ACENTO,
    "acento_claro": COLOR_ACENTO_CLARO,
    "cyan": COLOR_CYAN,
    "rosa": COLOR_ROSA,
    "texto": COLOR_TEXTO,
    "texto_secundario": COLOR_TEXTO_SECUNDARIO
}

# =========================================================
# CONFIGURACIÓN GUARDADA
# =========================================================
recordar_posicion_ventana = datos_config.get(
    "recordar_posicion_ventana",
    False
)

posicion_ventana = datos_config.get(
    "posicion_ventana",
    ""
)
mostrar_tooltips = datos_config.get(
    "mostrar_tooltips",
    True
)
mini_siempre_encima = datos_config.get(
    "mini_siempre_encima",
    True
)
modo_rendimiento = datos_config.get(
    "modo_rendimiento",
    "Normal"
)
volumen_guardado = datos_config.get(
    "volumen",
    70
)

ultima_carpeta = datos_config.get(
    "ultima_carpeta",
    ""
)

paso_volumen = datos_config.get(
    "paso_volumen",
    5
)
salto_segundos = datos_config.get(
    "salto_segundos",
    10
)

solo_hotkeys_oculto = datos_config.get(
    "solo_hotkeys_oculto",
    True
)


HOTKEYS_DEFAULT = {
    "play_pausa": None,
    "siguiente": None,
    "anterior": None,
    "retroceder_10": None,
    "adelantar_10": None,
    "volumen_menos": None,
    "volumen_mas": None
}


NOMBRES_DEFAULT = {
    "play_pausa": "Sin asignar",
    "siguiente": "Sin asignar",
    "anterior": "Sin asignar",
    "retroceder_10": "Sin asignar",
    "adelantar_10": "Sin asignar",
    "volumen_menos": "Sin asignar",
    "volumen_mas": "Sin asignar"
}


hotkeys_actuales = datos_config.get(
    "hotkeys",
    {}
)

hotkeys_nombres = datos_config.get(
    "hotkeys_nombres",
    {}
)


for clave, valor in HOTKEYS_DEFAULT.items():

    if clave not in hotkeys_actuales:

        hotkeys_actuales[clave] = valor


for clave, valor in NOMBRES_DEFAULT.items():

    if clave not in hotkeys_nombres:

        hotkeys_nombres[clave] = valor


# =========================================================
# ESTADO
# =========================================================

modo_aleatorio = False
modo_repetir = False

usuario_moviendo_barra = False

portada_imagen = None

ventana_oculta = False

volumen_antes_mute = volumen_guardado


# =========================================================
# ESTADO MINI
# =========================================================

ventana_mini = None

mini_nombre_cancion = None
mini_texto_artista = None
mini_boton_play = None
mini_tiempo = None
mini_portada = None
mini_barra_tiempo = None

mini_portada_imagen = None

usuario_moviendo_barra_mini = False


# =========================================================
# VENTANA PRINCIPAL
# =========================================================

ventana = tk.Tk()

ventana.title(
    "litesydug"
)
# =========================================================
# BUSCADOR
# =========================================================

texto_busqueda = tk.StringVar()

rutas_filtradas = []

# =========================================================
# POSICIÓN VENTANA PRINCIPAL
# =========================================================

ancho_ventana = 860
alto_ventana = 570

ancho_pantalla = ventana.winfo_screenwidth()

# =========================================================
# POSICIÓN INICIAL DE LA VENTANA
# =========================================================

x = (
    ancho_pantalla - ancho_ventana
) // 2

y = 20


if (
    recordar_posicion_ventana
    and posicion_ventana
):

    try:

        ventana.geometry(
            posicion_ventana
        )

    except Exception:

        ventana.geometry(
            f"{ancho_ventana}x{alto_ventana}+{x}+{y}"
        )

else:

    ventana.geometry(
        f"{ancho_ventana}x{alto_ventana}+{x}+{y}"
    )


ventana.resizable(
    False,
    False
)


ventana.configure(
    bg=COLOR_FONDO
)


# =========================================================
# ICONO
# =========================================================

logo_ventana = assets.cargar_tk(
    "logo.png",
    (64, 64)
)


if logo_ventana is not None:

    try:

        ventana.iconphoto(
            True,
            logo_ventana
        )

    except Exception:
        pass


# =========================================================
# VENTANA DE AJUSTES
# =========================================================

ventana_ajustes = None


# =========================================================
# TTK
# =========================================================
style = ttk.Style()

style.theme_use(
    "clam"
)


style.configure(
    "Retro.TCombobox",
    fieldbackground=COLOR_PANEL_INTERNO,
    background=COLOR_BOTON,
    foreground=COLOR_TEXTO,
    arrowcolor=COLOR_CYAN,
    bordercolor=COLOR_BORDE,
    lightcolor=COLOR_BORDE,
    darkcolor=COLOR_BORDE,
    padding=5
)


style.map(
    "Retro.TCombobox",

    fieldbackground=[
        (
            "readonly",
            COLOR_PANEL_INTERNO
        )
    ],

    foreground=[
        (
            "readonly",
            COLOR_TEXTO
        )
    ]
)


# =========================================================
# TOOLTIP
# =========================================================

class Tooltip:

    def __init__(
        self,
        widget,
        texto
    ):

        self.widget = widget
        self.texto = texto

        self.ventana_tooltip = None
        self.temporizador = None

        widget.bind(
            "<Enter>",
            self.programar,
            add="+"
        )

        widget.bind(
            "<Leave>",
            self.ocultar,
            add="+"
        )


    def programar(
        self,
        event=None
    ):

        self.cancelar()

        self.temporizador = (
            self.widget.after(
                400,
                self.mostrar
            )
        )


    def cancelar(self):

        if self.temporizador:

            self.widget.after_cancel(
                self.temporizador
            )

            self.temporizador = None


    def mostrar(self):

        if self.ventana_tooltip:
            return


        x = (
            self.widget.winfo_rootx()
            + self.widget.winfo_width() // 2
        )

        y = (
            self.widget.winfo_rooty()
            + self.widget.winfo_height()
            + 7
        )


        self.ventana_tooltip = tk.Toplevel(
            self.widget
        )


        self.ventana_tooltip.overrideredirect(
            True
        )


        self.ventana_tooltip.geometry(
            f"+{x}+{y}"
        )


        tk.Label(
            self.ventana_tooltip,
            text=self.texto,
            bg="#05080e",
            fg=COLOR_TEXTO,
            padx=9,
            pady=5,
            font=(
                "Segoe UI",
                8
            ),
            relief="solid",
            borderwidth=1
        ).pack()


    def ocultar(
        self,
        event=None
    ):

        self.cancelar()

        if self.ventana_tooltip:

            self.ventana_tooltip.destroy()

            self.ventana_tooltip = None


# =========================================================
# CONTENEDOR GENERAL
# =========================================================

marco_principal = tk.Frame(
    ventana,
    bg=COLOR_FONDO
)

marco_principal.place(
    x=18,
    y=18,
    width=824,
    height=534
)


# =========================================================
# CABECERA
# =========================================================

cabecera = tk.Frame(
    marco_principal,
    bg=COLOR_PANEL
)

cabecera.place(
    x=0,
    y=0,
    width=824,
    height=62
)


logo_cabecera_imagen = assets.cargar_tk(
    "logo.png",
    (42, 42)
)


logo_cabecera = tk.Label(
    cabecera,
    bg=COLOR_PANEL,
    borderwidth=0
)


if logo_cabecera_imagen is not None:

    logo_cabecera.config(
        image=logo_cabecera_imagen
    )

else:

    logo_cabecera.config(
        text="♫",
        fg=COLOR_CYAN,
        font=(
            "Segoe UI",
            20,
            "bold"
        )
    )


logo_cabecera.place(
    x=15,
    y=10,
    width=42,
    height=42
)


titulo_app = tk.Label(
    cabecera,
    text="LITESYDUG",
    bg=COLOR_PANEL,
    fg=COLOR_ACENTO_CLARO,
    font=(
        "Segoe UI",
        14,
        "bold"
    )
)

titulo_app.place(
    x=68,
    y=6
)


subtitulo_app = tk.Label(
    cabecera,
    text=(
        "Disfruta de este reproductor de canciones optimizado para Windows,\n"
        f"servido por Vulthy dev, {VERSION_APP}"
    ),
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO_SECUNDARIO,
    font=(
        "Segoe UI",
        7
    ),
    justify="left"
)

subtitulo_app.place(
    x=69,
    y=29
)


estado_app = tk.Label(
    cabecera,
    text="LOCAL PLAYER",
    bg=COLOR_PANEL_INTERNO,
    fg=COLOR_CYAN,
    font=(
        "Segoe UI",
        7,
        "bold"
    ),
    padx=10,
    pady=4
)

estado_app.place(
    x=580,
    y=19
)


boton_mini = tk.Button(
    cabecera,
    text="MINI",
    bg=COLOR_BOTON,
    fg=COLOR_CYAN,
    activebackground=COLOR_BOTON_HOVER,
    activeforeground=COLOR_CYAN,
    borderwidth=0,
    font=(
        "Segoe UI",
        8,
        "bold"
    ),
    cursor="hand2"
)

boton_mini.place(
    x=690,
    y=16,
    width=52,
    height=30
)


boton_ajustes = tk.Button(
    cabecera,
    text="⚙",
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO,
    activebackground=COLOR_BOTON_HOVER,
    activeforeground=COLOR_CYAN,
    borderwidth=0,
    font=(
        "Segoe UI Symbol",
        12
    ),
    cursor="hand2"
)

boton_ajustes.place(
    x=752,
    y=16,
    width=45,
    height=30
)


# =========================================================
# PANELES
# =========================================================

panel_izquierdo = tk.Frame(
    marco_principal,
    bg=COLOR_PANEL
)

panel_izquierdo.place(
    x=0,
    y=74,
    width=270,
    height=460
)


panel_derecho = tk.Frame(
    marco_principal,
    bg=COLOR_PANEL
)

panel_derecho.place(
    x=282,
    y=74,
    width=542,
    height=460
)


# =========================================================
# NOW PLAYING
# =========================================================

titulo_now = tk.Label(
    panel_izquierdo,
    text="NOW PLAYING",
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO_SECUNDARIO,
    font=(
        "Segoe UI",
        8,
        "bold"
    )
)

titulo_now.place(
    x=18,
    y=15
)


# =========================================================
# PORTADA
# =========================================================

marco_portada = tk.Frame(
    panel_izquierdo,
    bg=COLOR_BORDE
)

marco_portada.place(
    x=41,
    y=48,
    width=188,
    height=188
)


portada_default_inicial = assets.cargar_tk(
    "cover_default.png",
    (180, 180)
)


portada = tk.Label(
    marco_portada,
    bg=COLOR_PANEL_INTERNO,
    fg=COLOR_CYAN,
    borderwidth=0
)


if portada_default_inicial is not None:

    portada.config(
        image=portada_default_inicial
    )

else:

    portada.config(
        text="NO COVER",
        font=(
            "Segoe UI",
            9,
            "bold"
        )
    )


portada.place(
    x=4,
    y=4,
    width=180,
    height=180
)


# =========================================================
# INFO CANCIÓN
# =========================================================

nombre_cancion = tk.Label(
    panel_izquierdo,
    text="Ninguna canción",
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO,
    font=(
        "Segoe UI",
        11,
        "bold"
    ),
    wraplength=230,
    justify="center"
)

nombre_cancion.place(
    x=17,
    y=255,
    width=236,
    height=50
)


texto_artista = tk.Label(
    panel_izquierdo,
    text="Selecciona una canción",
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO_SECUNDARIO,
    font=(
        "Segoe UI",
        9
    ),
    wraplength=230,
    justify="center"
)

texto_artista.place(
    x=20,
    y=306,
    width=230,
    height=34
)


estado = tk.Label(
    panel_izquierdo,
    text="",
    bg=COLOR_PANEL,
    fg=COLOR_CYAN,
    font=(
        "Segoe UI",
        8,
        "bold"
    )
)

estado.place(
    x=20,
    y=344,
    width=230,
    height=20
)


# =========================================================
# ABRIR
# =========================================================

boton_abrir = tk.Button(
    panel_izquierdo,
    text="📁  ABRIR",
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO,
    activebackground=COLOR_ACENTO,
    activeforeground="white",
    borderwidth=0,
    font=(
        "Segoe UI",
        9,
        "bold"
    ),
    cursor="hand2"
)

boton_abrir.place(
    x=38,
    y=390,
    width=194,
    height=40
)


# =========================================================
# LIBRARY
# =========================================================

titulo_lista = tk.Label(
    panel_derecho,
    text="LIBRARY",
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO,
    font=(
        "Segoe UI",
        14,
        "bold"
    )
)

titulo_lista.place(
    x=18,
    y=12
)


contador_canciones = tk.Label(
    panel_derecho,
    text="0 canciones",
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO_SECUNDARIO,
    font=(
        "Segoe UI",
        8
    ),
    anchor="e"
)

contador_canciones.place(
    x=420,
    y=17,
    width=100
)


# =========================================================
# ORDEN
# =========================================================

texto_orden = tk.Label(
    panel_derecho,
    text="ORDEN",
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO_SECUNDARIO,
    font=(
        "Segoe UI",
        7,
        "bold"
    )
)

texto_orden.place(
    x=18,
    y=54
)


opciones_orden = (
    "Nombre A-Z",
    "Nombre Z-A",
    "Más recientes",
    "Más antiguos",
    "Mayor tamaño",
    "Menor tamaño"
)


selector_orden = ttk.Combobox(
    panel_derecho,
    values=opciones_orden,
    state="readonly",
    width=20,
    style="Retro.TCombobox"
)

selector_orden.set(
    "Nombre A-Z"
)

selector_orden.place(
    x=72,
    y=49
)


# =========================================================
# LISTA
# =========================================================

marco_lista = tk.Frame(
    panel_derecho,
    bg=COLOR_BORDE
)

marco_lista.place(
    x=18,
    y=88,
    width=506,
    height=235
)


# =========================================================
# BUSCADOR DE CANCIONES
# =========================================================

entrada_busqueda = tk.Entry(
    marco_lista,
    textvariable=texto_busqueda,
    bg=COLOR_PANEL_INTERNO,
    fg=COLOR_TEXTO_SECUNDARIO,
    insertbackground=COLOR_TEXTO,
    relief="flat",
    borderwidth=0,
    font=(
        "Segoe UI",
        9
    )
)

entrada_busqueda.place(
    x=3,
    y=3,
    width=445,
    height=26
)

# =========================================================
# LIMPIAR BUSCADOR
# =========================================================

def limpiar_busqueda():

    texto_busqueda.set(
        PLACEHOLDER_BUSQUEDA
    )


    entrada_busqueda.config(
        fg=COLOR_TEXTO_SECUNDARIO
    )


    actualizar_lista_visual()


    ventana.focus_set()
boton_limpiar_busqueda = tk.Button(
    marco_lista,
    text="✕",
    command=lambda: limpiar_busqueda(),
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO_SECUNDARIO,
    activebackground=COLOR_BOTON_HOVER,
    activeforeground=COLOR_TEXTO,
    borderwidth=0,
    font=(
        "Segoe UI",
        8,
        "bold"
    ),
    cursor="hand2"
)

boton_limpiar_busqueda.place(
    x=451,
    y=3,
    width=31,
    height=26
)


# =========================================================
# SCROLLBAR
# =========================================================

scroll_lista = tk.Scrollbar(
    marco_lista,
    orient=tk.VERTICAL,
    bg=COLOR_BOTON,
    troughcolor=COLOR_PANEL_INTERNO,
    activebackground=COLOR_ACENTO,
    borderwidth=0,
    highlightthickness=0
)

scroll_lista.place(
    x=482,
    y=34,
    width=20,
    height=198
)


# =========================================================
# LISTBOX
# =========================================================

lista_canciones = tk.Listbox(
    marco_lista,
    bg=COLOR_LISTA,
    fg=COLOR_TEXTO,
    selectbackground=COLOR_ACENTO,
    selectforeground="white",
    activestyle="none",
    borderwidth=0,
    highlightthickness=0,
    font=(
        "Segoe UI",
        10
    ),
    yscrollcommand=scroll_lista.set,
    selectmode=tk.SINGLE
)

lista_canciones.place(
    x=3,
    y=34,
    width=479,
    height=198
)


scroll_lista.config(
    command=lista_canciones.yview
)


# =========================================================
# MINI INFO
# =========================================================

def actualizar_info_mini():

    global mini_portada_imagen


    if ventana_mini is None:
        return


    try:

        if not ventana_mini.winfo_exists():
            return

    except Exception:
        return


    if player.indice_actual is None:

        if mini_nombre_cancion is not None:

            mini_nombre_cancion.config(
                text="Ninguna canción"
            )


        if mini_texto_artista is not None:

            mini_texto_artista.config(
                text="Selecciona una canción"
            )

        return


    ruta = library.obtener_ruta(
        player.indice_actual
    )


    if ruta is None:
        return


    titulo, artista = library.obtener_metadata(
        ruta
    )


    mini_nombre_cancion.config(
        text=titulo
    )


    mini_texto_artista.config(
        text=artista
    )


    imagen = library.obtener_portada(
        ruta,
        tamano=(64, 64)
    )


    if imagen is not None:

        mini_portada_imagen = imagen

        mini_portada.config(
            image=mini_portada_imagen,
            text=""
        )


# =========================================================
# INFORMACIÓN
# =========================================================

def mostrar_informacion(
    indice
):

    global portada_imagen


    ruta = library.obtener_ruta(
        indice
    )


    if ruta is None:
        return


    titulo, artista = library.obtener_metadata(
        ruta
    )


    duracion = library.obtener_duracion(
        ruta
    )


    nombre_cancion.config(
        text=titulo
    )


    texto_artista.config(
        text=artista
    )


    estado.config(
        text=library.convertir_tiempo(
            duracion
        )
    )


    imagen = library.obtener_portada(
        ruta,
        tamano=(180, 180)
    )


    if imagen is not None:

        portada_imagen = imagen

        portada.config(
            image=portada_imagen,
            text=""
        )

    else:

        portada_imagen = None

        portada.config(
            image="",
            text="NO COVER"
        )


    actualizar_info_mini()


# =========================================================
# BUSCADOR / LISTA VISUAL
# =========================================================

PLACEHOLDER_BUSQUEDA = "Buscar canción..."


def obtener_rutas_visibles():

    termino = texto_busqueda.get().strip()


    if (
        not termino
        or termino == PLACEHOLDER_BUSQUEDA
    ):

        return list(
            library.obtener_rutas()
        )


    termino = termino.lower()

    resultados = []


    for ruta in library.obtener_rutas():

        nombre_archivo = (
            library.nombre_sin_extension(
                ruta
            )
        )


        titulo, artista = (
            library.obtener_metadata(
                ruta
            )
        )


        texto_completo = (
            f"{nombre_archivo} "
            f"{titulo} "
            f"{artista}"
        ).lower()


        if termino in texto_completo:

            resultados.append(
                ruta
            )


    return resultados


def actualizar_lista_visual():

    global rutas_filtradas


    rutas_filtradas = (
        obtener_rutas_visibles()
    )


    lista_canciones.delete(
        0,
        tk.END
    )


    for ruta in rutas_filtradas:

        nombre = (
            library.nombre_sin_extension(
                ruta
            )
        )


        lista_canciones.insert(
            tk.END,
            nombre
        )


    cantidad_total = (
        library.cantidad()
    )


    if cantidad_total == 1:

        contador_canciones.config(
            text="1 canción"
        )

    else:

        contador_canciones.config(
            text=f"{cantidad_total} canciones"
        )


def actualizar_busqueda(
    *args
):

    actualizar_lista_visual()

# =========================================================
# ENTER EN BUSCADOR
# =========================================================

def reproducir_primer_resultado(
    event=None
):

    if not rutas_filtradas:

        return


    lista_canciones.selection_clear(
        0,
        tk.END
    )


    lista_canciones.selection_set(
        0
    )


    lista_canciones.activate(
        0
    )


    lista_canciones.see(
        0
    )


    reproducir_cancion()
def obtener_indice_real(
    indice_visual
):

    if not (
        0 <= indice_visual
        < len(rutas_filtradas)
    ):

        return None


    ruta = rutas_filtradas[
        indice_visual
    ]


    try:

        return (
            library.rutas.index(
                ruta
            )
        )

    except ValueError:

        return None


# =========================================================
# PLACEHOLDER DEL BUSCADOR
# =========================================================

def entrar_buscador(
    event=None
):

    if (
        texto_busqueda.get()
        == PLACEHOLDER_BUSQUEDA
    ):

        texto_busqueda.set(
            ""
        )


        entrada_busqueda.config(
            fg=COLOR_TEXTO
        )


def salir_buscador(
    event=None
):

    if not texto_busqueda.get().strip():

        texto_busqueda.set(
            PLACEHOLDER_BUSQUEDA
        )


        entrada_busqueda.config(
            fg=COLOR_TEXTO_SECUNDARIO
        )


# =========================================================
# ORDENAR
# =========================================================

def ordenar_canciones(
    event=None
):

    ruta_actual = None


    if player.indice_actual is not None:

        rutas = library.obtener_rutas()


        if (
            0 <= player.indice_actual < len(rutas)
        ):

            ruta_actual = rutas[
                player.indice_actual
            ]


    library.ordenar(
        selector_orden.get()
    )


    actualizar_lista_visual()


    rutas = library.obtener_rutas()


    player.establecer_canciones(
        rutas
    )


    if ruta_actual in rutas:

        player.indice_actual = rutas.index(
            ruta_actual
        )


# =========================================================
# ABRIR CARPETA
# =========================================================

def abrir_carpeta():

    global ultima_carpeta


    carpeta = filedialog.askdirectory(
        initialdir=(
            ultima_carpeta
            if ultima_carpeta
            else None
        )
    )


    if not carpeta:
        return


    library.cargar_carpeta(
        carpeta
    )


    ultima_carpeta = carpeta


    ordenar_canciones()


    texto_busqueda.set(
        PLACEHOLDER_BUSQUEDA
    )


    entrada_busqueda.config(
        fg=COLOR_TEXTO_SECUNDARIO
    )


    actualizar_lista_visual()


    if recordar_ultima_carpeta:

        config.establecer(
            "ultima_carpeta",
            carpeta
        )

    else:

        config.establecer(
            "ultima_carpeta",
            ""
        )


    config.guardar()


# =========================================================
# SELECCIONAR
# =========================================================

def seleccionar_cancion(
    event=None
):

    seleccion = (
        lista_canciones.curselection()
    )


    if not seleccion:

        return


    indice_visual = seleccion[0]


    indice_real = obtener_indice_real(
        indice_visual
    )


    if indice_real is None:

        return


    mostrar_informacion(
        indice_real
    )


# =========================================================
# REPRODUCIR
# =========================================================

def reproducir_cancion(
    event=None
):

    seleccion = (
        lista_canciones.curselection()
    )


    if not seleccion:

        return


    indice_visual = seleccion[0]


    indice_real = obtener_indice_real(
        indice_visual
    )


    if indice_real is None:

        return


    ruta = library.obtener_ruta(
        indice_real
    )


    if ruta is None:

        return


    # -----------------------------------------------------
    # ARCHIVO ELIMINADO / MOVIDO
    # -----------------------------------------------------

    if not os.path.isfile(
        ruta
    ):

        try:

            library.rutas.remove(
                ruta
            )

        except ValueError:

            pass


        player.establecer_canciones(
            library.rutas
        )


        actualizar_lista_visual()

        return


    # -----------------------------------------------------
    # DURACIÓN
    # -----------------------------------------------------

    duracion = (
        library.obtener_duracion(
            ruta
        )
    )


    # -----------------------------------------------------
    # REPRODUCIR
    # -----------------------------------------------------

    if player.reproducir(
        indice_real,
        duracion
    ):

        barra_tiempo.config(
            to=max(
                duracion,
                1
            )
        )


        barra_tiempo.set(
            0
        )


        boton_play_pausa.config(
            text="⏸"
        )


        if mini_barra_tiempo is not None:

            try:

                mini_barra_tiempo.config(
                    to=max(
                        duracion,
                        1
                    )
                )


                mini_barra_tiempo.set(
                    0
                )

            except Exception:

                pass


        if mini_boton_play is not None:

            try:

                mini_boton_play.config(
                    text="⏸"
                )

            except Exception:

                pass


        mostrar_informacion(
            indice_real
        )


# =========================================================
# PLAY / PAUSA
# =========================================================

def play_pausa(
    event=None
):

    resultado = player.play_pausa()


    if resultado == "sin_cancion":

        reproducir_cancion()


    elif resultado == "reproduciendo":

        boton_play_pausa.config(
            text="⏸"
        )


        if mini_boton_play is not None:

            try:

                mini_boton_play.config(
                    text="⏸"
                )

            except Exception:
                pass


    elif resultado == "pausado":

        boton_play_pausa.config(
            text="▶"
        )


        if mini_boton_play is not None:

            try:

                mini_boton_play.config(
                    text="▶"
                )

            except Exception:
                pass


# =========================================================
# SELECCIONAR ÍNDICE
# =========================================================

def seleccionar_indice(
    indice
):

    if indice is None:

        return


    if not (
        0 <= indice
        < len(library.rutas)
    ):

        return


    ruta = library.rutas[
        indice
    ]


    # -----------------------------------------------------
    # ARCHIVO YA NO EXISTE
    # -----------------------------------------------------

    if not os.path.isfile(
        ruta
    ):

        try:

            library.rutas.remove(
                ruta
            )

        except ValueError:

            pass


        player.establecer_canciones(
            library.rutas
        )


        actualizar_lista_visual()

        return


    # -----------------------------------------------------
    # SI EL FILTRO OCULTA LA CANCIÓN
    # -----------------------------------------------------

    if ruta not in rutas_filtradas:

        texto_busqueda.set(
            PLACEHOLDER_BUSQUEDA
        )


        entrada_busqueda.config(
            fg=COLOR_TEXTO_SECUNDARIO
        )


        actualizar_lista_visual()


    # -----------------------------------------------------
    # BUSCAR ÍNDICE VISUAL
    # -----------------------------------------------------

    try:

        indice_visual = (
            rutas_filtradas.index(
                ruta
            )
        )

    except ValueError:

        return


    lista_canciones.selection_clear(
        0,
        tk.END
    )


    lista_canciones.selection_set(
        indice_visual
    )


    lista_canciones.activate(
        indice_visual
    )


    lista_canciones.see(
        indice_visual
    )


    reproducir_cancion()


# =========================================================
# SIGUIENTE
# =========================================================

def siguiente_cancion(
    event=None
):

    if library.cantidad() == 0:
        return


    if modo_aleatorio:

        indice = random.randrange(
            library.cantidad()
        )

    else:

        indice = player.siguiente_indice()


    seleccionar_indice(
        indice
    )


# =========================================================
# ANTERIOR
# =========================================================

def anterior_cancion(
    event=None
):

    if library.cantidad() == 0:
        return


    indice = player.anterior_indice()


    seleccionar_indice(
        indice
    )


# =========================================================
# ± SALTO
# =========================================================

def adelantar_10(
    event=None
):

    if not player.hay_cancion_cargada:
        return


    posicion_actual = (
        player.obtener_posicion_actual()
    )


    nueva_posicion = min(
        posicion_actual + salto_segundos,
        player.duracion_actual
    )


    player.ir_a_posicion(
        nueva_posicion
    )


    boton_play_pausa.config(
        text="⏸"
    )


    if mini_boton_play is not None:

        try:

            mini_boton_play.config(
                text="⏸"
            )

        except Exception:
            pass


def retroceder_10(
    event=None
):

    if not player.hay_cancion_cargada:
        return


    posicion_actual = (
        player.obtener_posicion_actual()
    )


    nueva_posicion = max(
        posicion_actual - salto_segundos,
        0
    )


    player.ir_a_posicion(
        nueva_posicion
    )


    boton_play_pausa.config(
        text="⏸"
    )


    if mini_boton_play is not None:

        try:

            mini_boton_play.config(
                text="⏸"
            )

        except Exception:
            pass


# =========================================================
# SHUFFLE
# =========================================================

def alternar_shuffle():

    global modo_aleatorio


    modo_aleatorio = not modo_aleatorio


    boton_shuffle.config(
        bg=(
            COLOR_ROSA
            if modo_aleatorio
            else COLOR_BOTON
        )
    )


# =========================================================
# REPEAT
# =========================================================

def alternar_repeat():

    global modo_repetir


    modo_repetir = not modo_repetir


    boton_repeat.config(
        bg=(
            COLOR_CYAN
            if modo_repetir
            else COLOR_BOTON
        )
    )


# =========================================================
# VOLUMEN
# =========================================================

def cambiar_volumen(
    valor
):

    porcentaje = int(
        float(valor)
    )


    player.establecer_volumen(
        porcentaje / 100
    )


    texto_volumen.config(
        text=f"{porcentaje}%"
    )


def guardar_volumen(
    event=None
):

    porcentaje = int(
        control_volumen.get()
    )


    config.establecer(
        "volumen",
        porcentaje
    )


    config.guardar()


def subir_volumen():

    actual = int(
        control_volumen.get()
    )


    nuevo = min(
        actual + paso_volumen,
        100
    )


    control_volumen.set(
        nuevo
    )


    player.establecer_volumen(
        nuevo / 100
    )


    texto_volumen.config(
        text=f"{nuevo}%"
    )


def bajar_volumen():

    actual = int(
        control_volumen.get()
    )


    nuevo = max(
        actual - paso_volumen,
        0
    )


    control_volumen.set(
        nuevo
    )


    player.establecer_volumen(
        nuevo / 100
    )


    texto_volumen.config(
        text=f"{nuevo}%"
    )


def alternar_mute():

    global volumen_antes_mute


    volumen_actual = int(
        control_volumen.get()
    )


    if volumen_actual > 0:

        volumen_antes_mute = (
            volumen_actual
        )


        control_volumen.set(
            0
        )


        player.establecer_volumen(
            0
        )


        texto_volumen.config(
            text="0%"
        )


        boton_mute.config(
            text="🔇"
        )


    else:

        if volumen_antes_mute <= 0:

            volumen_antes_mute = 70


        control_volumen.set(
            volumen_antes_mute
        )


        player.establecer_volumen(
            volumen_antes_mute / 100
        )


        texto_volumen.config(
            text=f"{volumen_antes_mute}%"
        )


        boton_mute.config(
            text="🔊"
        )


# =========================================================
# BARRA TIEMPO PRINCIPAL
# =========================================================

def empezar_arrastre(
    event
):

    global usuario_moviendo_barra

    usuario_moviendo_barra = True


def terminar_arrastre(
    event
):

    global usuario_moviendo_barra


    usuario_moviendo_barra = False


    player.ir_a_posicion(
        barra_tiempo.get()
    )


# =========================================================
# CONTROLES PRINCIPALES
# =========================================================

marco_controles = tk.Frame(
    panel_derecho,
    bg=COLOR_PANEL_2
)

marco_controles.place(
    x=18,
    y=337,
    width=506,
    height=105
)


boton_shuffle = tk.Button(
    marco_controles,
    text="🔀",
    command=alternar_shuffle,
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO,
    activebackground=COLOR_BOTON_HOVER,
    activeforeground="white",
    borderwidth=0,
    font=("Segoe UI Emoji", 10),
    cursor="hand2"
)

boton_shuffle.place(
    x=14,
    y=14,
    width=42,
    height=36
)


boton_anterior = tk.Button(
    marco_controles,
    text="⏮️",
    command=anterior_cancion,
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO,
    activebackground=COLOR_BOTON_HOVER,
    activeforeground="white",
    borderwidth=0,
    font=("Segoe UI Emoji", 10),
    cursor="hand2"
)

boton_anterior.place(
    x=66,
    y=14,
    width=42,
    height=36
)


boton_atras_10 = tk.Button(
    marco_controles,
    text="⏪",
    command=retroceder_10,
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO,
    activebackground=COLOR_BOTON_HOVER,
    activeforeground="white",
    borderwidth=0,
    font=("Segoe UI Emoji", 10),
    cursor="hand2"
)

boton_atras_10.place(
    x=118,
    y=14,
    width=42,
    height=36
)


boton_play_pausa = tk.Button(
    marco_controles,
    text="▶",
    command=play_pausa,
    bg=COLOR_ACENTO,
    fg="white",
    activebackground=COLOR_ACENTO_CLARO,
    activeforeground="white",
    borderwidth=0,
    cursor="hand2",
    font=(
        "Segoe UI",
        12,
        "bold"
    )
)

boton_play_pausa.place(
    x=171,
    y=8,
    width=54,
    height=48
)


boton_adelante_10 = tk.Button(
    marco_controles,
    text="⏩",
    command=adelantar_10,
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO,
    activebackground=COLOR_BOTON_HOVER,
    activeforeground="white",
    borderwidth=0,
    font=("Segoe UI Emoji", 10),
    cursor="hand2"
)

boton_adelante_10.place(
    x=236,
    y=14,
    width=42,
    height=36
)


boton_siguiente = tk.Button(
    marco_controles,
    text="⏭️",
    command=siguiente_cancion,
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO,
    activebackground=COLOR_BOTON_HOVER,
    activeforeground="white",
    borderwidth=0,
    font=("Segoe UI Emoji", 10),
    cursor="hand2"
)

boton_siguiente.place(
    x=288,
    y=14,
    width=42,
    height=36
)


boton_repeat = tk.Button(
    marco_controles,
    text="🔁",
    command=alternar_repeat,
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO,
    activebackground=COLOR_BOTON_HOVER,
    activeforeground="white",
    borderwidth=0,
    font=("Segoe UI Emoji", 10),
    cursor="hand2"
)

boton_repeat.place(
    x=340,
    y=14,
    width=42,
    height=36
)


# =========================================================
# VOLUMEN
# =========================================================

boton_mute = tk.Button(
    marco_controles,
    text="🔊",
    command=alternar_mute,
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO,
    activebackground=COLOR_BOTON_HOVER,
    activeforeground="white",
    borderwidth=0,
    font=("Segoe UI Emoji", 10),
    cursor="hand2"
)

boton_mute.place(
    x=396,
    y=14,
    width=36,
    height=36
)


control_volumen = tk.Scale(
    marco_controles,
    from_=0,
    to=100,
    orient=tk.HORIZONTAL,
    showvalue=False,
    command=cambiar_volumen,
    bg=COLOR_PANEL_2,
    troughcolor=COLOR_PANEL_INTERNO,
    activebackground=COLOR_CYAN,
    highlightthickness=0,
    borderwidth=0,
    length=95
)

control_volumen.place(
    x=394,
    y=57
)


texto_volumen = tk.Label(
    marco_controles,
    text=f"{volumen_guardado}%",
    bg=COLOR_PANEL_2,
    fg=COLOR_TEXTO_SECUNDARIO,
    font=(
        "Segoe UI",
        7
    )
)

texto_volumen.place(
    x=465,
    y=18,
    width=36
)


control_volumen.set(
    volumen_guardado
)


player.establecer_volumen(
    volumen_guardado / 100
)


control_volumen.bind(
    "<ButtonRelease-1>",
    guardar_volumen
)


# =========================================================
# PROGRESO PRINCIPAL
# =========================================================

tiempo_actual = tk.Label(
    panel_derecho,
    text="0:00",
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO_SECUNDARIO,
    font=(
        "Segoe UI",
        7
    )
)

tiempo_actual.place(
    x=18,
    y=443
)


barra_tiempo = tk.Scale(
    panel_derecho,
    from_=0,
    to=1,
    orient=tk.HORIZONTAL,
    showvalue=False,
    bg=COLOR_PANEL,
    troughcolor=COLOR_PANEL_INTERNO,
    activebackground=COLOR_ACENTO,
    highlightthickness=0,
    borderwidth=0,
    sliderlength=22,
    width=15,
    length=430
)

barra_tiempo.place(
    x=52,
    y=425
)


tiempo_total = tk.Label(
    panel_derecho,
    text="0:00",
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO_SECUNDARIO,
    font=(
        "Segoe UI",
        7
    )
)

tiempo_total.place(
    x=487,
    y=443
)


# =========================================================
# ACTUALIZAR TIEMPO
# =========================================================

def obtener_intervalo_actualizacion():

    # -----------------------------------------------------
    # ULTRA LIGERO
    # -----------------------------------------------------

    if modo_rendimiento == "Ultra ligero":

        try:

            if ventana.state() == "withdrawn":

                return 5000

        except Exception:

            pass


        return 2000


    # -----------------------------------------------------
    # AHORRO
    # -----------------------------------------------------

    elif modo_rendimiento == "Ahorro":

        return 1000


    # -----------------------------------------------------
    # NORMAL
    # -----------------------------------------------------

    else:

        return 500


def actualizar_tiempo():

    if player.hay_cancion_cargada:

        posicion = player.obtener_posicion_actual()


        # -------------------------------------------------
        # SABER SI PRINCIPAL ESTÁ VISIBLE
        # -------------------------------------------------

        try:

            ventana_principal_visible = (
                ventana.state() != "withdrawn"
            )

        except Exception:

            ventana_principal_visible = True


        # -------------------------------------------------
        # INTERFAZ PRINCIPAL
        # -------------------------------------------------

        if ventana_principal_visible:

            if not usuario_moviendo_barra:

                barra_tiempo.set(
                    posicion
                )


            tiempo_actual.config(
                text=library.convertir_tiempo(
                    posicion
                )
            )


            tiempo_total.config(
                text=library.convertir_tiempo(
                    player.duracion_actual
                )
            )


        # -------------------------------------------------
        # TIEMPO MINI
        # -------------------------------------------------

        if mini_tiempo is not None:

            try:

                mini_tiempo.config(
                    text=(
                        library.convertir_tiempo(
                            posicion
                        )
                        + " / "
                        + library.convertir_tiempo(
                            player.duracion_actual
                        )
                    )
                )

            except Exception:

                pass


        # -------------------------------------------------
        # BARRA MINI
        # -------------------------------------------------

        if mini_barra_tiempo is not None:

            try:

                mini_barra_tiempo.config(
                    to=max(
                        player.duracion_actual,
                        1
                    )
                )


                if not usuario_moviendo_barra_mini:

                    mini_barra_tiempo.set(
                        posicion
                    )

            except Exception:

                pass


    ventana.after(
        obtener_intervalo_actualizacion(),
        actualizar_tiempo
    )


# =========================================================
# VIGILAR FIN DE CANCIÓN
# =========================================================

def vigilar_fin_cancion():

    if player.hay_cancion_cargada:

        if (
            not player.esta_reproduciendo()
            and not player.esta_pausado
        ):

            if modo_repetir:

                seleccionar_indice(
                    player.indice_actual
                )

            else:

                siguiente_cancion()


    # Esto es muy ligero:
    # solo comprobamos estado, no refrescamos toda la UI.

    ventana.after(
        500,
        vigilar_fin_cancion
    )
def empezar_arrastre_mini(
    event
):

    global usuario_moviendo_barra_mini

    usuario_moviendo_barra_mini = True


def terminar_arrastre_mini(
    event
):

    global usuario_moviendo_barra_mini

    usuario_moviendo_barra_mini = False


    if mini_barra_tiempo is not None:

        player.ir_a_posicion(
            mini_barra_tiempo.get()
        )


# =========================================================
# CERRAR MINI
# =========================================================

def cerrar_mini():

    global ventana_mini
    global mini_nombre_cancion
    global mini_texto_artista
    global mini_boton_play
    global mini_tiempo
    global mini_portada
    global mini_barra_tiempo
    global mini_portada_imagen
    global ventana_oculta


    if ventana_mini is not None:

        try:

            ventana_mini.destroy()

        except Exception:
            pass


    ventana_mini = None
    mini_nombre_cancion = None
    mini_texto_artista = None
    mini_boton_play = None
    mini_tiempo = None
    mini_portada = None
    mini_barra_tiempo = None
    mini_portada_imagen = None


    ventana.deiconify()

    ventana.lift()

    ventana.focus_force()


    ventana_oculta = False


    hotkey_manager.establecer_ventana_oculta(
        False
    )


# =========================================================
# ABRIR MINI
# =========================================================

def abrir_mini():

    global ventana_mini
    global mini_nombre_cancion
    global mini_texto_artista
    global mini_boton_play
    global mini_tiempo
    global mini_portada
    global mini_barra_tiempo
    global mini_portada_imagen
    global ventana_oculta


    # -----------------------------------------------------
    # SI YA EXISTE
    # -----------------------------------------------------

    if ventana_mini is not None:

        try:

            if ventana_mini.winfo_exists():

                ventana_mini.lift()

                return

        except Exception:
            pass


    # -----------------------------------------------------
    # OCULTAR PRINCIPAL
    # -----------------------------------------------------

    ventana.withdraw()


    ventana_oculta = True


    hotkey_manager.establecer_ventana_oculta(
        True
    )


    # -----------------------------------------------------
    # VENTANA
    # -----------------------------------------------------

    ventana_mini = tk.Toplevel(
        ventana
    )


    ventana_mini.title(
        "LITESYDUG MINI"
    )


    ventana_mini.geometry(
        "430x195"
    )


    ventana_mini.resizable(
        False,
        False
    )


    ventana_mini.configure(
        bg=COLOR_FONDO
    )


    if logo_ventana is not None:

        try:

            ventana_mini.iconphoto(
                True,
                logo_ventana
            )

        except Exception:
            pass


    ventana_mini.protocol(
        "WM_DELETE_WINDOW",
        cerrar_mini
    )


    # -----------------------------------------------------
    # PANEL
    # -----------------------------------------------------

    mini_panel = tk.Frame(
        ventana_mini,
        bg=COLOR_PANEL,
        highlightbackground=COLOR_ACENTO,
        highlightthickness=1
    )


    mini_panel.place(
        x=8,
        y=8,
        width=414,
        height=179
    )


    # -----------------------------------------------------
    # PORTADA
    # -----------------------------------------------------

    mini_portada_imagen = assets.cargar_tk(
        "cover_default.png",
        (64, 64)
    )


    mini_portada = tk.Label(
        mini_panel,
        bg=COLOR_PANEL_INTERNO,
        fg=COLOR_CYAN,
        borderwidth=0
    )


    if mini_portada_imagen is not None:

        mini_portada.config(
            image=mini_portada_imagen
        )

    else:

        mini_portada.config(
            text="NO\nCOVER",
            font=(
                "Segoe UI",
                7,
                "bold"
            )
        )


    mini_portada.place(
        x=12,
        y=12,
        width=64,
        height=64
    )


    # -----------------------------------------------------
    # NOMBRE
    # -----------------------------------------------------

    mini_nombre_cancion = tk.Label(
        mini_panel,
        text="Ninguna canción",
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO,
        anchor="w",
        font=(
            "Segoe UI",
            10,
            "bold"
        )
    )


    mini_nombre_cancion.place(
        x=88,
        y=10,
        width=220,
        height=23
    )


    # -----------------------------------------------------
    # ARTISTA
    # -----------------------------------------------------

    mini_texto_artista = tk.Label(
        mini_panel,
        text="Selecciona una canción",
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO_SECUNDARIO,
        anchor="w",
        font=(
            "Segoe UI",
            8
        )
    )


    mini_texto_artista.place(
        x=88,
        y=34,
        width=220,
        height=20
    )


    # -----------------------------------------------------
    # TIEMPO
    # -----------------------------------------------------

    mini_tiempo = tk.Label(
        mini_panel,
        text="0:00 / 0:00",
        bg=COLOR_PANEL,
        fg=COLOR_CYAN,
        anchor="w",
        font=(
            "Segoe UI",
            7,
            "bold"
        )
    )


    mini_tiempo.place(
        x=88,
        y=55,
        width=135,
        height=18
    )


    # -----------------------------------------------------
    # MOSTRAR ENCIMA
    # -----------------------------------------------------

    variable_top = tk.BooleanVar(
        value=mini_siempre_encima
    )


    def cambiar_siempre_encima():

        ventana_mini.attributes(
            "-topmost",
            variable_top.get()
        )


    checkbox_top = tk.Checkbutton(
        mini_panel,
        text="MOSTRAR ENCIMA",
        variable=variable_top,
        command=cambiar_siempre_encima,
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO_SECUNDARIO,
        activebackground=COLOR_PANEL,
        activeforeground=COLOR_TEXTO,
        selectcolor=COLOR_PANEL_INTERNO,
        font=(
            "Segoe UI",
            7
        ),
        cursor="hand2"
    )


    checkbox_top.place(
        x=270,
        y=52
    )


    ventana_mini.attributes(
        "-topmost",
        mini_siempre_encima
    )


    # -----------------------------------------------------
    # VOLVER A MODO NORMAL
    # -----------------------------------------------------

    boton_modo_normal = tk.Button(
        mini_panel,
        text="↗",
        command=cerrar_mini,
        bg=COLOR_BOTON,
        fg=COLOR_CYAN,
        activebackground=COLOR_BOTON_HOVER,
        activeforeground="white",
        borderwidth=0,
        font=(
            "Segoe UI Symbol",
            10,
            "bold"
        ),
        cursor="hand2"
    )


    boton_modo_normal.place(
        x=375,
        y=10,
        width=26,
        height=24
    )


    # -----------------------------------------------------
    # BARRA DE PROGRESO
    # -----------------------------------------------------

    mini_barra_tiempo = tk.Scale(
        mini_panel,
        from_=0,
        to=max(
            player.duracion_actual,
            1
        ),
        orient=tk.HORIZONTAL,
        showvalue=False,
        bg=COLOR_PANEL,
        troughcolor=COLOR_PANEL_INTERNO,
        activebackground=COLOR_ACENTO,
        highlightthickness=0,
        borderwidth=0,
        sliderlength=18,
        width=10,
        length=370
    )


    mini_barra_tiempo.place(
        x=20,
        y=78
    )


    if player.hay_cancion_cargada:

        mini_barra_tiempo.set(
            player.obtener_posicion_actual()
        )


    mini_barra_tiempo.bind(
        "<ButtonPress-1>",
        empezar_arrastre_mini
    )


    mini_barra_tiempo.bind(
        "<ButtonRelease-1>",
        terminar_arrastre_mini
    )


    # -----------------------------------------------------
    # CONTENEDOR BOTONES
    # -----------------------------------------------------

    mini_botones = tk.Frame(
        mini_panel,
        bg=COLOR_PANEL
    )


    mini_botones.place(
        x=20,
        y=116,
        width=375,
        height=46
    )


    # -----------------------------------------------------
    # ANTERIOR
    # -----------------------------------------------------

    tk.Button(
        mini_botones,
        text="⏮️",
        command=anterior_cancion,
        bg=COLOR_BOTON,
        fg="white",
        activebackground=COLOR_BOTON_HOVER,
        activeforeground="white",
        borderwidth=0,
        font=("Segoe UI Emoji", 11),
        cursor="hand2"
    ).place(
        x=0,
        y=5,
        width=42,
        height=36
    )


    # -----------------------------------------------------
    # RETROCEDER
    # -----------------------------------------------------

    tk.Button(
        mini_botones,
        text="⏪",
        command=retroceder_10,
        bg=COLOR_BOTON,
        fg="white",
        activebackground=COLOR_BOTON_HOVER,
        activeforeground="white",
        borderwidth=0,
        font=("Segoe UI Emoji", 11),
        cursor="hand2"
    ).place(
        x=52,
        y=5,
        width=42,
        height=36
    )


    # -----------------------------------------------------
    # PLAY
    # -----------------------------------------------------

    mini_boton_play = tk.Button(
        mini_botones,
        text=(
            "⏸"
            if (
                player.hay_cancion_cargada
                and not player.esta_pausado
            )
            else "▶"
        ),
        command=play_pausa,
        bg=COLOR_ACENTO,
        fg="white",
        activebackground=COLOR_ACENTO_CLARO,
        activeforeground="white",
        borderwidth=0,
        font=(
            "Segoe UI",
            12,
            "bold"
        ),
        cursor="hand2"
    )


    mini_boton_play.place(
        x=104,
        y=0,
        width=50,
        height=45
    )


    # -----------------------------------------------------
    # ADELANTAR
    # -----------------------------------------------------

    tk.Button(
        mini_botones,
        text="⏩",
        command=adelantar_10,
        bg=COLOR_BOTON,
        fg="white",
        activebackground=COLOR_BOTON_HOVER,
        activeforeground="white",
        borderwidth=0,
        font=("Segoe UI Emoji", 11),
        cursor="hand2"
    ).place(
        x=164,
        y=5,
        width=42,
        height=36
    )


    # -----------------------------------------------------
    # SIGUIENTE
    # -----------------------------------------------------

    tk.Button(
        mini_botones,
        text="⏭️",
        command=siguiente_cancion,
        bg=COLOR_BOTON,
        fg="white",
        activebackground=COLOR_BOTON_HOVER,
        activeforeground="white",
        borderwidth=0,
        font=("Segoe UI Emoji", 11),
        cursor="hand2"
    ).place(
        x=216,
        y=5,
        width=42,
        height=36
    )


    # -----------------------------------------------------
    # VOLUMEN -
    # -----------------------------------------------------

    tk.Button(
        mini_botones,
        text="🔉",
        command=bajar_volumen,
        bg=COLOR_BOTON,
        fg="white",
        activebackground=COLOR_BOTON_HOVER,
        activeforeground="white",
        borderwidth=0,
        font=("Segoe UI Emoji", 11),
        cursor="hand2"
    ).place(
        x=278,
        y=5,
        width=42,
        height=36
    )


    # -----------------------------------------------------
    # VOLUMEN +
    # -----------------------------------------------------

    tk.Button(
        mini_botones,
        text="🔊",
        command=subir_volumen,
        bg=COLOR_BOTON,
        fg="white",
        activebackground=COLOR_BOTON_HOVER,
        activeforeground="white",
        borderwidth=0,
        font=("Segoe UI Emoji", 11),
        cursor="hand2"
    ).place(
        x=330,
        y=5,
        width=42,
        height=36
    )


    actualizar_info_mini()


# =========================================================
# AJUSTES
# =========================================================

def aplicar_ajustes_en_vivo(
    nuevos_datos

):

    global paso_volumen
    global salto_segundos
    global solo_hotkeys_oculto
    global cerrar_a_bandeja
    global recordar_ultima_carpeta
    global modo_rendimiento
    global mini_siempre_encima
    global mostrar_tooltips
    global recordar_posicion_ventana


    # -----------------------------------------------------
    # PASO DE VOLUMEN
    # -----------------------------------------------------

    paso_volumen = nuevos_datos.get(
        "paso_volumen",
        5
    )


    # -----------------------------------------------------
    # SALTO ADELANTE / ATRÁS
    # -----------------------------------------------------

    salto_segundos = nuevos_datos.get(
        "salto_segundos",
        10
    )


    # -----------------------------------------------------
    # MODO RENDIMIENTO
    # -----------------------------------------------------

    modo_rendimiento = nuevos_datos.get(
        "modo_rendimiento",
        "Normal"
    )


    # -----------------------------------------------------
    # MINI SIEMPRE ENCIMA
    # -----------------------------------------------------

    mini_siempre_encima = nuevos_datos.get(
        "mini_siempre_encima",
        True
    )


    if ventana_mini is not None:

        try:

            if ventana_mini.winfo_exists():

                ventana_mini.attributes(
                    "-topmost",
                    mini_siempre_encima
                )

        except Exception:

            pass


    # -----------------------------------------------------
    # MOSTRAR TOOLTIPS
    # -----------------------------------------------------

    mostrar_tooltips = nuevos_datos.get(
        "mostrar_tooltips",
        True
    )

    # -----------------------------------------------------
    # RECORDAR POSICIÓN DE VENTANA
    # -----------------------------------------------------

    recordar_posicion_ventana = nuevos_datos.get(
        "recordar_posicion_ventana",
        False
    )
    # -----------------------------------------------------
    # HOTKEYS SOLO OCULTO
    # -----------------------------------------------------

    solo_hotkeys_oculto = nuevos_datos.get(
        "solo_hotkeys_oculto",
        True
    )


    hotkey_manager.establecer_solo_oculto(
        solo_hotkeys_oculto
    )


    # -----------------------------------------------------
    # CERRAR A BANDEJA
    # -----------------------------------------------------

    cerrar_a_bandeja = nuevos_datos.get(
        "cerrar_a_bandeja",
        True
    )


    # -----------------------------------------------------
    # RECORDAR ÚLTIMA CARPETA
    # -----------------------------------------------------

    recordar_ultima_carpeta = nuevos_datos.get(
        "recordar_ultima_carpeta",
        True
    )


# =========================================================
# CREAR VENTANA DE AJUSTES
# =========================================================

ventana_ajustes = SettingsWindow(
    ventana_principal=ventana,
    config=config,
    hotkey_manager=hotkey_manager,
    colores=colores_ajustes,
    logo=logo_ventana,
    version=VERSION_APP,

    enlaces={
        "github": "https://github.com/VulthyDev",
        "kofi": "https://ko-fi.com/vulthydev",
        "soporte": "https://github.com/VulthyDev",
    },

    al_guardar=aplicar_ajustes_en_vivo
)


def abrir_ajustes():

    ventana_ajustes.abrir()


def abrir_ajustes():

    ventana_ajustes.abrir()

# =========================================================
# TOOLTIPS
# =========================================================

class Tooltip:

    def __init__(
        self,
        widget,
        texto
    ):

        self.widget = widget
        self.texto = texto

        self.ventana_tooltip = None
        self.id_after = None


        self.widget.bind(
            "<Enter>",
            self.programar,
            add="+"
        )


        self.widget.bind(
            "<Leave>",
            self.ocultar,
            add="+"
        )


        self.widget.bind(
            "<ButtonPress>",
            self.ocultar,
            add="+"
        )


    # -----------------------------------------------------
    # PROGRAMAR
    # -----------------------------------------------------

    def programar(
        self,
        event=None
    ):

        if not mostrar_tooltips:

            return


        self.cancelar_programacion()


        self.id_after = self.widget.after(
            500,
            self.mostrar
        )


    # -----------------------------------------------------
    # CANCELAR PROGRAMACIÓN
    # -----------------------------------------------------

    def cancelar_programacion(
        self
    ):

        if self.id_after is not None:

            try:

                self.widget.after_cancel(
                    self.id_after
                )

            except Exception:

                pass


            self.id_after = None


    # -----------------------------------------------------
    # MOSTRAR
    # -----------------------------------------------------

    def mostrar(
        self
    ):

        self.id_after = None


        if not mostrar_tooltips:

            return


        if self.ventana_tooltip is not None:

            return


        try:

            x = (
                self.widget.winfo_rootx()
                + 10
            )


            y = (
                self.widget.winfo_rooty()
                + self.widget.winfo_height()
                + 8
            )


            self.ventana_tooltip = tk.Toplevel(
                self.widget
            )


            self.ventana_tooltip.wm_overrideredirect(
                True
            )


            self.ventana_tooltip.wm_attributes(
                "-topmost",
                True
            )


            self.ventana_tooltip.wm_geometry(
                f"+{x}+{y}"
            )


            etiqueta = tk.Label(
                self.ventana_tooltip,
                text=self.texto,
                bg=COLOR_PANEL_2,
                fg=COLOR_TEXTO,
                font=(
                    "Segoe UI",
                    8
                ),
                padx=8,
                pady=4,
                relief="solid",
                bd=1
            )


            etiqueta.pack()


        except Exception:

            self.ventana_tooltip = None


    # -----------------------------------------------------
    # OCULTAR
    # -----------------------------------------------------

    def ocultar(
        self,
        event=None
    ):

        self.cancelar_programacion()


        if self.ventana_tooltip is not None:

            try:

                self.ventana_tooltip.destroy()

            except Exception:

                pass


            self.ventana_tooltip = None


# =========================================================
# CREAR TOOLTIPS
# =========================================================

tooltips_activos = []


def agregar_tooltip(
    nombre_widget,
    texto
):

    widget = globals().get(
        nombre_widget
    )


    if widget is None:

        return


    try:

        tooltip = Tooltip(
            widget,
            texto
        )


        tooltips_activos.append(
            tooltip
        )

    except Exception:

        pass


# ---------------------------------------------------------
# REPRODUCTOR
# ---------------------------------------------------------

agregar_tooltip(
    "boton_shuffle",
    "Reproducción aleatoria"
)

agregar_tooltip(
    "boton_anterior",
    "Canción anterior"
)

agregar_tooltip(
    "boton_atras_10",
    "Retroceder"
)

agregar_tooltip(
    "boton_play_pausa",
    "Reproducir / Pausar"
)

agregar_tooltip(
    "boton_adelante_10",
    "Adelantar"
)

agregar_tooltip(
    "boton_siguiente",
    "Siguiente canción"
)

agregar_tooltip(
    "boton_repeat",
    "Repetir canción"
)

agregar_tooltip(
    "boton_mute",
    "Silenciar / Activar sonido"
)


# ---------------------------------------------------------
# OTROS BOTONES
# ---------------------------------------------------------

agregar_tooltip(
    "boton_abrir",
    "Abrir carpeta de música"
)

agregar_tooltip(
    "boton_mini",
    "Abrir modo mini"
)

agregar_tooltip(
    "boton_ajustes",
    "Abrir ajustes"
)


# =========================================================
# HOTKEYS
# =========================================================

def hotkey_play_pausa():

    ventana.after(
        0,
        play_pausa
    )


def hotkey_siguiente():

    ventana.after(
        0,
        siguiente_cancion
    )


def hotkey_anterior():

    ventana.after(
        0,
        anterior_cancion
    )


def hotkey_retroceder_10():

    ventana.after(
        0,
        retroceder_10
    )


def hotkey_adelantar_10():

    ventana.after(
        0,
        adelantar_10
    )


def hotkey_volumen_menos():

    ventana.after(
        0,
        bajar_volumen
    )


def hotkey_volumen_mas():

    ventana.after(
        0,
        subir_volumen
    )


hotkey_manager.configurar_funciones(
    play_pausa=hotkey_play_pausa,
    siguiente=hotkey_siguiente,
    anterior=hotkey_anterior,
    retroceder_10=hotkey_retroceder_10,
    adelantar_10=hotkey_adelantar_10,
    volumen_menos=hotkey_volumen_menos,
    volumen_mas=hotkey_volumen_mas
)


hotkey_manager.establecer_hotkeys(
    hotkeys_actuales
)


hotkey_manager.establecer_nombres_visibles(
    hotkeys_nombres
)


hotkey_manager.establecer_solo_oculto(
    solo_hotkeys_oculto
)


hotkey_manager.registrar()


# =========================================================
# TRAY
# =========================================================

tray = TrayManager(
    ventana,
    nombre="litesydug",
    color_fondo=COLOR_FONDO,
    color_acento=COLOR_ACENTO
)


def al_ocultar():

    global ventana_oculta


    ventana_oculta = True


    hotkey_manager.establecer_ventana_oculta(
        True
    )


def al_mostrar():

    global ventana_oculta


    ventana_oculta = False


    hotkey_manager.establecer_ventana_oculta(
        False
    )


def salir_programa():

    config.establecer(
    "volumen",
    int(
        control_volumen.get()
    )
)


    config.guardar()


    hotkey_manager.cerrar()

    player.cerrar()

    tray.cerrar()

    ventana.destroy()


tray.configurar_funciones(
    play_pausa=play_pausa,
    siguiente=siguiente_cancion,
    salir=salir_programa
)


tray.configurar_eventos(
    al_ocultar=al_ocultar,
    al_mostrar=al_mostrar
)


tray.iniciar()


# =========================================================
# EVENTOS
# =========================================================

boton_abrir.config(
    command=abrir_carpeta
)


boton_ajustes.config(
    command=abrir_ajustes
)


boton_mini.config(
    command=abrir_mini
)


selector_orden.bind(
    "<<ComboboxSelected>>",
    ordenar_canciones
)


# ---------------------------------------------------------
# BUSCADOR
# ---------------------------------------------------------

texto_busqueda.trace_add(
    "write",
    actualizar_busqueda
)


entrada_busqueda.bind(
    "<FocusIn>",
    entrar_buscador
)


entrada_busqueda.bind(
    "<FocusOut>",
    salir_buscador
)


entrada_busqueda.bind(
    "<Return>",
    reproducir_primer_resultado
)


# ---------------------------------------------------------
# LISTA DE CANCIONES
# ---------------------------------------------------------

lista_canciones.bind(
    "<<ListboxSelect>>",
    seleccionar_cancion
)


lista_canciones.bind(
    "<Double-Button-1>",
    reproducir_cancion
)


lista_canciones.bind(
    "<Return>",
    reproducir_cancion
)


def mover_lista_mouse(
    event
):

    lista_canciones.yview_scroll(
        int(
            -1 * (
                event.delta / 120
            )
        ),
        "units"
    )


lista_canciones.bind(
    "<MouseWheel>",
    mover_lista_mouse
)


barra_tiempo.bind(
    "<ButtonPress-1>",
    empezar_arrastre
)


barra_tiempo.bind(
    "<ButtonRelease-1>",
    terminar_arrastre
)


# =========================================================
# ATAJOS INTERNOS
# =========================================================

ventana.bind(
    "<space>",
    play_pausa
)


ventana.bind(
    "<Left>",
    retroceder_10
)


ventana.bind(
    "<Right>",
    adelantar_10
)


ventana.bind(
    "<Control-Left>",
    anterior_cancion
)


ventana.bind(
    "<Control-Right>",
    siguiente_cancion
)


# =========================================================
# CERRAR VENTANA PRINCIPAL
# =========================================================

def guardar_posicion_actual():

    if not recordar_posicion_ventana:

        return


    try:

        posicion = ventana.geometry()


        config.establecer(
            "posicion_ventana",
            posicion
        )


        config.guardar()


    except Exception:

        pass


def accion_cerrar_ventana():

    guardar_posicion_actual()


    if cerrar_a_bandeja:

        tray.ocultar()

    else:

        salir_programa()


ventana.protocol(
    "WM_DELETE_WINDOW",
    accion_cerrar_ventana
)

# =========================================================
# INICIAR BUSCADOR
# =========================================================

texto_busqueda.set(
    PLACEHOLDER_BUSQUEDA
)


entrada_busqueda.config(
    fg=COLOR_TEXTO_SECUNDARIO
)
# =========================================================
# ÚLTIMA CARPETA
# =========================================================

if recordar_ultima_carpeta and ultima_carpeta:

    rutas = library.cargar_carpeta(
        ultima_carpeta
    )

    if rutas:

        ordenar_canciones()


# =========================================================
# INICIAR
# =========================================================
# =========================================================
# INICIO SEGÚN CONFIGURACIÓN
# =========================================================

actualizar_tiempo()
vigilar_fin_cancion()

if iniciar_mini:

    ventana.after(
        150,
        abrir_mini
    )

elif iniciar_minimizado:

    ventana.after(
        150,
        tray.ocultar
    )


ventana.mainloop()
