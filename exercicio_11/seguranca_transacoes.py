import hashlib
import json

def gerar_hash_sha256(transacao: dict) -> str:
    transacao_json = json.dumps(transacao, sort_keys=True).encode()
    return hashlib.sha256(transacao_json).hexdigest()
