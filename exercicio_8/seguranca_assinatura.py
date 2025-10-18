from cryptography.fernet import Fernet
import hashlib

def gerar_chave():
    return Fernet.generate_key()

def criar_fernet(chave: bytes):
    return Fernet(chave)

def gerar_hash_sha256_texto(texto: str) -> str:
    return hashlib.sha256(texto.encode()).hexdigest()

def assinar_mensagem(fernet: Fernet, mensagem: str) -> bytes:
   
    resumo = gerar_hash_sha256_texto(mensagem)
    return fernet.encrypt(resumo.encode())

def verificar_assinatura(fernet: Fernet, mensagem: str, assinatura: bytes) -> bool:
  
    try:
        resumo_descript = fernet.decrypt(assinatura).decode()
    except Exception:
        return False
    resumo_atual = gerar_hash_sha256_texto(mensagem)
    return resumo_descript == resumo_atual
