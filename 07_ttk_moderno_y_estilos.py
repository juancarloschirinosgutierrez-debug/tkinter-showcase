"""
=============================================================================
07 - Widgets Modernos TTK (Themed Tkinter) y Motor de Estilos
=============================================================================
El submódulo tkinter.ttk introduce widgets temáticos con una apariencia moderna
y una clara separación entre la lógica del widget y su presentación visual:

1. Widgets Clave de TTK:
   - ttk.Notebook: Interfaz basada en pestañas / tabs organizativas.
   - ttk.Treeview: Tablas de datos tabulares (filas y columnas) y árboles jerárquicos.
   - ttk.Progressbar: Barras de progreso en modo determinado e indeterminado.
   - ttk.Combobox: Menús desplegables con autocompletado y selección segura.
   - ttk.Separator: Divisores visuales horizontales o verticales.
   - ttk.PanedWindow: Paneles divididos con tirador redimensionable por el usuario.

2. Motor de Temas y Estilos (ttk.Style):
   - Consulta y cambio de temas globales en tiempo de ejecución (theme_use).
   - Configuración de propiedades visuales (configure).
   - Mapeo dinámico de estados: hover, presionado, deshabilitado (map).
=============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, font


def centrar_ventana(ventana: tk.Tk, ancho: int, alto: int) -> None:
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    pos_x = (pantalla_ancho // 2) - (ancho // 2)
    pos_y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")


class AppTTK:
    def __init__(self, raiz: tk.Tk):
        self.raiz = raiz
        self.raiz.title("07 - Widgets Temáticos TTK y Estilos Modernos")
        centrar_ventana(self.raiz, 840, 700)
        self.raiz.minsize(760, 600)

        # Inicialización del gestor de estilos
        self.estilo = ttk.Style(self.raiz)

        # Encabezado superior
        encabezado = tk.Frame(self.raiz, bg="#2980B9", padx=20, pady=12)
        encabezado.pack(fill=tk.X)
        tk.Label(
            encabezado,
            text="Widgets Modernos TTK (Themed Tkinter)",
            font=("Segoe UI", 14, "bold"),
            fg="#FFFFFF",
            bg="#2980B9",
        ).pack()
        tk.Label(
            encabezado,
            text="Treeview (Tablas), Notebook (Pestañas), Combobox, Progressbar y Selector de Temas",
            font=("Segoe UI", 9),
            fg="#EBF5FB",
            bg="#2980B9",
        ).pack()

        # Selector de tema en tiempo real
        self.crear_barra_temas()

        # Notebook principal
        self.notebook = ttk.Notebook(self.raiz)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Pestañas
        tab_tabla = ttk.Frame(self.notebook, padding=10)
        tab_controles = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(tab_tabla, text="  1. Tabla de Datos (Treeview)  ")
        self.notebook.add(tab_controles, text="  2. Progressbar, Combobox y Paneles  ")

        self.configurar_pestaña_tabla(tab_tabla)
        self.configurar_pestaña_controles(tab_controles)

    # -------------------------------------------------------------------------
    # Selector de Temas
    # -------------------------------------------------------------------------
    def crear_barra_temas(self) -> None:
        barra_tema = ttk.Frame(self.raiz, padding=(15, 8))
        barra_tema.pack(fill=tk.X)

        ttk.Label(barra_tema, text="Tema visual del sistema:", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 8))

        temas_disponibles = self.estilo.theme_names()
        tema_actual = self.estilo.theme_use()

        self.combo_temas = ttk.Combobox(
            barra_tema,
            values=list(temas_disponibles),
            state="readonly",
            width=15,
        )
        self.combo_temas.set(tema_actual)
        self.combo_temas.pack(side=tk.LEFT)
        self.combo_temas.bind("<<ComboboxSelected>>", self.cambiar_tema)

        ttk.Label(
            barra_tema,
            text=f"Temas detectados en tu SO: {', '.join(temas_disponibles)}",
            font=("Segoe UI", 8, "italic"),
            foreground="#555555",
        ).pack(side=tk.RIGHT)

    def cambiar_tema(self, evento: tk.Event = None) -> None:
        nuevo_tema = self.combo_temas.get()
        try:
            self.estilo.theme_use(nuevo_tema)
        except Exception as e:
            messagebox.showwarning("Tema", f"No se pudo aplicar el tema '{nuevo_tema}': {e}")

    # -------------------------------------------------------------------------
    # PESTAÑA 1: Treeview (Tabla estructurada con ordenación)
    # -------------------------------------------------------------------------
    def configurar_pestaña_tabla(self, contenedor: ttk.Frame) -> None:
        lbl_info = ttk.Label(
            contenedor,
            text="Treeview permite mostrar tablas de datos profesionales con encabezados interactivos.\n"
                 "Haz clic en el encabezado de cualquier columna para ordenar los registros.",
            font=("Segoe UI", 9, "italic"),
        )
        lbl_info.pack(fill=tk.X, pady=(0, 8))

        # Contenedor para Treeview + Scrollbars
        frame_tree = ttk.Frame(contenedor)
        frame_tree.pack(fill=tk.BOTH, expand=True)

        columnas = ("id", "nombre", "categoria", "precio", "stock")
        self.tree = ttk.Treeview(frame_tree, columns=columnas, show="headings", selectmode="browse")

        # Configurar encabezados y anchos
        self.tree.heading("id", text="ID", command=lambda: self.ordenar_columna("id", False))
        self.tree.heading("nombre", text="Producto / Componente", command=lambda: self.ordenar_columna("nombre", False))
        self.tree.heading("categoria", text="Categoría", command=lambda: self.ordenar_columna("categoria", False))
        self.tree.heading("precio", text="Precio ($ USD)", command=lambda: self.ordenar_columna("precio", False))
        self.tree.heading("stock", text="Stock", command=lambda: self.ordenar_columna("stock", False))

        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("nombre", width=220, anchor=tk.W)
        self.tree.column("categoria", width=140, anchor=tk.W)
        self.tree.column("precio", width=110, anchor=tk.E)
        self.tree.column("stock", width=80, anchor=tk.CENTER)

        # Scrollbar vertical y horizontal
        scroll_y = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_x = ttk.Scrollbar(frame_tree, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configuración de filas alternadas (Striped Rows)
        self.tree.tag_configure("par", background="#F8F9F9")
        self.tree.tag_configure("impar", background="#FFFFFF")

        # Datos de ejemplo
        datos_ejemplo = [
            (101, "Monitor 4K IPS 27\"", "Periféricos", 349.99, 14),
            (102, "Teclado Mecánico RGB", "Accesorios", 89.50, 42),
            (103, "Ratón Ergonómico Inalámbrico", "Accesorios", 49.99, 58),
            (104, "Procesador Octa-Core 4.5GHz", "Hardware", 289.00, 20),
            (105, "Memoria RAM DDR5 32GB", "Hardware", 119.95, 35),
            (106, "Disco SSD NVMe 2TB", "Almacenamiento", 145.00, 27),
            (107, "Auriculares con Cancelación de Ruido", "Audio", 179.90, 19),
            (108, "Cámara Web Full HD 60fps", "Periféricos", 65.00, 31),
        ]

        for i, fila in enumerate(datos_ejemplo):
            tag = "par" if i % 2 == 0 else "impar"
            self.tree.insert("", tk.END, values=fila, tags=(tag,))

        # Barra de acciones inferiores para la tabla
        barra_acciones = ttk.Frame(contenedor, padding=(0, 8))
        barra_acciones.pack(fill=tk.X)

        btn_ver_sel = ttk.Button(barra_acciones, text="Ver Registro Seleccionado", command=self.ver_registro_seleccionado)
        btn_ver_sel.pack(side=tk.LEFT, padx=(0, 6))

        btn_eliminar_fila = ttk.Button(barra_acciones, text="Eliminar Registro", command=self.eliminar_fila_seleccionada)
        btn_eliminar_fila.pack(side=tk.LEFT)

    def ver_registro_seleccionado(self) -> None:
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Selección", "Por favor selecciona una fila de la tabla primero.")
            return
        valores = self.tree.item(seleccion[0], "values")
        info = f"ID: {valores[0]}\nProducto: {valores[1]}\nCategoría: {valores[2]}\nPrecio: ${valores[3]}\nStock: {valores[4]} unidades"
        messagebox.showinfo("Detalle de Registro", info)

    def eliminar_fila_seleccionada(self) -> None:
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Eliminar", "Selecciona una fila para eliminar.")
            return
        self.tree.delete(seleccion[0])

    def ordenar_columna(self, columna: str, reverso: bool) -> None:
        elementos = [(self.tree.set(k, columna), k) for k in self.tree.get_children("")]
        try:
            # Intenta ordenar numéricamente si aplica
            elementos.sort(key=lambda t: float(t[0].replace("$", "").strip()), reverse=reverso)
        except ValueError:
            elementos.sort(reverse=reverso)

        for indice, (_, k) in enumerate(elementos):
            self.tree.move(k, "", indice)

        # Alternar la dirección de la próxima ordenación
        self.tree.heading(columna, command=lambda: self.ordenar_columna(columna, not reverso))

    # -------------------------------------------------------------------------
    # PESTAÑA 2: Progressbars y Combobox
    # -------------------------------------------------------------------------
    def configurar_pestaña_controles(self, contenedor: ttk.Frame) -> None:
        # 1. Grupo Progressbars
        grp_progreso = ttk.LabelFrame(contenedor, text=" Barras de Progreso (ttk.Progressbar) ", padding=12)
        grp_progreso.pack(fill=tk.X, pady=(0, 15))

        # Modo Determinado
        ttk.Label(grp_progreso, text="Modo Determinado (Valor medible 0 a 100%):").pack(anchor=tk.W)
        self.prog_determinado = ttk.Progressbar(grp_progreso, orient=tk.HORIZONTAL, length=300, mode="determinate")
        self.prog_determinado.pack(fill=tk.X, pady=(4, 8))
        self.prog_determinado["value"] = 35

        frame_btns_det = ttk.Frame(grp_progreso)
        frame_btns_det.pack(anchor=tk.W, pady=(0, 12))

        def avanzar_progreso(paso: int) -> None:
            val = self.prog_determinado["value"] + paso
            if val > 100:
                val = 0
            self.prog_determinado["value"] = val

        ttk.Button(frame_btns_det, text="+10% Paso", command=lambda: avanzar_progreso(10)).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(frame_btns_det, text="Reiniciar a 0%", command=lambda: self.prog_determinado.configure(value=0)).pack(side=tk.LEFT)

        ttk.Separator(grp_progreso, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=8)

        # Modo Indeterminado
        ttk.Label(grp_progreso, text="Modo Indeterminado (Carga de proceso desconocido):").pack(anchor=tk.W)
        self.prog_indeterminado = ttk.Progressbar(grp_progreso, orient=tk.HORIZONTAL, length=300, mode="indeterminate")
        self.prog_indeterminado.pack(fill=tk.X, pady=(4, 8))

        frame_btns_indet = ttk.Frame(grp_progreso)
        frame_btns_indet.pack(anchor=tk.W)

        ttk.Button(frame_btns_indet, text="▶ Iniciar Giro", command=lambda: self.prog_indeterminado.start(10)).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(frame_btns_indet, text="⏹ Detener Giro", command=lambda: self.prog_indeterminado.stop()).pack(side=tk.LEFT)

        # 2. Grupo PanedWindow / Split View
        grp_paned = ttk.LabelFrame(contenedor, text=" Ventana Dividida (ttk.PanedWindow) ", padding=12)
        grp_paned.pack(fill=tk.BOTH, expand=True)

        paned = ttk.PanedWindow(grp_paned, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        panel_izq = ttk.Frame(paned, padding=8, relief=tk.SUNKEN)
        panel_der = ttk.Frame(paned, padding=8, relief=tk.SUNKEN)

        paned.add(panel_izq, weight=1)
        paned.add(panel_der, weight=2)

        ttk.Label(panel_izq, text="Panel Izquierdo\nArrastra la barra divisoria\npara ajustar el ancho relativo.", justify=tk.CENTER).pack(expand=True)
        ttk.Label(panel_der, text="Panel Derecho\nContenido ampliable responsivo.", justify=tk.CENTER).pack(expand=True)


def main() -> None:
    raiz = tk.Tk()
    app = AppTTK(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
