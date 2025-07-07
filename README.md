# Chaos Testing für verteilte Systeme in Kubernetes

Dieses Repository gehört zur Masterarbeit mit dem Titel:

**Chaos Testing für verteilte Systeme in Kubernetes: Zuverlässigkeit von Distributed-Process-Mining Algorithmen**

Diese Arbeit untersucht die Zuverlässigkeit und Robustheit verteilter Process-Mining-Algorithmen – insbesondere des *Edge Miner Algorithmus* – mithilfe von Chaos Testing in einer Kubernetes-basierten Umgebung.

Ziel war es, die Auswirkungen gezielter Störungen wie Knotenausfällen, Netzwerkverzögerungen und Zeitinkonsistenzen systematisch zu analysieren. Die Ergebnisse zeigen, dass Chaos Testing kritische Schwachstellen offenlegen kann, die im regulären Betrieb oft unentdeckt bleiben.

## 📁 Projektstruktur

Das Repository enthält mehrere Implementierungen und Konfigurationen zur Untersuchung verteilter Process-Mining-Algorithmen unter Chaosbedingungen. Insgesamt wurden **drei Testumgebungen** umgesetzt:

### 1. 🛰 Dezentrale Variante (Edge Miner)

Im Hauptverzeichnis (`edgeNode.py`) befindet sich die erste dezentrale Variante, die sich an den Prinzipien des **Edge Miner Algorithmus** orientiert. Jeder Knoten speichert lokale Events und tauscht sich mit Peers über HTTP aus.

### 2. 🧠 Zentrale Variante

Im Ordner [`central/`](central/) befindet sich eine zentralisierte Implementierung. Hier verarbeitet ein einzelner Knoten (Central Node) alle Events, die von Worker-Nodes gesendet werden. Diese Architektur dient als Vergleich zur dezentralen Variante.

### 3. 🏗 BPI Challenge – Erweiterte dezentrale Variante

Die dritte, komplexere Variante basiert auf dem **BPI-Challenge-Datensatz** und ist unter [`bpi/k8s/`](bpi/k8s/) zu finden. Hier wurde ein realitätsnaher Prozessverlauf simuliert. Der Ordner [`bpi/`](bpi/) enthält zusätzlich:
- vollständige Ergebnisse (Footprint-Matrizen, DFGs),
- den Datensatz selbst,
- sowie alle Python-Skripte zur Datenverarbeitung.

### 🔧 Verbesserungen

Der Ordner [`improvement-deployments/`](improvement-deplyments/) enthält alternative Deployments und Verbesserungen, die im Rahmen der Arbeit entwickelt und evaluiert wurden.

### 🧪 Testskripte

Im Ordner [`testing/`](testing/) liegen verschiedene Python-Tests zur automatisierten Ausführung und Auswertung der Testumgebungen.

### ⚡ Chaos Mesh Szenarien

Im Ordner [`chaos-mesh/`](chaos-mesh/) befinden sich definierte Störungsszenarien (z. B. Node-Ausfälle, Latenz), welche mithilfe von **Chaos Mesh** im Kubernetes-Cluster ausgeführt wurden.



## 🔧 Nutzung & Ausführung

Um dieses Repository bzw. die enthaltenen Testumgebungen nutzen zu können, müssen zunächst folgende Voraussetzungen erfüllt sein:

### ✅ Voraussetzungen

- [Kubernetes](https://kubernetes.io/docs/setup/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [Chaos Mesh](https://chaos-mesh.org/) (für das Chaos Testing)

Ein Installationsleitfaden für Chaos Mesh befindet sich unter:  
https://chaos-mesh.org/docs/quick-start/

---

### 📦 Testumgebungen starten

Nach erfolgreicher Einrichtung von Minikube und Chaos Mesh können die gewünschten Testumgebungen erstellt werden – entweder durch:

- direkte Ausführung der zugehörigen `.yaml`-Dateien in Minikube, oder
- durch bereitgestellte Startskripte.

#### Testumgebungen:

- **Dezentrale Variante (Edge Miner):** [start_dezentral.sh](start_dezentral.sh)
- **Zentrale Variante:** [start_zentral.sh](start_zentral.sh)
- **BPI-Challenge Umgebung:** [start_bpi.sh](start_bpi.sh)

Nach dem Start der Pods kannst du den Status über das folgende Kommando prüfen:

```bash
kubectl get pods --namespace=<dein-namespace>
```

---

### 🧪 Testausführung

Wenn die Umgebung aktiv ist, können die zugehörigen Tests ausgeführt werden.  
**Achte dabei darauf, die IP-Adresse der Minikube-Instanz anzupassen**, da diese variieren kann:

```bash
minikube ip
```

Die Ports müssen in der Regel **nicht angepasst** werden.

#### Standard-Testskripte:

| Variante        | Pfad zum Testskript                                |
|----------------|-----------------------------------------------------|
| Zentral         | [`testing/central-test.py`](testing/central-test.py) |
| Dezentral       | [`testing/test.py`](testing/test.py)                 |
| BPI-Umgebung    | [`bpi/k8s/bpi-test.py`](bpi/k8s/bpi-test.py)         |

---

### ⚠️ Tests unter Chaos-Bedingungen

Um die Robustheit unter realistischen Fehlerbedingungen zu prüfen, können gezielt Störungen mittels Chaos Mesh injiziert werden.  
Diese sollten **vor dem Ausführen der Python-Tests** aktiviert werden.

| Umgebung        | Chaos-Szenarien Pfad                                  |
|----------------|--------------------------------------------------------|
| Zentral         | [`chaos-mesh/central-tests/`](chaos-mesh/central-tests/) |
| Dezentral       | [`chaos-mesh/edge-tests/`](chaos-mesh/edge-tests/)       |
| BPI             | [`bpi/chaos/`](bpi/chaos/)                               |

>  **Hinweis:** Zwischen dem Start der Chaos-Injektion und dem Python-Testskript sollte eine kurze Wartezeit eingeplant werden, damit der Chaos Daemon zuverlässig auf die betroffenen Pods wirkt.
