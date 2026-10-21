"""
=============================================================================
02 - Administradores de Geometría y Posicionamiento (Layouts)
=============================================================================
Tkinter ofrece tres administradores de geometría fundamentales para organizar
los widgets dentro de ventanas o contenedores (Frames):

1. pack():
   - Organiza los widgets apilándolos vertical u horizontalmente.
   - Parámetros clave: side (TOP, BOTTOM, LEFT, RIGHT), fill (X, Y, BOTH, NONE),
     expand (True/False), anchor (N, S, E, W, CENTER), padx, pady, ipadx, ipady.

2. grid():
   - Organiza los widgets en una tabla bidimensional de filas y columnas.
   - Es el más potente y flexible para formularios y layouts estructurados.
   - Parámetros clave: row, column, rowspan, columnspan, sticky (N, S, E, W),
     columnconfigure, rowconfigure (asignación de pesos para redimensión responsiva).

3. place():
   - Posicionamiento exacto por coordenadas absolutas (píxeles) o relativas (porcentajes).
   - Parámetros clave: x, y, width, height, relx, rely, relwidth, relheight, anchor.

Regla de oro de Tkinter: NUNCA mezcles pack() y grid() directamente dentro del
mismo contenedor padre (utiliza Frames intermedios para combinarlos).
=============================================================================
"""

import tkinter as tk
from tkinter import ttk, font


def centrar_ventana(ventana: tk.Tk, ancho: int, alto: int) -> None:
    """Centra la ventana en la pantalla del usuario."""
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    pos_x = (pantalla_ancho // 2) - (ancho // 2)
    pos_y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")


def crear_seccion_pack(notebook: ttk.Notebook) -> ttk.Frame:
    """Crea una pestaña demostrativa del administrador de geometría PACK."""
    tab = ttk.Frame(notebook, padding=15)

    lbl_info = tk.Label(
        tab,
        text="El método pack() apila widgets a lo largo de los bordes del contenedor.\n"
             "Prueba cambiar la orientación y mira cómo responde con 'fill' y 'expand'.",
        font=("Segoe UI", 9, "italic"),
        fg="#555555",
        justify=tk.LEFT,
    )
    lbl_info.pack(fill=tk.X, pady=(0, 10))

    # Contenedor demostrativo
    caja_demo = tk.Frame(tab, bg="#EAEDED", bd=2, relief=tk.SUNKEN, height=180)
    caja_demo.pack(fill=tk.BOTH, expand=True, pady=10)
    caja_demo.pack_propagate(False)  # Mantener tamaño fijo para ilustrar

    # Widgets apilados con pack
    b1 = tk.Button(caja_demo, text="Top / Fill X", bg="#E74C3C", fg="white", relief=tk.FLAT)
    b1.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    b2 = tk.Button(caja_demo, text="Bottom / Expand", bg="#3498DB", fg="white", relief=tk.FLAT)
    b2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)

    b3 = tk.Button(caja_demo, text="Left", bg="#2ECC71", fg="white", relief=tk.FLAT)
    b3.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

    b4 = tk.Button(caja_demo, text="Right", bg="#F39C12", fg="white", relief=tk.FLAT)
    b4.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

    lbl_explicacion = tk.Label(
        tab,
        text="• side=TOP / BOTTOM / LEFT / RIGHT determina el borde de anclaje.\n"
             "• fill=X / Y / BOTH indica si el widget se estira para llenar el espacio.\n"
             "• expand=True reclama todo el espacio sobrante del contenedor padre.",
        font=("Segoe UI", 9),
        justify=tk.LEFT,
        bg="#FEF9E7",
        padx=10,
        pady=8,
    )
    lbl_explicacion.pack(fill=tk.X, pady=(10, 0))

    return tab


