import os

from PIL import Image, ImageTk


class Assets:

    def __init__(self):

        self.carpeta_proyecto = os.path.dirname(
            os.path.abspath(__file__)
        )

        self.carpeta_assets = os.path.join(
            self.carpeta_proyecto,
            "assets"
        )


    # =====================================================
    # OBTENER RUTA
    # =====================================================

    def ruta(
        self,
        nombre
    ):

        return os.path.join(
            self.carpeta_assets,
            nombre
        )


    # =====================================================
    # CARGAR IMAGEN PARA TKINTER
    # =====================================================

    def cargar_tk(
        self,
        nombre,
        tamano
    ):

        ruta_imagen = self.ruta(
            nombre
        )


        if not os.path.exists(
            ruta_imagen
        ):

            print(
                f"No se encontró asset: {ruta_imagen}"
            )

            return None


        try:

            imagen = Image.open(
                ruta_imagen
            )


            imagen = imagen.convert(
                "RGBA"
            )


            imagen.thumbnail(
                tamano,
                Image.Resampling.LANCZOS
            )


            return ImageTk.PhotoImage(
                imagen
            )


        except Exception as error:

            print(
                f"Error cargando {nombre}:",
                error
            )

            return None


    # =====================================================
    # CARGAR PIL
    # =====================================================

    def cargar_pil(
        self,
        nombre,
        tamano=None
    ):

        ruta_imagen = self.ruta(
            nombre
        )


        if not os.path.exists(
            ruta_imagen
        ):

            return None


        try:

            imagen = Image.open(
                ruta_imagen
            ).convert(
                "RGBA"
            )


            if tamano is not None:

                imagen.thumbnail(
                    tamano,
                    Image.Resampling.LANCZOS
                )


            return imagen


        except Exception as error:

            print(
                f"Error cargando {nombre}:",
                error
            )

            return None