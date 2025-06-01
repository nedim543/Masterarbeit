import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.exporter.xes import exporter as xes_exporter

# Pfade
CSV_PATH = "bpi_ohne_A_FINALIZED.csv"
XES_OUTPUT_PATH = "bpi_ohne_A_FINALIZED.xes"

def main():
    # CSV einlesen
    df = pd.read_csv(CSV_PATH)

    # Spalten umbenennen für PM4Py
    df.rename(columns={
        "case": "case:concept:name",
        "event": "concept:name",
        "startTime": "time:timestamp"
    }, inplace=True)

    # Zeitstempel konvertieren
    df["time:timestamp"] = pd.to_datetime(df["time:timestamp"], format="%Y/%m/%d %H:%M:%S.%f")

    # Vorbereitung für PM4Py
    df = dataframe_utils.convert_timestamp_columns_in_df(df)

    # In Event Log umwandeln
    event_log = log_converter.apply(df, variant=log_converter.Variants.TO_EVENT_LOG)

    # Exportieren als XES
    xes_exporter.apply(event_log, XES_OUTPUT_PATH)
    print(f"✅ XES-Datei gespeichert unter: {XES_OUTPUT_PATH}")

if __name__ == "__main__":
    main()
