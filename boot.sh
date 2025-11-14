#!/bin/bash

# 1. Démarrer le serveur Ollama en arrière-plan
ollama serve &

# Récupère le PID (ID de processus) du serveur Ollama
PID=$!

# 2. Attendre qu'Ollama soit prêt (max 30s)
echo "Attente du démarrage d'Ollama..."
timeout 30 bash -c 'until curl -s http://localhost:11434 > /dev/null; do sleep 1; done'

echo "Ollama démarré. Téléchargement du modèle llama3..."

# 3. Télécharger le modèle (pour qu'il soit prêt au premier démarrage)
ollama pull llama3

echo "Modèle téléchargé. Démarrage de l'API FastAPI..."

# 4. Démarrer Uvicorn (FastAPI) au premier plan
# Hugging Face Spaces ATTEND que l'application soit sur le port 7860
uvicorn src.main:app --host 0.0.0.0 --port 7860

# Arrêter Ollama si Uvicorn s'arrête
kill $PID