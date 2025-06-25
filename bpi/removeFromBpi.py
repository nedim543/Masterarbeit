import pandas as pd

# Pfade zur Ein- und Ausgabedatei
INPUT_PATH = "bpi_all.csv"
OUTPUT_PATH = "W_Completeren_aanvraag.csv"

def main():
    # CSV-Datei einlesen
    df = pd.read_csv(INPUT_PATH)

    # Alle Zeilen mit event == "A_PREACCEPTED" herausfiltern
    df_filtered = df[df["event"] != "W_Completeren aanvraag"]

    # Gefilterte CSV speichern
    df_filtered.to_csv(OUTPUT_PATH, index=False)

    print(f"Datei erfolgreich gespeichert unter: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
