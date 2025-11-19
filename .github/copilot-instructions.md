# Instructions Copilot — projet `project_AI_ZERO`

Résumé rapide
- But du projet : API FastAPI + frontend HTML/JS pour interroger une base de documents via RAG (retrieval-augmented generation) avec pipeline local : S2T (Whisper) → Embeddings (HuggingFace) → LLM (Ollama via LlamaIndex).
- Points d'entrée code : `src/main.py` (FastAPI), `src/rag_engine.py` (construction et configuration du RAG), `src/s2t_transcribe.py` (Whisper S2T).

Architecture & flux de données (big picture)
- Ingestion utilisateur : `/query_voice` (upload audio) ou `/query_text` (JSON). Voir `src/main.py`.
- Voix : `s2t_transcribe.transcribe_audio()` (Whisper) → texte.
- RAG : `setup_rag_engine()` (dans `src/rag_engine.py`) configure `Settings.llm` (Ollama) et `Settings.embed_model` (HuggingFaceEmbedding) puis construit/charge `VectorStoreIndex`.
- Persistance : dossier `storage/` (index et vecteurs persistés). Ne pas supprimer ce dossier en prod.

Commandes dev & build importantes
- Virtualenv & deps (Windows PowerShell):
  - `python -m venv .venv`
  - `.\.venv\Scripts\Activate.ps1`
  - `pip install -r requirements.txt`
- Lancer API localement (développement) :
  - `uvicorn src.main:app --reload` (port par défaut configuré dans `boot.sh` pour conteneur : 7860)
- Docker (image utilisée en prod):
  - Local build: `docker build -t zeroai:latest .`
  - Local run (mount storage & data):
    `docker run --rm -it -p 7860:7860 -v <pwd>/storage:/app/storage -v <pwd>/data:/app/data zeroai:latest`
- CI/Registry: workflows GitHub Actions ajoutés — GHCR (`.github/workflows/publish-ghcr.yml`) et Docker Hub (`.github/workflows/publish-dockerhub.yml`).

Patterns et conventions spécifiques au projet
- Global Settings usage: `rag_engine.py` modifie `Settings.llm` et `Settings.embed_model` directement. Quand tu changes l'embedder/LLM, garde cette API (LlamaIndex Settings) cohérente.
- Chargement unique des modèles: `s2t_transcribe.py` charge Whisper au module import (`S2T_MODEL = whisper.load_model("base")`). Evite de recloner/charger plusieurs fois — garde le modèle en singleton.
- Nettoyage temporaire: `main.py` crée et supprime `temp_audio.webm` dans les routes voix.
- Retour d'erreur: les fonctions retournent souvent des chaînes spécifiques (ex: transcription retourne "Erreur de transcription.") — utilises-les pour déterminer flow d'erreur.

Intégrations externes & risques
- Ollama: binaire installé via script dans `Dockerfile` et démarré dans `boot.sh` (`ollama serve`). En production, privilégier image pré-buildée (runner Coolify peut échouer lors du build si ressources limitées).
- HuggingFace models: embeddings `BAAI/bge-small-en-v1.5` téléchargé au runtime. Si modèle privé, configurer `HUGGINGFACE_HUB_TOKEN` dans l'environnement.
- Whisper (openai-whisper): nécessite `ffmpeg` (installé dans Dockerfile). Transcription peut être lourde en CPU.

Conseils pratiques pour un agent
- Préfère modifications ciblées : si tu modifies `Settings.embed_model`, mets à jour `requirements.txt` et teste `tools_test_imports.py` (fourni) pour vérifier imports.
- Ne supprime pas `storage/` dans les PRs ; les tests/commits ne doivent pas vider les données persistantes sans raison.
- Pour changement de Dockerfile/boot.sh : documente l'impact sur le startup d'Ollama (peut nécessiter plus de timeout ou ressources).
- Si tu changes le modèle d'embedding pour tests légers, propose `sentence-transformers/all-MiniLM-L6-v2` comme alternative (moins RAM/disque).

Fichiers clefs à lire pour contexte
- `src/main.py` — routes FastAPI, pattern de gestion d'erreur, nettoyage fichiers temporaires.
- `src/rag_engine.py` — configuration LlamaIndex, Settings, chemins `storage/` et `data/`.
- `src/s2t_transcribe.py` — initialisation Whisper et méthode `transcribe_audio`.
- `Dockerfile`, `boot.sh` — build/run en conteneur; attention à l'installation d'Ollama et au port `7860`.
- `requirements.txt` — liste des dépendances requis pour reproduire l'environnement.

Que faire quand tu rencontres une erreur
- Si import absent : exécute `.\.venv\Scripts\Activate.ps1` puis `pip install -r requirements.txt` et `python -c "import <module>; print(<module>.__version__)"`.
- Si build Docker échoue en CI : proposer de prébuilder l'image et pousser vers GHCR/DockerHub (workflows déjà présents), ou réduire les étapes d'installation dans Dockerfile.
- Si Ollama ne démarre dans container : vérifier logs (`boot.sh` attend `curl http://localhost:11434`) et augmenter timeout/ressources.

Asks & feedback
- Si une section est incomplète (ex : secrets GHCR/DockerHub, commandes de debug additionnelles), dis-moi quelle partie tu veux approfondir et je l'ajouterai.

*** Fin du fichier (garde concis et actionnable) ***
