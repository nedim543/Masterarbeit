import pandas as pd

# Liste aller Events aus der Matrix
EVENTS = [
    "A_SUBMITTED", "A_PARTLYSUBMITTED", "A_PREACCEPTED", "W_Completeren aanvraag",
    "A_ACCEPTED", "O_SELECTED", "A_FINALIZED", "O_CREATED", "O_SENT",
    "W_Nabellen offertes", "O_SENT_BACK", "W_Valideren aanvraag", "A_REGISTERED",
    "A_APPROVED", "O_ACCEPTED", "A_ACTIVATED", "O_CANCELLED", "A_DECLINED",
    "A_CANCELLED", "W_Afhandelen leads", "O_DECLINED", "W_Nabellen incomplete dossiers",
    "W_Beoordelen fraude"
]

# Pfade zur Ein- und Ausgabedatei
CSV_PATH = "bpi.csv"
OUTPUT_PATH = "footprint_matrix.csv"

# Übergang, den wir debuggen wollen
DEBUG_FROM = "W_Afhandelen leads"
DEBUG_TO = "A_CANCELLED"

def create_footprint_matrix():
    return pd.DataFrame(0, index=EVENTS, columns=EVENTS)

def main():
    df = pd.read_csv(CSV_PATH)

    # Sortiere nach Case-ID und Startzeit
    df = df.sort_values(by=["case", "startTime"])

    matrix = create_footprint_matrix()

    previous_case = None
    previous_event = None

    for index, row in df.iterrows():
        current_case = row["case"]
        current_event = row["event"]

        if current_event not in EVENTS:
            continue

        if previous_case == current_case and previous_event != current_event:
            if previous_event in EVENTS:
                # Debug: Wenn genau der gesuchte Übergang passiert, Index drucken
                if previous_event == DEBUG_FROM and current_event == DEBUG_TO:
                    print(f"1 gefunden bei index: {index} ({previous_event} → {current_event})")

                matrix.loc[current_event, previous_event] += 1

        previous_case = current_case
        previous_event = current_event

    # Exportiere die Matrix als CSV-Datei
    matrix.to_csv(OUTPUT_PATH)
    print(f"Footprint-Matrix erfolgreich gespeichert unter: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
