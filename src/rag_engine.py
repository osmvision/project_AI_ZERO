from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os
from pathlib import Path

# --- CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent.parent
# On utilise /tmp pour éviter les erreurs de permission sur Hugging Face
STORAGE_DIR = Path("/tmp/storage") 
DATA_DIR = BASE_DIR / "data"

def setup_rag_engine():
    print("🛠️ Configuration RAG (Mode Éco-Mémoire)...")

    # 1. EMBEDDING (Vecteurs)
    print("   -> Chargement Embedding BAAI/bge-small-en-v1.5...")
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5",
        cache_folder="/app/hf_cache"
    )

    # 2. LLM (Cerveau)
    # CRITIQUE: On force context_window=2048 pour ne pas exploser la RAM
    print("   -> Connexion à Ollama (phi3) avec limite 2k...")
    Settings.llm = Ollama(
        model="phi3", 
        request_timeout=300.0,
        context_window=2048,  # <--- LA CLÉ EST ICI
        additional_kwargs={"num_ctx": 2048} # Double sécurité
    )

    # 3. INDEXATION
    if not STORAGE_DIR.exists():
        os.makedirs(STORAGE_DIR)

    if (STORAGE_DIR / "docstore.json").exists():
        print("✅ Index existant trouvé. Chargement...")
        try:
            storage_context = StorageContext.from_defaults(persist_dir=str(STORAGE_DIR))
            return load_index_from_storage(storage_context).as_chat_engine()
        except Exception:
            print("⚠️ Index corrompu, reconstruction...")

    if not DATA_DIR.exists():
        os.makedirs(DATA_DIR)
        documents = []
    else:
        try:
            documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()
        except Exception:
            documents = []

    if not documents:
        index = VectorStoreIndex.from_documents([])
    else:
        index = VectorStoreIndex.from_documents(documents)
        try:
            index.storage_context.persist(persist_dir=str(STORAGE_DIR))
        except Exception:
            pass

    print("✅ RAG Engine prêt !")
    return index.as_chat_engine()