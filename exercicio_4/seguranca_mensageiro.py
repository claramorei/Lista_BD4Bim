from cryptography.fernet import Fernet

def gerar_chave():
    return Fernet.generate_key()

def criar_fernet(chave: bytes):
    return Fernet(chave)

def criptografar_mensagem(mensagem: str, fernet: Fernet) -> bytes:
    return fernet.encrypt(mensagem.encode())

def descriptografar_mensagem(mensagem_cript: bytes, fernet: Fernet) -> str:
    return fernet.decrypt(mensagem_cript).decode()
