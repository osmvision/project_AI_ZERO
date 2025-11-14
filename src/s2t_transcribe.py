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
            