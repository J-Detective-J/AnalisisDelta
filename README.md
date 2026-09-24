# Integrantes
- Juan Pablo Beltrán Santana
- Santiago Alejandro Céspedes Daza
- Jhonatan David Valdés González

# Timeline DNS

Script en Python que genera una gráfica temporal de consultas DNS a partir de un archivo **JSON Lines** (un objeto JSON por línea).

## Requisitos

- Python 3.8+
- Dependencias:

```bash
pip install pandas matplotlib
```

## Uso

1. Coloca tu archivo JSON Lines en la raíz del proyecto y renómbralo a `informe.json` (o edita `ARCHIVO` en `timeline.py`).
2. Ejecuta:

```bash
python timeline.py
```

3. Se generará `timeline.png` con la línea temporal de consultas.

## Formato de entrada

Cada línea debe ser un objeto JSON independiente. La línea de cabecera (`{"header": ...}`) se ignora automáticamente.

```json
{"header":{"file":"zdns-20241110.json","filetype":"prefix-probing-ipv4-reverse-dns"}}
{"data":{"protocol":"udp","resolver":"204.61.216.50:53"},"name":"100.63.254.1","status":"NXDOMAIN","timestamp":"2024-11-10T13:50:55Z"}
```

Campo obligatorio: `timestamp`.

## Configuración

Edita las constantes al inicio de `timeline.py`:

```python
ARCHIVO    = "informe.json"   # archivo de entrada
RESOLUCION = "1min"           # "1s", "1min", "1h", "1D"
SALIDA     = "timeline.png"   # imagen de salida
```

Guía rápida de `RESOLUCION` según el tamaño del dataset:

| Eventos | RESOLUCION |
|---|---|
| < 100 | `"1s"` |
| 100 – 100 000 | `"1min"` |
| 100 000 – 10 000 000 | `"1h"` |
| > 10 000 000 | `"1D"` |

## Salida

`timeline.png` con:

- Línea azul: consultas por intervalo.
- Relleno azul: área bajo la curva.
- Línea gris discontinua: media global del período.

## Notas

- Lectura en **streaming**: no carga todo el archivo en memoria.
- Tolerante a líneas vacías, JSON malformado o `timestamp` inválido.
- Pensado para datasets grandes (millones de líneas).

## Referencias

- [CAIDA ITDK](https://catalog.caida.org/dataset/ark_itdk)
- [CAIDA Ookla Speedtest Server Metadata](https://catalog.caida.org/dataset/ooklacrawling)
- [CAIDA Country-level IP Reputation](https://www.caida.org/archive/policy/country-level-ip-reputation/)
