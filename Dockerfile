# 1. Image de base : Python + Outils CUDA (pour le GPU)
FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# 2. Variables d'environnement
ENV DEBIAN_FRONTEND=noninteractive
ENV OLLAMA_HOST="0.0.0.0"

# 3. Installation des dépendances système (Python, pip, ffmpeg pour Whisper)
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python3.11-venv \
    ffmpeg \
    curl \
    && apt-get clean

# 4. Installation d'Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# 5. Création du répertoire de travail
WORKDIR /app

# 6. Copie des requirements et installation
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 7. Copie de TOUT votre projet dans le conteneur
COPY . .

# 8. Rendre le script de démarrage exécutable
COPY boot.sh /usr/local/bin/boot.sh
RUN chmod +x /usr/local/bin/boot.sh

# 9. Commande de démarrage (Hugging Face s'attend au port 7860)
EXPOSE 7860
CMD ["/usr/local/bin/boot.sh"]