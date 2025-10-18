import hashlib

def gerar_hash_sha512(caminho_arquivo: str) -> str:
    hash_obj = hashlib.sha512()
    with open(caminho_arquivo, "rb") as f:
        for bloco in iter(lambda: f.read(4096), b""):
            hash_obj.update(bloco)
    return hash_obj.hexdigest()

def comparar_hashes(hash_armazenado: str, hash_atual: str) -> bool:
    return hash_armazenado == hash_atual
