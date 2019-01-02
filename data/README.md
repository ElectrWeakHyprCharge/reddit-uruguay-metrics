`generate.py` amalgama las distintas fuentes de información (redditmetrics, archive.org, etc) creando dos archivos:

- `data.csv`: el que contiene los valores numéricos de Subscriptores, Posts y Comentarios para una Fecha dada
- `sources.js`: el que contiene las fuentes de los valores previamente mencionados, `sources[n]` se corresponde con los valores de la enésima fila de `data.csv`
