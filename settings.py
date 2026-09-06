# =========================================================
# SETTINGS - LITESYDUG
# =========================================================

import json
import os


class Settings:

    def __init__(
        self,
        archivo="settings.json"
    ):

        # =====================================================
        # CARPETA DE CONFIGURACIÓN
        # =====================================================

        carpeta_local = os.environ.get(
            "LOCALAPPDATA"
        )


        if not carpeta_local:

            carpeta_local = os.path.join(
                os.path.expanduser("~"),
                "AppData",
                "Local"
            )


        carpeta_config = os.path.join(
            carpeta_local,
            "LITESYDUG"
        )


        # Crear la carpeta si todavía no existe
        try:

            os.makedirs(
                carpeta_config,
                exist_ok=True
            )

        except Exception:

            pass


        self.ruta_archivo = os.path.join(
            carpeta_config,
            archivo
        )


        # =====================================================
        # VALORES POR DEFECTO
        # =====================================================

        self.defaults = {

            # -------------------------------------------------
            # GENERAL
            # -------------------------------------------------

            "volumen": 70,

            "ultima_carpeta": "",

            "recordar_ultima_carpeta": True,

            "iniciar_minimizado": False,

            "iniciar_mini": False,

            "cerrar_a_bandeja": True,

            "salto_segundos": 10,


            # -------------------------------------------------
            # RENDIMIENTO
            # -------------------------------------------------

            "modo_rendimiento": "Normal",


            # -------------------------------------------------
            # INTERFAZ
            # -------------------------------------------------

            "mostrar_tooltips": True,

            "mini_siempre_encima": True,

            "recordar_posicion_ventana": False,

            "posicion_ventana": "",


            # -------------------------------------------------
            # HOTKEYS
            # -------------------------------------------------

            "hotkeys": {

                "play_pausa": None,

                "siguiente": None,

                "anterior": None,

                "retroceder_10": None,

                "adelantar_10": None,

                "volumen_menos": None,

                "volumen_mas": None
            },


            "hotkeys_nombres": {

                "play_pausa": "Sin asignar",

                "siguiente": "Sin asignar",

                "anterior": "Sin asignar",

                "retroceder_10": "Sin asignar",

                "adelantar_10": "Sin asignar",

                "volumen_menos": "Sin asignar",

                "volumen_mas": "Sin asignar"
            },


            "solo_hotkeys_oculto": True,

            "paso_volumen": 5
        }


        # =====================================================
        # DATOS ACTUALES
        # =====================================================

        self.datos = self.defaults.copy()


        self.datos[
            "hotkeys"
        ] = self.defaults[
            "hotkeys"
        ].copy()


        self.datos[
            "hotkeys_nombres"
        ] = self.defaults[
            "hotkeys_nombres"
        ].copy()


        self.cargar()


    # =====================================================
    # CARGAR
    # =====================================================

    def cargar(self):

        # -------------------------------------------------
        # EMPEZAR DESDE DEFAULTS
        # -------------------------------------------------

        datos_nuevos = self.defaults.copy()


        datos_nuevos[
            "hotkeys"
        ] = self.defaults[
            "hotkeys"
        ].copy()


        datos_nuevos[
            "hotkeys_nombres"
        ] = self.defaults[
            "hotkeys_nombres"
        ].copy()


        # -------------------------------------------------
        # LEER JSON
        # -------------------------------------------------

        if os.path.exists(
            self.ruta_archivo
        ):

            try:

                with open(
                    self.ruta_archivo,
                    "r",
                    encoding="utf-8"
                ) as archivo:

                    datos_guardados = json.load(
                        archivo
                    )


                if isinstance(
                    datos_guardados,
                    dict
                ):

                    # -------------------------------------
                    # DATOS GENERALES
                    # -------------------------------------

                    for clave, valor in (
                        datos_guardados.items()
                    ):

                        if clave not in (
                            "hotkeys",
                            "hotkeys_nombres"
                        ):

                            datos_nuevos[
                                clave
                            ] = valor


                    # -------------------------------------
                    # HOTKEYS
                    # -------------------------------------

                    hotkeys_guardadas = (
                        datos_guardados.get(
                            "hotkeys",
                            {}
                        )
                    )


                    if isinstance(
                        hotkeys_guardadas,
                        dict
                    ):

                        datos_nuevos[
                            "hotkeys"
                        ].update(
                            hotkeys_guardadas
                        )


                    # -------------------------------------
                    # NOMBRES DE HOTKEYS
                    # -------------------------------------

                    nombres_guardados = (
                        datos_guardados.get(
                            "hotkeys_nombres",
                            {}
                        )
                    )


                    if isinstance(
                        nombres_guardados,
                        dict
                    ):

                        datos_nuevos[
                            "hotkeys_nombres"
                        ].update(
                            nombres_guardados
                        )


            except Exception:

                pass


        self.datos = datos_nuevos


        return self.datos


    # =====================================================
    # GUARDAR
    # =====================================================

    def guardar(self):

        try:

            carpeta = os.path.dirname(
                self.ruta_archivo
            )


            os.makedirs(
                carpeta,
                exist_ok=True
            )


            with open(
                self.ruta_archivo,
                "w",
                encoding="utf-8"
            ) as archivo:

                json.dump(
                    self.datos,
                    archivo,
                    indent=4,
                    ensure_ascii=False
                )


            return True


        except Exception:

            return False


    # =====================================================
    # OBTENER
    # =====================================================

    def obtener(
        self,
        clave,
        valor_default=None
    ):

        return self.datos.get(
            clave,
            valor_default
        )


    # =====================================================
    # ESTABLECER
    # =====================================================

    def establecer(
        self,
        clave,
        valor
    ):

        self.datos[
            clave
        ] = valor


    # =====================================================
    # OBTENER HOTKEYS
    # =====================================================

    def obtener_hotkeys(self):

        return self.datos.get(
            "hotkeys",
            {}
        ).copy()


    # =====================================================
    # ESTABLECER HOTKEYS
    # =====================================================

    def establecer_hotkeys(
        self,
        hotkeys
    ):

        if not isinstance(
            hotkeys,
            dict
        ):

            return


        self.datos[
            "hotkeys"
        ] = hotkeys.copy()


    # =====================================================
    # OBTENER NOMBRES HOTKEYS
    # =====================================================

    def obtener_nombres_hotkeys(self):

        return self.datos.get(
            "hotkeys_nombres",
            {}
        ).copy()


    # =====================================================
    # ESTABLECER NOMBRES HOTKEYS
    # =====================================================

    def establecer_nombres_hotkeys(
        self,
        nombres
    ):

        if not isinstance(
            nombres,
            dict
        ):

            return


        self.datos[
            "hotkeys_nombres"
        ] = nombres.copy()


    # =====================================================
    # RESTABLECER
    # =====================================================

    def restablecer(self):

        self.datos = self.defaults.copy()


        self.datos[
            "hotkeys"
        ] = self.defaults[
            "hotkeys"
        ].copy()


        self.datos[
            "hotkeys_nombres"
        ] = self.defaults[
            "hotkeys_nombres"
        ].copy()


        self.guardar()


        return self.datos