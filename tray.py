import os
import threading

import pystray

from PIL import Image, ImageDraw


class TrayManager:

    def __init__(
        self,
        ventana,
        nombre="litesydug",
        color_fondo="#090d16",
        color_acento="#7c5cff"
    ):

        self.ventana = ventana

        self.nombre = nombre

        self.color_fondo = color_fondo
        self.color_acento = color_acento

        self.icono = None

        self.funcion_play_pausa = None
        self.funcion_siguiente = None
        self.funcion_salir = None

        self.funcion_al_ocultar = None
        self.funcion_al_mostrar = None


        self.carpeta_proyecto = os.path.dirname(
            os.path.abspath(__file__)
        )


        self.ruta_logo = os.path.join(
            self.carpeta_proyecto,
            "assets",
            "logo.png"
        )


    # =====================================================
    # FUNCIONES
    # =====================================================

    def configurar_funciones(
        self,
        play_pausa=None,
        siguiente=None,
        salir=None
    ):

        self.funcion_play_pausa = play_pausa
        self.funcion_siguiente = siguiente
        self.funcion_salir = salir


    # =====================================================
    # EVENTOS
    # =====================================================

    def configurar_eventos(
        self,
        al_ocultar=None,
        al_mostrar=None
    ):

        self.funcion_al_ocultar = al_ocultar
        self.funcion_al_mostrar = al_mostrar


    # =====================================================
    # CREAR ICONO
    # =====================================================

    def crear_icono(self):

        if os.path.exists(
            self.ruta_logo
        ):

            try:

                imagen = Image.open(
                    self.ruta_logo
                ).convert(
                    "RGBA"
                )


                imagen = imagen.resize(
                    (64, 64),
                    Image.Resampling.LANCZOS
                )


                return imagen


            except Exception as error:

                print(
                    "Error cargando logo del tray:",
                    error
                )


        # Fallback
        imagen = Image.new(
            "RGB",
            (64, 64),
            self.color_fondo
        )


        dibujo = ImageDraw.Draw(
            imagen
        )


        dibujo.ellipse(
            (8, 8, 56, 56),
            fill=self.color_acento
        )


        dibujo.text(
            (25, 19),
            "L",
            fill="white"
        )


        return imagen


    # =====================================================
    # MOSTRAR
    # =====================================================

    def mostrar(
        self,
        icon=None,
        item=None
    ):

        def accion():

            self.ventana.deiconify()

            self.ventana.lift()

            self.ventana.focus_force()


            if self.funcion_al_mostrar is not None:

                self.funcion_al_mostrar()


        self.ventana.after(
            0,
            accion
        )


    # =====================================================
    # OCULTAR
    # =====================================================

    def ocultar(self):

        if self.funcion_al_ocultar is not None:

            self.funcion_al_ocultar()


        self.ventana.withdraw()


    # =====================================================
    # PLAY / PAUSA
    # =====================================================

    def play_pausa(
        self,
        icon=None,
        item=None
    ):

        if self.funcion_play_pausa is not None:

            self.ventana.after(
                0,
                self.funcion_play_pausa
            )


    # =====================================================
    # SIGUIENTE
    # =====================================================

    def siguiente(
        self,
        icon=None,
        item=None
    ):

        if self.funcion_siguiente is not None:

            self.ventana.after(
                0,
                self.funcion_siguiente
            )


    # =====================================================
    # SALIR
    # =====================================================

    def salir(
        self,
        icon=None,
        item=None
    ):

        if self.funcion_salir is not None:

            self.ventana.after(
                0,
                self.funcion_salir
            )


    # =====================================================
    # EJECUTAR
    # =====================================================

    def ejecutar(self):

        imagen = self.crear_icono()


        menu = pystray.Menu(

            pystray.MenuItem(
                "Abrir litesydug",
                self.mostrar,
                default=True
            ),

            pystray.MenuItem(
                "Play / Pausa",
                self.play_pausa
            ),

            pystray.MenuItem(
                "Siguiente",
                self.siguiente
            ),

            pystray.Menu.SEPARATOR,

            pystray.MenuItem(
                "Salir",
                self.salir
            )
        )


        self.icono = pystray.Icon(
            self.nombre,
            imagen,
            self.nombre,
            menu
        )


        self.icono.run()


    # =====================================================
    # INICIAR
    # =====================================================

    def iniciar(self):

        hilo = threading.Thread(
            target=self.ejecutar,
            daemon=True
        )

        hilo.start()


    # =====================================================
    # CERRAR
    # =====================================================

    def cerrar(self):

        try:

            if self.icono is not None:

                self.icono.stop()

        except Exception:

            pass
        