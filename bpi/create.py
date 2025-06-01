# Nach dem Zurücksetzen der Umgebung: Neuimport und Rekonstruktion der YAML-Dateien

import os

# Liste der Events
events = [
    "A_SUBMITTED",
    "A_PARTLYSUBMITTED",
    "A_PREACCEPTED",
    "W_Completeren aanvraag",
    "A_ACCEPTED",
    "O_SELECTED",
    "A_FINALIZED",
    "O_CREATED",
    "O_SENT",
    "W_Nabellen offertes",
    "O_SENT_BACK",
    "W_Valideren aanvraag",
    "A_REGISTERED",
    "A_APPROVED",
    "O_ACCEPTED",
    "A_ACTIVATED",
    "O_CANCELLED",
    "A_DECLINED",
    "A_CANCELLED",
    "W_Afhandelen leads",
    "O_DECLINED",
    "W_Nabellen incomplete dossiers",
    "W_Beoordelen fraude"
]

def sanitize_name(name):
    return name.replace(" ", "-")

deployment_yaml = ""
service_yaml = ""
base_node_port = 30030

for i, event in enumerate(events):
    sanitized = sanitize_name(event)
    
    deployment_yaml += f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {sanitized}
  namespace: bpi
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {sanitized}
  template:
    metadata:
      labels:
        app: {sanitized}
    spec:
      containers:
        - name: {sanitized}
          image: stu240498/flask-node
          ports:
            - containerPort: 5000
          env:
            - name: NAME
              value: "{event}"
---
"""
    service_yaml += f"""apiVersion: v1
kind: Service
metadata:
  name: {sanitized}-service
spec:
  type: NodePort
  selector:
    app: {sanitized}
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
      nodePort: {base_node_port + i}
---
"""

# Dateien speichern
deployment_file_path = "/mnt/data/deployments.yaml"
service_file_path = "/mnt/data/services.yaml"

with open(deployment_file_path, "w") as f:
    f.write(deployment_yaml)

with open(service_file_path, "w") as f:
    f.write(service_yaml)

deployment_file_path, service_file_path

# Wir korrigieren jetzt die Deployment- und Service-Dateien nach RFC 1123:
# - Alles in Kleinbuchstaben
# - Unterstriche durch Bindestriche ersetzen
# - Leerzeichen durch Bindestriche ersetzen

def sanitize_rfc1123(name):
    return name.lower().replace("_", "-").replace(" ", "-")

deployment_yaml_rfc1123 = ""
service_yaml_rfc1123 = ""

for i, event in enumerate(events):
    sanitized = sanitize_rfc1123(event)

    deployment_yaml_rfc1123 += f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {sanitized}
  namespace: bpi
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {sanitized}
  template:
    metadata:
      labels:
        app: {sanitized}
    spec:
      containers:
        - name: {sanitized}
          image: stu240498/flask-node
          ports:
            - containerPort: 5000
          env:
            - name: NAME
              value: "{event}"
---
"""
    service_yaml_rfc1123 += f"""apiVersion: v1
kind: Service
metadata:
  name: {sanitized}-service
spec:
  type: NodePort
  selector:
    app: {sanitized}
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
      nodePort: {base_node_port + i}
---
"""

# Dateien speichern
deployment_file_rfc1123 = "/mnt/data/deployments-rfc1123.yaml"
service_file_rfc1123 = "/mnt/data/services-rfc1123.yaml"

with open(deployment_file_rfc1123, "w") as f:
    f.write(deployment_yaml_rfc1123)

with open(service_file_rfc1123, "w") as f:
    f.write(service_yaml_rfc1123)

deployment_file_rfc1123, service_file_rfc1123
