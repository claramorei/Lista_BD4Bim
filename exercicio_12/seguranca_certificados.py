from cryptography.fernet import Fernet
import hashlib

def gerar_chave():
    return Fernet.generate_key()

def criar_fernet(chave: bytes):
    return Fernet(chave)

def criptografar_certificado(certificado: str, fernet: Fernet) -> bytes:
    return fernet.encrypt(certificado.encode())

def descriptografar_certificado(certificado_cript: bytes, fernet: Fernet) -> str:
    return fernet.decrypt(certificado_cript).decode()

def gerar_hash_sha512(conteudo_bytes: bytes) -> str:
    hash_obj = hashlib.sha512()
    hash_obj.update(conteudo_bytes)
    return hash_obj.hexdigest()
