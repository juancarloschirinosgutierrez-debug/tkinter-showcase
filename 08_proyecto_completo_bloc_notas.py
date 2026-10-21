"""
=============================================================================
08 - Proyecto Integral: Bloc de Notas Profesional con POO
=============================================================================
Este proyecto reúne todas las funcionalidades de Tkinter estudiadas en los
módulos anteriores en una aplicación de escritorio completa, robusta y modular
estructurada con Programación Orientada a Objetos (POO):

Características implementadas:
1. Widget Text avanzado con soporte nativo de Undo/Redo y Tags de formato.
2. Gestión integral de archivos (Nuevo, Abrir, Guardar, Guardar Como).
3. Detección de modificaciones no guardadas con indicador (*) en el título.
4. Cuadros de confirmación inteligentes al salir o crear nuevo archivo.
5. Sistema de Búsqueda de texto con resaltado visual en tiempo real.
6. Barra de estado inferior con conteo reactivo de líneas, columnas, palabras y caracteres.
7. Alternancia de temas visuales: Modo Claro y Modo Oscuro.
8. Control de ajuste de línea (Word Wrap) y tamaño de fuente tipográfica.
9. Atajos globales de teclado (Ctrl+N, Ctrl+O, Ctrl+S, Ctrl+F, Ctrl+Z, etc.).
=============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog, font
import os


def centrar_ventana(ventana: tk.Tk, ancho: int, alto: int) -> None:
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    pos_x = (pantalla_ancho // 2) - (ancho // 2)
    pos_y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")


class BlocDeNotas:
    def __init__(self, raiz: tk.Tk):
        self.raiz = raiz
        self.archivo_actual = None
        self.modificado = False
        self.tamano_fuente = 11
        self.modo_oscuro = False

        self.raiz.title("Sin título - Bloc de Notas Python")
        centrar_ventana(self.raiz, 880, 640)
        self.raiz.minsize(600, 400)

        # Configuración de fuentes
        self.fuente_editor = font.Font(family="Consolas", size=self.tamano_fuente)
        self.fuente_ui = font.Font(family="Segoe UI", size=9)

        # Construcción de la interfaz
        self.crear_menus()
        self.crear_barra_herramientas()
        self.crear_area_edicion()
        self.crear_barra_estado()
        self.configurar_atajos()

        # Interceptar el evento de cierre de ventana (X)
        self.raiz.protocol("WM_DELETE_WINDOW", self.confirmar_cierre)

    # -------------------------------------------------------------------------
    # 1. Menús de la Aplicación
    # -------------------------------------------------------------------------
    def crear_menus(self) -> None:
        self.barra_menus = tk.Menu(self.raiz)
        self.raiz.config(menu=self.barra_menus)

        # Menú Archivo
        menu_archivo = tk.Menu(self.barra_menus, tearoff=0)
        self.barra_menus.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Nuevo", command=self.nuevo_archivo, accelerator="Ctrl+N")
        menu_archivo.add_command(label="Abrir...", command=self.abrir_archivo, accelerator="Ctrl+O")
        menu_archivo.add_command(label="Guardar", command=self.guardar_archivo, accelerator="Ctrl+S")
        menu_archivo.add_command(label="Guardar como...", command=self.guardar_como, accelerator="Ctrl+Shift+S")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.confirmar_cierre, accelerator="Alt+F4")

        # Menú Edición
        menu_edicion = tk.Menu(self.barra_menus, tearoff=0)
        self.barra_menus.add_cascade(label="Edición", menu=menu_edicion)
        menu_edicion.add_command(label="Deshacer", command=self.deshacer, accelerator="Ctrl+Z")
        menu_edicion.add_command(label="Rehacer", command=self.rehacer, accelerator="Ctrl+Y")
        menu_edicion.add_separator()
        menu_edicion.add_command(label="Cortar", command=lambda: self.editor.event_generate("<<Cut>>"), accelerator="Ctrl+X")
        menu_edicion.add_command(label="Copiar", command=lambda: self.editor.event_generate("<<Copy>>"), accelerator="Ctrl+C")
        menu_edicion.add_command(label="Pegar", command=lambda: self.editor.event_generate("<<Paste>>"), accelerator="Ctrl+V")
        menu_edicion.add_separator()
        menu_edicion.add_command(label="Buscar...", command=self.abrir_cuadro_busqueda, accelerator="Ctrl+F")
        menu_edicion.add_command(label="Seleccionar todo", command=self.seleccionar_todo, accelerator="Ctrl+A")

        # Menú Ver / Preferencias
        menu_ver = tk.Menu(self.barra_menus, tearoff=0)
        self.barra_menus.add_cascade(label="Ver", menu=menu_ver)

        self.var_wrap = tk.BooleanVar(value=True)
        menu_ver.add_checkbutton(label="Ajuste de línea", variable=self.var_wrap, command=self.alternar_wrap)

        menu_ver.add_command(label="Aumentar fuente", command=self.aumentar_fuente, accelerator="Ctrl++")
        menu_ver.add_command(label="Disminuir fuente", command=self.disminuir_fuente, accelerator="Ctrl+-")
        menu_ver.add_separator()
        menu_ver.add_command(label="Alternar Modo Oscuro/Claro", command=self.alternar_tema)

        # Menú Ayuda
        menu_ayuda = tk.Menu(self.barra_menus, tearoff=0)
        self.barra_menus.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca del Bloc de Notas", command=self.mostrar_acerca_de)

    # -------------------------------------------------------------------------
    # 2. Barra de Herramientas Rápida
    # -------------------------------------------------------------------------
    def crear_barra_herramientas(self) -> None:
        self.toolbar = tk.Frame(self.raiz, bg="#EAECEE", padx=5, pady=3, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_nuevo = tk.Button(self.toolbar, text="📄 Nuevo", font=self.fuente_ui, command=self.nuevo_archivo, relief=tk.FLAT, bg="#EAECEE", cursor="hand2")
        btn_nuevo.pack(side=tk.LEFT, padx=2)

        btn_abrir = tk.Button(self.toolbar, text="📂 Abrir", font=self.fuente_ui, command=self.abrir_archivo, relief=tk.FLAT, bg="#EAECEE", cursor="hand2")
        btn_abrir.pack(side=tk.LEFT, padx=2)

        btn_guardar = tk.Button(self.toolbar, text="💾 Guardar", font=self.fuente_ui, command=self.guardar_archivo, relief=tk.FLAT, bg="#EAECEE", cursor="hand2")
        btn_guardar.pack(side=tk.LEFT, padx=2)

        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=2)

        btn_buscar = tk.Button(self.toolbar, text="🔍 Buscar", font=self.fuente_ui, command=self.abrir_cuadro_busqueda, relief=tk.FLAT, bg="#EAECEE", cursor="hand2")
        btn_buscar.pack(side=tk.LEFT, padx=2)

        btn_tema = tk.Button(self.toolbar, text="🌓 Tema", font=self.fuente_ui, command=self.alternar_tema, relief=tk.FLAT, bg="#EAECEE", cursor="hand2")
        btn_tema.pack(side=tk.LEFT, padx=2)

    # -------------------------------------------------------------------------
    # 3. Área de Edición (Text + Scrollbars)
    # -------------------------------------------------------------------------
    def crear_area_edicion(self) -> None:
        frame_editor = tk.Frame(self.raiz)
        frame_editor.pack(fill=tk.BOTH, expand=True)

        scroll_y = tk.Scrollbar(frame_editor, orient=tk.VERTICAL)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x = tk.Scrollbar(frame_editor, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.editor = tk.Text(
            frame_editor,
            wrap=tk.WORD,
            undo=True,
            font=self.fuente_editor,
            bg="#FFFFFF",
            fg="#2C3E50",
            insertbackground="#2C3E50",
            padx=10,
            pady=10,
            relief=tk.FLAT,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )
        self.editor.pack(fill=tk.BOTH, expand=True)

        scroll_y.config(command=self.editor.yview)
        scroll_x.config(command=self.editor.xview)

        # Configuración de tags para resaltado de búsqueda
        self.editor.tag_configure("resaltado", background="#F9E79F", foreground="#000000")

        # Vincular eventos de escritura para detectar cambios y conteo
        self.editor.bind("<<Modified>>", self.al_modificar_texto)
        self.editor.bind("<KeyRelease>", lambda e: self.actualizar_barra_estado())
        self.editor.bind("<ButtonRelease-1>", lambda e: self.actualizar_barra_estado())

    # -------------------------------------------------------------------------
    # 4. Barra de Estado
    # -------------------------------------------------------------------------
    def crear_barra_estado(self) -> None:
        self.barra_estado = tk.Frame(self.raiz, bg="#D5D8DC", padx=10, pady=3)
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)

        self.lbl_estado_pos = tk.Label(
            self.barra_estado,
            text="Lín: 1, Col: 1",
            font=self.fuente_ui,
            bg="#D5D8DC",
            fg="#34495E",
        )
        self.lbl_estado_pos.pack(side=tk.RIGHT, padx=10)

        self.lbl_estado_conteo = tk.Label(
            self.barra_estado,
            text="Palabras: 0 | Caracteres: 0",
            font=self.fuente_ui,
            bg="#D5D8DC",
            fg="#34495E",
        )
        self.lbl_estado_conteo.pack(side=tk.RIGHT, padx=10)

        self.lbl_archivo_info = tk.Label(
            self.barra_estado,
            text="Codificación: UTF-8  |  Listo",
            font=self.fuente_ui,
            bg="#D5D8DC",
            fg="#34495E",
        )
        self.lbl_archivo_info.pack(side=tk.LEFT)

    def actualizar_barra_estado(self) -> None:
        pos = self.editor.index(tk.INSERT)
        linea, columna = pos.split(".")
        columna_ajustada = int(columna) + 1
        self.lbl_estado_pos.config(text=f"Lín: {linea}, Col: {columna_ajustada}")

        contenido = self.editor.get("1.0", "end-1c")
        caracteres = len(contenido)
        palabras = len(contenido.split()) if contenido.strip() else 0
        self.lbl_estado_conteo.config(text=f"Palabras: {palabras} | Caracteres: {caracteres}")

    def al_modificar_texto(self, evento: tk.Event = None) -> None:
        if self.editor.edit_modified():
            self.modificado = True
            self.actualizar_titulo()
            self.editor.edit_modified(False)
            self.actualizar_barra_estado()

    def actualizar_titulo(self) -> None:
        nombre = os.path.basename(self.archivo_actual) if self.archivo_actual else "Sin título"
        asterisco = "*" if self.modificado else ""
        self.raiz.title(f"{asterisco}{nombre} - Bloc de Notas Python")

    # -------------------------------------------------------------------------
    # 5. Operaciones de Archivo
    # -------------------------------------------------------------------------
    def nuevo_archivo(self) -> None:
        if self.modificado:
            if not self.preguntar_guardar():
                return
        self.editor.delete("1.0", tk.END)
        self.archivo_actual = None
        self.modificado = False
        self.actualizar_titulo()
        self.actualizar_barra_estado()

    def abrir_archivo(self) -> None:
        if self.modificado:
            if not self.preguntar_guardar():
                return

        ruta = filedialog.askopenfilename(
            title="Abrir archivo",
            filetypes=[("Archivos de texto", "*.txt"), ("Archivos Python", "*.py"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", contenido)
                self.archivo_actual = ruta
                self.modificado = False
                self.actualizar_titulo()
                self.actualizar_barra_estado()
                self.lbl_archivo_info.config(text=f"Archivo cargado: {os.path.basename(ruta)}")
            except Exception as e:
                messagebox.showerror("Error al Abrir", f"No se pudo abrir el archivo:\n{e}")

    def guardar_archivo(self) -> bool:
        if not self.archivo_actual:
            return self.guardar_como()
        try:
            contenido = self.editor.get("1.0", "end-1c")
            with open(self.archivo_actual, "w", encoding="utf-8") as f:
                f.write(contenido)
            self.modificado = False
            self.actualizar_titulo()
            self.lbl_archivo_info.config(text=f"Guardado exitoso: {os.path.basename(self.archivo_actual)}")
            return True
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"No se pudo guardar el archivo:\n{e}")
            return False

    def guardar_como(self) -> bool:
        ruta = filedialog.asksaveasfilename(
            title="Guardar archivo como",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Archivos Python", "*.py"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            self.archivo_actual = ruta
            return self.guardar_archivo()
        return False

    def preguntar_guardar(self) -> bool:
        nombre = os.path.basename(self.archivo_actual) if self.archivo_actual else "Sin título"
        respuesta = messagebox.askyesnocancel(
            "Guardar Cambios",
            f"¿Deseas guardar los cambios en '{nombre}' antes de continuar?"
        )
        if respuesta is True:
            return self.guardar_archivo()
        elif respuesta is False:
            return True  # Continúa sin guardar
        else:
            return False  # Cancela la acción

    def confirmar_cierre(self) -> None:
        if self.modificado:
            if not self.preguntar_guardar():
                return
        self.raiz.destroy()

    # -------------------------------------------------------------------------
    # 6. Funcionalidades de Edición y Búsqueda
    # -------------------------------------------------------------------------
    def deshacer(self) -> None:
        try:
            self.editor.edit_undo()
        except tk.TclError:
            pass

    def rehacer(self) -> None:
        try:
            self.editor.edit_redo()
        except tk.TclError:
            pass

    def seleccionar_todo(self) -> str:
        self.editor.tag_add(tk.SEL, "1.0", tk.END)
        self.editor.mark_set(tk.INSERT, "1.0")
        self.editor.see(tk.INSERT)
        return "break"

    def abrir_cuadro_busqueda(self) -> None:
        termino = simpledialog.askstring("Buscar en el texto", "Ingresa el texto a buscar:")
        self.editor.tag_remove("resaltado", "1.0", tk.END)

        if not termino:
            return

        coincidencias = 0
        pos_inicio = "1.0"
        while True:
            pos_inicio = self.editor.search(termino, pos_inicio, stopindex=tk.END)
            if not pos_inicio:
                break
            pos_fin = f"{pos_inicio}+{len(termino)}c"
            self.editor.tag_add("resaltado", pos_inicio, pos_fin)
            coincidencias += 1
            pos_inicio = pos_fin

        if coincidencias > 0:
            messagebox.showinfo("Búsqueda", f"Se encontraron y resaltaron {coincidencias} coincidencia(s).")
        else:
            messagebox.showinfo("Búsqueda", f"No se encontró el término '{termino}'.")

    # -------------------------------------------------------------------------
    # 7. Preferencias de Visualización (Temas, Fuente, Wrap)
    # -------------------------------------------------------------------------
    def alternar_wrap(self) -> None:
        nuevo_wrap = tk.WORD if self.var_wrap.get() else tk.NONE
        self.editor.config(wrap=nuevo_wrap)

    def aumentar_fuente(self) -> None:
        if self.tamano_fuente < 36:
            self.tamano_fuente += 1
            self.fuente_editor.configure(size=self.tamano_fuente)

    def disminuir_fuente(self) -> None:
        if self.tamano_fuente > 8:
            self.tamano_fuente -= 1
            self.fuente_editor.configure(size=self.tamano_fuente)

    def alternar_tema(self) -> None:
        self.modo_oscuro = not self.modo_oscuro
        if self.modo_oscuro:
            # Paleta modo oscuro
            self.editor.config(bg="#1E1E1E", fg="#D4D4D4", insertbackground="#FFFFFF")
            self.toolbar.config(bg="#2D2D2D")
            self.barra_estado.config(bg="#252526")
            self.lbl_estado_pos.config(bg="#252526", fg="#CCCCCC")
            self.lbl_estado_conteo.config(bg="#252526", fg="#CCCCCC")
            self.lbl_archivo_info.config(bg="#252526", fg="#CCCCCC")
            self.editor.tag_configure("resaltado", background="#614A19", foreground="#FFFFFF")
        else:
            # Paleta modo claro
            self.editor.config(bg="#FFFFFF", fg="#2C3E50", insertbackground="#2C3E50")
            self.toolbar.config(bg="#EAECEE")
            self.barra_estado.config(bg="#D5D8DC")
            self.lbl_estado_pos.config(bg="#D5D8DC", fg="#34495E")
            self.lbl_estado_conteo.config(bg="#D5D8DC", fg="#34495E")
            self.lbl_archivo_info.config(bg="#D5D8DC", fg="#34495E")
            self.editor.tag_configure("resaltado", background="#F9E79F", foreground="#000000")

    def mostrar_acerca_de(self) -> None:
        messagebox.showinfo(
            "Acerca de",
            "Bloc de Notas en Python con Tkinter\nVersión 1.0\n\nDemostración práctica de desarrollo GUI con Python."
        )

    # -------------------------------------------------------------------------
    # 8. Atajos de Teclado
    # -------------------------------------------------------------------------
    def configurar_atajos(self) -> None:
        self.raiz.bind("<Control-n>", lambda e: self.nuevo_archivo())
        self.raiz.bind("<Control-N>", lambda e: self.nuevo_archivo())
        self.raiz.bind("<Control-o>", lambda e: self.abrir_archivo())
        self.raiz.bind("<Control-O>", lambda e: self.abrir_archivo())
        self.raiz.bind("<Control-s>", lambda e: self.guardar_archivo())
        self.raiz.bind("<Control-S>", lambda e: self.guardar_archivo())
        self.raiz.bind("<Control-Shift-s>", lambda e: self.guardar_como())
        self.raiz.bind("<Control-Shift-S>", lambda e: self.guardar_como())
        self.raiz.bind("<Control-f>", lambda e: self.abrir_cuadro_busqueda())
        self.raiz.bind("<Control-F>", lambda e: self.abrir_cuadro_busqueda())
        self.raiz.bind("<Control-plus>", lambda e: self.aumentar_fuente())
        self.raiz.bind("<Control-minus>", lambda e: self.disminuir_fuente())


def main() -> None:
    raiz = tk.Tk()
    app = BlocDeNotas(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
