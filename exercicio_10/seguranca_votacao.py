from cryptography.fernet import Fernet
import hashlib

def gerar_chave():
    return Fernet.generate_key()

def criar_fernet(chave: bytes):
    return Fernet(chave)

def criptografar_voto(voto: str, fernet: Fernet) -> bytes:
    return fernet.encrypt(voto.encode())

def descriptografar_voto(voto_cript: bytes, fernet: Fernet) -> str:
    return fernet.decrypt(voto_cript).decode()

def gerar_hash_sha256(conteudo_bytes: bytes) -> str:
    hash_obj = hashlib.sha256()
    hash_obj.update(conteudo_bytes)
    return hash_obj.hexdigest()
