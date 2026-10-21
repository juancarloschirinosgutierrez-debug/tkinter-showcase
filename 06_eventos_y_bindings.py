"""
=============================================================================
06 - Sistema de Eventos, Atajos de Teclado y Bindings
=============================================================================
Tkinter utiliza una arquitectura dirigida por eventos (Event-Driven).
Cualquier acción del usuario (teclado, ratón, ventana) genera un evento
que puede capturarse mediante el método:

    widget.bind(secuencia_evento, funcion_callback)

1. Secuencias de Eventos del Ratón:
   - <Button-1>: Clic izquierdo.
   - <Button-2>: Clic central (rueda).
   - <Button-3>: Clic derecho.
   - <Double-Button-1>: Doble clic izquierdo.
   - <B1-Motion>: Arrastrar manteniendo clic izquierdo.
   - <Motion>: Movimiento libre del cursor sobre el widget.
   - <Enter> / <Leave>: El cursor entra o sale del área del widget (Hover).
   - <MouseWheel>: Giro de la rueda del ratón.

2. Secuencias de Eventos del Teclado:
   - <Key>: Cualquier tecla presionada.
   - Teclas específicas: <Return>, <Escape>, <space>, <BackSpace>, <Tab>.
   - Flechas direccionales: <Up>, <Down>, <Left>, <Right>.
   - Modificadores y atajos: <Control-s>, <Control-Shift-Z>, <Alt-F4>.

3. El Objeto Event (tk.Event):
   - event.x, event.y: Coordenadas relativas al widget.
   - event.x_root, event.y_root: Coordenadas absolutas de la pantalla.
   - event.char: Carácter alfanumérico generado.
   - event.keysym: Nombre simbólico de la tecla ('Return', 'Escape', 'F5').
   - event.widget: Referencia al widget emisor del evento.
=============================================================================
"""

import tkinter as tk
from tkinter import font


