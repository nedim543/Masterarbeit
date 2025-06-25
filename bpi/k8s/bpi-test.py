import requests
import pandas as pd
from datetime import datetime
import time

# Pfad zur CSV-Datei
CSV_PATH = "test.csv"

# Eventnamen in RFC1123-kompatibles Format umwandeln
def sanitize_event_name(name):
    return name.lower().replace("_", "-").replace(" ", "-")

# Feste Port-Zuweisung gemäß services.yaml
event_port_map = {
    "a-submitted": 30030,
    "a-partlysubmitted": 30031,
    "a-preaccepted": 30032,
    "w-completeren-aanvraag": 30033,
    "a-accepted": 30034,
    "o-selected": 30035,
    "a-finalized": 30036,
    "o-created": 30037,
    "o-sent": 30038,
    "w-nabellen-offertes": 30039,
    "o-sent-back": 30040,
    "w-valideren-aanvraag": 30041,
    "a-registered": 30042,
    "a-approved": 30043,
    "o-accepted": 30044,
    "a-activated": 30045,
    "o-cancelled": 30046,
    "a-declined": 30047,
    "a-cancelled": 30048,
    "w-afhandelen-leads": 30049,
    "o-declined": 30050,
    "w-nabellen-incomplete-dossiers": 30051,
    "w-beoordelen-fraude": 30052
}

event_for_test = {
    "a-submitted": 30030,
    "a-partlysubmitted": 30031,
    "a-preaccepted": 30032
}

def get_node_ip(event):
    node = sanitize_event_name(event)
    port = event_port_map.get(node)
    return f"192.168.49.2:{port}" if port else None

def send_event(ip, timestamp, caseid, node):
    url = f"http://{ip}/event"
    data = {
        "timestamp": timestamp,
        "activity": "Start Production",  # Optional
        "caseid": f"case_{caseid}",
        "node": node
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"✅ Erfolgreich gesendet an {node} ({ip}) | CaseID: case_{caseid}")
        else:
            print(f"❌ Fehler {response.status_code} beim Senden an {node}: {response.text}")
    except Exception as e:
        print(f"⚠ Fehler beim Senden an {node}: {e}")

def get_footprint_matrix(ip, node):
    url = f"http://192.168.49.2:{ip}/footprint_matrix"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            matrix = response.json()
            print(f"\n📊 Footprint-Matrix von Node {node} ({ip}):")
            print(matrix)
        else:
            print(f"❌ Fehler {response.status_code} beim Abrufen der Footprint-Matrix von {node}: {response.text}")
    except Exception as e:
        print(f"⚠ Fehler beim Abrufen der Footprint-Matrix von {node}: {e}")

def main():
    df = pd.read_csv(CSV_PATH)

    for _, row in df.iterrows():
        caseid = row["case"]
        event = row["event"]
        node = sanitize_event_name(event)
        ip = get_node_ip(event)

        if not ip:
            print(f"⚠ Kein Port für Event {event}")
            continue

        try:
            dt = datetime.strptime(row["startTime"], "%Y/%m/%d %H:%M:%S.%f")
        except ValueError:
            dt = datetime.strptime(row["startTime"], "%Y/%m/%d %H:%M:%S")
        timestamp = dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        send_event(ip, timestamp, caseid, node)
        #time.sleep(0.03)  # Optional: vermeidet Flooding

    for node, ip in event_port_map.items():
        get_footprint_matrix(ip, node)


if __name__ == "__main__":
    main()
