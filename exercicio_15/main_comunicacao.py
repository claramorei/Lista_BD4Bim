import os
from db_comunicacao import conectar_mongo
from seguranca_comunicacao import gerar_chave, criar_fernet, criptografar_mensagem, descriptografar_mensagem, gerar_hash_sha256

colecao = conectar_mongo()

def carregar_ou_criar_chave():
    if os.path.exists("chave_comunicacao.key"):
        with open("chave_comunicacao.key", "rb") as f:
            return f.read()
    else:
        chave = gerar_chave()
        with open("chave_comunicacao.key", "wb") as f:
            f.write(chave)
        return chave

chave = carregar_ou_criar_chave()
fernet = criar_fernet(chave)

def enviar_mensagem(remetente: str, destinatario: str, conteudo: str):
    conteudo_cript = criptografar_mensagem(conteudo, fernet)
    hash_msg = gerar_hash_sha256(conteudo.encode())

    colecao.insert_one({
        "remetente": remetente,
        "destinatario": destinatario,
        "mensagem_criptografada": conteudo_cript,
        "hash_sha256": hash_msg
    })

    print(f"\nmensagem enviada com hash: {hash_msg}\n" + "-"*40)

def receber_mensagem(destinatario: str):
    msgs = colecao.find({"destinatario": {"$regex": f"^{destinatario}$", "$options": "i"}})
    encontrou = False
    for m in msgs:
        encontrou = True
        conteudo_cript = m["mensagem_criptografada"]
        conteudo = descriptografar_mensagem(conteudo_cript, fernet)
        hash_atual = gerar_hash_sha256(conteudo.encode())
        print(f"\nremetente: {m['remetente']}")
        print(f"mensagem: {conteudo}")
        print(f"hash armazenado: {m['hash_sha256']}")
        print(f"hash atual: {hash_atual}")
        print("-"*40)
    if not encontrou:
        print("\nnenhuma mensagem para este destinatario.\n" + "-"*40)

while True:
    print("\n" + "="*48)
    print("sistema de comunicacao cliente-servidor criptografado")
    print("="*48)
    escolha = input("enviar (e) / receber (r) / sair (s)? ").lower().strip()

    if escolha == "e":
        remetente = input("remetente: ").strip()
        destinatario = input("destinatario: ").strip()
        conteudo = input("mensagem: ").strip()
        enviar_mensagem(remetente, destinatario, conteudo)
    elif escolha == "r":
        destinatario = input("destinatario: ").strip()
        receber_mensagem(destinatario)
    elif escolha == "s":
        print("\nencerrando sistema de comunicacao.")
        break
    else:
        print("\nopcao invalida. tente novamente.\n" + "-"*40)
