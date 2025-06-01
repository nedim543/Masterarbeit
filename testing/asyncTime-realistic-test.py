import requests
import time
import random
from datetime import datetime

def send_event(ip, timestamp, caseid, node):
    url = f"http://{ip}/event"
    data = {
        "timestamp": timestamp,
        "activity": "Start Production",
        "caseid": f"case_{caseid}",
        "node": node
    }

    try:
        start_time = time.time()
        response = requests.post(url, json=data)
        end_time = time.time()
        duration = end_time - start_time

        if response.status_code == 200:
            print(f"✅ Erfolgreich gesendet an {node} ({ip}) | CaseID: case_{caseid} | Dauer: {duration:.3f}s")
        else:
            print(f"❌ Fehler {response.status_code} beim Senden an {node}: {response.text} | Dauer: {duration:.3f}s")
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"⚠ Fehler beim Senden an {node}: {e} | Dauer: {duration:.3f}s")    

def get_footprint_matrix(ip, node):
    url = f"http://{ip}/footprint_matrix"

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

    ip1 = "192.168.49.2:30010"
    ip2 = "192.168.49.2:30011"
    ip3 = "192.168.49.2:30012"
    ip4 = "192.168.49.2:30013"

    num_messages = int(input("Wie viele Nachrichten sollen gesendet werden? "))

    if num_messages < 1:
        print("⚠ Anzahl der Nachrichten muss mindestens 1 sein!")
        return

    caseid = 1
    base_timestamp = time.time()  # float mit Sekunden und Millisekunden

    nodes = [(ip1, "a"), (ip2, "b"), (ip3, "c"), (ip4, "d")]

    start_script_time = time.time()

    for i in range(num_messages):
        current_ts = base_timestamp + i
        ip, node = nodes[i % len(nodes)]

        if node == "b":
            delay = random.uniform(0, 2)  # Zufallsverzögerung in Sekunden (inkl. Millisekunden)
            delayed_ts = current_ts + delay
            dt_b = datetime.fromtimestamp(delayed_ts)
            timestamp = dt_b.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(f"⏸ Node B Zufallsverzögerung: +{delay:.3f}s | Zeitstempel: {timestamp}")
        else:
            dt = datetime.fromtimestamp(current_ts)
            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(f" {timestamp}")

        send_event(ip, timestamp, caseid, node)

        if (i + 1) % len(nodes) == 0:
            caseid += 1

        time.sleep(1)


    print("\n🔄 Warten, damit die Nodes ihre Footprint-Matrix aktualisieren können...")
    time.sleep(1)

    for ip, node in nodes[:num_messages]:
        get_footprint_matrix(ip, node)

    end_script_time = time.time()
    total_duration = end_script_time - start_script_time
    print(f"\n✅ Gesamtdauer des Skripts: {total_duration:.2f} Sekunden")

if __name__ == "__main__":
    main()
