import hashlib
from cryptography.fernet import Fernet

def gerar_chave():
    return Fernet.generate_key()

def criar_fernet(chave: bytes):
    return Fernet(chave)

def criptografar_arquivo(caminho_arquivo: str, fernet: Fernet) -> bytes:
    with open(caminho_arquivo, "rb") as f:
        dados = f.read()
    return fernet.encrypt(dados)

def descriptografar_arquivo(dados_cript: bytes, fernet: Fernet, destino: str):
    dados = fernet.decrypt(dados_cript)
    with open(destino, "wb") as f:
        f.write(dados)

def gerar_hash_sha256(dados: bytes) -> str:
    return hashlib.sha256(dados).hexdigest()
