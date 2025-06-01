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
        
        response = requests.post(url, json=data)

        if response.status_code == 200:
            print(f"✅ Erfolgreich gesendet an {node} ({ip}) | CaseID: case_{caseid}")
        else:
            print(f"❌ Fehler {response.status_code} beim Senden an {node}: {response.text} ")
    except Exception as e:
        print(f"⚠ Fehler beim Senden an {node}: {e}")    

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

    ip1 = "192.168.49.2:30030"
    ip2 = "192.168.49.2:30031"
    ip3 = "192.168.49.2:30032"
    ip4 = "192.168.49.2:30033"
    #...  es fehelen noch ips

    num_messages = int(input("Wie viele Nachrichten sollen gesendet werden? "))

    if num_messages < 1:
        print("⚠ Anzahl der Nachrichten muss mindestens 1 sein!")
        return

    caseid = 1
    base_timestamp = time.time()  # float mit Sekunden und Millisekunden

    nodes = [(ip1, "a-submitted"), (ip2, "a-partlysubmitted"), (ip3, "a-preaccepted"), (ip4, "w-completeren-aanvraag")]


    for i in range(num_messages):
        current_ts = base_timestamp + i
        ip, node = nodes[i % len(nodes)]

        
        dt = datetime.fromtimestamp(current_ts)
        timestamp = dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        send_event(ip, timestamp, caseid, node)

        if (i + 1) % len(nodes) == 0:
            caseid += 1

        #time.sleep(1)


    print("\n🔄 Warten, damit die Nodes ihre Footprint-Matrix aktualisieren können...")
    time.sleep(1)

    for ip, node in nodes[:num_messages]:
        get_footprint_matrix(ip, node)

if __name__ == "__main__":
    main()



