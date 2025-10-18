import os
from db_votacao import conectar_mongo
from seguranca_votacao import gerar_chave, criar_fernet, criptografar_voto, descriptografar_voto, gerar_hash_sha256

colecao = conectar_mongo()

def carregar_ou_criar_chave():
    if os.path.exists("chave_votacao.key"):
        with open("chave_votacao.key", "rb") as f:
            return f.read()
    else:
        chave = gerar_chave()
        with open("chave_votacao.key", "wb") as f:
            f.write(chave)
        return chave

chave = carregar_ou_criar_chave()
fernet = criar_fernet(chave)

def registrar_voto(eleitor: str, voto: str):
    voto_cript = criptografar_voto(voto, fernet)
    hash_voto = gerar_hash_sha256(voto.encode())
    
    colecao.insert_one({
        "eleitor": eleitor,
        "voto_criptografado": voto_cript,
        "hash_sha256": hash_voto
    })
    print(f"\nvoto registrado para '{eleitor}'. hash armazenado: {hash_voto}\n" + "-"*40)

def auditar_voto(eleitor: str):
    doc = colecao.find_one({"eleitor": {"$regex": f"^{eleitor}$", "$options": "i"}})
    if not doc:
        print("\neleitor não encontrado.\n" + "-"*40)
        return
    voto_cript = doc["voto_criptografado"]
    voto = descriptografar_voto(voto_cript, fernet)
    hash_atual = gerar_hash_sha256(voto.encode())

    print(f"\nvoto do eleitor '{eleitor}': {voto}")
    print(f"hash armazenado: {doc['hash_sha256']}")
    print(f"hash atual: {hash_atual}")
    if hash_atual == doc["hash_sha256"]:
        print("integridade confirmada.\n" + "-"*40)
    else:
        print("falha de integridade detectada!\n" + "-"*40)

while True:
    print("\n" + "="*48)
    print("sistema de votação eletrônica segura")
    print("="*48)
    escolha = input("registrar voto (r) / auditar voto (a) / sair (s)? ").lower().strip()

    if escolha == "r":
        eleitor = input("nome do eleitor: ").strip()
        voto = input("voto: ").strip()
        registrar_voto(eleitor, voto)
    elif escolha == "a":
        eleitor = input("nome do eleitor para auditoria: ").strip()
        auditar_voto(eleitor)
    elif escolha == "s":
        print("\nencerrando sistema de votação.")
        break
    else:
        print("\nopção inválida. tente novamente.\n" + "-"*40)
