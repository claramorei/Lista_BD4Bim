import os
from db_rastreamento import conectar_mongo
from seguranca_rastreamento import gerar_chave, criar_fernet, gerar_hash_sha256_bytes, assinar_hash, verificar_assinatura_hash

colecao = conectar_mongo()

def carregar_ou_criar_chave():
    if os.path.exists("chave_rastreamento.key"):
        with open("chave_rastreamento.key", "rb") as f:
            return f.read()
    else:
        chave = gerar_chave()
        with open("chave_rastreamento.key", "wb") as f:
            f.write(chave)
        return chave

chave = carregar_ou_criar_chave()
fernet = criar_fernet(chave)

def enviar_arquivo(nome: str, conteudo: str):
    conteudo_bytes = conteudo.encode()
    hash_arquivo = gerar_hash_sha256_bytes(conteudo_bytes)
    assinatura = assinar_hash(fernet, hash_arquivo)

    colecao.insert_one({
        "nome_arquivo": nome,
        "conteudo": conteudo_bytes,
        "hash_sha256": hash_arquivo,
        "assinatura": assinatura
    })

    print(f"\narquivo '{nome}' registrado com hash e assinatura.\n" + "-"*40)

def verificar_arquivo(nome: str):
    doc = colecao.find_one({"nome_arquivo": {"$regex": f"^{nome}$", "$options": "i"}})
    if not doc:
        print("\narquivo não encontrado.\n" + "-"*40)
        return

    hash_atual = gerar_hash_sha256_bytes(doc["conteudo"])
    if verificar_assinatura_hash(fernet, hash_atual, doc["assinatura"]):
        print(f"\narquivo '{nome}' íntegro. hash: {hash_atual}\n" + "-"*40)
    else:
        print(f"\narquivo '{nome}' adulterado! hash atual: {hash_atual}\n" + "-"*40)

while True:
    print("\n" + "="*48)
    print("sistema de rastreamento de arquivos")
    print("="*48)
    escolha = input("enviar arquivo (e) / verificar arquivo (v) / sair (s)? ").lower().strip()

    if escolha == "e":
        nome = input("nome do arquivo: ").strip()
        conteudo = input("conteudo do arquivo: ").strip()
        enviar_arquivo(nome, conteudo)
    elif escolha == "v":
        nome = input("nome do arquivo: ").strip()
        verificar_arquivo(nome)
    elif escolha == "s":
        print("\nencerrando sistema de rastreamento.")
        break
    else:
        print("\nopcao inválida. tente novamente.\n" + "-"*40)
