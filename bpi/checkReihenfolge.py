import pandas as pd

# CSV-Datei einlesen
df = pd.read_csv("bpi_all.csv")

# 'case' sicher als numerischen Wert laden
df["case"] = pd.to_numeric(df["case"], errors="coerce")

# Initialisierung
previous_case = None
unsorted_rows = []

# Schleife über Zeilen
for index, row in df.iterrows():
    current_case = row["case"]
    if previous_case is not None:
        if previous_case > current_case:
            unsorted_rows.append((index, previous_case, current_case))
    previous_case = current_case

# Ergebnis anzeigen
if unsorted_rows:
    print("❌ Unsortierte case-IDs gefunden:")
    for idx, prev, curr in unsorted_rows:
        print(f"Zeile {idx}: {prev} > {curr}")
else:
    print("✅ Die 'case'-Spalte ist korrekt (nicht absteigend) sortiert.")
