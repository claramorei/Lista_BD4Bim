from cryptography.fernet import Fernet
import hashlib

def gerar_chave():
    return Fernet.generate_key()

def criar_fernet(chave: bytes):
    return Fernet(chave)

def criptografar_mensagem(msg: str, fernet: Fernet) -> bytes:
    return fernet.encrypt(msg.encode())

def descriptografar_mensagem(msg_cript: bytes, fernet: Fernet) -> str:
    return fernet.decrypt(msg_cript).decode()

def gerar_hash_sha256(conteudo_bytes: bytes) -> str:
    hash_obj = hashlib.sha256()
    hash_obj.update(conteudo_bytes)
    return hash_obj.hexdigest()
