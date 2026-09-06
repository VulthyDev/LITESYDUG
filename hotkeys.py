import keyboard


class HotkeyManager:

    def __init__(self):

        self.ids_hotkeys = []

        self.hotkeys = {
            "play_pausa": None,
            "siguiente": None,
            "anterior": None,
            "retroceder_10": None,
            "adelantar_10": None,
            "volumen_menos": None,
            "volumen_mas": None
        }

        self.nombres_visibles = {}

        self.solo_cuando_oculto = True
        self.ventana_oculta = False

        self.funciones = {}

        self.capturando = False


    def configurar_funciones(
        self,
        play_pausa=None,
        siguiente=None,
        anterior=None,
        retroceder_10=None,
        adelantar_10=None,
        volumen_menos=None,
        volumen_mas=None
    ):

        self.funciones = {
            "play_pausa": play_pausa,
            "siguiente": siguiente,
            "anterior": anterior,
            "retroceder_10": retroceder_10,
            "adelantar_10": adelantar_10,
            "volumen_menos": volumen_menos,
            "volumen_mas": volumen_mas
        }


    def establecer_hotkeys(
        self,
        nuevas_hotkeys
    ):

        self.hotkeys = nuevas_hotkeys.copy()


    def obtener_hotkeys(self):

        return self.hotkeys.copy()


    def establecer_nombres_visibles(
        self,
        nombres
    ):

        self.nombres_visibles = nombres.copy()


    def obtener_nombres_visibles(self):

        return self.nombres_visibles.copy()


    def establecer_solo_oculto(
        self,
        valor
    ):

        self.solo_cuando_oculto = bool(
            valor
        )


    def establecer_ventana_oculta(
        self,
        valor
    ):

        self.ventana_oculta = bool(
            valor
        )


    def ejecutar(
        self,
        accion
    ):

        if self.capturando:
            return

        if (
            self.solo_cuando_oculto
            and not self.ventana_oculta
        ):
            return

        funcion = self.funciones.get(
            accion
        )

        if funcion is not None:
            funcion()


    def limpiar(self):

        for identificador in self.ids_hotkeys:

            try:
                keyboard.remove_hotkey(
                    identificador
                )

            except Exception:

                try:
                    keyboard.unhook(
                        identificador
                    )

                except Exception:
                    pass

        self.ids_hotkeys.clear()


    def registrar_una(
        self,
        tecla,
        accion
    ):

        if tecla is None:
            return None


        if isinstance(tecla, int):

            def callback(event):

                if (
                    event.event_type == "down"
                    and event.scan_code == tecla
                ):

                    self.ejecutar(
                        accion
                    )

            return keyboard.hook(
                callback
            )


        return keyboard.add_hotkey(
            tecla,
            lambda:
            self.ejecutar(
                accion
            )
        )


    def registrar(self):

        self.limpiar()

        try:

            for accion, tecla in self.hotkeys.items():

                identificador = self.registrar_una(
                    tecla,
                    accion
                )

                if identificador is not None:

                    self.ids_hotkeys.append(
                        identificador
                    )

            return True

        except Exception as error:

            print(
                "Error registrando hotkeys:",
                error
            )

            self.limpiar()

            return False


    def capturar_tecla(self):

        self.capturando = True

        self.limpiar()

        try:

            while True:

                evento = keyboard.read_event()

                if evento.event_type != "down":
                    continue


                nombre = evento.name
                scan_code = evento.scan_code


                if nombre in (
                    "shift",
                    "ctrl",
                    "alt",
                    "windows",
                    "left shift",
                    "right shift",
                    "left ctrl",
                    "right ctrl",
                    "left alt",
                    "right alt"
                ):
                    continue


                modificadores = []


                if keyboard.is_pressed("ctrl"):
                    modificadores.append("ctrl")

                if keyboard.is_pressed("shift"):
                    modificadores.append("shift")

                if keyboard.is_pressed("alt"):
                    modificadores.append("alt")


                if modificadores:

                    combinacion = "+".join(
                        modificadores + [nombre]
                    )

                    nombre_bonito = " + ".join(
                        [
                            palabra.upper()
                            if len(palabra) <= 4
                            else palabra.title()
                            for palabra in modificadores + [nombre]
                        ]
                    )

                    self.capturando = False

                    return (
                        combinacion,
                        nombre_bonito
                    )


                nombre_bonito = (
                    self.convertir_nombre_evento(
                        nombre,
                        scan_code
                    )
                )

                self.capturando = False

                return (
                    scan_code,
                    nombre_bonito
                )


        except Exception as error:

            print(
                "Error capturando tecla:",
                error
            )

            self.capturando = False

            return (
                None,
                "Sin asignar"
            )


    def convertir_nombre_evento(
        self,
        nombre,
        scan_code
    ):

        nombre_minuscula = str(
            nombre
        ).lower()


        equivalencias = {
            "multiply": "Numpad *",
            "*": "Numpad *",
            "divide": "Numpad /",
            "subtract": "Numpad -",
            "add": "Numpad +",
            "decimal": "Numpad .",
            "enter": "Enter",
            "space": "Espacio",
            "page up": "Page Up",
            "page down": "Page Down",
            "left": "←",
            "right": "→",
            "up": "↑",
            "down": "↓"
        }


        if nombre_minuscula in equivalencias:

            return equivalencias[
                nombre_minuscula
            ]


        if (
            nombre_minuscula.startswith("f")
            and nombre_minuscula[1:].isdigit()
        ):

            return nombre_minuscula.upper()


        if len(nombre_minuscula) == 1:

            return nombre_minuscula.upper()


        if nombre:

            return str(
                nombre
            ).title()


        return f"Tecla {scan_code}"


    def nombre_visible(
        self,
        accion,
        tecla
    ):

        nombre_guardado = (
            self.nombres_visibles.get(
                accion
            )
        )

        if nombre_guardado:

            return nombre_guardado


        if tecla is None:
            return "Sin asignar"


        if isinstance(tecla, str):

            return tecla.replace(
                "+",
                " + "
            ).upper()


        return f"Tecla {tecla}"


    def hay_repetidas(
        self,
        hotkeys
    ):

        valores = [
            valor
            for valor in hotkeys.values()
            if valor is not None
        ]

        return (
            len(valores)
            != len(set(valores))
        )


    def es_peligrosa(
        self,
        tecla
    ):

        if not isinstance(tecla, str):
            return False


        normalizada = tecla.lower().replace(
            " ",
            ""
        )


        bloqueadas = {
            "alt+f4",
            "ctrl+alt+delete",
            "ctrl+alt+del",
            "windows+l",
            "win+l"
        }


        return normalizada in bloqueadas


    def predeterminados(self):

        return {
            "play_pausa": None,
            "siguiente": None,
            "anterior": None,
            "retroceder_10": None,
            "adelantar_10": None,
            "volumen_menos": None,
            "volumen_mas": None
        }


    def cerrar(self):

        self.limpiar()
        