def centrar_ventana(ventana: tk.Tk, ancho: int, alto: int) -> None:
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    pos_x = (pantalla_ancho // 2) - (ancho // 2)
    pos_y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")


def main() -> None:
    raiz = tk.Tk()
    raiz.title("06 - Eventos, Teclado, Ratón y Bindings")
    centrar_ventana(raiz, 760, 680)
    raiz.minsize(680, 580)
    raiz.configure(bg="#F4F6F9")

    fuente_titulo = font.Font(family="Segoe UI", size=14, weight="bold")
    fuente_subtitulo = font.Font(family="Segoe UI", size=10, weight="bold")
    fuente_normal = font.Font(family="Segoe UI", size=9)

    # Encabezado
    encabezado = tk.Frame(raiz, bg="#D35400", padx=20, pady=12)
    encabezado.pack(fill=tk.X)
    tk.Label(
        encabezado,
        text="Sistema de Eventos y Manejadores (.bind)",
        font=fuente_titulo,
        fg="#FFFFFF",
        bg="#D35400",
    ).pack()
    tk.Label(
        encabezado,
        text="Detección de pulsaciones de teclas, atajos, clics, hover y coordenadas del cursor",
        font=fuente_normal,
        fg="#FDEBD0",
        bg="#D35400",
    ).pack()

    # Contenedor central dividido en 2 columnas
    cuerpo = tk.Frame(raiz, bg="#F4F6F9", padx=15, pady=12)
    cuerpo.pack(fill=tk.BOTH, expand=True)

    col_izq = tk.Frame(cuerpo, bg="#F4F6F9")
    col_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

    col_der = tk.Frame(cuerpo, bg="#F4F6F9")
    col_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # ---------------------------------------------------------
    # 1. Zona de Pruebas del Ratón (Mouse Sandbox)
    # ---------------------------------------------------------
    grp_mouse = tk.LabelFrame(
        col_izq,
        text=" 1. Interacción con Ratón (Haz clic, mueve o haz doble clic) ",
        font=fuente_subtitulo,
        bg="#FFFFFF",
        fg="#2C3E50",
        padx=12,
        pady=10,
    )
    grp_mouse.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    area_raton = tk.Frame(grp_mouse, bg="#EAEDED", bd=2, relief=tk.SUNKEN, height=160)
    area_raton.pack(fill=tk.BOTH, expand=True)
    area_raton.pack_propagate(False)

    lbl_raton_instruccion = tk.Label(
        area_raton,
        text="Pasa el ratón aquí,\nhaz clic izquierdo, derecho o doble clic",
        font=("Segoe UI", 10),
        bg="#EAEDED",
        fg="#7F8C8D",
    )
    lbl_raton_instruccion.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # ---------------------------------------------------------
    # 2. Zona de Pruebas del Teclado (Keyboard Sandbox)
    # ---------------------------------------------------------
    grp_teclado = tk.LabelFrame(
        col_der,
        text=" 2. Interacción con Teclado (Escribe o prueba atajos) ",
        font=fuente_subtitulo,
        bg="#FFFFFF",
        fg="#2C3E50",
        padx=12,
        pady=10,
    )
    grp_teclado.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    tk.Label(
        grp_teclado,
        text="Haz clic en esta caja y presiona cualquier tecla (ej: flechas, F1-F12, Esc, Enter):",
        font=fuente_normal,
        bg="#FFFFFF",
        wraplength=300,
        justify=tk.LEFT,
    ).pack(anchor=tk.W, pady=(0, 6))

    entry_teclas = tk.Entry(
        grp_teclado,
        font=("Segoe UI", 11),
        relief=tk.SOLID,
        bd=1,
        bg="#FEF9E7",
        justify=tk.CENTER,
    )
    entry_teclas.pack(fill=tk.X, ipady=6, pady=(0, 10))
    entry_teclas.insert(0, "¡Escribe aquí!")

    lbl_atajos_info = tk.Label(
        grp_teclado,
        text="Atajos activos en esta ventana:\n• Ctrl + S -> Guardar simulado\n• Ctrl + D -> Limpiar historial de eventos\n• Escape -> Reiniciar campos",
        font=("Segoe UI", 9),
        bg="#FDEDEC",
        fg="#922B21",
        justify=tk.LEFT,
        padx=10,
        pady=8,
    )
    lbl_atajos_info.pack(fill=tk.X)

    # ---------------------------------------------------------
    # 3. Consola de Registro de Eventos (Event Inspector)
    # ---------------------------------------------------------
    grp_log = tk.LabelFrame(
        raiz,
        text=" Monitor de Inspección de Eventos (Parámetros del tk.Event) ",
        font=fuente_subtitulo,
        bg="#FFFFFF",
        fg="#2C3E50",
        padx=12,
        pady=10,
    )
    grp_log.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

    txt_log = tk.Text(
        grp_log,
        height=8,
        bg="#1C2833",
        fg="#58D68D",
        font=font.Font(family="Consolas", size=9),
        relief=tk.FLAT,
    )
    scroll_log = tk.Scrollbar(grp_log, command=txt_log.yview)
    txt_log.config(yscrollcommand=scroll_log.set)
    scroll_log.pack(side=tk.RIGHT, fill=tk.Y)
    txt_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def registrar_evento(tipo: str, detalles: str) -> None:
        txt_log.insert(tk.END, f"[{tipo:^16}] {detalles}\n")
        txt_log.see(tk.END)

    # ---------------------------------------------------------
    # BINDINGS DEL RATÓN
    # ---------------------------------------------------------
    def on_mouse_enter(e: tk.Event) -> None:
        area_raton.config(bg="#D4EFDF")
        lbl_raton_instruccion.config(bg="#D4EFDF", text="¡Cursor dentro del área! (<Enter>)")
        registrar_evento("<Enter>", f"Cursor entró al widget. Coords: (x={e.x}, y={e.y})")

    def on_mouse_leave(e: tk.Event) -> None:
        area_raton.config(bg="#EAEDED")
        lbl_raton_instruccion.config(bg="#EAEDED", text="Pasa el ratón aquí,\nhaz clic izquierdo, derecho o doble clic")
        registrar_evento("<Leave>", "Cursor salió del widget.")

    def on_click_izq(e: tk.Event) -> None:
        registrar_evento("<Button-1>", f"Clic Izquierdo en widget: (x={e.x}, y={e.y}), Pantalla: ({e.x_root}, {e.y_root})")

    def on_click_der(e: tk.Event) -> None:
        registrar_evento("<Button-3>", f"Clic Derecho en widget: (x={e.x}, y={e.y})")

    def on_doble_click(e: tk.Event) -> None:
        registrar_evento("<Double-Button-1>", f"¡Doble clic detectado! Coords: ({e.x}, {e.y})")

    def on_mouse_motion(e: tk.Event) -> None:
        # Actualizamos sutilmente sin saturar
        lbl_raton_instruccion.config(text=f"Coords: X={e.x}, Y={e.y}")

    area_raton.bind("<Enter>", on_mouse_enter)
    area_raton.bind("<Leave>", on_mouse_leave)
    area_raton.bind("<Button-1>", on_click_izq)
    area_raton.bind("<Button-3>", on_click_der)
    area_raton.bind("<Double-Button-1>", on_doble_click)
    area_raton.bind("<Motion>", on_mouse_motion)

    # ---------------------------------------------------------
    # BINDINGS DEL TECLADO
    # ---------------------------------------------------------
    def on_tecla_presionada(e: tk.Event) -> None:
        detalles = f"keysym='{e.keysym}' | char='{e.char}' | keycode={e.keycode}"
        registrar_evento("<Key>", detalles)

    entry_teclas.bind("<Key>", on_tecla_presionada)

    # ---------------------------------------------------------
    # ATAJOS GLOBALES EN LA VENTANA (Root bindings)
    # ---------------------------------------------------------
    def atajo_guardar(e: tk.Event) -> str:
        registrar_evento("<Control-s>", "¡Atajo detectado! Simulación de guardado exitosa.")
        return "break"  # Evita propagación por defecto

    def atajo_limpiar(e: tk.Event) -> str:
        txt_log.delete("1.0", tk.END)
        registrar_evento("SYSTEM", "Historial de eventos limpiado.")
        return "break"

    def atajo_escape(e: tk.Event) -> str:
        entry_teclas.delete(0, tk.END)
        entry_teclas.insert(0, "")
        registrar_evento("<Escape>", "Campo de texto reiniciado.")
        return "break"

    raiz.bind("<Control-s>", atajo_guardar)
    raiz.bind("<Control-S>", atajo_guardar)
    raiz.bind("<Control-d>", atajo_limpiar)
    raiz.bind("<Control-D>", atajo_limpiar)
    raiz.bind("<Escape>", atajo_escape)

    registrar_evento("INICIALIZACIÓN", "Sistema de eventos preparado. Prueba a interactuar.")

    raiz.mainloop()


if __name__ == "__main__":
    main()
