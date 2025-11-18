#!/bin/bash

# 1. Démarrer le serveur Ollama en arrière-plan
ollama serve &

# Récupère le PID
PID=$!

# 2. Attendre qu'Ollama soit prêt
echo "Attente du démarrage d'Ollama..."
timeout 30 bash -c 'until curl -s http://localhost:11434 > /dev/null; do sleep 1; done'

echo "Ollama démarré. Téléchargement du modèle llama3..."

# 3. Télécharger le modèle
ollama pull llama3

echo "Modèle téléchargé. Démarrage de l'API FastAPI..."

# 4. Démarrer Uvicorn (FastAPI) au premier plan
uvicorn src.main:app --host 0.0.0.0 --port 7860

# Arrêter Ollama si Uvicorn s'arrête
kill $PID