import os
from db_cofre import conectar_mongo
from seguranca_cofre import gerar_chave, criar_fernet, criptografar_texto, descriptografar_texto, gerar_hash_sha256

colecao = conectar_mongo()

def carregar_ou_criar_chave():
    if os.path.exists("chave_cofre.key"):
        with open("chave_cofre.key", "rb") as f:
            return f.read()
    else:
        chave = gerar_chave()
        with open("chave_cofre.key", "wb") as f:
            f.write(chave)
        return chave

chave = carregar_ou_criar_chave()
fernet = criar_fernet(chave)

def guardar_documento(nome: str, conteudo: str):
    conteudo_bytes = conteudo.encode()
    conteudo_cript = criptografar_texto(conteudo, fernet)
    hash_sha = gerar_hash_sha256(conteudo_bytes)
    
    colecao.insert_one({
        "nome_documento": nome,
        "conteudo_criptografado": conteudo_cript,
        "hash_sha256": hash_sha
    })
    
    print(f"\ndocumento '{nome}' armazenado com sucesso.")
    print(f"hash registrado: {hash_sha}\n" + "-"*40)

def ler_documento(nome: str):
    doc = colecao.find_one({"nome_documento": {"$regex": f"^{nome}$", "$options": "i"}})
    if not doc:
        print("\ndocumento não encontrado.\n" + "-"*40)
        return
    conteudo_cript = doc["conteudo_criptografado"]
    conteudo = descriptografar_texto(conteudo_cript, fernet)
    hash_calculado = gerar_hash_sha256(conteudo.encode())
    
    print(f"\ndocumento: {nome}")
    print(f"conteúdo: {conteudo}")
    print(f"hash armazenado: {doc['hash_sha256']}")
    print(f"hash atual: {hash_calculado}")
    if hash_calculado == doc["hash_sha256"]:
        print("integridade confirmada e não repúdio garantido.\n" + "-"*40)
    else:
        print("falha de integridade: documento alterado.\n" + "-"*40)

while True:
    print("\n" + "="*48)
    print("cofre de notas e documentos")
    print("="*48)
    escolha = input("guardar (g) / ler (l) / sair (s)? ").lower().strip()
    
    if escolha == "g":
        nome = input("nome do documento: ").strip()
        conteudo = input("conteúdo do documento: ").strip()
        guardar_documento(nome, conteudo)
    elif escolha == "l":
        nome = input("nome do documento: ").strip()
        ler_documento(nome)
    elif escolha == "s":
        print("\nencerrando cofre de documentos.")
        break
    else:
        print("\nopção inválida. tente novamente.\n" + "-"*40)
