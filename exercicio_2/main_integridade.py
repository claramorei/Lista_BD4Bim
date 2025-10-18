import os
from db_integridade import conectar_mongo
from hash_integridade import gerar_hash_sha512, comparar_hashes

colecao = conectar_mongo()

def registrar_arquivo(caminho_arquivo: str):
    if not os.path.exists(caminho_arquivo):
        print("\narquivo não encontrado.\n" + "-"*40)
        return

    nome_arquivo = os.path.basename(caminho_arquivo)
    hash_arquivo = gerar_hash_sha512(caminho_arquivo)

    colecao.insert_one({
        "nome_arquivo": nome_arquivo,
        "hash_sha512": hash_arquivo
    })

    print(f"\narquivo '{nome_arquivo}' registrado com sucesso.")
    print(f"hash sha-512: {hash_arquivo}\n" + "-"*40)

def verificar_arquivo(caminho_arquivo: str):
    if not os.path.exists(caminho_arquivo):
        print("\narquivo não encontrado.\n" + "-"*40)
        return

    nome_arquivo = os.path.basename(caminho_arquivo)
    doc = colecao.find_one({"nome_arquivo": {"$regex": f"^{nome_arquivo}$", "$options": "i"}})
    if not doc:
        print("\narquivo não registrado no banco.\n" + "-"*40)
        return

    hash_atual = gerar_hash_sha512(caminho_arquivo)
    hash_armazenado = doc["hash_sha512"]

    print(f"\narquivo: {nome_arquivo}")
    print(f"hash armazenado: {hash_armazenado}")
    print(f"hash atual:      {hash_atual}")

    if comparar_hashes(hash_armazenado, hash_atual):
        print("integridade preservada.\n" + "-"*40)
    else:
        print("integridade comprometida (arquivo foi alterado).\n" + "-"*40)

while True:
    print("\n" + "="*48)
    print("verificador de integridade de arquivos")
    print("="*48)
    escolha = input("registrar (r) / verificar (v) / sair (s)? ").lower().strip()

    if escolha == "r":
        caminho = input("caminho completo do arquivo: ").strip()
        registrar_arquivo(caminho)
    elif escolha == "v":
        caminho = input("caminho completo do arquivo: ").strip()
        verificar_arquivo(caminho)
    elif escolha == "s":
        print("\nencerrando verificador.")
        break
    else:
        print("\nopção inválida. tente novamente.\n" + "-"*40)
