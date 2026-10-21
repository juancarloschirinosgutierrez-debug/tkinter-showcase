"""
=============================================================================
05 - Canvas: Gráficos Vectoriales, Animaciones e Interactividad
=============================================================================
El widget Canvas es uno de los componentes más poderosos de Tkinter. Permite:

1. Dibujo de primitivas geométricas vectoriales:
   - create_line: líneas con grosores, flechas y estilos.
   - create_rectangle: rectángulos con relleno y bordes.
   - create_oval: elipses y círculos perfectos.
   - create_arc: sectores circulares y arcos.
   - create_polygon: polígonos complejos definidos por vértices.
   - create_text: textos con fuentes y anclajes personalizables.

2. Animación fluida con el bucle root.after():
   - Animación sin bloquear la interfaz gráfica (sin usar time.sleep).
   - Manipulación de elementos con canvas.move() y canvas.coords().
   - Detección de colisiones contra bordes de la pantalla.

3. Pizarra de dibujo interactiva:
   - Captura de trazos a mano alzada mediante el evento <B1-Motion>.
=============================================================================
"""

import tkinter as tk
from tkinter import ttk, font
import random


def centrar_ventana(ventana: tk.Tk, ancho: int, alto: int) -> None:
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    pos_x = (pantalla_ancho // 2) - (ancho // 2)
    pos_y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")


class AppCanvas:
    def __init__(self, raiz: tk.Tk):
        self.raiz = raiz
        self.raiz.title("05 - Canvas, Gráficos Vectoriales y Animación")
        centrar_ventana(self.raiz, 820, 680)
        self.raiz.minsize(750, 600)
        self.raiz.configure(bg="#F4F6F9")

        self.fuente_subtitulo = font.Font(family="Segoe UI", size=10, weight="bold")
        self.fuente_normal = font.Font(family="Segoe UI", size=9)

        # Encabezado
        encabezado = tk.Frame(self.raiz, bg="#8E44AD", padx=20, pady=12)
        encabezado.pack(fill=tk.X)
        tk.Label(
            encabezado,
            text="Lienzo Vectorial y Animaciones (Tkinter Canvas)",
            font=("Segoe UI", 14, "bold"),
            fg="#FFFFFF",
            bg="#8E44AD",
        ).pack()
        tk.Label(
            encabezado,
            text="Figuras geométricas, animación en tiempo real con after() y pizarra de dibujo",
            font=self.fuente_normal,
            fg="#F4ECF7",
            bg="#8E44AD",
        ).pack()

        # Notebook de 2 pestañas: 1) Gráficos y Animación, 2) Pizarra Interactiva
        notebook = ttk.Notebook(self.raiz)
        notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tab_animacion = ttk.Frame(notebook, padding=10)
        tab_pizarra = ttk.Frame(notebook, padding=10)

        notebook.add(tab_animacion, text="  1. Gráficos y Animación de Pelota  ")
        notebook.add(tab_pizarra, text="  2. Pizarra de Dibujo con Ratón  ")

        self.configurar_pestaña_animacion(tab_animacion)
        self.configurar_pestaña_pizarra(tab_pizarra)

    # -------------------------------------------------------------------------
    # PESTAÑA 1: Formas y Animación
    # -------------------------------------------------------------------------
    def configurar_pestaña_animacion(self, contenedor: ttk.Frame) -> None:
        # Lienzo principal para gráficos
        self.ancho_canvas = 760
        self.alto_canvas = 380

        self.canvas_anim = tk.Canvas(
            contenedor,
            width=self.ancho_canvas,
            height=self.alto_canvas,
            bg="#1B2631",
            highlightthickness=0,
        )
        self.canvas_anim.pack(fill=tk.BOTH, expand=True)

        # Dibujar figuras vectoriales de fondo ilustrativas
        self.dibujar_figuras_estaticas()

        # Crear la pelota animada
        self.radio = 16
        self.pos_x = 100
        self.pos_y = 100
        self.vel_x = 5
        self.vel_y = 4
        self.animando = False
        self.id_after = None

        self.pelota = self.canvas_anim.create_oval(
            self.pos_x - self.radio,
            self.pos_y - self.radio,
            self.pos_x + self.radio,
            self.pos_y + self.radio,
            fill="#E74C3C",
            outline="#FFFFFF",
            width=2,
        )

        # Panel de Controles de Animación
        panel_controles = tk.Frame(contenedor, bg="#FFFFFF", pady=10, padx=15, relief=tk.GROOVE, bd=1)
        panel_controles.pack(fill=tk.X, pady=(10, 0))

        self.btn_toggle_anim = tk.Button(
            panel_controles,
            text="▶ Iniciar Animación",
            font=("Segoe UI", 9, "bold"),
            bg="#27AE60",
            fg="white",
            relief=tk.FLAT,
            padx=12,
            pady=5,
            command=self.alternar_animacion,
            cursor="hand2",
        )
        self.btn_toggle_anim.pack(side=tk.LEFT, padx=(0, 10))

        btn_color = tk.Button(
            panel_controles,
            text="Cambiar Color Pelota",
            font=self.fuente_normal,
            bg="#3498DB",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            command=self.cambiar_color_pelota,
            cursor="hand2",
        )
        btn_color.pack(side=tk.LEFT, padx=(0, 15))

        tk.Label(panel_controles, text="Velocidad (FPS / delay):", font=self.fuente_normal, bg="#FFFFFF").pack(side=tk.LEFT)
        self.scale_delay = tk.Scale(
            panel_controles,
            from_=5,
            to=50,
            orient=tk.HORIZONTAL,
            bg="#FFFFFF",
            highlightthickness=0,
            troughcolor="#EAEDED",
            length=140,
        )
        self.scale_delay.set(16)  # ~60 fps
        self.scale_delay.pack(side=tk.LEFT, padx=(5, 0))

    def dibujar_figuras_estaticas(self) -> None:
        """Dibuja varios ejemplos de primitivas vectoriales en el lienzo."""
        # Rectángulo con borde
        self.canvas_anim.create_rectangle(30, 30, 150, 100, fill="#2E4053", outline="#5DADE2", width=2)
        self.canvas_anim.create_text(90, 65, text="Rectángulo", fill="#EAECEE", font=("Segoe UI", 9, "bold"))

        # Elipse
        self.canvas_anim.create_oval(180, 30, 300, 100, fill="#117A65", outline="#A3E4D7", width=2)
        self.canvas_anim.create_text(240, 65, text="Óvalo / Elipse", fill="#EAECEE", font=("Segoe UI", 9, "bold"))

        # Polígono (Triángulo)
        puntos = [340, 100, 390, 30, 440, 100]
        self.canvas_anim.create_polygon(puntos, fill="#B7950B", outline="#F7DC6F", width=2)
        self.canvas_anim.create_text(390, 75, text="Polígono", fill="#1B2631", font=("Segoe UI", 8, "bold"))

        # Arco circular
        self.canvas_anim.create_arc(480, 30, 580, 100, start=30, extent=240, fill="#7D3C98", outline="#D2B4DE", width=2)
        self.canvas_anim.create_text(530, 65, text="Arco", fill="#FFFFFF", font=("Segoe UI", 9, "bold"))

        # Línea con flecha
        self.canvas_anim.create_line(620, 40, 720, 90, arrow=tk.LAST, fill="#E67E22", width=3)
        self.canvas_anim.create_text(670, 45, text="Línea con flecha", fill="#E67E22", font=("Segoe UI", 8))

        # Texto explicativo en el lienzo
        self.canvas_anim.create_text(
            380, 340,
            text="Física del Canvas: La pelota detecta colisiones con los bordes y rebota en tiempo real.",
            fill="#85929E",
            font=("Segoe UI", 9, "italic"),
        )

    def alternar_animacion(self) -> None:
        if self.animando:
            self.animando = False
            self.btn_toggle_anim.config(text="▶ Reanudar", bg="#27AE60")
            if self.id_after:
                self.raiz.after_cancel(self.id_after)
        else:
            self.animando = True
            self.btn_toggle_anim.config(text="⏸ Pausar", bg="#E67E22")
            self.actualizar_animacion()

    def actualizar_animacion(self) -> None:
        if not self.animando:
            return

        # Ancho y alto actual del canvas
        ancho = self.canvas_anim.winfo_width()
        alto = self.canvas_anim.winfo_height()

        if ancho > 1 and alto > 1:
            coords = self.canvas_anim.coords(self.pelota)
            x1, y1, x2, y2 = coords

            # Rebotar en bordes horizontales
            if x2 + self.vel_x >= ancho or x1 + self.vel_x <= 0:
                self.vel_x = -self.vel_x

            # Rebotar en bordes verticales
            if y2 + self.vel_y >= alto or y1 + self.vel_y <= 0:
                self.vel_y = -self.vel_y

            # Mover la pelota
            self.canvas_anim.move(self.pelota, self.vel_x, self.vel_y)

        delay = int(self.scale_delay.get())
        self.id_after = self.raiz.after(delay, self.actualizar_animacion)

    def cambiar_color_pelota(self) -> None:
        colores = ["#E74C3C", "#3498DB", "#2ECC71", "#F1C40F", "#9B59B6", "#1ABC9C", "#E67E22"]
        nuevo_color = random.choice(colores)
        self.canvas_anim.itemconfig(self.pelota, fill=nuevo_color)

    # -------------------------------------------------------------------------
    # PESTAÑA 2: Pizarra Interactiva
    # -------------------------------------------------------------------------
    def configurar_pestaña_pizarra(self, contenedor: ttk.Frame) -> None:
        # Lienzo para pintar
        self.canvas_draw = tk.Canvas(
            contenedor,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#BDC3C7",
            cursor="crosshair",
        )
        self.canvas_draw.pack(fill=tk.BOTH, expand=True)

        self.color_pincel = "#2C3E50"
        self.grosor_pincel = 3
        self.pos_anterior_x = None
        self.pos_anterior_y = None

        # Eventos del ratón para dibujar
        self.canvas_draw.bind("<Button-1>", self.iniciar_trazo)
        self.canvas_draw.bind("<B1-Motion>", self.dibujar_trazo)
        self.canvas_draw.bind("<ButtonRelease-1>", self.finalizar_trazo)

        # Barra de herramientas de dibujo
        barra = tk.Frame(contenedor, bg="#F4F6F9", pady=8)
        barra.pack(fill=tk.X)

        tk.Label(barra, text="Color:", font=self.fuente_normal, bg="#F4F6F9").pack(side=tk.LEFT, padx=(0, 4))

        colores = [("#2C3E50", "Negro"), ("#E74C3C", "Rojo"), ("#3498DB", "Azul"), ("#27AE60", "Verde")]
        for hex_col, nombre in colores:
            btn = tk.Button(
                barra,
                bg=hex_col,
                width=3,
                height=1,
                relief=tk.FLAT,
                command=lambda c=hex_col: self.set_color_pincel(c),
                cursor="hand2",
            )
            btn.pack(side=tk.LEFT, padx=2)

        tk.Label(barra, text="Grosor:", font=self.fuente_normal, bg="#F4F6F9").pack(side=tk.LEFT, padx=(15, 4))
        scale_grosor = tk.Scale(
            barra,
            from_=1,
            to=20,
            orient=tk.HORIZONTAL,
            bg="#F4F6F9",
            highlightthickness=0,
            length=100,
            command=lambda val: self.set_grosor(int(val)),
        )
        scale_grosor.set(3)
        scale_grosor.pack(side=tk.LEFT)

        btn_limpiar = tk.Button(
            barra,
            text="Limpiar Pizarra",
            font=self.fuente_normal,
            bg="#95A5A6",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            command=lambda: self.canvas_draw.delete("all"),
            cursor="hand2",
        )
        btn_limpiar.pack(side=tk.RIGHT)

    def iniciar_trazo(self, evento: tk.Event) -> None:
        self.pos_anterior_x = evento.x
        self.pos_anterior_y = evento.y

    def dibujar_trazo(self, evento: tk.Event) -> None:
        if self.pos_anterior_x and self.pos_anterior_y:
            self.canvas_draw.create_line(
                self.pos_anterior_x,
                self.pos_anterior_y,
                evento.x,
                evento.y,
                fill=self.color_pincel,
                width=self.grosor_pincel,
                capstyle=tk.ROUND,
                smooth=True,
            )
            self.pos_anterior_x = evento.x
            self.pos_anterior_y = evento.y

    def finalizar_trazo(self, evento: tk.Event) -> None:
        self.pos_anterior_x = None
        self.pos_anterior_y = None

    def set_color_pincel(self, color: str) -> None:
        self.color_pincel = color

    def set_grosor(self, grosor: int) -> None:
        self.grosor_pincel = grosor


def main() -> None:
    raiz = tk.Tk()
    app = AppCanvas(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
