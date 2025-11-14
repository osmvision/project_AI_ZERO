# /src/main.py

from fastapi import FastAPI, UploadFile, File
import shutil
from pathlib import Path
from fastapi.responses import FileResponse
from pydantic import BaseModel  # <-- NOUVEL IMPORT

# Importe les fonctions des autres fichiers
from .rag_engine import setup_rag_engine
from .s2t_transcribe import transcribe_audio

# --- Initialisation ---
app = FastAPI(title="Moteur RAG Vocal")
RAG_ENGINE = setup_rag_engine() 

# --- Modèle Pydantic pour l'entrée texte ---
class TextQuery(BaseModel):
    text: str

# --- ROUTE POUR LE FRONTEND ---
@app.get("/")
async def get_frontend():
    """Sert la page web principale (votre interface utilisateur)."""
    return FileResponse("index.html")

# --- API POUR LA VOIX (Inchangée) ---
@app.post("/query_voice")
async def query_voice(audio_file: UploadFile = File(...)):
    """
    Accepte un fichier audio, le transcrit, et interroge le moteur RAG.
    """
    temp_file_path = Path("temp_audio.mp3") 
    
    try:
        with temp_file_path.open("wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
        
        question_text = transcribe_audio(str(temp_file_path))
        
        if "Erreur de transcription" in question_text:
            return {"error": question_text, "status": "failed"}

        print(f"🧠 Interrogation (Chat) du RAG avec: {question_text}")
        response = RAG_ENGINE.chat(question_text) 
        
        return {
            "question_voice": audio_file.filename,
            "transcribed_text": question_text,
            "answer_rag": str(response)
        }
        
    except Exception as e:
        print(f"Erreur d'orchestration (voix): {e}")
        return {"error": f"Une erreur s'est produite: {e}", "status": "failed"}

# --- NOUVEAU POINT DE TERMINAISON POUR LE TEXTE ---
@app.post("/query_text")
async def query_text(query: TextQuery):
    """
    Accepte une question textuelle et interroge le moteur RAG.
    """
    try:
        question_text = query.text
        if not question_text:
            return {"error": "La question ne peut pas être vide", "status": "failed"}
            
        print(f"🧠 Interrogation (Chat) du RAG avec: {question_text}")
        
        # Utilise le MÊME moteur de chat pour garder la mémoire
        response = RAG_ENGINE.chat(question_text) 
        
        return {
            "transcribed_text": question_text, # Renvoyé pour l'affichage
            "answer_rag": str(response)
        }
    except Exception as e:
        print(f"Erreur d'orchestration (texte): {e}")
        return {"error": f"Une erreur s'est produite: {e}", "status": "failed"}

# --- API POUR LE RESET (Inchangée) ---
@app.get("/reset_chat")
async def reset_chat_history():
    """Réinitialise l'historique de la conversation du moteur de chat."""
    print("🔄 Réinitialisation de la mémoire du chat...")
    if hasattr(RAG_ENGINE, 'reset'):
        RAG_ENGINE.reset()
        return {"status": "ok", "message": "Historique réinitialisé."}
    else:
        return {"status": "error", "message": "Impossible de réinitialiser le moteur."}