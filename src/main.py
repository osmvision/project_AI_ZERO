# /src/main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware # <--- LE VRAI IMPORT POUR FASTAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import shutil
from pathlib import Path

# Importe les fonctions des autres fichiers
# Assure-toi que ces fichiers existent bien dans le dossier src
from .rag_engine import setup_rag_engine
from .s2t_transcribe import transcribe_audio

# --- Initialisation de l'application FastAPI ---
app = FastAPI(title="Moteur RAG Vocal")

# ==========================================
# 🔒 CONFIGURATION DE LA SÉCURITÉ (CORS) 🔒
# ==========================================
# Ceci autorise ton site Cloudflare à parler à ce serveur
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" autorise tout le monde. Pour la prod, tu pourras mettre l'URL de ton site.
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes (POST, GET, OPTIONS...)
    allow_headers=["*"],  # Autorise tous les headers
)

# --- Initialisation du moteur IA ---
print("🚀 Démarrage du moteur RAG...")
try:
    RAG_ENGINE = setup_rag_engine()
    print("✅ Moteur RAG prêt !")
except Exception as e:
    print(f"❌ Erreur critique au chargement du RAG: {e}")
    RAG_ENGINE = None

# --- Modèle pour l'entrée texte ---
class TextQuery(BaseModel):
    text: str

# --- ROUTE: Accueil ---
@app.get("/")
async def get_frontend():
    return {"message": "L'API RAG est en ligne et fonctionnelle. Utilisez /query_text ou /query_voice."}

# --- ROUTE: Voix ---
@app.post("/query_voice")
async def query_voice(audio_file: UploadFile = File(...)):
    temp_file_path = Path("temp_audio.webm") # .webm est mieux pour le web
    
    try:
        # Sauvegarde du fichier audio reçu
        with temp_file_path.open("wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
        
        # Transcription
        question_text = transcribe_audio(str(temp_file_path))
        
        if "Erreur" in question_text:
            return {"error": question_text, "status": "failed"}

        print(f"🎤 Question reçue (Audio): {question_text}")
        
        # Interrogation RAG
        if RAG_ENGINE:
            response = RAG_ENGINE.chat(question_text)
            answer = str(response)
        else:
            answer = "Le moteur RAG n'est pas chargé."

        return {
            "question_voice": audio_file.filename,
            "transcribed_text": question_text,
            "answer_rag": answer
        }
        
    except Exception as e:
        print(f"❌ Erreur (Voix): {e}")
        return {"error": str(e), "status": "failed"}
    finally:
        # Nettoyage du fichier temporaire
        if temp_file_path.exists():
            temp_file_path.unlink()

# --- ROUTE: Texte ---
@app.post("/query_text")
async def query_text(query: TextQuery):
    try:
        question_text = query.text
        if not question_text:
            return {"error": "Question vide", "status": "failed"}
            
        print(f"⌨️ Question reçue (Texte): {question_text}")
        
        if RAG_ENGINE:
            response = RAG_ENGINE.chat(question_text)
            answer = str(response)
        else:
            answer = "Le moteur RAG n'est pas chargé."
        
        return {
            "transcribed_text": question_text,
            "answer_rag": answer
        }
    except Exception as e:
        print(f"❌ Erreur (Texte): {e}")
        return {"error": str(e), "status": "failed"}

# --- ROUTE: Reset ---
@app.get("/reset_chat")
async def reset_chat_history():
    print("🔄 Reset demandé")
    try:
        if RAG_ENGINE and hasattr(RAG_ENGINE, 'reset'):
            RAG_ENGINE.reset()
            return {"status": "ok", "message": "Mémoire effacée."}
        elif RAG_ENGINE:
             # Si la méthode reset n'existe pas sur l'objet, on recrée le moteur (méthode brutale mais efficace)
            global RAG_ENGINE
            RAG_ENGINE = setup_rag_engine()
            return {"status": "ok", "message": "Moteur rechargé à neuf."}
        else:
            return {"status": "error", "message": "Moteur non chargé."}
    except Exception as e:
        return {"status": "error", "message": str(e)}