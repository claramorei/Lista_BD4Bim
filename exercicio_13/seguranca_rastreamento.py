from cryptography.fernet import Fernet
import hashlib

def gerar_chave():
    return Fernet.generate_key()

def criar_fernet(chave: bytes):
    return Fernet(chave)

def gerar_hash_sha256_bytes(conteudo_bytes: bytes) -> str:
    hash_obj = hashlib.sha256()
    hash_obj.update(conteudo_bytes)
    return hash_obj.hexdigest()

def assinar_hash(fernet: Fernet, hash_str: str) -> bytes:
    return fernet.encrypt(hash_str.encode())

def verificar_assinatura_hash(fernet: Fernet, hash_str: str, assinatura: bytes) -> bool:
    try:
        hash_descript = fernet.decrypt(assinatura).decode()
    except Exception:
        return False
    return hash_str == hash_descript
