import hashlib
import json

def calcular_hash(bloco: dict) -> str:

    bloco_para_hash = {
        "index": bloco["index"],
        "timestamp": bloco["timestamp"],
        "dados": bloco["dados"],
        "prev_hash": bloco["prev_hash"]
    }
    bloco_json = json.dumps(bloco_para_hash, sort_keys=True).encode()
    return hashlib.sha256(bloco_json).hexdigest()
