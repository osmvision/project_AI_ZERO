# /src/main.py

from fastapi import FastAPI, UploadFile, File
import shutil
from pathlib import Path
from fastapi.responses import FileResponse  # <-- IMPORTEZ CECI

# Importe les fonctions des autres fichiers
from .rag_engine import setup_rag_engine
from .s2t_transcribe import transcribe_audio

# --- Initialisation ---
app = FastAPI(title="Moteur RAG Vocal")
RAG_ENGINE = setup_rag_engine() 

# --- NOUVELLE ROUTE POUR LE FRONTEND ---
@app.get("/")
async def get_frontend():
    """Sert la page web principale (votre interface utilisateur)."""
    # Ce fichier doit être à la racine de votre projet (à côté de 'src')
    return FileResponse("index.html")

# --- VOTRE API EXISTANTE ---
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

        print(f"🧠 Interrogation du RAG avec: {question_text}")
        response = RAG_ENGINE.query(question_text)
        
        return {
            "question_voice": audio_file.filename,
            "transcribed_text": question_text,
            "answer_rag": str(response)
        }
        
    except Exception as e:
        print(f"Erreur d'orchestration: {e}")
        return {"error": f"Une erreur s'est produite: {e}", "status": "failed"}