# -S10-Queque---Print-Queue-Simulation
# 🖨 Simulación de Cola de Impresión

Simulación de una cola de impresión en Python, aplicando la estructura de datos **Queue** para modelar cómo distintos trabajos llegan, esperan turno y son procesados por una impresora.

---

## 📁 Estructura del Proyecto

```
print_queue_sim/
├── app.py                  # Interfaz gráfica (Tkinter) — punto de entrada
├── src/
│   ├── __init__.py
│   ├── queue_ds.py         # Clase Queue (implementación propia FIFO)
│   ├── models.py           # Clases PrintTask y Printer
│   └── simulation.py       # Motor de simulación + generate_random_tasks
├── tests/
│   ├── __init__.py
│   └── test_simulation.py  # Pruebas unitarias e integración
└── README.md
```

---

## 🚀 Instalación y Ejecución

### Requisitos
- Python 3.10 o superior
- `tkinter` incluido con Python estándar (no requiere instalación adicional)

### Verificar instalación
```bash
python --version        # debe ser 3.10+
python -c "import tkinter; print('Tkinter OK')"
```

### Ejecutar la interfaz gráfica
```bash
cd print_queue_sim
python app.py
```

### Ejecutar las pruebas
```bash
# Con pytest (recomendado)
pip install pytest
pytest tests/test_simulation.py -v

# Sin pytest
python tests/test_simulation.py
```

---

## 🏗 Clases Implementadas

### `Queue` (`src/queue_ds.py`)
Estructura de datos FIFO implementada desde cero.

| Método | Descripción |
|--------|-------------|
| `enqueue(item)` | Agrega al final de la cola |
| `dequeue()` | Extrae del frente (lanza `QueueEmptyError` si vacía) |
| `peek()` | Consulta el frente sin extraer |
| `is_empty()` | `True` si la cola está vacía |
| `size()` | Cantidad de elementos |
| `clear()` | Vacía la cola |
| `to_list()` | Copia en orden FIFO |
| `max_size_reached` | Pico histórico de tamaño |

### `PrintTask` (`src/models.py`)
Representa un trabajo de impresión.

- `job_id` — identificador único
- `pages` — cantidad de páginas
- `arrival_time` — segundo de llegada
- `start_time` / `end_time` — marcas de tiempo
- `wait_time` — propiedad calculada: `start_time - arrival_time`

### `Printer` (`src/models.py`)
Gestiona el procesamiento de trabajos.

- `start_job(task, clock)` — comienza a imprimir un trabajo
- `tick(clock)` — avanza 1 segundo; retorna el trabajo al completar
- `is_busy()` — `True` si está procesando

### `Simulation` (`src/simulation.py`)
Orquesta toda la simulación.

- `run()` — ejecuta completa y retorna métricas
- `prepare()` / `step()` — modo paso a paso (para animación)
- `get_metrics()` — retorna `SimulationMetrics`

---

## 📊 Métricas Reportadas

| Métrica | Descripción |
|---------|-------------|
| Total de trabajos procesados | Cantidad completada |
| Tiempo promedio de espera | `sum(wait) / total_jobs` |
| Trabajo con mayor espera | ID + tiempo |
| Tamaño máximo de la cola | Pico histórico |
| Utilización de la impresora | `busy_time / total_time × 100%` |
| Tiempo total de simulación | Duración del ciclo |

---

## 🖥 Interfaz Gráfica

La GUI está organizada en **tres paneles**:

1. **Configuración** — velocidad de impresora, velocidad de animación, modo manual/aleatorio, lista de trabajos
2. **Cola en vivo** — estado de la impresora con barra de progreso, cola visual animada, log de eventos
3. **Métricas** — tarjetas en tiempo real + tabla de trabajos completados

---

## ✅ Validaciones

- Simulación sin trabajos: muestra métricas en cero sin errores
- Páginas ≤ 0 o no numéricas: lanza `ValueError`
- Llegada negativa: lanza `ValueError`
- ID vacío: lanza `ValueError`
- IDs duplicados: se renombran automáticamente
- Velocidad impresora ≤ 0: se fuerza a 1 pág/min
- `dequeue()` en cola vacía: lanza `QueueEmptyError`

---

## 🧪 Pruebas

El archivo `tests/test_simulation.py` incluye **30+ pruebas** distribuidas en 5 clases:

| Clase de prueba | Qué valida |
|-----------------|------------|
| `TestQueue` | FIFO, tamaño, peek, max_size, clear, to_list |
| `TestPrintTask` | Creación, validaciones, wait_time, is_done |
| `TestPrinter` | Estado, start_job, tick, reset, ppm inválido |
| `TestSimulation` | Flujo completo, FIFO, métricas, step a paso |
| `TestGenerateRandomTasks` | Cantidad, reproducibilidad, rangos, orden |

---

## 📝 Licencia

Proyecto académico — uso educativo.
