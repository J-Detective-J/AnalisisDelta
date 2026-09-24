# AnalisisDelta
Data set de CAIDA (no fue posible)

## 1. Timeline DNS (`timeline.py`)

### 1.1 Descripción

Genera una gráfica temporal de consultas DNS a partir de un archivo **JSON Lines** (un objeto JSON por línea). El script:

- Lee el archivo en **streaming** (no carga todo en memoria).
- Agrupa los eventos por intervalo temporal configurable.
- Dibuja una línea principal con relleno suave.
- Añade una línea de **media global** como referencia.
- Formatea el eje X de forma adaptativa al rango de fechas.

### 1.2 Estructura esperada del JSON de entrada

Cada línea debe ser un objeto JSON independiente. El script **ignora** la línea de cabecera si contiene la clave `header`.

```json
{"header":{"file":"zdns-20241110.json","filetype":"prefix-probing-ipv4-reverse-dns"}}
{"data":{"protocol":"udp","resolver":"204.61.216.50:53"},"name":"100.63.254.1","status":"NXDOMAIN","timestamp":"2024-11-10T13:50:55Z"}
{"data":{"answers":[{"answer":"one.one.one.one.","class":"IN","name":"1.0.0.1.in-addr.arpa","ttl":1800,"type":"PTR"}],"protocol":"udp","resolver":"162.159.7.226:53"},"name":"1.0.0.1","status":"NOERROR","timestamp":"2024-11-10T13:50:55Z"}
```

**Campos utilizados por el script:**

| Campo | Uso |
|---|---|
| `timestamp` | Marca temporal para el eje X (obligatorio) |
| `header` | Se usa solo para descartar la línea de cabecera |

Los demás campos (`data`, `name`, `status`, etc.) son ignorados por `timeline.py`, aunque pueden usarse para análisis adicionales.

### 1.3 Requisitos

- Python **3.8+**
- Dependencias:

```bash
pip install pandas matplotlib
```

### 1.4 Configuración

Edita las constantes al inicio del script:

```python
ARCHIVO = "informe.json"     # Nombre del archivo JSON Lines
RESOLUCION = "1min"          # "1s", "1min", "1h", "1D"
SALIDA = "timeline.png"      # Nombre de la imagen de salida
```

**Guía de resolución según tamaño del dataset:**

| Eventos totales | RESOLUCION recomendada |
|---|---|
| < 100 | `"1s"` |
| 100 – 100 000 | `"1min"` |
| 100 000 – 10 000 000 | `"1h"` |
| > 10 000 000 | `"1D"` |

### 1.5 Ejecución

```bash
python timeline.py
```

Salida esperada:

```
Gráfica guardada en: timeline.png
```

Y la imagen `timeline.png` con la línea temporal.

### 1.6 Interpretación de la gráfica

| Elemento | Significado |
|---|---|
| **Línea azul** | Número de consultas DNS por intervalo |
| **Relleno azul** | Área bajo la curva (intensidad visual) |
| **Línea gris discontinua** | Media global del período |
| **Eje X** | Tiempo con formato adaptativo |
| **Eje Y** | Cantidad de consultas por bucket |

### 1.7 Manejo de errores

El script es tolerante a fallos:

- **Líneas vacías** → ignoradas.
- **JSON malformado** → se descarta la línea.
- **Timestamp inválido o ausente** → se descarta el registro.
- **Línea de cabecera** → detectada por la clave `header` y saltada.

### 1.8 Optimizaciones para archivos grandes

- **Lectura por streaming** con `for linea in f` en vez de `json.load()`.
- **`Counter`** en lugar de listas o DataFrames para agregar.
- **Bucket temporal** aplicado antes de construir la serie, reduciendo el número de puntos a graficar.
- **`ax.margins(x=0.01)`** evita recortes visuales cuando hay miles de puntos.

### 1.9 Posibles mejoras

- Añadir filtrado por estado DNS (`NXDOMAIN`, `NOERROR`, etc.).
- Separar por resolver o por protocolo (`udp`/`tcp`).
- Comparar múltiples archivos en una misma gráfica.
- Exportar la serie agregada a CSV con `serie.to_csv()`.

---

## 2. Informe sobre la constante universal Δ (`informe_delta.md`)

### 2.1 Objetivo

