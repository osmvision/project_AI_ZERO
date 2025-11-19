#!/bin/bash

# 1. Démarrer le serveur Ollama en arrière-plan
# On lance le serveur pour qu'il soit prêt à recevoir des commandes
ollama serve &

# On garde l'ID du processus pour plus tard (bonnes pratiques)
PID=$!

# 2. Attendre qu'Ollama soit réellement prêt
# Cette boucle vérifie chaque seconde si le port 11434 répond
echo "Attente du démarrage d'Ollama..."
timeout 30 bash -c 'until curl -s http://localhost:11434 > /dev/null; do sleep 1; done'

# 3. Télécharger le modèle léger (CORRECTION ICI : phi3 au lieu de llama3)
echo "Ollama est prêt. Téléchargement du modèle phi3..."
ollama pull phi3

# 4. Démarrer l'application FastAPI
echo "Modèle téléchargé. Démarrage de l'application..."
# On utilise le port 7860 qui est obligatoire pour Hugging Face Spaces
uvicorn src.main:app --host 0.0.0.0 --port 7860