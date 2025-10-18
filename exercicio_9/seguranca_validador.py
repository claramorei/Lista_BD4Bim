import hashlib
import json

def gerar_hash_sha512_registro(registro: dict) -> str:
    
    registro_para_hash = {k: v for k, v in registro.items() if k != "hash"}
    registro_json = json.dumps(registro_para_hash, sort_keys=True).encode()
    return hashlib.sha512(registro_json).hexdigest()
