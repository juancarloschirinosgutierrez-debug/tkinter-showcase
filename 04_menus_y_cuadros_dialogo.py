"""
=============================================================================
04 - Menús de Aplicación, Menú Contextual y Cuadros de Diálogo
=============================================================================
Este módulo enseña la implementación de sistemas de navegación y diálogos modales:

1. Barra de Menús Superior (tk.Menu):
   - Menús en cascada (Archivo, Edición, Herramientas, Ayuda).
   - Separadores visuales (add_separator).
   - Opciones de verificación y radio dentro de menús (add_checkbutton, add_radiobutton).
   - Atajos visuales de teclado (accelerator).

2. Menú Contextual (Pop-up / Clic Derecho):
   - Vinculado al evento <Button-3> (o <Button-2> en macOS).
   - Métodos tk_popup() y grab_release().

3. Cuadros de Diálogo Estándar:
   - messagebox: showinfo, showwarning, showerror, askyesno, askokcancel, askretrycancel.
   - filedialog: askopenfilename, asksaveasfilename, askdirectory.
   - colorchooser: askcolor (selección de colores con paleta visual del sistema).
=============================================================================
"""

import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser, font
import sys


def centrar_ventana(ventana: tk.Tk, ancho: int, alto: int) -> None:
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    pos_x = (pantalla_ancho // 2) - (ancho // 2)
    pos_y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")


def main() -> None:
    raiz = tk.Tk()
    raiz.title("04 - Menús y Cuadros de Diálogo")
    centrar_ventana(raiz, 720, 620)
    raiz.minsize(620, 520)
    raiz.configure(bg="#F4F6F9")

    fuente_titulo = font.Font(family="Segoe UI", size=14, weight="bold")
    fuente_subtitulo = font.Font(family="Segoe UI", size=10, weight="bold")
    fuente_normal = font.Font(family="Segoe UI", size=9)

    # ---------------------------------------------------------
    # Área de Log / Salida visual
    # ---------------------------------------------------------
    frame_consola = tk.LabelFrame(
        raiz,
        text=" Historial de Acciones y Retornos de Diálogo ",
        font=fuente_subtitulo,
        bg="#FFFFFF",
        fg="#2C3E50",
        padx=12,
        pady=10,
    )
    frame_consola.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

    txt_log = tk.Text(
        frame_consola,
        height=8,
        bg="#1E272C",
        fg="#2ECC71",
        insertbackground="white",
        font=font.Font(family="Consolas", size=9),
        relief=tk.FLAT,
    )
    scroll_log = tk.Scrollbar(frame_consola, command=txt_log.yview)
    txt_log.config(yscrollcommand=scroll_log.set)
    scroll_log.pack(side=tk.RIGHT, fill=tk.Y)
    txt_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def log(mensaje: str) -> None:
        txt_log.insert(tk.END, f">> {mensaje}\n")
        txt_log.see(tk.END)

    log("Aplicación iniciada. Explora la barra superior o presiona los botones de prueba.")

    # ---------------------------------------------------------
    # 1. Barra de Menús Superior
    # ---------------------------------------------------------
    barra_menus = tk.Menu(raiz)
    raiz.config(menu=barra_menus)

    # --- Menú Archivo ---
    menu_archivo = tk.Menu(barra_menus, tearoff=0)
    barra_menus.add_cascade(label="Archivo", menu=menu_archivo)

    def nuevo_archivo() -> None:
        log("Acción: 'Nuevo Archivo' ejecutada.")

    def abrir_archivo() -> None:
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Archivos de Texto", "*.txt"), ("Archivos Python", "*.py"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            log(f"Archivo seleccionado para abrir: {ruta}")
        else:
            log("Apertura de archivo cancelada.")

    def guardar_archivo() -> None:
        ruta = filedialog.asksaveasfilename(
            title="Guardar archivo como",
            defaultextension=".txt",
            filetypes=[("Texto plano", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            log(f"Archivo guardado en: {ruta}")
        else:
            log("Guardado de archivo cancelado.")

    def salir_app() -> None:
        respuesta = messagebox.askyesno("Confirmar Salida", "¿Realmente deseas salir de la aplicación?")
        if respuesta:
            log("Saliendo de la aplicación...")
            raiz.destroy()

    menu_archivo.add_command(label="Nuevo", command=nuevo_archivo, accelerator="Ctrl+N")
    menu_archivo.add_command(label="Abrir...", command=abrir_archivo, accelerator="Ctrl+O")
    menu_archivo.add_command(label="Guardar Como...", command=guardar_archivo, accelerator="Ctrl+S")
    menu_archivo.add_separator()
    menu_archivo.add_command(label="Salir", command=salir_app, accelerator="Alt+F4")

    # --- Menú Opciones (Con Checkbuttons y Radiobuttons dentro de menús) ---
    menu_opciones = tk.Menu(barra_menus, tearoff=0)
    barra_menus.add_cascade(label="Opciones", menu=menu_opciones)

    var_autoguardado = tk.BooleanVar(value=True)
    menu_opciones.add_checkbutton(
        label="Autoguardado en segundo plano",
        variable=var_autoguardado,
        command=lambda: log(f"Autoguardado: {var_autoguardado.get()}")
    )

    menu_opciones.add_separator()
    var_nivel_log = tk.StringVar(value="Info")
    for nivel in ["Debug", "Info", "Warning", "Error"]:
        menu_opciones.add_radiobutton(
            label=f"Nivel de Log: {nivel}",
            variable=var_nivel_log,
            value=nivel,
            command=lambda: log(f"Nivel de log cambiado a: {var_nivel_log.get()}")
        )

    # --- Menú Ayuda ---
    menu_ayuda = tk.Menu(barra_menus, tearoff=0)
    barra_menus.add_cascade(label="Ayuda", menu=menu_ayuda)

    def mostrar_acerca_de() -> None:
        messagebox.showinfo(
            "Acerca de este Módulo",
            "Módulo 04: Menús y Cuadros de Diálogo en Tkinter.\nDesarrollado para demostración de interfaces gráficas con Python."
        )
        log("Diálogo 'Acerca de' consultado.")

    menu_ayuda.add_command(label="Acerca de...", command=mostrar_acerca_de)

    # ---------------------------------------------------------
    # 2. Menú Contextual (Clic Derecho)
    # ---------------------------------------------------------
    menu_contextual = tk.Menu(raiz, tearoff=0)
    menu_contextual.add_command(label="Copiar texto de log", command=lambda: log("Texto copiado al portapapeles."))
    menu_contextual.add_command(label="Limpiar log", command=lambda: txt_log.delete("1.0", tk.END))
    menu_contextual.add_separator()
    menu_contextual.add_command(label="Seleccionar Color de Fondo", command=lambda: probar_color())

    def mostrar_menu_contextual(evento: tk.Event) -> None:
        try:
            menu_contextual.tk_popup(evento.x_root, evento.y_root)
        finally:
            menu_contextual.grab_release()

    # Vincular al clic derecho (<Button-3> en Windows/Linux, <Button-2> en macOS)
    boton_secundario = "<Button-2>" if sys.platform == "darwin" else "<Button-3>"
    raiz.bind(boton_secundario, mostrar_menu_contextual)

    # ---------------------------------------------------------
    # 3. Botones de Demostración de Diálogos Modales
    # ---------------------------------------------------------
    cuerpo = tk.Frame(raiz, bg="#F4F6F9", padx=15, pady=15)
    cuerpo.pack(fill=tk.BOTH, expand=False)

    grp_msg = tk.LabelFrame(
        cuerpo,
        text=" Demostración de Cuadros de Mensaje (messagebox) ",
        font=fuente_subtitulo,
        bg="#FFFFFF",
        fg="#2C3E50",
        padx=12,
        pady=10,
    )
    grp_msg.pack(fill=tk.X, pady=(0, 10))

    frame_btns_msg = tk.Frame(grp_msg, bg="#FFFFFF")
    frame_btns_msg.pack(fill=tk.X)

    def msg_info() -> None:
        messagebox.showinfo("Información", "Operación completada con éxito.")
        log("messagebox.showinfo ejecutado.")

    def msg_warn() -> None:
        messagebox.showwarning("Advertencia", "El espacio en disco es inferior al 10%.")
        log("messagebox.showwarning ejecutado.")

    def msg_error() -> None:
        messagebox.showerror("Error Crítico", "No se pudo conectar a la base de datos.")
        log("messagebox.showerror ejecutado.")

    def msg_pregunta() -> None:
        resp = messagebox.askyesno("Pregunta", "¿Deseas formatear la unidad externa?")
        log(f"messagebox.askyesno respuesta: {resp} ({'Sí' if resp else 'No'})")

    tk.Button(frame_btns_msg, text="Info", bg="#3498DB", fg="white", padx=10, relief=tk.FLAT, command=msg_info, cursor="hand2").pack(side=tk.LEFT, padx=3)
    tk.Button(frame_btns_msg, text="Advertencia", bg="#F39C12", fg="white", padx=10, relief=tk.FLAT, command=msg_warn, cursor="hand2").pack(side=tk.LEFT, padx=3)
    tk.Button(frame_btns_msg, text="Error", bg="#E74C3C", fg="white", padx=10, relief=tk.FLAT, command=msg_error, cursor="hand2").pack(side=tk.LEFT, padx=3)
    tk.Button(frame_btns_msg, text="Pregunta Sí/No", bg="#9B59B6", fg="white", padx=10, relief=tk.FLAT, command=msg_pregunta, cursor="hand2").pack(side=tk.LEFT, padx=3)

    # --- Diálogos de Sistema (Archivos y Colores) ---
    grp_archivos = tk.LabelFrame(
        cuerpo,
        text=" Diálogos del Sistema Operativo (filedialog y colorchooser) ",
        font=fuente_subtitulo,
        bg="#FFFFFF",
        fg="#2C3E50",
        padx=12,
        pady=10,
    )
    grp_archivos.pack(fill=tk.X)

    frame_btns_sis = tk.Frame(grp_archivos, bg="#FFFFFF")
    frame_btns_sis.pack(fill=tk.X)

    def seleccionar_carpeta() -> None:
        directorio = filedialog.askdirectory(title="Seleccionar Directorio de Trabajo")
        if directorio:
            log(f"Directorio seleccionado: {directorio}")
        else:
            log("Selección de directorio cancelada.")

    def probar_color() -> None:
        color = colorchooser.askcolor(title="Seleccionar un Color")
        # askcolor retorna una tupla: ((r, g, b), '#hex')
        if color[1]:
            color_hex = color[1]
            lbl_color_muestra.config(bg=color_hex)
            log(f"Color elegido: RGB={color[0]}, Hex={color_hex}")

    tk.Button(frame_btns_sis, text="Abrir Archivo...", bg="#16A085", fg="white", padx=8, relief=tk.FLAT, command=abrir_archivo, cursor="hand2").pack(side=tk.LEFT, padx=3)
    tk.Button(frame_btns_sis, text="Guardar Como...", bg="#27AE60", fg="white", padx=8, relief=tk.FLAT, command=guardar_archivo, cursor="hand2").pack(side=tk.LEFT, padx=3)
    tk.Button(frame_btns_sis, text="Elegir Carpeta...", bg="#2980B9", fg="white", padx=8, relief=tk.FLAT, command=seleccionar_carpeta, cursor="hand2").pack(side=tk.LEFT, padx=3)
    tk.Button(frame_btns_sis, text="Selector de Color...", bg="#8E44AD", fg="white", padx=8, relief=tk.FLAT, command=probar_color, cursor="hand2").pack(side=tk.LEFT, padx=3)

    lbl_color_muestra = tk.Label(frame_btns_sis, text="  Muestra  ", bg="#BDC3C7", fg="#2C3E50", font=("Segoe UI", 9, "bold"), relief=tk.SOLID, bd=1)
    lbl_color_muestra.pack(side=tk.LEFT, padx=(10, 0))

    # Mensaje de ayuda contextual
    lbl_hint = tk.Label(
        cuerpo,
        text="Pista: Haz clic derecho en cualquier parte vacía para abrir el menú contextual flotante.",
        font=("Segoe UI", 8, "italic"),
        fg="#7F8C8D",
        bg="#F4F6F9"
    )
    lbl_hint.pack(anchor=tk.W, pady=(6, 0))

    raiz.mainloop()


if __name__ == "__main__":
    main()
