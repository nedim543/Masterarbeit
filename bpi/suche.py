
import pandas as pd


#Dise File sucht bstimmte bezihungen um überpüfungen auszuführen

# Pfad zur CSV-Datei
CSV_PATH = "bpi.csv"

def main():
    df = pd.read_csv(CSV_PATH)
    previous_case = None
    previous_event = None

    for index, row in df.iterrows():
        current_case = row["case"]
        current_event = row["event"]

        if previous_case == current_case:
            if previous_event == "A_CANCELLED" and current_event == "W_Afhandelen leads":
            #if previous_event == "A_SUBMITTED" and current_event == "A_CANCELLED":
                print(f"Gefunden bei Zeile {index}: {previous_event} → {current_event} im Case {current_case}")
                return
        
        previous_case = current_case
        previous_event = current_event
    print("nichts gefunden :)")
        

if __name__ == "__main__":
    main()
