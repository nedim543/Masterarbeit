import requests
import time

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
        end_time = time.time()  # Ende auch bei Fehler
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
    import time
    import requests

    ip1 = "192.168.49.2:30010"
    ip2 = "192.168.49.2:30011"
    ip3 = "192.168.49.2:30012"
    ip4 = "192.168.49.2:30013"

    num_messages = int(input("Wie viele Nachrichten sollen gesendet werden? "))

    if num_messages < 1:
        print("⚠ Anzahl der Nachrichten muss mindestens 1 sein!")
        return

    caseid = 1
    base_timestamp = time.time()

    nodes = [(ip1, "a"), (ip2, "b"), (ip3, "c"), (ip4, "d")]

    start_script_time = time.time()

    delayed_message = None
    delay_counter = 0

    for i in range(num_messages):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(base_timestamp + i * 60))
        ip, node = nodes[i % len(nodes)]

        # Alle 8 Nachrichten: eine verzögern (z.B. 2., 10., 18. Nachricht)
        if i % 8 == 2:
            delayed_message = (ip, timestamp, caseid, node)
            delay_counter = 2  # Verzögere genau um 2 Nachrichten
            print(f"⏸ Verzögere Nachricht an {node} ({ip}) | CaseID: case_{caseid}")
        else:
            send_event(ip, timestamp, caseid, node)

        # Wenn wir noch eine verzögerte Nachricht haben und 2 Schritte vergangen sind
        if delayed_message and delay_counter == 0:
            print(f"⏩ Sende verzögerte Nachricht jetzt an {delayed_message[3]} ({delayed_message[0]})")
            send_event(delayed_message[0], delayed_message[1], delayed_message[2], delayed_message[3])
            delayed_message = None
        elif delayed_message:
            delay_counter -= 1  # Schritte herunterzählen

        if (i + 1) % len(nodes) == 0:
            caseid += 1

        time.sleep(1)

    # Falls am Ende noch eine verzögerte Nachricht übrig bleibt
    if delayed_message:
        print(f"⏩ Sende am Ende noch verzögerte Nachricht an {delayed_message[3]} ({delayed_message[0]})")
        send_event(delayed_message[0], delayed_message[1], delayed_message[2], delayed_message[3])

    print("\n🔄 Warten, damit die Nodes ihre Footprint-Matrix aktualisieren können...")
    time.sleep(2)

    for ip, node in nodes[:num_messages]:
        get_footprint_matrix(ip, node)

    end_script_time = time.time()
    total_duration = end_script_time - start_script_time
    print(f"\n✅ Gesamtdauer des Skripts: {total_duration:.2f} Sekunden")


if __name__ == "__main__":
    main()
