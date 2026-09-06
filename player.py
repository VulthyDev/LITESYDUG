# =========================================================
# PLAYER - LITESYDUG
# =========================================================

import os
import pygame


class Player:

    def __init__(self):

        # -------------------------------------------------
        # INICIAR AUDIO
        # -------------------------------------------------

        try:

            if not pygame.mixer.get_init():

                pygame.mixer.init()

        except Exception:

            pass


        # -------------------------------------------------
        # ESTADO
        # -------------------------------------------------

        self.rutas_canciones = []

        self.indice_actual = -1

        self.esta_pausado = False

        self.hay_cancion_cargada = False


        # -------------------------------------------------
        # TIEMPO
        # -------------------------------------------------

        self.inicio_segundos = 0

        self.duracion_actual = 0


        # -------------------------------------------------
        # VOLUMEN
        # -------------------------------------------------

        self.volumen = 0.7


        try:

            pygame.mixer.music.set_volume(
                self.volumen
            )

        except Exception:

            pass


        # -------------------------------------------------
        # ERROR
        # -------------------------------------------------

        self.ultimo_error = ""


    # =====================================================
    # ESTABLECER CANCIONES
    # =====================================================

    def establecer_canciones(
        self,
        rutas
    ):

        if rutas is None:

            self.rutas_canciones = []

        else:

            self.rutas_canciones = list(
                rutas
            )


        # Si el índice actual ya no existe,
        # lo reiniciamos.

        if not (
            0 <= self.indice_actual
            < len(self.rutas_canciones)
        ):

            self.indice_actual = -1


    # =====================================================
    # REPRODUCIR
    # =====================================================

    def reproducir(
        self,
        indice,
        duracion=0
    ):

        self.ultimo_error = ""


        # -------------------------------------------------
        # VALIDAR ÍNDICE
        # -------------------------------------------------

        if not (
            0 <= indice
            < len(self.rutas_canciones)
        ):

            self.ultimo_error = (
                "Índice de canción inválido."
            )

            return False


        ruta = self.rutas_canciones[
            indice
        ]


        # -------------------------------------------------
        # COMPROBAR QUE EL ARCHIVO TODAVÍA EXISTE
        # -------------------------------------------------

        if not os.path.isfile(
            ruta
        ):

            self.ultimo_error = (
                "El archivo ya no existe "
                "o fue movido."
            )

            self.hay_cancion_cargada = False

            self.esta_pausado = False

            self.inicio_segundos = 0

            self.duracion_actual = 0

            return False


        # -------------------------------------------------
        # INTENTAR CARGAR
        # -------------------------------------------------

        try:

            pygame.mixer.music.stop()


            pygame.mixer.music.load(
                ruta
            )


            pygame.mixer.music.set_volume(
                self.volumen
            )


            pygame.mixer.music.play()


        except Exception as error:

            self.hay_cancion_cargada = False

            self.esta_pausado = False

            self.inicio_segundos = 0

            self.duracion_actual = 0


            self.ultimo_error = str(
                error
            )


            return False


        # -------------------------------------------------
        # ACTUALIZAR ESTADO
        # -------------------------------------------------

        self.indice_actual = indice

        self.esta_pausado = False

        self.hay_cancion_cargada = True

        self.inicio_segundos = 0


        try:

            self.duracion_actual = float(
                duracion
            )

        except Exception:

            self.duracion_actual = 0


        return True


    # =====================================================
    # PLAY / PAUSA
    # =====================================================

    def play_pausa(self):

        if not self.hay_cancion_cargada:

            return "sin_cancion"


        # -------------------------------------------------
        # REANUDAR
        # -------------------------------------------------

        if self.esta_pausado:

            try:

                pygame.mixer.music.unpause()

                self.esta_pausado = False

                return "reproduciendo"


            except Exception as error:

                self.ultimo_error = str(
                    error
                )

                return "sin_cancion"


        # -------------------------------------------------
        # PAUSAR
        # -------------------------------------------------

        try:

            pygame.mixer.music.pause()

            self.esta_pausado = True

            return "pausado"


        except Exception as error:

            self.ultimo_error = str(
                error
            )

            return "sin_cancion"


    # =====================================================
    # SIGUIENTE ÍNDICE
    # =====================================================

    def siguiente_indice(self):

        if not self.rutas_canciones:

            return None


        if self.indice_actual < 0:

            return 0


        return (
            self.indice_actual + 1
        ) % len(
            self.rutas_canciones
        )


    # =====================================================
    # ANTERIOR ÍNDICE
    # =====================================================

    def anterior_indice(self):

        if not self.rutas_canciones:

            return None


        if self.indice_actual < 0:

            return 0


        return (
            self.indice_actual - 1
        ) % len(
            self.rutas_canciones
        )


    # =====================================================
    # POSICIÓN ACTUAL
    # =====================================================

    def obtener_posicion_actual(self):

        if not self.hay_cancion_cargada:

            return 0


        try:

            milisegundos = (
                pygame.mixer.music.get_pos()
            )


            if milisegundos < 0:

                return self.inicio_segundos


            posicion = (
                self.inicio_segundos
                + milisegundos / 1000
            )


            if self.duracion_actual > 0:

                posicion = min(
                    posicion,
                    self.duracion_actual
                )


            return max(
                posicion,
                0
            )


        except Exception:

            return self.inicio_segundos


    # =====================================================
    # IR A POSICIÓN
    # =====================================================

    def ir_a_posicion(
        self,
        segundos
    ):

        if not self.hay_cancion_cargada:

            return False


        try:

            segundos = float(
                segundos
            )

        except Exception:

            return False


        segundos = max(
            segundos,
            0
        )


        if self.duracion_actual > 0:

            segundos = min(
                segundos,
                self.duracion_actual
            )


        estaba_pausado = self.esta_pausado


        try:

            # Reproducimos desde la nueva posición.

            pygame.mixer.music.play(
                start=segundos
            )


            pygame.mixer.music.set_volume(
                self.volumen
            )


            self.inicio_segundos = segundos


            if estaba_pausado:

                pygame.mixer.music.pause()

                self.esta_pausado = True

            else:

                self.esta_pausado = False


            return True


        except Exception as error:

            self.ultimo_error = str(
                error
            )

            return False


    # =====================================================
    # ADELANTAR 10
    # =====================================================

    def adelantar_10(self):

        posicion = (
            self.obtener_posicion_actual()
            + 10
        )


        return self.ir_a_posicion(
            posicion
        )


    # =====================================================
    # RETROCEDER 10
    # =====================================================

    def retroceder_10(self):

        posicion = (
            self.obtener_posicion_actual()
            - 10
        )


        return self.ir_a_posicion(
            posicion
        )


    # =====================================================
    # ESTABLECER VOLUMEN
    # =====================================================

    def establecer_volumen(
        self,
        volumen
    ):

        try:

            volumen = float(
                volumen
            )

        except Exception:

            return


        volumen = max(
            0.0,
            min(
                volumen,
                1.0
            )
        )


        self.volumen = volumen


        try:

            pygame.mixer.music.set_volume(
                self.volumen
            )

        except Exception:

            pass


    # =====================================================
    # OBTENER VOLUMEN
    # =====================================================

    def obtener_volumen(self):

        return self.volumen


    # =====================================================
    # ESTÁ REPRODUCIENDO
    # =====================================================

    def esta_reproduciendo(self):

        if not self.hay_cancion_cargada:

            return False


        if self.esta_pausado:

            return False


        try:

            return bool(
                pygame.mixer.music.get_busy()
            )

        except Exception:

            return False


    # =====================================================
    # DETENER
    # =====================================================

    def detener(self):

        try:

            pygame.mixer.music.stop()

        except Exception:

            pass


        self.esta_pausado = False

        self.hay_cancion_cargada = False

        self.inicio_segundos = 0

        self.duracion_actual = 0


    # =====================================================
    # OBTENER ÚLTIMO ERROR
    # =====================================================

    def obtener_ultimo_error(self):

        return self.ultimo_error


    # =====================================================
    # CERRAR
    # =====================================================

    def cerrar(self):

        try:

            pygame.mixer.music.stop()

        except Exception:

            pass


        try:

            pygame.mixer.quit()

        except Exception:

            pass


        self.hay_cancion_cargada = False

        self.esta_pausado = False
        