def crear_seccion_grid(notebook: ttk.Notebook) -> ttk.Frame:
    """Crea una pestaña demostrativa del administrador de geometría GRID (Formulario)."""
    tab = ttk.Frame(notebook, padding=15)

    lbl_info = tk.Label(
        tab,
        text="El método grid() organiza widgets en filas y columnas matemáticas.\n"
             "Es ideal para formularios limpios y alineados pixel-perfect.",
        font=("Segoe UI", 9, "italic"),
        fg="#555555",
        justify=tk.LEFT,
    )
    lbl_info.pack(fill=tk.X, pady=(0, 10))

    # Formulario dentro de un Frame con grid
    form_frame = tk.LabelFrame(
        tab,
        text=" Formulario de Registro con Grid ",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=15,
        bg="#FFFFFF",
    )
    form_frame.pack(fill=tk.BOTH, expand=True)

    # Configurar pesos de columnas para hacerlo responsivo
    form_frame.columnconfigure(1, weight=1)

    # Fila 0: Nombre
    tk.Label(form_frame, text="Nombre completo:", bg="#FFFFFF", font=("Segoe UI", 9, "bold")).grid(
        row=0, column=0, sticky=tk.W, pady=6, padx=(0, 10)
    )
    tk.Entry(form_frame, font=("Segoe UI", 9), relief=tk.SOLID, bd=1).grid(
        row=0, column=1, sticky="ew", pady=6
    )

    # Fila 1: Correo
    tk.Label(form_frame, text="Correo Electrónico:", bg="#FFFFFF", font=("Segoe UI", 9, "bold")).grid(
        row=1, column=0, sticky=tk.W, pady=6, padx=(0, 10)
    )
    tk.Entry(form_frame, font=("Segoe UI", 9), relief=tk.SOLID, bd=1).grid(
        row=1, column=1, sticky="ew", pady=6
    )

    # Fila 2: Comentarios (Usa columnspan para abarcar 2 columnas)
    tk.Label(form_frame, text="Observaciones (columnspan=2):", bg="#FFFFFF", font=("Segoe UI", 9, "bold")).grid(
        row=2, column=0, columnspan=2, sticky=tk.W, pady=(12, 4)
    )
    txt_comentario = tk.Text(form_frame, height=3, font=("Segoe UI", 9), relief=tk.SOLID, bd=1)
    txt_comentario.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=4)
    form_frame.rowconfigure(3, weight=1)

    # Fila 4: Botones alineados a la derecha
    btn_frame = tk.Frame(form_frame, bg="#FFFFFF")
    btn_frame.grid(row=4, column=0, columnspan=2, sticky=tk.E, pady=(10, 0))

    tk.Button(
        btn_frame, text="Cancelar", bg="#95A5A6", fg="white", padx=10, relief=tk.FLAT
    ).pack(side=tk.RIGHT, padx=(6, 0))
    tk.Button(
        btn_frame, text="Guardar", bg="#27AE60", fg="white", padx=15, relief=tk.FLAT
    ).pack(side=tk.RIGHT)

    return tab


def crear_seccion_place(notebook: ttk.Notebook) -> ttk.Frame:
    """Crea una pestaña demostrativa del administrador de geometría PLACE."""
    tab = ttk.Frame(notebook, padding=15)

    lbl_info = tk.Label(
        tab,
        text="place() ubica elementos por coordenadas fijas (x, y) o porcentajes relativos.\n"
             "Útil para superposiciones, insignias flotantes o animaciones personalizadas.",
        font=("Segoe UI", 9, "italic"),
        fg="#555555",
        justify=tk.LEFT,
    )
    lbl_info.pack(fill=tk.X, pady=(0, 10))

    # Lienzo contenedor con place
    lienzo = tk.Frame(tab, bg="#2C3E50", bd=2, relief=tk.RIDGE)
    lienzo.pack(fill=tk.BOTH, expand=True)

    # Posicionamiento absoluto en píxeles: (x=20, y=20)
    lbl_fijo = tk.Label(
        lienzo,
        text="Fijo en (x=20, y=20)",
        bg="#E74C3C",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        padx=8,
        pady=4,
    )
    lbl_fijo.place(x=20, y=20)

    # Posicionamiento relativo al centro: relx=0.5, rely=0.5, anchor=CENTER
    lbl_centro = tk.Label(
        lienzo,
        text="Centro relativo\n(relx=0.5, rely=0.5)",
        bg="#3498DB",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        justify=tk.CENTER,
        padx=12,
        pady=8,
    )
    lbl_centro.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Posicionamiento en esquina inferior derecha: relx=1.0, rely=1.0, anchor=SE
    lbl_esquina = tk.Label(
        lienzo,
        text="Esquina (relx=1.0, rely=1.0)",
        bg="#2ECC71",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        padx=8,
        pady=4,
    )
    lbl_esquina.place(relx=0.95, rely=0.92, anchor=tk.SE)

    return tab


def main() -> None:
    raiz = tk.Tk()
    raiz.title("02 - Layouts y Administradores de Geometría")
    centrar_ventana(raiz, 650, 560)
    raiz.minsize(550, 480)

    # Encabezado
    encabezado = tk.Frame(raiz, bg="#34495E", padx=15, pady=12)
    encabezado.pack(fill=tk.X)

    tk.Label(
        encabezado,
        text="Administradores de Geometría en Tkinter",
        font=("Segoe UI", 14, "bold"),
        fg="#FFFFFF",
        bg="#34495E",
    ).pack()

    tk.Label(
        encabezado,
        text="Comparativa interactiva: pack() vs grid() vs place()",
        font=("Segoe UI", 9),
        fg="#BDC3C7",
        bg="#34495E",
    ).pack()

    # Notebook (Pestañas)
    notebook = ttk.Notebook(raiz)
    notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    tab_pack = crear_seccion_pack(notebook)
    tab_grid = crear_seccion_grid(notebook)
    tab_place = crear_seccion_place(notebook)

    notebook.add(tab_pack, text="  1. pack()  ")
    notebook.add(tab_grid, text="  2. grid()  ")
    notebook.add(tab_place, text="  3. place()  ")

    # Pie de página informativo
    tk.Label(
        raiz,
        text="Tip: Diseña interfaces complejas usando Frame/LabelFrame como bloques modulares.",
        font=("Segoe UI", 9),
        bg="#EAEDED",
        fg="#7F8C8D",
        pady=6,
    ).pack(side=tk.BOTTOM, fill=tk.X)

    raiz.mainloop()


if __name__ == "__main__":
    main()
