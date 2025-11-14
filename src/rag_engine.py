# /src/rag_engine.py

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core import Settings  # <-- NOUVEAU
from llama_index.llms.ollama import Ollama  # <-- NOUVEAU
from llama_index.embeddings.huggingface import HuggingFaceEmbedding  # <-- NOUVEAU
import os
from pathlib import Path

# --- Configuration des Modèles (LA SECTION IMPORTANTE) ---
# Nous disons à LlamaIndex d'utiliser nos modèles locaux gratuits
# au lieu des modèles payants d'OpenAI.

print("Configuration des modèles locaux (LLM et Embedding)...")

# 1. Configurer le LLM (via Ollama)
Settings.llm = Ollama(model="llama3", request_timeout=60.0)

# 2. Configurer le Modèle d'Embedding (via HuggingFace)
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# Remarque : La première exécution téléchargera le modèle 'bge-small-en-v1.5'.
# ---------------------------------------------------------


# --- Configuration des Chemins ---
BASE_DIR = Path.cwd()
STORAGE_DIR = BASE_DIR.joinpath("storage")
DATA_DIR = BASE_DIR.joinpath("data")

TOP_K_CHUNKS = 3

def setup_rag_engine():
    """Charge l'index RAG existant ou le construit si non trouvé."""
    
    if STORAGE_DIR.exists():
        print("✅ Index RAG existant trouvé. Chargement...")
        try:
            storage_context = StorageContext.from_defaults(persist_dir=str(STORAGE_DIR))
            index = load_index_from_storage(storage_context)
        except Exception as e:
            print(f"❌ Erreur de chargement, reconstruction en cours... ({e})")
            index = build_rag_index()
    else:
        print("⚠️ Index RAG non trouvé. Démarrage de la construction...")
        index = build_rag_index()
        
    return index.as_query_engine(similarity_top_k=TOP_K_CHUNKS)


def build_rag_index():
    """Construit l'index RAG à partir des documents."""
    
    print(f"   -> Lecture des documents dans {DATA_DIR}...")
    documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()
    
    print("   -> Création des vecteurs (Embeddings)...")
    # LlamaIndex utilisera 'Settings.embed_model' (HuggingFace)
    index = VectorStoreIndex.from_documents(documents)
    
    print(f"   -> Sauvegarde de l'index dans {STORAGE_DIR}...")
    index.storage_context.persist(persist_dir=str(STORAGE_DIR))
    
    return index