"""
=============================================================================
03 - Controles de Selección e Interacción Avanzados
=============================================================================
Este módulo enseña los controles de formulario interactivos más utilizados:

1. Checkbutton:
   - Casillas de verificación para opciones booleanas independientes.
   - Vinculado a BooleanVar o IntVar.

2. Radiobutton:
   - Botones de selección excluyente (solo uno activo a la vez).
   - Todos los botones del mismo grupo comparten la misma variable de control.

3. Scale:
   - Deslizador de rango numérico (ej. volumen, porcentaje, brillo).
   - Permite configurar orientación (HORIZONTAL / VERTICAL), rango (from_, to),
     y resolución (resolution).

4. Spinbox:
   - Selector numérico con botones de incremento/decremento o listas de valores.

5. Listbox y Scrollbar:
   - Lista deslizable de elementos con modos de selección (SINGLE, MULTIPLE, EXTENDED).
   - Métodos esenciales: insert(), delete(), curselection(), get().

Incluye un panel de resumen en tiempo real que refleja el estado de todos los controles.
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
    raiz.title("03 - Controles de Selección e Interacción")
    centrar_ventana(raiz, 750, 680)
    raiz.minsize(680, 600)
    raiz.configure(bg="#F4F6F9")

    fuente_titulo = font.Font(family="Segoe UI", size=14, weight="bold")
    fuente_subtitulo = font.Font(family="Segoe UI", size=10, weight="bold")
    fuente_normal = font.Font(family="Segoe UI", size=9)

    # Encabezado
    encabezado = tk.Frame(raiz, bg="#16A085", padx=20, pady=12)
    encabezado.pack(fill=tk.X)
    tk.Label(
        encabezado,
        text="Controles de Selección y Entrada en Tkinter",
        font=fuente_titulo,
        fg="#FFFFFF",
        bg="#16A085",
    ).pack()
    tk.Label(
        encabezado,
        text="Checkbuttons, Radiobuttons, Scales, Spinboxes y Listboxes interactivos",
        font=fuente_normal,
        fg="#E8F8F5",
        bg="#16A085",
    ).pack()

    # Contenedor principal de dos columnas
    panel_principal = tk.Frame(raiz, bg="#F4F6F9", padx=15, pady=15)
    panel_principal.pack(fill=tk.BOTH, expand=True)

    columna_izq = tk.Frame(panel_principal, bg="#F4F6F9")
    columna_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

    columna_der = tk.Frame(panel_principal, bg="#F4F6F9")
    columna_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # ---------------------------------------------------------
    # 1. Checkbuttons (Opciones múltiples independientes)
    # ---------------------------------------------------------
    grp_checks = tk.LabelFrame(
        columna_izq,
        text=" 1. Checkbuttons (Preferencias) ",
        font=fuente_subtitulo,
        bg="#FFFFFF",
        fg="#2C3E50",
        padx=12,
        pady=8,
    )
    grp_checks.pack(fill=tk.X, pady=(0, 10))

    var_notif = tk.BooleanVar(value=True)
    var_dark = tk.BooleanVar(value=False)
    var_backup = tk.BooleanVar(value=True)

    chk1 = tk.Checkbutton(
        grp_checks,
        text="Recibir notificaciones por correo",
        variable=var_notif,
        font=fuente_normal,
        bg="#FFFFFF",
        activebackground="#FFFFFF",
        command=lambda: actualizar_resumen(),
    )
    chk1.pack(anchor=tk.W, pady=2)

    chk2 = tk.Checkbutton(
        grp_checks,
        text="Activar modo oscuro preliminar",
        variable=var_dark,
        font=fuente_normal,
        bg="#FFFFFF",
        activebackground="#FFFFFF",
        command=lambda: actualizar_resumen(),
    )
    chk2.pack(anchor=tk.W, pady=2)

    chk3 = tk.Checkbutton(
        grp_checks,
        text="Copia de seguridad automática",
        variable=var_backup,
        font=fuente_normal,
        bg="#FFFFFF",
        activebackground="#FFFFFF",
        command=lambda: actualizar_resumen(),
    )
    chk3.pack(anchor=tk.W, pady=2)

    # ---------------------------------------------------------
    # 2. Radiobuttons (Selección mutuamente excluyente)
    # ---------------------------------------------------------
    grp_radios = tk.LabelFrame(
        columna_izq,
        text=" 2. Radiobuttons (Plan de Suscripción) ",
        font=fuente_subtitulo,
        bg="#FFFFFF",
        fg="#2C3E50",
        padx=12,
        pady=8,
    )
    grp_radios.pack(fill=tk.X, pady=(0, 10))

    var_plan = tk.StringVar(value="Pro")

    for plan in ["Gratuito (Free)", "Pro ($9.99/mes)", "Empresarial (Custom)"]:
        nombre_clave = plan.split()[0]
        rb = tk.Radiobutton(
            grp_radios,
            text=plan,
            value=nombre_clave,
            variable=var_plan,
            font=fuente_normal,
            bg="#FFFFFF",
            activebackground="#FFFFFF",
            command=lambda: actualizar_resumen(),
        )
        rb.pack(anchor=tk.W, pady=2)

    # ---------------------------------------------------------
    # 3. Scale y Spinbox
    # ---------------------------------------------------------
    grp_rango = tk.LabelFrame(
        columna_izq,
        text=" 3. Scale y Spinbox ",
        font=fuente_subtitulo,
        bg="#FFFFFF",
        fg="#2C3E50",
        padx=12,
        pady=8,
    )
    grp_rango.pack(fill=tk.X)

    tk.Label(grp_rango, text="Volumen del Sistema (Scale):", font=fuente_normal, bg="#FFFFFF").pack(anchor=tk.W)
    scale_volumen = tk.Scale(
        grp_rango,
        from_=0,
        to=100,
        orient=tk.HORIZONTAL,
        bg="#FFFFFF",
        highlightthickness=0,
        troughcolor="#EAEDED",
        activebackground="#16A085",
        command=lambda val: actualizar_resumen(),
    )
    scale_volumen.set(70)
    scale_volumen.pack(fill=tk.X, pady=(0, 8))

    tk.Label(grp_rango, text="Número de licencias (Spinbox):", font=fuente_normal, bg="#FFFFFF").pack(anchor=tk.W)
    var_spin = tk.IntVar(value=3)
    spin_licencias = tk.Spinbox(
        grp_rango,
        from_=1,
        to=50,
        textvariable=var_spin,
        font=fuente_normal,
        width=10,
        command=lambda: actualizar_resumen(),
    )
    spin_licencias.pack(anchor=tk.W, pady=(2, 6))

    # ---------------------------------------------------------
    # 4. Listbox con Scrollbar
    # ---------------------------------------------------------
    grp_listbox = tk.LabelFrame(
        columna_der,
        text=" 4. Listbox con Scrollbar ",
        font=fuente_subtitulo,
        bg="#FFFFFF",
        fg="#2C3E50",
        padx=12,
        pady=8,
    )
    grp_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    frame_list = tk.Frame(grp_listbox, bg="#FFFFFF")
    frame_list.pack(fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame_list, orient=tk.VERTICAL)
    listbox = tk.Listbox(
        frame_list,
        yscrollcommand=scrollbar.set,
        selectmode=tk.BROWSE,
        font=fuente_normal,
        relief=tk.SOLID,
        bd=1,
    )
    scrollbar.config(command=listbox.yview)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    elementos_iniciales = [
        "Python (Core)", "Tkinter (GUI)", "NumPy (Cálculo)",
        "Pandas (Datos)", "Matplotlib (Gráficos)", "Django (Web)",
        "FastAPI (APIs)", "Pytest (Testing)", "Requests (HTTP)",
        "SQLAlchemy (ORM)", "Scikit-Learn (ML)"
    ]
    for item in elementos_iniciales:
        listbox.insert(tk.END, item)
    listbox.select_set(0)

    # Entradas para agregar o quitar elementos de la lista
    frame_controles_list = tk.Frame(grp_listbox, bg="#FFFFFF")
    frame_controles_list.pack(fill=tk.X, pady=(6, 0))

    entry_nuevo_item = tk.Entry(frame_controles_list, font=fuente_normal, relief=tk.SOLID, bd=1)
    entry_nuevo_item.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6), ipady=2)

    def agregar_item() -> None:
        texto = entry_nuevo_item.get().strip()
        if texto:
            listbox.insert(tk.END, texto)
            entry_nuevo_item.delete(0, tk.END)
            actualizar_resumen()

    def eliminar_item() -> None:
        seleccion = listbox.curselection()
        if seleccion:
            listbox.delete(seleccion[0])
            actualizar_resumen()

    btn_add = tk.Button(
        frame_controles_list, text="+ Agregar", font=fuente_normal, bg="#27AE60", fg="white",
        relief=tk.FLAT, padx=8, command=agregar_item, cursor="hand2"
    )
    btn_add.pack(side=tk.LEFT, padx=(0, 4))

    btn_del = tk.Button(
        frame_controles_list, text="- Quitar", font=fuente_normal, bg="#E74C3C", fg="white",
        relief=tk.FLAT, padx=8, command=eliminar_item, cursor="hand2"
    )
    btn_del.pack(side=tk.LEFT)

    listbox.bind("<<ListboxSelect>>", lambda e: actualizar_resumen())

    # ---------------------------------------------------------
    # 5. Panel de Resumen en Tiempo Real
    # ---------------------------------------------------------
    grp_resumen = tk.LabelFrame(
        columna_der,
        text=" Resumen de Estado en Vivo ",
        font=fuente_subtitulo,
        bg="#EBF5FB",
        fg="#1F618D",
        padx=12,
        pady=8,
    )
    grp_resumen.pack(fill=tk.BOTH, expand=True)

    lbl_resumen = tk.Label(
        grp_resumen,
        text="",
        font=font.Font(family="Consolas", size=9),
        bg="#EBF5FB",
        fg="#154360",
        justify=tk.LEFT,
        anchor=tk.NW,
    )
    lbl_resumen.pack(fill=tk.BOTH, expand=True)

    def actualizar_resumen() -> None:
        sel_idx = listbox.curselection()
        item_sel = listbox.get(sel_idx[0]) if sel_idx else "Ninguno seleccionado"

        texto = (
            f"Notificaciones : {'Activadas' if var_notif.get() else 'Desactivadas'}\n"
            f"Modo Oscuro    : {'Sí' if var_dark.get() else 'No'}\n"
            f"Backup Auto    : {'Sí' if var_backup.get() else 'No'}\n"
            f"Plan Elegido   : {var_plan.get()}\n"
            f"Nivel Volumen  : {scale_volumen.get()}%\n"
            f"Licencias      : {var_spin.get()}\n"
            f"Librería Sel.  : {item_sel}\n"
            f"Total Lista    : {listbox.size()} elementos"
        )
        lbl_resumen.config(text=texto)

    # Inicializar resumen
    actualizar_resumen()

    raiz.mainloop()


if __name__ == "__main__":
    main()
