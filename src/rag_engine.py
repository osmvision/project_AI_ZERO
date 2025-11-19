from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os

def setup_rag_engine():
    print("🛠️ Initialisation du RAG Engine...")

    # 1. Configuration du modèle d'Embedding (Vectorisation)
    # On utilise le même modèle que celui pré-téléchargé dans le Dockerfile
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    # 2. Configuration du LLM (Cerveau)
    # CORRECTION ICI : On force l'utilisation de 'phi3' pour correspondre au boot.sh
    Settings.llm = Ollama(
        model="phi3", 
        request_timeout=300.0
    )

    # 3. Chargement des documents
    # On vérifie si le dossier data existe, sinon on crée un document vide pour éviter le crash
    data_path = "./data"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        
    # Chargement des données
    print(f"📂 Chargement des documents depuis {data_path}...")
    try:
        documents = SimpleDirectoryReader(data_path).load_data()
    except Exception as e:
        print(f"⚠️ Attention: Aucun document trouvé ou erreur de lecture: {e}")
        documents = []

    # Si aucun document, on crée un index vide, sinon on indexe les fichiers
    if not documents:
        index = VectorStoreIndex.from_documents([])
    else:
        index = VectorStoreIndex.from_documents(documents)

    # 4. Création du moteur de chat
    print("✅ RAG Engine prêt !")
    return index.as_chat_engine()