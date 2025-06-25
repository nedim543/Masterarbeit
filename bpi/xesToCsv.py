import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as log_converter

# Dateipfad zur XES-Datei
XES_PATH = "bpi_ohne_W_Completer.xes"

# Zielpfad für CSV-Datei
CSV_PATH = "bpi_ohne_W_Completer.csv"

# 1. XES-Datei einlesen
log = xes_importer.apply(XES_PATH)

# 2. In pandas DataFrame konvertieren
df = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
df.rename(columns={
    "case:concept:name": "case",
    "concept:name": "event",
    "time:timestamp": "startTime"
}, inplace=True)

# 3. DataFrame als CSV speichern
df.to_csv(CSV_PATH, index=False)

print(f"Konvertierung abgeschlossen. CSV gespeichert unter: {CSV_PATH}")
