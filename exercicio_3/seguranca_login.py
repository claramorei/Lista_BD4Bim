import os
import hashlib
import base64

def gerar_salt() -> str:
    salt_bytes = os.urandom(16)
    return base64.b64encode(salt_bytes).decode()

def gerar_hash_senha(senha: str, salt: str) -> str:
    combinacao = (senha + salt).encode()
    return hashlib.sha256(combinacao).hexdigest()

def verificar_senha(senha_digitada: str, salt_armazenado: str, hash_armazenado: str) -> bool:
    hash_teste = gerar_hash_senha(senha_digitada, salt_armazenado)
    return hash_teste == hash_armazenado
