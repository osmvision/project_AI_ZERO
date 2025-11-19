```python
# /src/s2t_transcribe.py

import os
import whisper
from typing import Optional

# Choix du modèle via variable d'environnement pour tests/production rapide
# Par défaut on utilise 'tiny' pour la vitesse. Pour plus de précision, définir S2T_MODEL=base|small|medium
MODEL_NAME = os.environ.get("S2T_MODEL", "tiny")

# Chargement paresseux du modèle (unique instance)
S2T_MODEL: Optional[object] = None

def _load_model():
    global S2T_MODEL
    if S2T_MODEL is None:
        print(f"Chargement du modèle Whisper '{MODEL_NAME}' (peut prendre du temps)...")
        S2T_MODEL = whisper.load_model(MODEL_NAME)
        print("Modèle Whisper chargé.")

def transcribe_audio(file_path: str) -> str:
    """Transcrit le fichier audio en texte. Charge le modèle à la première utilisation.

    - Par défaut utilise le modèle indiqué par `S2T_MODEL` env var (ex: `tiny`, `base`).
    - Supprime le fichier temporaire après traitement.
    """
    print(f"🎤 Démarrage de la transcription pour: {file_path}")

    try:
        _load_model()
        result = S2T_MODEL.transcribe(file_path, language="fr")
        transcription = result.get("text", "").strip()
        print(f"✅ Transcription réussie: {transcription[:50]}...")
        return transcription

    except Exception as e:
        print(f"❌ Erreur lors de la transcription: {e}")
        return "Erreur de transcription."

    finally:
        # Nettoyage : supprimer le fichier temporaire après utilisation
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

```
# /src/s2t_transcribe.py

import whisper
import os

# Déclaration du modèle Whisper (chargé une seule fois)
S2T_MODEL = whisper.load_model("base") 
# "base" est le modèle le plus petit et rapide, mais moins précis que "small" ou "medium".

def transcribe_audio(file_path: str) -> str:
    """Utilise Whisper pour transcrire un fichier audio donné."""
    
    print(f"🎤 Démarrage de la transcription pour: {file_path}")
    
    try:
        # Transcrit le fichier audio
        result = S2T_MODEL.transcribe(file_path, language="fr")
        transcription = result["text"]
        
        print(f"✅ Transcription réussie: {transcription[:50]}...")
        return transcription.strip()
    
    except Exception as e:
        print(f"❌ Erreur lors de la transcription: {e}")
        return "Erreur de transcription."
    finally:
        # Nettoyage : supprimer le fichier temporaire après utilisation
        if os.path.exists(file_path):
            os.remove(file_path)
            