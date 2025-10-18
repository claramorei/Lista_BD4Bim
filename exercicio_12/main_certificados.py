import os
from db_certificados import conectar_mongo
from seguranca_certificados import gerar_chave, criar_fernet, criptografar_certificado, descriptografar_certificado, gerar_hash_sha512

colecao = conectar_mongo()

def carregar_ou_criar_chave():
    if os.path.exists("chave_certificados.key"):
        with open("chave_certificados.key", "rb") as f:
            return f.read()
    else:
        chave = gerar_chave()
        with open("chave_certificados.key", "wb") as f:
            f.write(chave)
        return chave

chave = carregar_ou_criar_chave()
fernet = criar_fernet(chave)

def armazenar_certificado(nome: str, conteudo: str):
    conteudo_bytes = conteudo.encode()
    conteudo_cript = criptografar_certificado(conteudo, fernet)
    hash_cert = gerar_hash_sha512(conteudo_bytes)

    colecao.insert_one({
        "nome_certificado": nome,
        "conteudo_criptografado": conteudo_cript,
        "hash_sha512": hash_cert
    })
    print(f"\ncertificado '{nome}' armazenado com sucesso.\nhash: {hash_cert}\n" + "-"*40)

def verificar_certificado(nome: str):
    doc = colecao.find_one({"nome_certificado": {"$regex": f"^{nome}$", "$options": "i"}})
    if not doc:
        print("\ncertificado não encontrado.\n" + "-"*40)
        return

    conteudo_cript = doc["conteudo_criptografado"]
    conteudo = descriptografar_certificado(conteudo_cript, fernet)
    hash_atual = gerar_hash_sha512(conteudo.encode())

    print(f"\ncertificado: {nome}")
    print(f"hash armazenado: {doc['hash_sha512']}")
    print(f"hash atual: {hash_atual}")
    if hash_atual == doc["hash_sha512"]:
        print("autenticidade confirmada.\n" + "-"*40)
    else:
        print("falha de autenticidade detectada!\n" + "-"*40)

while True:
    print("\n" + "="*48)
    print("repositorio de certificados digitais")
    print("="*48)
    escolha = input("armazenar (a) / verificar (v) / sair (s)? ").lower().strip()

    if escolha == "a":
        nome = input("nome do certificado: ").strip()
        conteudo = input("conteudo do certificado: ").strip()
        armazenar_certificado(nome, conteudo)
    elif escolha == "v":
        nome = input("nome do certificado: ").strip()
        verificar_certificado(nome)
    elif escolha == "s":
        print("\nencerrando repositorio de certificados.")
        break
    else:
        print("\nopcao invalida. tente novamente.\n" + "-"*40)
