#!/bin/bash

echo " Starte Minikube..."
minikube start

echo " Erstelle Namespace 'central-network' (falls nicht vorhanden)..."
kubectl get namespace central-network > /dev/null 2>&1
if [ $? -ne 0 ]; then
  kubectl create namespace central-network
  echo " Namespace 'central-network' wurde erstellt."
else
  echo " Namespace 'central-network' existiert bereits."
fi

echo " Setze aktuellen Kontext auf Namespace 'central-network'..."
kubectl config set-context --current --namespace=central-network

echo " Wende YAML-Dateien an..."
kubectl apply -f central/central-deployment.yaml
kubectl apply -f central/central-servic.yaml
kubectl apply -f central/worker-deployment.yaml
kubectl apply -f central/worker-servic.yaml

echo " Aktueller Status der Pods:"
kubectl get pods
