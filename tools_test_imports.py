import sys, importlib, traceback
print('Python', sys.version)
modules = [
    'torch',
    'transformers',
    'huggingface_hub',
    'llama_index.embeddings.huggingface',
    'llama_index',
    'sentence_transformers'
]
for m in modules:
    print('\n--- testing', m)
    try:
        mod = importlib.import_module(m)
        ver = getattr(mod, '__version__', None)
        print(f'{m}: OK, version={ver}')
    except Exception as e:
        print(f'{m}: ERROR ->', e)
        traceback.print_exc()
print('\n--- end of checks')
