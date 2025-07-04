#!/bin/bash

echo "🚀 Starte Minikube..."
minikube start

echo " Erstelle Namespace 'edge-network' (falls nicht vorhanden)..."
kubectl get namespace edge-network > /dev/null 2>&1
if [ $? -ne 0 ]; then
  kubectl create namespace edge-network
  echo " Namespace 'edge-network' wurde erstellt."
else
  echo " Namespace 'edge-network' existiert bereits."
fi

echo "🔧 Setze aktuellen Kontext auf Namespace 'edge-network'..."
kubectl config set-context --current --namespace=edge-network

echo " Wende YAML-Dateien an..."
kubectl apply -f rbac.yaml
kubectl apply -f flask-deployment.yaml
kubectl apply -f flask-service.yaml

echo " Aktueller Status der Pods:"
kubectl get pods
