# =========================================================
# LIBRARY - LITESYDUG
# =========================================================

import os
import io

from collections import OrderedDict

from mutagen import File

from PIL import (
    Image,
    ImageTk,
    ImageOps
)


class Library:

    def __init__(self):

        # -------------------------------------------------
        # CANCIONES
        # -------------------------------------------------

        self.rutas = []


        # -------------------------------------------------
        # FORMATOS
        # -------------------------------------------------

        self.extensiones_validas = (
            ".mp3",
            ".wav",
            ".ogg",
            ".flac"
        )


        # -------------------------------------------------
        # RUTAS DEL PROYECTO
        # -------------------------------------------------

        self.carpeta_proyecto = os.path.dirname(
            os.path.abspath(__file__)
        )


        self.ruta_cover_default = os.path.join(
            self.carpeta_proyecto,
            "assets",
            "cover_default.png"
        )


        # -------------------------------------------------
        # CACHÉ DE INFORMACIÓN
        # -------------------------------------------------

        # ruta -> (titulo, artista)
        self.cache_metadata = {}


        # ruta -> duración
        self.cache_duracion = {}


        # Rutas cuya metadata y duración
        # ya fueron leídas
        self.cache_info_leida = set()


        # -------------------------------------------------
        # CACHÉ DE PORTADAS
        # -------------------------------------------------

        # OrderedDict permite eliminar primero
        # las portadas menos usadas recientemente.
        #
        # clave:
        # (ruta, ancho, alto)
        #
        # valor:
        # PhotoImage

        self.cache_portadas = OrderedDict()


        # Máximo de portadas procesadas
        # guardadas simultáneamente en memoria.

        self.limite_cache_portadas = 80


        # Portada default por tamaño:
        # (ancho, alto) -> PhotoImage

        self.cache_cover_default = {}


    # =====================================================
    # LIMPIAR CACHÉ
    # =====================================================

    def limpiar_cache(self):

        self.cache_metadata.clear()

        self.cache_duracion.clear()

        self.cache_info_leida.clear()

        self.cache_portadas.clear()

        self.cache_cover_default.clear()


    # =====================================================
    # CARGAR CARPETA
    # =====================================================

    def cargar_carpeta(
        self,
        carpeta
    ):

        self.rutas = []


        if not carpeta:

            return self.rutas


        if not os.path.isdir(
            carpeta
        ):

            return self.rutas


        # Cambió la biblioteca:
        # limpiamos datos de la anterior.

        self.limpiar_cache()


        try:

            for archivo in os.listdir(
                carpeta
            ):

                ruta = os.path.join(
                    carpeta,
                    archivo
                )


                if not os.path.isfile(
                    ruta
                ):

                    continue


                extension = os.path.splitext(
                    archivo
                )[1].lower()


                if extension in self.extensiones_validas:

                    self.rutas.append(
                        ruta
                    )


        except Exception:

            return self.rutas


        return self.rutas


    # =====================================================
    # OBTENER RUTAS
    # =====================================================

    def obtener_rutas(self):

        return self.rutas


    # =====================================================
    # OBTENER RUTA
    # =====================================================

    def obtener_ruta(
        self,
        indice
    ):

        if indice is None:

            return None


        if not (
            0 <= indice < len(
                self.rutas
            )
        ):

            return None


        return self.rutas[
            indice
        ]


    # =====================================================
    # CANTIDAD
    # =====================================================

    def cantidad(self):

        return len(
            self.rutas
        )


    # =====================================================
    # NOMBRE SIN EXTENSIÓN
    # =====================================================

    def nombre_sin_extension(
        self,
        ruta
    ):

        nombre = os.path.basename(
            ruta
        )


        nombre = os.path.splitext(
            nombre
        )[0]


        return nombre


    # =====================================================
    # LEER INFORMACIÓN BÁSICA DEL AUDIO
    # =====================================================

    def leer_info_audio(
        self,
        ruta
    ):

        # Si ya fue leído una vez,
        # no volvemos a abrir el archivo.

        if ruta in self.cache_info_leida:

            return


        titulo = self.nombre_sin_extension(
            ruta
        )

        artista = "Artista desconocido"

        duracion = 0


        try:

            # Abrimos el archivo UNA sola vez
            # para obtener:
            #
            # - título
            # - artista
            # - duración

            audio = File(
                ruta,
                easy=True
            )


            if audio is not None:

                # -----------------------------------------
                # METADATA
                # -----------------------------------------

                if audio.tags:

                    titulos = audio.tags.get(
                        "title"
                    )


                    artistas = audio.tags.get(
                        "artist"
                    )


                    if titulos:

                        titulo = str(
                            titulos[0]
                        )


                    if artistas:

                        artista = str(
                            artistas[0]
                        )


                # -----------------------------------------
                # DURACIÓN
                # -----------------------------------------

                if (
                    hasattr(
                        audio,
                        "info"
                    )
                    and audio.info is not None
                    and hasattr(
                        audio.info,
                        "length"
                    )
                ):

                    duracion = float(
                        audio.info.length
                    )


        except Exception:

            pass


        # -------------------------------------------------
        # GUARDAR EN CACHÉ
        # -------------------------------------------------

        self.cache_metadata[
            ruta
        ] = (
            titulo,
            artista
        )


        self.cache_duracion[
            ruta
        ] = duracion


        self.cache_info_leida.add(
            ruta
        )


    # =====================================================
    # METADATA
    # =====================================================

    def obtener_metadata(
        self,
        ruta
    ):

        if ruta not in self.cache_info_leida:

            self.leer_info_audio(
                ruta
            )


        return self.cache_metadata.get(
            ruta,
            (
                self.nombre_sin_extension(
                    ruta
                ),
                "Artista desconocido"
            )
        )


    # =====================================================
    # DURACIÓN
    # =====================================================

    def obtener_duracion(
        self,
        ruta
    ):

        if ruta not in self.cache_info_leida:

            self.leer_info_audio(
                ruta
            )


        return self.cache_duracion.get(
            ruta,
            0
        )


    # =====================================================
    # CONVERTIR TIEMPO
    # =====================================================

    def convertir_tiempo(
        self,
        segundos
    ):

        try:

            segundos = int(
                segundos
            )

        except Exception:

            segundos = 0


        if segundos < 0:

            segundos = 0


        minutos = segundos // 60

        segundos_restantes = (
            segundos % 60
        )


        return (
            f"{minutos}:"
            f"{segundos_restantes:02d}"
        )


    # =====================================================
    # PROCESAR IMAGEN
    # =====================================================

    def procesar_imagen(
        self,
        imagen,
        tamano
    ):

        try:

            imagen = imagen.convert(
                "RGB"
            )


            imagen = ImageOps.fit(
                imagen,
                tamano,
                method=Image.Resampling.LANCZOS
            )


            return ImageTk.PhotoImage(
                imagen
            )


        except Exception:

            return None


    # =====================================================
    # COVER DEFAULT
    # =====================================================

    def cargar_cover_default(
        self,
        tamano
    ):

        clave = (
            tamano[0],
            tamano[1]
        )


        # -------------------------------------------------
        # DEVOLVER CACHÉ
        # -------------------------------------------------

        if clave in self.cache_cover_default:

            return self.cache_cover_default[
                clave
            ]


        if not os.path.exists(
            self.ruta_cover_default
        ):

            return None


        try:

            with Image.open(
                self.ruta_cover_default
            ) as imagen:

                portada = self.procesar_imagen(
                    imagen,
                    tamano
                )


            self.cache_cover_default[
                clave
            ] = portada


            return portada


        except Exception:

            return None


    # =====================================================
    # GUARDAR PORTADA EN CACHÉ
    # =====================================================

    def guardar_portada_cache(
        self,
        clave,
        portada
    ):

        if portada is None:

            return


        # Si ya existe, la marcamos
        # como utilizada recientemente.

        if clave in self.cache_portadas:

            self.cache_portadas.move_to_end(
                clave
            )


        self.cache_portadas[
            clave
        ] = portada


        # -------------------------------------------------
        # LIMITAR MEMORIA
        # -------------------------------------------------

        while (
            len(self.cache_portadas)
            > self.limite_cache_portadas
        ):

            # Borra la portada menos usada
            # recientemente.

            self.cache_portadas.popitem(
                last=False
            )


    # =====================================================
    # OBTENER PORTADA
    # =====================================================

    def obtener_portada(
        self,
        ruta,
        tamano=(180, 180)
    ):

        clave_cache = (
            ruta,
            tamano[0],
            tamano[1]
        )


        # -------------------------------------------------
        # DEVOLVER CACHÉ
        # -------------------------------------------------

        if clave_cache in self.cache_portadas:

            portada = self.cache_portadas[
                clave_cache
            ]


            # Marcamos esta portada como
            # usada recientemente.

            self.cache_portadas.move_to_end(
                clave_cache
            )


            return portada


        portada = None


        try:

            audio = File(
                ruta
            )


            if audio is not None:

                # =========================================
                # FLAC
                # =========================================

                if hasattr(
                    audio,
                    "pictures"
                ):

                    if audio.pictures:

                        datos_imagen = (
                            audio.pictures[0].data
                        )


                        with Image.open(
                            io.BytesIO(
                                datos_imagen
                            )
                        ) as imagen:

                            portada = (
                                self.procesar_imagen(
                                    imagen,
                                    tamano
                                )
                            )


                # =========================================
                # MP3 / ID3
                # =========================================

                if (
                    portada is None
                    and audio.tags
                ):

                    for etiqueta in audio.tags.values():

                        if not hasattr(
                            etiqueta,
                            "data"
                        ):

                            continue


                        nombre_clase = (
                            etiqueta.__class__.__name__
                        )


                        if nombre_clase != "APIC":

                            continue


                        try:

                            with Image.open(
                                io.BytesIO(
                                    etiqueta.data
                                )
                            ) as imagen:

                                portada = (
                                    self.procesar_imagen(
                                        imagen,
                                        tamano
                                    )
                                )


                            break


                        except Exception:

                            pass


        except Exception:

            portada = None


        # -------------------------------------------------
        # SIN PORTADA EMBEBIDA
        # -------------------------------------------------

        if portada is None:

            portada = self.cargar_cover_default(
                tamano
            )


        # -------------------------------------------------
        # GUARDAR PORTADA CON LÍMITE
        # -------------------------------------------------

        self.guardar_portada_cache(
            clave_cache,
            portada
        )


        return portada


    # =====================================================
    # ORDENAR
    # =====================================================

    def ordenar(
        self,
        opcion
    ):

        try:

            # ---------------------------------------------
            # NOMBRE A-Z
            # ---------------------------------------------

            if opcion == "Nombre A-Z":

                self.rutas.sort(
                    key=lambda ruta:
                    self.nombre_sin_extension(
                        ruta
                    ).lower()
                )


            # ---------------------------------------------
            # NOMBRE Z-A
            # ---------------------------------------------

            elif opcion == "Nombre Z-A":

                self.rutas.sort(
                    key=lambda ruta:
                    self.nombre_sin_extension(
                        ruta
                    ).lower(),
                    reverse=True
                )


            # ---------------------------------------------
            # MÁS RECIENTES
            # ---------------------------------------------

            elif opcion == "Más recientes":

                self.rutas.sort(
                    key=lambda ruta:
                    os.path.getmtime(
                        ruta
                    ),
                    reverse=True
                )


            # ---------------------------------------------
            # MÁS ANTIGUOS
            # ---------------------------------------------

            elif opcion == "Más antiguos":

                self.rutas.sort(
                    key=lambda ruta:
                    os.path.getmtime(
                        ruta
                    )
                )


            # ---------------------------------------------
            # MAYOR TAMAÑO
            # ---------------------------------------------

            elif opcion == "Mayor tamaño":

                self.rutas.sort(
                    key=lambda ruta:
                    os.path.getsize(
                        ruta
                    ),
                    reverse=True
                )


            # ---------------------------------------------
            # MENOR TAMAÑO
            # ---------------------------------------------

            elif opcion == "Menor tamaño":

                self.rutas.sort(
                    key=lambda ruta:
                    os.path.getsize(
                        ruta
                    )
                )


        except Exception:

            pass