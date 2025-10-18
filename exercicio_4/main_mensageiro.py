import os
from db_mensageiro import conectar_mongo
from seguranca_mensageiro import gerar_chave, criar_fernet, criptografar_mensagem, descriptografar_mensagem

colecao = conectar_mongo()

def carregar_ou_criar_chave(usuario: str):
    nome_arquivo = f"chave_{usuario}.key"
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "rb") as f:
            return f.read()
    else:
        chave = gerar_chave()
        with open(nome_arquivo, "wb") as f:
            f.write(chave)
        return chave

def enviar_mensagem(remetente: str, destinatario: str, texto: str):
    chave = carregar_ou_criar_chave(destinatario)
    fernet = criar_fernet(chave)
    mensagem_cript = criptografar_mensagem(texto, fernet)

    colecao.insert_one({
        "remetente": remetente,
        "destinatario": destinatario,
        "mensagem_criptografada": mensagem_cript
    })

    print(f"\nmensagem enviada de '{remetente}' para '{destinatario}'.\n" + "-"*40)

def ler_mensagens(usuario: str):
    chave = carregar_ou_criar_chave(usuario)
    fernet = criar_fernet(chave)

    mensagens = colecao.find({"destinatario": {"$regex": f"^{usuario}$", "$options": "i"}})
    encontrou = False

    for msg in mensagens:
        encontrou = True
        remetente = msg["remetente"]
        conteudo = descriptografar_mensagem(msg["mensagem_criptografada"], fernet)
        print(f"\nde {remetente}: {conteudo}\n" + "-"*40)

    if not encontrou:
        print("\nnenhuma mensagem encontrada.\n" + "-"*40)

while True:
    print("\n" + "="*48)
    print("mensageiro criptografado com fernet")
    print("="*48)
    escolha = input("enviar (e) / ler (l) / sair (s)? ").lower().strip()

    if escolha == "e":
        remetente = input("remetente: ").strip()
        destinatario = input("destinatário: ").strip()
        texto = input("mensagem: ").strip()
        enviar_mensagem(remetente, destinatario, texto)
    elif escolha == "l":
        usuario = input("usuário que vai ler as mensagens: ").strip()
        ler_mensagens(usuario)
    elif escolha == "s":
        print("\nencerrando mensageiro.")
        break
    else:
        print("\nopção inválida. tente novamente.\n" + "-"*40)
