"""
=============================================================================
01 - Hola Mundo y Widgets Básicos de Tkinter
=============================================================================
Este módulo introduce los fundamentos esenciales para crear interfaces gráficas
(GUI) en Python utilizando Tkinter.

Conceptos cubiertos:
1. Creación e inicialización de la ventana principal (Tk).
2. Configuración de propiedades de la ventana: título, dimensiones, color y redimensión.
3. Centrado dinámico de ventanas en la pantalla.
4. Widgets fundamentales:
   - Label: Mostrar textos informativos o estados.
   - Entry: Capturar entradas de texto del usuario.
   - Button: Ejecutar acciones y responder a clics.
5. Variables de control de Tkinter (StringVar, IntVar):
   - Vinculación bidireccional de datos (Data Binding).
   - Observadores de cambios (trace_add).
6. El bucle de eventos principal (mainloop).
=============================================================================
"""

import tkinter as tk
from tkinter import font


def centrar_ventana(ventana: tk.Tk, ancho: int, alto: int) -> None:
    """Calcula las coordenadas necesarias para centrar la ventana en pantalla."""
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    pos_x = (pantalla_ancho // 2) - (ancho // 2)
    pos_y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")


def main() -> None:
    # ---------------------------------------------------------
    # 1. Ventana Principal
    # ---------------------------------------------------------
    raiz = tk.Tk()
    raiz.title("01 - Hola Mundo y Widgets Básicos")
    centrar_ventana(raiz, 550, 600)
    raiz.minsize(450, 500)
    raiz.configure(bg="#F4F6F9")

    # Fuentes personalizadas
    fuente_titulo = font.Font(family="Segoe UI", size=16, weight="bold")
    fuente_subtitulo = font.Font(family="Segoe UI", size=11, weight="bold")
    fuente_texto = font.Font(family="Segoe UI", size=10)
    fuente_boton = font.Font(family="Segoe UI", size=10, weight="bold")

    # ---------------------------------------------------------
    # 2. Encabezado
    # ---------------------------------------------------------
    header_frame = tk.Frame(raiz, bg="#2C3E50", padx=20, pady=15)
    header_frame.pack(fill=tk.X)

    lbl_titulo = tk.Label(
        header_frame,
        text="Fundamentos de Tkinter",
        font=fuente_titulo,
        fg="#FFFFFF",
        bg="#2C3E50",
    )
    lbl_titulo.pack()

    lbl_subtitulo = tk.Label(
        header_frame,
        text="Demostración de Labels, Entries, Buttons y Variables de Control",
        font=fuente_texto,
        fg="#BDC3C7",
        bg="#2C3E50",
    )
    lbl_subtitulo.pack(pady=(4, 0))

    # Contenedor central
    cuerpo = tk.Frame(raiz, bg="#F4F6F9", padx=30, pady=20)
    cuerpo.pack(fill=tk.BOTH, expand=True)

    # ---------------------------------------------------------
    # 3. Sección: Saludo Interactivo (Entry + StringVar)
    # ---------------------------------------------------------
    seccion1 = tk.LabelFrame(
        cuerpo,
        text=" 1. Captura de Texto y Saludo ",
        font=fuente_subtitulo,
        bg="#FFFFFF",
        fg="#2C3E50",
        padx=15,
        pady=15,
        relief=tk.GROOVE,
        bd=1,
    )
    seccion1.pack(fill=tk.X, pady=(0, 15))

    lbl_instruccion = tk.Label(
        seccion1,
        text="Escribe tu nombre a continuación:",
        font=fuente_texto,
        bg="#FFFFFF",
        fg="#34495E",
    )
    lbl_instruccion.pack(anchor=tk.W)

    # Variable de control reactiva para el texto
    var_nombre = tk.StringVar(value="")

    entry_nombre = tk.Entry(
        seccion1,
        textvariable=var_nombre,
        font=fuente_texto,
        bg="#F8F9F9",
        fg="#2C3E50",
        relief=tk.SOLID,
        bd=1,
    )
    entry_nombre.pack(fill=tk.X, pady=(6, 10), ipady=4)
    entry_nombre.focus()  # Poner el foco en el campo al iniciar

    # Etiqueta que reaccionará dinámicamente
    var_saludo = tk.StringVar(value="¡Hola! Esperando que ingreses tu nombre...")
    lbl_saludo = tk.Label(
        seccion1,
        textvariable=var_saludo,
        font=fuente_texto,
        bg="#EBF5FB",
        fg="#2980B9",
        padx=10,
        pady=8,
        relief=tk.FLAT,
    )
    lbl_saludo.pack(fill=tk.X)

    # Función ejecutada por el botón de saludar
    def saludar() -> None:
        nombre = var_nombre.get().strip()
        if nombre:
            var_saludo.set(f"¡Un gusto saludarte, {nombre}! Bienvenido a Tkinter.")
        else:
            var_saludo.set("Por favor escribe tu nombre en la caja de texto.")

    # Función para limpiar el campo
    def limpiar_texto() -> None:
        var_nombre.set("")
        var_saludo.set("¡Hola! Esperando que ingreses tu nombre...")
        entry_nombre.focus()

    frame_botones = tk.Frame(seccion1, bg="#FFFFFF")
    frame_botones.pack(fill=tk.X, pady=(10, 0))

    btn_saludar = tk.Button(
        frame_botones,
        text="Saludar",
        command=saludar,
        font=fuente_boton,
        bg="#27AE60",
        fg="#FFFFFF",
        activebackground="#229954",
        activeforeground="#FFFFFF",
        relief=tk.FLAT,
        padx=15,
        pady=5,
        cursor="hand2",
    )
    btn_saludar.pack(side=tk.LEFT, padx=(0, 8))

    btn_limpiar = tk.Button(
        frame_botones,
        text="Limpiar",
        command=limpiar_texto,
        font=fuente_boton,
        bg="#95A5A6",
        fg="#FFFFFF",
        activebackground="#7F8C8D",
        activeforeground="#FFFFFF",
        relief=tk.FLAT,
        padx=15,
        pady=5,
        cursor="hand2",
    )
    btn_limpiar.pack(side=tk.LEFT)

    # Al presionar Enter en el campo de texto también saluda
    entry_nombre.bind("<Return>", lambda event: saludar())

    # ---------------------------------------------------------
    # 4. Sección: Contador Numérico (IntVar)
    # ---------------------------------------------------------
    seccion2 = tk.LabelFrame(
        cuerpo,
        text=" 2. Contador Reactivo (IntVar) ",
        font=fuente_subtitulo,
        bg="#FFFFFF",
        fg="#2C3E50",
        padx=15,
        pady=15,
        relief=tk.GROOVE,
        bd=1,
    )
    seccion2.pack(fill=tk.X)

    var_contador = tk.IntVar(value=0)

    lbl_valor_contador = tk.Label(
        seccion2,
        textvariable=var_contador,
        font=font.Font(family="Segoe UI", size=26, weight="bold"),
        bg="#FFFFFF",
        fg="#E67E22",
    )
    lbl_valor_contador.pack(pady=(0, 10))

    frame_controles_contador = tk.Frame(seccion2, bg="#FFFFFF")
    frame_controles_contador.pack()

    def incrementar() -> None:
        var_contador.set(var_contador.get() + 1)

    def decrementar() -> None:
        var_contador.set(var_contador.get() - 1)

    def reiniciar() -> None:
        var_contador.set(0)

    btn_decrementar = tk.Button(
        frame_controles_contador,
        text="- Disminuir",
        command=decrementar,
        font=fuente_boton,
        bg="#E74C3C",
        fg="#FFFFFF",
        activebackground="#C0392B",
        relief=tk.FLAT,
        padx=10,
        pady=4,
        cursor="hand2",
    )
    btn_decrementar.pack(side=tk.LEFT, padx=4)

    btn_reiniciar = tk.Button(
        frame_controles_contador,
        text="Reiniciar",
        command=reiniciar,
        font=fuente_boton,
        bg="#BDC3C7",
        fg="#2C3E50",
        activebackground="#A6ACAF",
        relief=tk.FLAT,
        padx=10,
        pady=4,
        cursor="hand2",
    )
    btn_reiniciar.pack(side=tk.LEFT, padx=4)

    btn_incrementar = tk.Button(
        frame_controles_contador,
        text="+ Aumentar",
        command=incrementar,
        font=fuente_boton,
        bg="#3498DB",
        fg="#FFFFFF",
        activebackground="#2980B9",
        relief=tk.FLAT,
        padx=10,
        pady=4,
        cursor="hand2",
    )
    btn_incrementar.pack(side=tk.LEFT, padx=4)

    # ---------------------------------------------------------
    # 5. Pie de Página con Estado
    # ---------------------------------------------------------
    lbl_pie = tk.Label(
        raiz,
        text="Python Tkinter • Módulo 01 de Ejemplos",
        font=font.Font(family="Segoe UI", size=9),
        bg="#EAEDED",
        fg="#7F8C8D",
        pady=6,
    )
    lbl_pie.pack(side=tk.BOTTOM, fill=tk.X)

    # Iniciar el bucle de eventos
    raiz.mainloop()


if __name__ == "__main__":
    main()
