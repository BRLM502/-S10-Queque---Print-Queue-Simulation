class Queue:
    """Implementación de una Cola básica (FIFO)."""
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Desencolando de una cola vacía")
        return self.items.pop(0)

    def peek(self):
        if self.is_empty():
            return None
        return self.items[0]

    def size(self):
        return len(self.items)

class PrintTask:
    """Representa un trabajo de impresión individual."""
    def __init__(self, task_id, pages, arrival_time):
        if pages <= 0:
            raise ValueError("La cantidad de páginas debe ser mayor a 0.")
        if arrival_time < 0:
            raise ValueError("El tiempo de llegada no puede ser negativo.")
            
        self.task_id = task_id
        self.pages = pages
        self.arrival_time = arrival_time

class Printer:
    """Representa la impresora que procesa los trabajos."""
    def __init__(self, pages_per_minute):
        if pages_per_minute <= 0:
            raise ValueError("Las páginas por minuto deben ser mayores a 0.")
        self.ppm = pages_per_minute
        self.current_task = None
        self.time_finished = 0

    def is_busy(self):
        return self.current_task is not None

    def start_job(self, task, current_time):
        """Inicia un trabajo y calcula cuándo terminará."""
        self.current_task = task
        # Calcula el tiempo en segundos (páginas / ppm) * 60
        print_time_seconds = (task.pages / self.ppm) * 60
        self.time_finished = current_time + print_time_seconds

    def finish_job(self):
        """Libera la impresora."""
        self.current_task = None

class PrintSimulation:
    """Motor principal de la simulación."""
    def __init__(self, ppm=10):
        self.printer = Printer(ppm)
        self.print_queue = Queue()
        self.tasks_to_arrive = [] 
        
        # Métricas
        self.metrics = {
            "total_processed": 0,
            "total_wait_time": 0.0,
            "max_wait_time": 0.0,
            "max_wait_task": "N/A",
            "max_queue_size": 0
        }

    def add_task(self, task_id, pages, arrival_time):
        """Añade un trabajo a la lista de futuras llegadas."""
        task = PrintTask(task_id, pages, arrival_time)
        self.tasks_to_arrive.append(task)

    def run(self):
        """Ejecuta la simulación basada en eventos."""
        if not self.tasks_to_arrive:
            return self.metrics # Simulación sin trabajos

        # Ordenar por tiempo de llegada por si se ingresaron desordenados
        self.tasks_to_arrive.sort(key=lambda t: t.arrival_time)
        
        # Usar una Queue secundaria para manejar las llegadas
        arrival_queue = Queue()
        for t in self.tasks_to_arrive:
            arrival_queue.enqueue(t)

        current_time = 0.0

        # La simulación corre mientras haya trabajos por llegar, en la cola principal o en la impresora
        while not arrival_queue.is_empty() or not self.print_queue.is_empty() or self.printer.is_busy():
            
            # 1. Ingresar trabajos a la cola de la impresora si ya es su hora de llegada
            while not arrival_queue.is_empty() and arrival_queue.peek().arrival_time <= current_time:
                arriving_task = arrival_queue.dequeue()
                self.print_queue.enqueue(arriving_task)
                
                # Actualizar tamaño máximo de la cola
                if self.print_queue.size() > self.metrics["max_queue_size"]:
                    self.metrics["max_queue_size"] = self.print_queue.size()

            # 2. Si la impresora está libre y hay trabajos en la cola, empezar a imprimir
            if not self.printer.is_busy() and not self.print_queue.is_empty():
                next_task = self.print_queue.dequeue()
                wait_time = current_time - next_task.arrival_time
                
                # Actualizar métricas de espera
                self.metrics["total_processed"] += 1
                self.metrics["total_wait_time"] += wait_time
                if wait_time >= self.metrics["max_wait_time"]:
                    self.metrics["max_wait_time"] = wait_time
                    self.metrics["max_wait_task"] = next_task.task_id
                    
                self.printer.start_job(next_task, current_time)

            # 3. Avanzar el tiempo hacia el próximo evento (llegada de trabajo o fin de impresión)
            next_arrival_time = arrival_queue.peek().arrival_time if not arrival_queue.is_empty() else float('inf')
            next_finish_time = self.printer.time_finished if self.printer.is_busy() else float('inf')
            
            next_event_time = min(next_arrival_time, next_finish_time)
            
            if next_event_time == float('inf'):
                break # Evitar bucles infinitos si hay un error de lógica
                
            # Si el siguiente evento es que la impresora termina, liberarla
            if self.printer.is_busy() and self.printer.time_finished == next_event_time:
                self.printer.finish_job()
                
            current_time = next_event_time

        return self.metrics
