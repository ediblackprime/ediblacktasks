import tkinter as tk
from tkinter import ttk

class AplicacionTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Tareas")
        self.root.geometry("550x500")
        self.root.configure(bg="#f4f6f9")

        self.filas = [] # Lista para rastrear los widgets de cada tarea

        # Mapa de colores para el porcentaje completado (del 10% al 100%)
        # Va progresando desde tonos amarillos hasta un verde suave óptimo para lectura
        self.colores_progreso = {
            "10%": "#fffde7",  # Amarillo muy claro
            "20%": "#fff9c4",  # Amarillo pastel claro
            "30%": "#fff59d",  # Amarillo pastel
            "40%": "#fff176",  # Amarillo brillante
            "50%": "#ffee58",  # Amarillo sólido
            "60%": "#d4e157",  # Verde lima claro
            "70%": "#c6ff00",  # Lima brillante
            "80%": "#a5d6a7",  # Verde claro pastel
            "90%": "#81c784",  # Verde medio
            "100%": "#a8e6cf"  # Verde menta / Completado exitoso
        }

        # --- ENCABEZADO ---
        self.lbl_nombre = tk.Label(root, text="TASKS", font=("Arial", 14, "bold"), bg="#f4f6f9", fg="#333333")
        self.lbl_nombre.grid(row=0, column=0, padx=15, pady=15, sticky="w")

        # --- BOTONES DE CONTROL ---
        self.btn_nuevo = tk.Button(root, text="+ Nuevo", command=self.agregar_fila, relief="flat", fg="#1a73e8", font=("Arial", 10, "bold"), bg="#f4f6f9", activebackground="#e8f0fe")
        self.btn_nuevo.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="w")

        self.btn_borrar = tk.Button(root, text="Borrar todo", command=self.borrar_todo, relief="flat", fg="#d93025", font=("Arial", 10, "bold"), bg="#f4f6f9", activebackground="#fce8e6")
        self.btn_borrar.grid(row=1, column=2, padx=15, pady=(0, 10), sticky="e")

        # --- TABLA (ENCABEZADOS) ---
        headers = ["Task", "Prior", "Completed"]
        
        # Frame contenedor para asegurar la perfecta alineación de los encabezados fijos
        self.header_frame = tk.Frame(root, bg="#f4f6f9")
        self.header_frame.grid(row=2, column=0, columnspan=3, padx=15, sticky="ew")
        
        # Espacio invisible para alinear correctamente con el botón "+" de las filas dinámicas
        lbl_spacer = tk.Label(self.header_frame, text="", width=3, bg="#f4f6f9")
        lbl_spacer.grid(row=0, column=0)

        for i, header in enumerate(headers):
            lbl = tk.Label(self.header_frame, text=header, borderwidth=1, relief="solid", font=("Arial", 10, "bold"), width=16, bg="#ffffff", fg="#000000")
            lbl.grid(row=0, column=i+1, sticky="nsew")

        # Contenedor para las filas dinámicas
        self.container = tk.Frame(root, bg="#f4f6f9")
        self.container.grid(row=3, column=0, columnspan=3, padx=15, pady=5, sticky="nw")
        
        # Opciones numéricas para el ComboBox de porcentaje
        self.opciones_porcentaje = [f"{i}%" for i in range(10, 110, 10)]

        # Configurar el motor de temas para permitir cambiar el fondo de los Combobox integrados
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Agregar la primera fila por defecto
        self.agregar_fila()

    def agregar_fila(self):
        row_idx = len(self.filas)
        
        # Botón "+" a la izquierda de la fila dinámica
        btn_add = tk.Button(self.container, text="+", command=self.agregar_fila, width=2, relief="groove", bd=1)
        btn_add.grid(row=row_idx, column=0, padx=(0, 5), pady=2)

        # Entrada para la Tarea (Task)
        ent_task = tk.Entry(self.container, width=19, highlightthickness=1, highlightbackground="#cccccc")
        ent_task.grid(row=row_idx, column=1, pady=2)

        # Entrada para la Prioridad (Prior)
        ent_prior = tk.Entry(self.container, width=19, highlightthickness=1, highlightbackground="#cccccc")
        ent_prior.grid(row=row_idx, column=2, pady=2)

        # Dropdown para el porcentaje (Completed)
        cmb_comp = ttk.Combobox(self.container, values=self.opciones_porcentaje, width=16, state="readonly")
        cmb_comp.grid(row=row_idx, column=3, pady=2, padx=(1, 0))
        
        # Valor por defecto inicializado en 10%
        cmb_comp.set("10%")
        
        # Asignar color correspondiente a su ID único de widget
        self.cambiar_color_porcentaje(cmb_comp)

        # Enlazar la selección del dropdown para que cambie de color en tiempo real
        cmb_comp.bind("<<ComboboxSelected>>", lambda event, c=cmb_comp: self.cambiar_color_porcentaje(c))

        self.filas.append({
            "btn": btn_add,
            "task": ent_task,
            "prior": ent_prior,
            "comp": cmb_comp
        })

    def cambiar_color_porcentaje(self, combo):
        seleccion = combo.get()
        color = self.colores_progreso.get(seleccion, "#ffffff")
        
        # Generar un sub-estilo dinámico único para este Combobox específico usando su ID de memoria interna (winfo_id)
        # Esto evita que cambiar el color de una celda altere o pinte las demás celdas de la tabla.
        style_name = f"Color.{combo.winfo_id()}.TCombobox"
        self.style.configure(style_name, fieldbackground=color, background=color)
        combo.config(style=style_name)

    def borrar_todo(self):
        # Limpieza y destrucción de todos los objetos en pantalla
        for fila in self.filas:
            fila["btn"].destroy()
            fila["task"].destroy()
            fila["prior"].destroy()
            fila["comp"].destroy()
        
        self.filas = []
        self.agregar_fila() # Reestablecer fila limpia de inicio

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionTareasMarcela(root)
    root.mainloop()
