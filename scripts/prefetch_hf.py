#!/usr/bin/env python3
"""Simple helper to pre-download a HuggingFace model repository into the cache.
Usage:
  set HUGGINGFACE_HUB_TOKEN=... (Windows PowerShell)
  set EMBED_MODEL=BAAI/bge-small-en-v1.5
  python scripts/prefetch_hf.py
"""
import os
import traceback
from huggingface_hub import snapshot_download, HFValidationError

model = os.environ.get("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
token = os.environ.get("HUGGINGFACE_HUB_TOKEN")

print(f"Prefetching HuggingFace model: {model}")
try:
  path = snapshot_download(repo_id=model, token=token)
  print(f"Model downloaded to: {path}")
except HFValidationError as e:
  print("HFValidationError: likely bad repo id or access issue:")
  print(e)
  raise
except Exception as e:
  print("Unexpected error downloading model:")
  traceback.print_exc()
  raise
