import tkinter as tk
from tkinter import ttk, messagebox

import threading
import webbrowser


class SettingsWindow:

    def __init__(
        self,
        ventana_principal,
        config,
        hotkey_manager,
        colores,
        logo=None,
        version="v0.1.0",
        enlaces=None,
        al_guardar=None
    ):

        self.ventana_principal = ventana_principal

        self.config = config

        self.hotkey_manager = hotkey_manager

        self.colores = colores

        self.logo = logo

        self.version = version

        self.enlaces = enlaces or {}

        self.al_guardar = al_guardar

        self.ventana = None

        self.datos = self.config.cargar()

        self.hotkeys_temporales = {}

        self.nombres_temporales = {}

        self.etiquetas_hotkeys = {}


    # =====================================================
    # COLORES
    # =====================================================

    def color(
        self,
        nombre,
        defecto="#ffffff"
    ):

        return self.colores.get(
            nombre,
            defecto
        )


    # =====================================================
    # ABRIR
    # =====================================================

    def abrir(self):

        if self.ventana is not None:

            try:

                if self.ventana.winfo_exists():

                    self.ventana.lift()
                    self.ventana.focus_force()

                    return

            except Exception:
                pass


        self.datos = self.config.cargar()


        self.ventana = tk.Toplevel(
            self.ventana_principal
        )


        self.ventana.title(
            "Ajustes - LITESYDUG"
        )


        ancho = 720
        alto = 650

        ancho_pantalla = (
            self.ventana.winfo_screenwidth()
        )


        x = (
            ancho_pantalla - ancho
        ) // 2


        self.ventana.geometry(
            f"{ancho}x{alto}+{x}+20"
        )


        self.ventana.minsize(
            720,
            650
        )


        self.ventana.configure(
            bg=self.color(
                "fondo"
            )
        )


        if self.logo is not None:

            try:

                self.ventana.iconphoto(
                    True,
                    self.logo
                )

            except Exception:
                pass


        self.ventana.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar
        )


        self.crear_interfaz()


    # =====================================================
    # INTERFAZ GENERAL
    # =====================================================

    def crear_interfaz(self):

        fondo = self.color("fondo")
        panel = self.color("panel")
        panel_2 = self.color("panel_2")
        boton = self.color("boton")
        boton_hover = self.color("boton_hover")

        texto = self.color("texto")
        texto_sec = self.color("texto_secundario")

        acento = self.color("acento")
        acento_claro = self.color("acento_claro")

        cyan = self.color("cyan")


        # -------------------------------------------------
        # CABECERA
        # -------------------------------------------------

        cabecera = tk.Frame(
            self.ventana,
            bg=panel
        )

        cabecera.pack(
            fill="x"
        )


        tk.Label(
            cabecera,
            text="⚙  AJUSTES",
            bg=panel,
            fg=acento_claro,
            font=(
                "Segoe UI",
                15,
                "bold"
            )
        ).pack(
            side="left",
            padx=20,
            pady=15
        )


        tk.Label(
            cabecera,
            text=f"LITESYDUG {self.version}",
            bg=panel,
            fg=texto_sec,
            font=(
                "Segoe UI",
                8
            )
        ).pack(
            side="right",
            padx=20
        )


        # -------------------------------------------------
        # CONTENIDO
        # -------------------------------------------------

        cuerpo = tk.Frame(
            self.ventana,
            bg=fondo
        )

        cuerpo.pack(
            fill="both",
            expand=True
        )


        # -------------------------------------------------
        # MENÚ IZQUIERDO
        # -------------------------------------------------

        menu = tk.Frame(
            cuerpo,
            bg=panel,
            width=165
        )

        menu.pack(
            side="left",
            fill="y",
            padx=(12, 6),
            pady=12
        )

        menu.pack_propagate(
            False
        )


        # -------------------------------------------------
        # ÁREA DE PÁGINAS
        # -------------------------------------------------

        contenido = tk.Frame(
            cuerpo,
            bg=fondo
        )

        contenido.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(6, 12),
            pady=12
        )


        self.paginas = {}


        nombres_paginas = (
            "General",
            "Rendimiento",
            "Hotkeys",
            "Interfaz",
            "Ayuda",
            "Acerca de"
        )


        for nombre in nombres_paginas:

            pagina = tk.Frame(
                contenido,
                bg=panel_2
            )

            pagina.place(
                x=0,
                y=0,
                relwidth=1,
                relheight=1
            )

            self.paginas[
                nombre
            ] = pagina


        def mostrar_pagina(
            nombre
        ):

            self.paginas[
                nombre
            ].tkraise()


        botones_menu = (
            (
                "⚙  General",
                "General"
            ),
            (
                "⚡  Rendimiento",
                "Rendimiento"
            ),
            (
                "⌨  Hotkeys",
                "Hotkeys"
            ),
            (
                "◫  Interfaz",
                "Interfaz"
            ),
            (
                "?  Ayuda",
                "Ayuda"
            ),
            (
                "ⓘ  Acerca de",
                "Acerca de"
            )
        )


        for texto_boton, pagina in botones_menu:

            tk.Button(
                menu,
                text=texto_boton,
                command=lambda p=pagina:
                mostrar_pagina(p),
                bg=boton,
                fg=texto,
                activebackground=boton_hover,
                activeforeground="white",
                borderwidth=0,
                anchor="w",
                padx=12,
                font=(
                    "Segoe UI",
                    9,
                    "bold"
                ),
                cursor="hand2"
            ).pack(
                fill="x",
                padx=8,
                pady=5,
                ipady=7
            )


        self.crear_general()
        self.crear_rendimiento()
        self.crear_hotkeys()
        self.crear_interfaz_config()
        self.crear_ayuda()
        self.crear_acerca()


        mostrar_pagina(
            "General"
        )


        # -------------------------------------------------
        # GUARDAR
        # -------------------------------------------------

        pie = tk.Frame(
            self.ventana,
            bg=panel
        )

        pie.pack(
            fill="x"
        )


        tk.Button(
            pie,
            text="GUARDAR CAMBIOS",
            command=self.guardar,
            bg=acento,
            fg="white",
            activebackground=acento_claro,
            activeforeground="white",
            borderwidth=0,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            cursor="hand2"
        ).pack(
            side="right",
            padx=20,
            pady=12,
            ipadx=15,
            ipady=6
        )


        tk.Button(
            pie,
            text="CANCELAR",
            command=self.cerrar,
            bg=boton,
            fg=texto,
            activebackground=boton_hover,
            activeforeground="white",
            borderwidth=0,
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            cursor="hand2"
        ).pack(
            side="right",
            pady=12,
            ipadx=10,
            ipady=6
        )


    # =====================================================
    # TÍTULO PÁGINA
    # =====================================================

    def titulo_pagina(
        self,
        pagina,
        titulo,
        descripcion
    ):

        tk.Label(
            pagina,
            text=titulo,
            bg=self.color(
                "panel_2"
            ),
            fg=self.color(
                "acento_claro"
            ),
            font=(
                "Segoe UI",
                14,
                "bold"
            ),
            anchor="w"
        ).pack(
            fill="x",
            padx=22,
            pady=(20, 3)
        )


        tk.Label(
            pagina,
            text=descripcion,
            bg=self.color(
                "panel_2"
            ),
            fg=self.color(
                "texto_secundario"
            ),
            font=(
                "Segoe UI",
                8
            ),
            anchor="w",
            justify="left"
        ).pack(
            fill="x",
            padx=22,
            pady=(0, 16)
        )


    # =====================================================
    # GENERAL
    # =====================================================

    def crear_general(self):

        pagina = self.paginas[
            "General"
        ]


        self.titulo_pagina(
            pagina,
            "GENERAL",
            "Comportamiento general de LITESYDUG."
        )


        self.var_recordar_carpeta = tk.BooleanVar(
            value=self.datos.get(
                "recordar_ultima_carpeta",
                True
            )
        )


        self.var_iniciar_minimizado = tk.BooleanVar(
            value=self.datos.get(
                "iniciar_minimizado",
                False
            )
        )


        self.var_iniciar_mini = tk.BooleanVar(
            value=self.datos.get(
                "iniciar_mini",
                False
            )
        )


        self.var_cerrar_tray = tk.BooleanVar(
            value=self.datos.get(
                "cerrar_a_bandeja",
                True
            )
        )


        opciones = (
            (
                "Recordar última carpeta de música",
                self.var_recordar_carpeta
            ),
            (
                "Iniciar minimizado",
                self.var_iniciar_minimizado
            ),
            (
                "Iniciar directamente en modo mini",
                self.var_iniciar_mini
            ),
            (
                "Cerrar LITESYDUG a la bandeja",
                self.var_cerrar_tray
            )
        )


        for texto, variable in opciones:

            tk.Checkbutton(
                pagina,
                text=texto,
                variable=variable,
                bg=self.color(
                    "panel_2"
                ),
                fg=self.color(
                    "texto"
                ),
                activebackground=self.color(
                    "panel_2"
                ),
                activeforeground=self.color(
                    "texto"
                ),
                selectcolor=self.color(
                    "panel"
                ),
                font=(
                    "Segoe UI",
                    9
                ),
                anchor="w"
            ).pack(
                fill="x",
                padx=28,
                pady=8
            )


        tk.Label(
            pagina,
            text="Salto adelante / atrás",
            bg=self.color(
                "panel_2"
            ),
            fg=self.color(
                "texto_secundario"
            ),
            font=(
                "Segoe UI",
                8
            )
        ).pack(
            anchor="w",
            padx=28,
            pady=(18, 5)
        )


        self.selector_salto = ttk.Combobox(
            pagina,
            values=(
                "5",
                "10",
                "15",
                "30"
            ),
            state="readonly",
            width=8
        )


        self.selector_salto.set(
            str(
                self.datos.get(
                    "salto_segundos",
                    10
                )
            )
        )


        self.selector_salto.pack(
            anchor="w",
            padx=28
        )


    # =====================================================
    # RENDIMIENTO
    # =====================================================

    def crear_rendimiento(self):

        pagina = self.paginas[
            "Rendimiento"
        ]


        self.titulo_pagina(
            pagina,
            "RENDIMIENTO",
            "Controla cuánto trabajo hace la interfaz mientras juegas."
        )


        tk.Label(
            pagina,
            text="Modo de rendimiento",
            bg=self.color(
                "panel_2"
            ),
            fg=self.color(
                "texto"
            ),
            font=(
                "Segoe UI",
                9,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=28,
            pady=(10, 5)
        )


        self.selector_rendimiento = ttk.Combobox(
            pagina,
            values=(
                "Normal",
                "Ahorro",
                "Ultra ligero"
            ),
            state="readonly",
            width=20
        )


        self.selector_rendimiento.set(
            self.datos.get(
                "modo_rendimiento",
                "Normal"
            )
        )


        self.selector_rendimiento.pack(
            anchor="w",
            padx=28,
            pady=(0, 15)
        )


        descripcion = (
            "NORMAL\n"
            "Actualiza la interfaz con mayor frecuencia.\n\n"
            "AHORRO\n"
            "Reduce actualizaciones visuales para consumir menos CPU.\n\n"
            "ULTRA LIGERO\n"
            "Prioriza el menor consumo posible mientras juegas."
        )


        tk.Label(
            pagina,
            text=descripcion,
            bg=self.color(
                "panel"
            ),
            fg=self.color(
                "texto_secundario"
            ),
            justify="left",
            anchor="nw",
            padx=15,
            pady=15,
            font=(
                "Segoe UI",
                8
            )
        ).pack(
            fill="x",
            padx=28,
            pady=10
        )


    # =====================================================
    # HOTKEYS
    # =====================================================

    def crear_hotkeys(self):

        pagina = self.paginas[
            "Hotkeys"
        ]


        self.titulo_pagina(
            pagina,
            "HOTKEYS GLOBALES",
            "Configura controles que funcionan incluso mientras juegas."
        )


        self.hotkeys_temporales = (
            self.datos.get(
                "hotkeys",
                {}
            ).copy()
        )


        self.nombres_temporales = (
            self.datos.get(
                "hotkeys_nombres",
                {}
            ).copy()
        )


        opciones = (
            (
                "Play / Pausa",
                "play_pausa"
            ),
            (
                "Siguiente",
                "siguiente"
            ),
            (
                "Anterior",
                "anterior"
            ),
            (
                "Retroceder 10 s",
                "retroceder_10"
            ),
            (
                "Adelantar 10 s",
                "adelantar_10"
            ),
            (
                "Volumen -",
                "volumen_menos"
            ),
            (
                "Volumen +",
                "volumen_mas"
            )
        )


        marco = tk.Frame(
            pagina,
            bg=self.color(
                "panel"
            )
        )


        marco.pack(
            fill="x",
            padx=22,
            pady=5
        )


        for fila, (
            texto,
            clave
        ) in enumerate(
            opciones
        ):

            tk.Label(
                marco,
                text=texto,
                bg=self.color(
                    "panel"
                ),
                fg=self.color(
                    "texto"
                ),
                font=(
                    "Segoe UI",
                    8
                )
            ).grid(
                row=fila,
                column=0,
                padx=8,
                pady=6,
                sticky="w"
            )


            etiqueta = tk.Label(
                marco,
                text=self.nombres_temporales.get(
                    clave,
                    "Sin asignar"
                ),
                bg=self.color(
                    "panel_interno"
                ),
                fg=self.color(
                    "texto"
                ),
                width=14,
                font=(
                    "Segoe UI",
                    8,
                    "bold"
                )
            )


            etiqueta.grid(
                row=fila,
                column=1,
                padx=6,
                pady=6,
                ipady=4
            )


            self.etiquetas_hotkeys[
                clave
            ] = etiqueta


            tk.Button(
                marco,
                text="CAMBIAR",
                command=lambda c=clave:
                self.capturar_hotkey(c),
                bg=self.color(
                    "boton"
                ),
                fg="white",
                activebackground=self.color(
                    "acento"
                ),
                activeforeground="white",
                borderwidth=0,
                font=(
                    "Segoe UI",
                    7,
                    "bold"
                ),
                cursor="hand2"
            ).grid(
                row=fila,
                column=2,
                padx=5,
                pady=6,
                ipadx=5,
                ipady=3
            )


            tk.Button(
                marco,
                text="X",
                command=lambda c=clave:
                self.quitar_hotkey(c),
                bg=self.color(
                    "boton"
                ),
                fg=self.color(
                    "rosa"
                ),
                activebackground=self.color(
                    "boton_hover"
                ),
                borderwidth=0,
                cursor="hand2"
            ).grid(
                row=fila,
                column=3,
                padx=5,
                pady=6,
                ipadx=4,
                ipady=3
            )


        self.var_solo_oculto = tk.BooleanVar(
            value=self.datos.get(
                "solo_hotkeys_oculto",
                True
            )
        )


        tk.Checkbutton(
            pagina,
            text="Usar hotkeys solo cuando LITESYDUG esté oculto",
            variable=self.var_solo_oculto,
            bg=self.color(
                "panel_2"
            ),
            fg=self.color(
                "texto"
            ),
            activebackground=self.color(
                "panel_2"
            ),
            activeforeground=self.color(
                "texto"
            ),
            selectcolor=self.color(
                "panel"
            ),
            font=(
                "Segoe UI",
                8
            )
        ).pack(
            pady=10
        )


        self.selector_paso_volumen = ttk.Combobox(
            pagina,
            values=(
                "1",
                "5",
                "10"
            ),
            state="readonly",
            width=6
        )


        self.selector_paso_volumen.set(
            str(
                self.datos.get(
                    "paso_volumen",
                    5
                )
            )
        )


        self.selector_paso_volumen.pack()


    # =====================================================
    # CAPTURA HOTKEY
    # =====================================================

    def capturar_hotkey(
        self,
        clave
    ):

        etiqueta = self.etiquetas_hotkeys[
            clave
        ]


        etiqueta.config(
            text="Pulsa tecla...",
            fg=self.color(
                "cyan"
            )
        )


        self.hotkey_manager.limpiar()


        def hilo():

            nueva_tecla, nombre = (
                self.hotkey_manager.capturar_tecla()
            )


            if self.ventana is None:
                return


            self.ventana.after(
                0,
                lambda:
                self.finalizar_hotkey(
                    clave,
                    nueva_tecla,
                    nombre
                )
            )


        threading.Thread(
            target=hilo,
            daemon=True
        ).start()


    def finalizar_hotkey(
        self,
        clave,
        nueva_tecla,
        nombre
    ):

        if nueva_tecla is None:

            self.restaurar_hotkeys()

            return


        if self.hotkey_manager.es_peligrosa(
            nueva_tecla
        ):

            messagebox.showwarning(
                "Atajo bloqueado",
                "Esa combinación puede interferir con Windows."
            )

            self.restaurar_hotkeys()

            return


        for otra_clave, valor in (
            self.hotkeys_temporales.items()
        ):

            if (
                otra_clave != clave
                and valor == nueva_tecla
            ):

                messagebox.showwarning(
                    "Atajo repetido",
                    "Esa tecla ya está asignada."
                )

                self.restaurar_hotkeys()

                return


        self.hotkeys_temporales[
            clave
        ] = nueva_tecla


        self.nombres_temporales[
            clave
        ] = nombre


        self.etiquetas_hotkeys[
            clave
        ].config(
            text=nombre,
            fg=self.color(
                "texto"
            )
        )


        self.restaurar_hotkeys()


    def quitar_hotkey(
        self,
        clave
    ):

        self.hotkeys_temporales[
            clave
        ] = None


        self.nombres_temporales[
            clave
        ] = "Sin asignar"


        self.etiquetas_hotkeys[
            clave
        ].config(
            text="Sin asignar",
            fg=self.color(
                "texto"
            )
        )


    def restaurar_hotkeys(self):

        self.hotkey_manager.establecer_hotkeys(
            self.datos.get(
                "hotkeys",
                {}
            )
        )


        self.hotkey_manager.registrar()


    # =====================================================
    # INTERFAZ
    # =====================================================

    def crear_interfaz_config(self):

        pagina = self.paginas[
            "Interfaz"
        ]


        self.titulo_pagina(
            pagina,
            "INTERFAZ",
            "Personaliza algunos comportamientos visuales."
        )


        self.var_tooltips = tk.BooleanVar(
            value=self.datos.get(
                "mostrar_tooltips",
                True
            )
        )


        self.var_mini_encima = tk.BooleanVar(
            value=self.datos.get(
                "mini_siempre_encima",
                True
            )
        )


        self.var_recordar_posicion = tk.BooleanVar(
            value=self.datos.get(
                "recordar_posicion_ventana",
                False
            )
        )


        opciones = (
            (
                "Mostrar ayudas al pasar el mouse",
                self.var_tooltips
            ),
            (
                "Modo mini encima por defecto",
                self.var_mini_encima
            ),
            (
                "Recordar posición de ventanas",
                self.var_recordar_posicion
            )
        )


        for texto, variable in opciones:

            tk.Checkbutton(
                pagina,
                text=texto,
                variable=variable,
                bg=self.color(
                    "panel_2"
                ),
                fg=self.color(
                    "texto"
                ),
                activebackground=self.color(
                    "panel_2"
                ),
                activeforeground=self.color(
                    "texto"
                ),
                selectcolor=self.color(
                    "panel"
                ),
                font=(
                    "Segoe UI",
                    9
                )
            ).pack(
                anchor="w",
                padx=28,
                pady=10
            )


    # =====================================================
    # AYUDA
    # =====================================================

    def crear_ayuda(self):

        pagina = self.paginas[
            "Ayuda"
        ]


        self.titulo_pagina(
            pagina,
            "AYUDA Y SERVICIO",
            "Preguntas frecuentes y acceso rápido al soporte."
        )


        ayuda = (
            "¿CÓMO REPRODUZCO UNA CANCIÓN?\n"
            "Haz doble clic sobre una canción de la biblioteca.\n\n"

            "¿CÓMO ADELANTO O RETROCEDO?\n"
            "Usa las flechas izquierda y derecha.\n\n"

            "¿CÓMO CAMBIO DE CANCIÓN CON EL TECLADO?\n"
            "Usa Ctrl + flecha izquierda o derecha.\n\n"

            "¿CÓMO PAUSO O CONTINÚO LA MÚSICA?\n"
            "Presiona la barra espaciadora.\n\n"

            "¿PUEDO CONTROLAR LITESYDUG MIENTRAS JUEGO?\n"
            "Sí. Puedes configurar hotkeys globales "
            "desde Ajustes > Hotkeys.\n\n"

            "¿QUÉ PASA SI CIERRO LITESYDUG?\n"
            "Si tienes activada la opción de cerrar a bandeja, "
            "LITESYDUG seguirá funcionando desde la bandeja del sistema."
        )


        tk.Label(
            pagina,
            text=ayuda,
            bg=self.color(
                "panel"
            ),
            fg=self.color(
                "texto"
            ),
            justify="left",
            anchor="nw",
            padx=18,
            pady=18,
            font=(
                "Segoe UI",
                9
            ),
            wraplength=440
        ).pack(
            fill="x",
            padx=24,
            pady=8
        )


        tk.Label(
            pagina,
            text="SOPORTE",
            bg=self.color(
                "panel_2"
            ),
            fg=self.color(
                "acento_claro"
            ),
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        ).pack(
            pady=(
                8,
                6
            )
        )


        marco_soporte = tk.Frame(
            pagina,
            bg=self.color(
                "panel_2"
            )
        )


        marco_soporte.pack(
            pady=4
        )


        if self.enlaces.get(
            "github"
        ):

            tk.Button(
                marco_soporte,
                text="GITHUB",
                command=lambda:
                self.abrir_enlace(
                    "github"
                ),
                bg=self.color(
                    "boton"
                ),
                fg=self.color(
                    "cyan"
                ),
                activebackground=self.color(
                    "boton_hover"
                ),
                activeforeground="white",
                borderwidth=0,
                cursor="hand2"
            ).pack(
                side="left",
                padx=6,
                ipadx=15,
                ipady=5
            )


        if self.enlaces.get(
            "soporte"
        ):

            tk.Button(
                marco_soporte,
                text="REPORTAR UN PROBLEMA",
                command=lambda:
                self.abrir_enlace(
                    "soporte"
                ),
                bg=self.color(
                    "boton"
                ),
                fg=self.color(
                    "rosa"
                ),
                activebackground=self.color(
                    "boton_hover"
                ),
                activeforeground="white",
                borderwidth=0,
                cursor="hand2"
            ).pack(
                side="left",
                padx=6,
                ipadx=15,
                ipady=5
            )


    # =====================================================
    # ACERCA DE
    # =====================================================

    def crear_acerca(self):

        pagina = self.paginas[
            "Acerca de"
        ]


        self.titulo_pagina(
            pagina,
            "ACERCA DE",
            "HOLAA, disfruta LITESYDUG, suerte en tus partidas!"
        )


        tk.Label(
            pagina,
            text="LITESYDUG",
            bg=self.color(
                "panel_2"
            ),
            fg=self.color(
                "acento_claro"
            ),
            font=(
                "Segoe UI",
                22,
                "bold"
            )
        ).pack(
            pady=(35, 5)
        )


        tk.Label(
            pagina,
            text=self.version,
            bg=self.color(
                "panel_2"
            ),
            fg=self.color(
                "cyan"
            ),
            font=(
                "Segoe UI",
                9,
                "bold"
            )
        ).pack()


        tk.Label(
            pagina,
            text=(
                "Reproductor de música ligero y optimizado para Windows.\n"
                "Servido por Vulthy dev."
            ),
            bg=self.color(
                "panel_2"
            ),
            fg=self.color(
                "texto_secundario"
            ),
            justify="center",
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            pady=18
        )


        for clave, texto in (
            (
                "github",
                "GitHub"
            ),
            (
                "instagram",
                "Instagram"
            ),
            (
                "tiktok",
                "TikTok"
            )
        ):

            if self.enlaces.get(
                clave
            ):

                tk.Button(
                    pagina,
                    text=texto,
                    command=lambda c=clave:
                    self.abrir_enlace(c),
                    bg=self.color(
                        "boton"
                    ),
                    fg=self.color(
                        "texto"
                    ),
                    activebackground=self.color(
                        "boton_hover"
                    ),
                    activeforeground="white",
                    borderwidth=0,
                    cursor="hand2"
                ).pack(
                    pady=5,
                    ipadx=25,
                    ipady=5
                )


        # -----------------------------------------------------
        # APOYAR PROYECTO
        # -----------------------------------------------------

        tk.Label(
            pagina,
            text="¿Te gusta LITESYDUG?",
            bg=self.color(
                "panel_2"
            ),
            fg=self.color(
                "acento_claro"
            ),
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        ).pack(
            pady=(
                18,
                4
            )
        )


        tk.Label(
            pagina,
            text="Puedes apoyar el desarrollo del proyecto.",
            bg=self.color(
                "panel_2"
            ),
            fg=self.color(
                "texto_secundario"
            ),
            font=(
                "Segoe UI",
                9
            )
        ).pack(
            pady=(
                0,
                8
            )
        )


        if self.enlaces.get(
            "kofi"
        ):

            tk.Button(
                pagina,
                text="☕ APOYAR PROYECTO",
                command=lambda:
                self.abrir_enlace(
                    "kofi"
                ),
                bg=self.color(
                    "boton"
                ),
                fg=self.color(
                    "cyan"
                ),
                activebackground=self.color(
                    "boton_hover"
                ),
                activeforeground="white",
                borderwidth=0,
                cursor="hand2"
            ).pack(
                pady=5,
                ipadx=20,
                ipady=5
            )


    # =====================================================
    # ENLACES
    # =====================================================

    def abrir_enlace(
        self,
        clave
    ):

        url = self.enlaces.get(
            clave
        )


        if url:

            webbrowser.open(
                url
            )


    # =====================================================
    # GUARDAR
    # =====================================================

    def guardar(self):

        # -----------------------------------------------------
        # GENERAL
        # -----------------------------------------------------

        self.config.establecer(
            "recordar_ultima_carpeta",
            self.var_recordar_carpeta.get()
        )


        self.config.establecer(
            "iniciar_minimizado",
            self.var_iniciar_minimizado.get()
        )


        self.config.establecer(
            "iniciar_mini",
            self.var_iniciar_mini.get()
        )


        self.config.establecer(
            "cerrar_a_bandeja",
            self.var_cerrar_tray.get()
        )


        self.config.establecer(
            "salto_segundos",
            int(
                self.selector_salto.get()
            )
        )


        # -----------------------------------------------------
        # RENDIMIENTO
        # -----------------------------------------------------

        self.config.establecer(
            "modo_rendimiento",
            self.selector_rendimiento.get()
        )


        # -----------------------------------------------------
        # INTERFAZ
        # -----------------------------------------------------

        self.config.establecer(
            "mostrar_tooltips",
            self.var_tooltips.get()
        )


        self.config.establecer(
            "mini_siempre_encima",
            self.var_mini_encima.get()
        )


        self.config.establecer(
            "recordar_posicion_ventana",
            self.var_recordar_posicion.get()
        )


        # -----------------------------------------------------
        # HOTKEYS
        # -----------------------------------------------------

        self.config.establecer_hotkeys(
            self.hotkeys_temporales
        )


        self.config.establecer_nombres_hotkeys(
            self.nombres_temporales
        )


        self.config.establecer(
            "solo_hotkeys_oculto",
            self.var_solo_oculto.get()
        )


        self.config.establecer(
            "paso_volumen",
            int(
                self.selector_paso_volumen.get()
            )
        )


        self.config.guardar()


        self.hotkey_manager.establecer_hotkeys(
            self.hotkeys_temporales
        )


        self.hotkey_manager.establecer_nombres_visibles(
            self.nombres_temporales
        )


        self.hotkey_manager.establecer_solo_oculto(
            self.var_solo_oculto.get()
        )


        self.hotkey_manager.registrar()


        if self.al_guardar is not None:

            try:

                self.al_guardar(
                    self.config.cargar()
                )

            except Exception:

                pass


        messagebox.showinfo(
            "LITESYDUG",
            "Ajustes guardados correctamente."
        )


        self.cerrar()


    # =====================================================
    # CERRAR
    # =====================================================

    def cerrar(self):

        if self.ventana is not None:

            try:

                self.ventana.destroy()

            except Exception:

                pass


        self.ventana = None