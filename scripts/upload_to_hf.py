#!/usr/bin/env python3
"""
Script pour téléverser le projet sur le Hub Hugging Face.

Usage :
  1. Assurez-vous d'être connecté : `huggingface-cli login`
  2. Exécutez le script : `python scripts/upload_to_hf.py`
"""
import os
from huggingface_hub import HfApi, HfFolder


def upload_project_to_hf():
    """Téléverse les fichiers importants du projet sur le Hub Hugging Face."""
    repo_id = "osmvision/project_Zero_AI"
    api = HfApi()
    token = HfFolder.get_token()
    if not token:
        print("❌ Token Hugging Face non trouvé. Veuillez vous connecter via 'huggingface-cli login'.")
        return

    print(f"🚀 Téléversement du projet vers le dépôt : {repo_id}")
    api.upload_folder(
        folder_path=".",
        repo_id=repo_id,
        repo_type="space",  # ou "model" si vous préférez
        allow_patterns=["src/*.py", "scripts/*.py", "*.txt", "*.md", "requirements.txt", "main.py"],
        ignore_patterns=["storage/*", "data/*", ".env", "__pycache__/", "*.pyc"]
    )
    print("✅ Téléversement terminé !")

if __name__ == "__main__":
    upload_project_to_hf()