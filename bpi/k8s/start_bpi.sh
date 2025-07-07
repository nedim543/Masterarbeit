#!/bin/bash

echo " Starte Minikube..."
minikube start

echo " Erstelle Namespace 'bpi' (falls nicht vorhanden)..."
kubectl get namespace bpi > /dev/null 2>&1
if [ $? -ne 0 ]; then
  kubectl create namespace bpi
  echo " Namespace 'bpi' wurde erstellt."
else
  echo " Namespace 'bpi' existiert bereits."
fi

echo " Setze aktuellen Kontext auf Namespace 'bpi'..."
kubectl config set-context --current --namespace=bpi

echo " Wende YAML-Dateien an..."
kubectl apply -f bpi/k8s/bpi-rbac.yaml
kubectl apply -f bpi/k8s/bpi-deployments.yaml
kubectl apply -f bpi/k8s/bpi-services.yaml

echo " Aktueller Status der Pods:"
kubectl get pods
