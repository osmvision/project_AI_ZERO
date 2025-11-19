from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core import Settings  
from llama_index.llms.ollama import Ollama  
from llama_index.embeddings.huggingface import HuggingFaceEmbedding  
import os
from pathlib import Path

# --- Configuration des Modèles (LA SECTION IMPORTANTE) ---
# Nous disons à LlamaIndex d'utiliser nos modèles locaux gratuits.

print("Configuration des modèles locaux (LLM et Embedding)...")

# 1. Configurer le LLM (via Ollama)
# Timeout augmenté pour laisser Ollama répondre sur de longues requêtes
ollama_model = os.environ.get("OLLAMA_MODEL", "llama3")
ollama_timeout = float(os.environ.get("OLLAMA_TIMEOUT", "360.0"))
Settings.llm = Ollama(
    model=ollama_model,
    request_timeout=ollama_timeout
)

# 2. Configurer le Modèle d'Embedding (via HuggingFace)
# Par défaut on choisit un embedder léger et rapide pour la production:
# - `sentence-transformers/all-MiniLM-L6-v2` (petit, rapide, bon compromis)
# On permet d'écraser via la variable d'environnement `EMBED_MODEL`.
embed_model_name = os.environ.get("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
embed_model_kwargs = {"device": os.environ.get("EMBED_DEVICE", "cpu")}
try:
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=embed_model_name,
        model_kwargs=embed_model_kwargs
    )
    print(f"Using embedding model: {embed_model_name} (device={embed_model_kwargs['device']})")
except TypeError:
    # Certaines versions de la classe n'acceptent pas model_kwargs
    Settings.embed_model = HuggingFaceEmbedding(model_name=embed_model_name)
    print(f"Using embedding model: {embed_model_name} (no model_kwargs support)")
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
        
    return index.as_chat_engine(
        chat_mode="context", 
        verbose=True  # Pratique pour voir ce que fait l'IA dans le terminal
    )


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