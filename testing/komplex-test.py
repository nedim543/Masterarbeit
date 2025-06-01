import requests
import time

# ------------------------------
# Prozessstruktur (gerichteter Graph)
#      A
#      |
#      B
#      |
#      C
#     / \
#    D   E
#    |   |
#    F   G
#      \ |
#       H
# ------------------------------

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
        duration = time.time() - start_time
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
    # IP-Zuordnung für die 8 Nodes
    nodes = {
        "a": "192.168.49.2:30010",
        "b": "192.168.49.2:30011",
        "c": "192.168.49.2:30012",
        "d": "192.168.49.2:30013",
        "e": "192.168.49.2:30014",
        "f": "192.168.49.2:30015",
        "g": "192.168.49.2:30016",
        "h": "192.168.49.2:30017",
    }

    # Struktur des Prozesses
    process_flow = {
        "a": ["b"],
        "b": ["c"],
        "c": ["d", "e"],
        "d": ["f"],
        "e": ["g"],
        "f": ["h"],
        "g": ["h"],
        "h": []
    }

    num_cases = int(input("Wie viele Prozessdurchläufe (Cases) sollen simuliert werden? "))
    if num_cases < 1:
        print("⚠ Anzahl muss mindestens 1 sein!")
        return

    start_script_time = time.time()

    for caseid in range(1, num_cases + 1):
        print(f"\n🚀 Starte Case {caseid}")
        base_timestamp = time.time()
        
        # Reihenfolge der Ausführung: manuell gesteuert
        for node in ["a", "b", "c"]:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(base_timestamp))
            send_event(nodes[node], timestamp, caseid, node)
            time.sleep(1)

        # D und E parallel nach C
        for node in ["d", "e"]:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            send_event(nodes[node], timestamp, caseid, node)
        time.sleep(1)

        # Danach F und G
        for node in ["f", "g"]:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            send_event(nodes[node], timestamp, caseid, node)
        time.sleep(1)

        # H ganz am Ende
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        send_event(nodes["h"], timestamp, caseid, "h")
        time.sleep(1)

    print("\n🔄 Warten, damit die Nodes ihre Footprint-Matrix aktualisieren können...")
    time.sleep(2)

    for node, ip in nodes.items():
        get_footprint_matrix(ip, node)

    total_duration = time.time() - start_script_time
    print(f"\n✅ Gesamtdauer des Skripts: {total_duration:.2f} Sekunden")

if __name__ == "__main__":
    main()
