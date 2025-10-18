import hashlib

def gerar_hash_biometrico(dado_biometrico: str) -> str:
   
    hash_obj = hashlib.sha256()
    hash_obj.update(dado_biometrico.encode())
    return hash_obj.hexdigest()
