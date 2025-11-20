
echo "🚀 DÉMARRAGE DU SCRIPT BOOT (MODE ÉCONOMIE MÉMOIRE)..."

# --- LIMITATIONS STRICTES (CRUCIAL POUR NE PAS CRASHER) ---
# On limite le contexte à 2048 tokens au lieu de 128k.
# Cela réduit la consommation de 49Go à ~1.5Go.
export OLLAMA_NUM_CTX=2048
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_KEEP_ALIVE=24h
export OLLAMA_HOST=0.0.0.0

# 1. Lancer Ollama
ollama serve > /var/log/ollama.log 2>&1 &
PID=$!
echo "✅ Ollama lancé (PID: $PID) avec restrictions mémoire."

# 2. Attendre Ollama (Boucle robuste)
echo "⏳ Attente de la disponibilité d'Ollama..."
count=0
while ! curl -s http://localhost:11434 > /dev/null; do
    sleep 1
    count=$((count+1))
    if [ $count -ge 60 ]; then
        echo "❌ ERREUR: Ollama ne répond pas."
        cat /var/log/ollama.log
        exit 1
    fi
done

# 3. Téléchargement du modèle
echo "📥 Téléchargement du modèle phi3..."
ollama pull phi3

# 4. Lancement de l'application
echo "🔥 Lancement de FastAPI..."
uvicorn src.main:app --host 0.0.0.0 --port 7860