import tkinter as tk
from tkinter import messagebox
from logica_impresora import PrintSimulation  # Importamos la lógica

class PrintSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Cola de Impresión")
        self.root.geometry("450x500")
        
        # Lista temporal para guardar los inputs antes de simular
        self.temp_tasks = []

        self.setup_ui()

    def setup_ui(self):
        # Frame Entradas
        frame_inputs = tk.LabelFrame(self.root, text="Agregar Trabajo", padx=10, pady=10)
        frame_inputs.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_inputs, text="ID del Trabajo:").grid(row=0, column=0, sticky="w")
        self.entry_id = tk.Entry(frame_inputs)
        self.entry_id.grid(row=0, column=1)

        tk.Label(frame_inputs, text="Páginas:").grid(row=1, column=0, sticky="w")
        self.entry_pages = tk.Entry(frame_inputs)
        self.entry_pages.grid(row=1, column=1)

        tk.Label(frame_inputs, text="Tiempo de llegada (s):").grid(row=2, column=0, sticky="w")
        self.entry_arrival = tk.Entry(frame_inputs)
        self.entry_arrival.grid(row=2, column=1)

        tk.Button(frame_inputs, text="Añadir a lista", command=self.add_task).grid(row=3, column=0, columnspan=2, pady=10)

        # Frame Lista de Trabajos
        self.listbox = tk.Listbox(self.root, height=8)
        self.listbox.pack(fill="x", padx=10, pady=5)

        # Configuración de impresora
        frame_config = tk.Frame(self.root)
        frame_config.pack(fill="x", padx=10, pady=5)
        tk.Label(frame_config, text="Páginas por minuto (PPM):").pack(side="left")
        self.entry_ppm = tk.Entry(frame_config, width=10)
        self.entry_ppm.insert(0, "10")
        self.entry_ppm.pack(side="left", padx=5)

        tk.Button(self.root, text="Ejecutar Simulación", bg="green", fg="white", command=self.run_simulation).pack(pady=10)

        # Resultados
        self.lbl_results = tk.Label(self.root, text="", justify="left", font=("Helvetica", 10))
        self.lbl_results.pack(padx=10, pady=5)

    def add_task(self):
        try:
            task_id = self.entry_id.get()
            pages = int(self.entry_pages.get())
            arrival = float(self.entry_arrival.get())

            if not task_id:
                raise ValueError("El ID no puede estar vacío.")

            self.temp_tasks.append((task_id, pages, arrival))
            self.listbox.insert(tk.END, f"[{arrival}s] {task_id} - {pages} págs")
            
            # Limpiar campos
            self.entry_id.delete(0, tk.END)
            self.entry_pages.delete(0, tk.END)
            self.entry_arrival.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error de Validación", f"Datos inválidos: {e}")

    def run_simulation(self):
        try:
            ppm = int(self.entry_ppm.get())
            sim = PrintSimulation(ppm=ppm)
            
            for task_id, pages, arrival in self.temp_tasks:
                sim.add_task(task_id, pages, arrival)
                
            metrics = sim.run()
            
            avg_wait = metrics['total_wait_time'] / metrics['total_processed'] if metrics['total_processed'] > 0 else 0
            
            res_text = (
                f"--- RESULTADOS ---\n"
                f"Trabajos procesados: {metrics['total_processed']}\n"
                f"Tiempo promedio de espera: {avg_wait:.2f} segundos\n"
                f"Trabajo con mayor espera: {metrics['max_wait_task']} ({metrics['max_wait_time']:.2f}s)\n"
                f"Tamaño máximo de la cola: {metrics['max_queue_size']}"
            )
            self.lbl_results.config(text=res_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en simulación: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PrintSimulatorApp(root)
    root.mainloop()
