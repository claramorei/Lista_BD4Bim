from cryptography.fernet import Fernet
import hashlib

def gerar_chave():
    return Fernet.generate_key()

def criar_fernet(chave: bytes):
    return Fernet(chave)

def criptografar_texto(texto: str, fernet: Fernet) -> bytes:
    return fernet.encrypt(texto.encode())

def descriptografar_texto(texto_cript: bytes, fernet: Fernet) -> str:
    return fernet.decrypt(texto_cript).decode()

def gerar_hash_sha256(texto: str) -> str:
    hash_obj = hashlib.sha256()
    hash_obj.update(texto.encode())
    return hash_obj.hexdigest()
