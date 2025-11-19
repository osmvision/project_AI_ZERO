import whisper
import os

# On charge le modèle une seule fois au lancement de l'app.
# "base" est un bon équilibre. Si ça plante (OOM), on passera à "tiny".
print("🎧 Chargement du modèle Whisper (Base)...")
try:
    # Le modèle est chargé en RAM globale
    S2T_MODEL = whisper.load_model("base")
    print("✅ Modèle Whisper chargé avec succès.")
except Exception as e:
    print(f"⚠️ Erreur critique : Impossible de charger Whisper : {e}")
    S2T_MODEL = None

def transcribe_audio(file_path: str) -> str:
    """
    Transcrit le fichier audio en texte.
    Nettoie le fichier temporaire à la fin.
    """
    if S2T_MODEL is None:
        return "Erreur configuration : Le modèle Whisper n'est pas chargé."

    print(f"🎤 Démarrage de la transcription pour: {file_path}")

    try:
        # fp16=False est CRUCIAL sur Hugging Face Spaces (CPU only)
        # Si on laisse True, ça génère des warnings ou des erreurs.
        result = S2T_MODEL.transcribe(file_path, language="fr", fp16=False)
        
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
                print(f"🧹 Fichier temporaire supprimé : {file_path}")
            except Exception:
                pass