El informe documenta por qué **no es posible** realizar el taller:

> *"Ir a CAIDA, escoger un dataset de la topología de Internet, analizarlo, encontrar la constante universal (Δ) y explicar para qué sirve en el diseño."*

### 2.2 Datasets evaluados

| Dataset | URL | Veredicto |
|---|---|---|
| `ooklacrawling` | https://catalog.caida.org/dataset/ooklacrawling | No es topología |
| `country-level-ip-reputation` | https://www.caida.org/archive/policy/country-level-ip-reputation/ | Estudio de reputación, página histórica |
| `ark_itdk` ✅ | https://catalog.caida.org/dataset/ark_itdk | Único dataset topológico viable |

### 2.3 Conclusión principal

El taller **no es realizable** porque:

1. **Δ no está definida** en el enunciado ni existe en la literatura de topología de Internet.
2. **`ark_itdk` no contiene un campo `delta`** ni un esquema que permita derivarlo directamente.
3. Los otros dos datasets **no son topologías**.
4. La topología de Internet es **no estacionaria y dependiente del método de medición**.
5. **Falta una definición operacional** de Δ.

### 2.4 Recomendación

Reformular el taller usando una métrica bien definida y medible, por ejemplo:

- **Exponente γ** de la ley de potencias de la distribución de grados.
- **Coeficiente de clustering medio**.
- **Diámetro / camino medio** de la red.

Comparar su estabilidad entre distintos snapshots de `ark_itdk`. Ese ejercicio sí es factible y tiene valor pedagógico.

### 2.5 Relación con `timeline.py`

`timeline.py` es una herramienta de **análisis temporal** del mismo tipo de dataset que se intentó usar para el informe. Aunque no sirve para encontrar Δ, sí permite:

- Visualizar la actividad de mediciones a lo largo del tiempo.
- Detectar pausas, ráfagas o caídas en la captura.
- Verificar la estabilidad temporal del conjunto de datos antes de cualquier análisis estructural.

---

## 3. Cómo reproducir todo

### 3.1 Clonar / descargar

```bash
git clone <url-del-repo>
cd <repo>
```

### 3.2 Instalar dependencias

```bash
pip install pandas matplotlib
```

### 3.3 Colocar el dataset

Asegúrate de que `informe.json` esté en la raíz del proyecto.

### 3.4 Ejecutar el script

```bash
python timeline.py
```

### 3.5 Leer el informe

Abre `informe_delta.md` en cualquier visor Markdown (VS Code, GitHub, Obsidian, etc.).

---

## 4. Notas técnicas

### 4.1 ¿Por qué JSON Lines y no un JSON array?

- **JSON Lines** permite leer línea por línea sin cargar todo en memoria.
- Es el formato estándar de salida de herramientas como `zdns` (ZMap DNS).
- Facilita procesar archivos de varios GB con RAM limitada.

### 4.2 ¿Por qué `Counter` y no `pandas` durante la lectura?

- `Counter` es **mucho más rápido** y ligero para incrementar contadores.
- `pandas` se usa **solo al final**, una vez agregados los datos, para aprovechar su manejo de series temporales.

### 4.3 ¿Por qué `mdates.AutoDateLocator`?

- El rango temporal puede ir de segundos a meses.
- `AutoDateLocator` ajusta automáticamente la densidad de ticks del eje X.
- `ConciseDateFormatter` produce etiquetas cortas y legibles.

---

## 5. Referencias

- CAIDA. *Ookla Speedtest Server Metadata.* https://catalog.caida.org/dataset/ooklacrawling
- CAIDA. *Correlation between country governance regimes and the reputation of their Internet (IP) address allocations.* https://www.caida.org/archive/policy/country-level-ip-reputation/
- CAIDA. *ITDK: Internet Topology Data Kit.* https://catalog.caida.org/dataset/ark_itdk
- Faloutsos, M., Faloutsos, P., Faloutsos, C. *On Power-Law Relationships of the Internet Topology.* SIGCOMM 1999.
- Pastor-Satorras, R., Vespignani, A. *Evolution and Structure of the Internet: A Statistical Physics Approach.* Cambridge University Press, 2004.
- Matplotlib. *Date tick locators and formatters.* https://matplotlib.org/stable/api/dates_api.html

---
