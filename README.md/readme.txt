# 🚀 Projet : Assistant RAG Vocal avec IA Locale

Ce projet est une application web complète (FastAPI + HTML/JS) qui permet à un utilisateur de poser des questions vocalement à une base de documents.

L'ensemble du pipeline (S2T, Embedding, LLM) tourne localement.

## Fonctionnalités

* **Frontend :** Interface de chat en HTML/JS pur.
* **API :** Serveur FastAPI (Python).
* **S2T (Voix->Texte) :** `openai-whisper` (tourne localement).
* **RAG (IA) :** `LlamaIndex` utilisant des modèles locaux.
* **Modèle d'Embedding :** `HuggingFace (BAAI/bge-small-en-v1.5)`.
* **LLM (Cerveau) :** `Ollama (llama3)`.

## 🛠️ Installation et Lancement

1.  **Prérequis :**
    * Installer Python 3.11 (64-bit).
    * Installer [Ollama](https://ollama.com/) et le laisser tourner en fond.

2.  **Télécharger le modèle LLM :**
    ```bash
    ollama pull llama3
    ```

3.  **Cloner le dépôt et installer les dépendances :**
    ```bash
    git clone [VOTRE_URL_GITHUB]
    cd zeroAI
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

4.  **Ajouter les documents :**
    * Placez vos fichiers `.txt` ou `.pdf` dans le dossier `/data`.

5.  **Lancer le serveur :**
    ```bash
    uvicorn src.main:app --reload
    ```

6.  **Accéder à l'application :**
    * Ouvrez `http://127.0.0.1:8000/` dans votre navigateur.


