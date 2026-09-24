"""
Timeline DNS — versión limpia.
- Línea principal + relleno suave
- Línea de media global
- Eje X adaptativo
"""

import json
from collections import Counter
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

ARCHIVO = "informe.json"
RESOLUCION = "1min"          # "1s", "1min", "1h", "1D"
SALIDA = "timeline.png"

# ---------- 1. Leer en streaming ----------
def parse_ts(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))

def bucket(dt, res):
    if res.endswith("s"):   return dt.replace(microsecond=0)
    if res.endswith("min"): return dt.replace(second=0, microsecond=0)
    if res.endswith("h"):   return dt.replace(minute=0, second=0, microsecond=0)
    if res.endswith("D"):   return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return dt

contador = Counter()
with open(ARCHIVO, "r", encoding="utf-8") as f:
    for linea in f:
        linea = linea.strip()
        if not linea:
            continue
        try:
            obj = json.loads(linea)
        except json.JSONDecodeError:
            continue
        if "header" in obj or "timestamp" not in obj:
            continue
        try:
            dt = parse_ts(obj["timestamp"])
        except (ValueError, TypeError):
            continue
        contador[bucket(dt, RESOLUCION)] += 1

# ---------- 2. Serie ordenada ----------
serie = pd.Series(contador).sort_index()
serie.index = pd.to_datetime(serie.index)
media_global = serie.mean()

# ---------- 3. Gráfica ----------
fig, ax = plt.subplots(figsize=(15, 6))

ax.fill_between(serie.index, serie.values, color="steelblue", alpha=0.20)
ax.plot(serie.index, serie.values, color="steelblue",
        linewidth=1.1, label="Consultas")

ax.axhline(media_global, color="gray", linestyle="--", linewidth=1,
           label=f"Media global = {media_global:.0f}")

# ---------- 4. Estilo ----------
ax.set_title(f"Timeline de consultas DNS — resolución {RESOLUCION}",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Tiempo")
ax.set_ylabel("Consultas")

locator = mdates.AutoDateLocator()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
fig.autofmt_xdate()

ax.grid(True, linestyle=":", alpha=0.4)
ax.legend(loc="upper left", frameon=True, fontsize=9)
ax.margins(x=0.01)

plt.tight_layout()
plt.savefig(SALIDA, dpi=150)
plt.show()
print(f"Gráfica guardada en: {SALIDA}")