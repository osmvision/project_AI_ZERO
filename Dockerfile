# 1. Image de base : Python standard (pas NVIDIA)
FROM python:3.11-slim-bookworm

# 2. Variables d'environnement
ENV DEBIAN_FRONTEND=noninteractive
ENV OLLAMA_HOST="0.0.0.0"

# Optional build arg to prefetch HuggingFace models during image build
ARG HUGGINGFACE_HUB_TOKEN
ENV HUGGINGFACE_HUB_TOKEN=${HUGGINGFACE_HUB_TOKEN}

# 3. Installation des dépendances système (Python, pip, ffmpeg pour Whisper)
RUN apt-get update && apt-get install -y \
    python3-pip \
    ffmpeg \
    curl \
    && apt-get clean

# 4. Installation d'Ollama (version CPU)
RUN curl -fsSL https://ollama.com/install.sh | sh

# 5. Création du répertoire de travail
WORKDIR /app

# 6. Copie des requirements et installation
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# 7. Copie de TOUT votre projet dans le conteneur
COPY . .

# 8. Copier le cache HF pré-téléchargé (préparé par le workflow) si présent
# Le workflow doit créer un dossier `hf_cache/` dans le contexte de build.
COPY hf_cache /root/.cache/huggingface/

# 8. Rendre le script de démarrage exécutable
COPY boot.sh /usr/local/bin/boot.sh
RUN chmod +x /usr/local/bin/boot.sh

# 9. Commande de démarrage (Hugging Face s'attend au port 7860)
EXPOSE 7860
CMD ["/usr/local/bin/boot.sh"]