# Chaos Testing für verteilte Systeme in Kubernetes

Dieses Repository gehört zur Masterarbeit mit dem Titel:

**Chaos Testing für verteilte Systeme in Kubernetes: Zuverlässigkeit von Distributed-Process-Mining Algorithmen**

Diese Arbeit untersucht die Zuverlässigkeit und Robustheit verteilter Process-Mining-Algorithmen – insbesondere des *Edge Miner Algorithmus* – mithilfe von Chaos Testing in einer Kubernetes-basierten Umgebung.

Ziel war es, die Auswirkungen gezielter Störungen wie Knotenausfällen, Netzwerkverzögerungen und Zeitinkonsistenzen systematisch zu analysieren. Die Ergebnisse zeigen, dass Chaos Testing kritische Schwachstellen offenlegen kann, die im regulären Betrieb oft unentdeckt bleiben.

## 📁 Projektstruktur

Das Repository enthält mehrere Implementierungen und Konfigurationen zur Untersuchung verteilter Process-Mining-Algorithmen unter Chaosbedingungen. Insgesamt wurden **drei Testumgebungen** umgesetzt:

### 1. 🛰 Dezentrale Variante (Edge Miner)

Im Hauptverzeichnis (`edgeNode.py`) befindet sich die erste dezentrale Variante, die sich an den Prinzipien des **Edge Miner Algorithmus** orientiert. Jeder Knoten speichert lokale Events und tauscht sich mit Peers über HTTP aus. Die Footprint-Matrix wird on-demand generiert.

### 2. 🧠 Zentrale Variante

Im Ordner [`central/`](central/) befindet sich eine zentralisierte Implementierung. Hier verarbeitet ein einzelner Knoten (Central Node) alle Events, die von Worker-Nodes gesendet werden. Diese Architektur dient als Vergleich zur dezentralen Variante.

### 3. 🏗 BPI Challenge – Erweiterte dezentrale Variante

Die dritte, komplexere Variante basiert auf dem **BPI-Challenge-Datensatz** und ist unter [`bpi/k8s/`](bpi/k8s/) zu finden. Hier wurde ein realitätsnaher Prozessverlauf simuliert. Der Ordner [`bpi/`](bpi/) enthält zusätzlich:
- vollständige Ergebnisse (Footprint-Matrizen, DFGs),
- den Datensatz selbst,
- sowie alle Python-Skripte zur Datenverarbeitung.

### 🔧 Verbesserungen

Der Ordner [`improvement-deployments/`](improvement-deployments/) enthält alternative Deployments und Verbesserungen, die im Rahmen der Arbeit entwickelt und evaluiert wurden.

### 🧪 Testskripte

Im Ordner [`testing/`](testing/) liegen verschiedene Python-Tests zur automatisierten Ausführung und Auswertung der Testumgebungen.

### ⚡ Chaos Mesh Szenarien

Im Ordner [`chaos-mesh/`](chaos-mesh/) befinden sich definierte Störungsszenarien (z. B. Node-Ausfälle, Latenz), welche mithilfe von **Chaos Mesh** im Kubernetes-Cluster ausgeführt wurden.
