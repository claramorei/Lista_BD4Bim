import os
import datetime
from db_assinatura import conectar_mongo
from seguranca_assinatura import gerar_chave, criar_fernet, assinar_mensagem, verificar_assinatura, gerar_hash_sha256_texto

colecao = conectar_mongo()

def carregar_ou_criar_chave(usuario: str):
  
    nome_arquivo = f"chave_assinatura_{usuario}.key"
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "rb") as f:
            return f.read()
    else:
        chave = gerar_chave()
        with open(nome_arquivo, "wb") as f:
            f.write(chave)
        return chave

def enviar_mensagem_assinada(remetente: str, destinatario: str, mensagem: str):
    chave_rem = carregar_ou_criar_chave(remetente)
    fernet_rem = criar_fernet(chave_rem)
    assinatura = assinar_mensagem(fernet_rem, mensagem)
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    colecao.insert_one({
        "remetente": remetente,
        "destinatario": destinatario,
        "mensagem": mensagem,
        "assinatura": assinatura,
        "data_envio": data_hora
    })

    print(f"\nmensagem assinada enviada e registrada no banco.\n" + "-"*40)

def listar_mensagens(usuario: str = None):
   
    filtro = {}
    if usuario:
        filtro = {"$or": [{"remetente": {"$regex": f"^{usuario}$", "$options": "i"}},
                           {"destinatario": {"$regex": f"^{usuario}$", "$options": "i"}}]}
    mensagens = colecao.find(filtro).sort("data_envio", -1)
    encontrou = False
    for m in mensagens:
        encontrou = True
        print(f"\nid: {m['_id']}")
        print(f"data: {m.get('data_envio')}")
        print(f"remetente: {m.get('remetente')}")
        print(f"destinatario: {m.get('destinatario')}")
        print(f"mensagem: {m.get('mensagem')}")
        print(f"assinatura (bytes): {m.get('assinatura')[:30]}...") 
        print("-"*40)
    if not encontrou:
        print("\nnenhuma mensagem encontrada.\n" + "-"*40)

def verificar_mensagem(id_mensagem):
   
    from bson.objectid import ObjectId
    try:
        obj_id = ObjectId(id_mensagem)
    except Exception:
        print("\nid inválido.\n" + "-"*40)
        return

    doc = colecao.find_one({"_id": obj_id})
    if not doc:
        print("\nmensagem não encontrada.\n" + "-"*40)
        return

    remetente = doc["remetente"]
    mensagem = doc["mensagem"]
    assinatura = doc["assinatura"]

    chave_rem = carregar_ou_criar_chave(remetente)
    fernet_rem = criar_fernet(chave_rem)

    if verificar_assinatura(fernet_rem, mensagem, assinatura):
        resumo = gerar_hash_sha256_texto(mensagem)
        print("\nautenticidade confirmada: assinatura válida.")
        print(f"resumo (sha-256): {resumo}\n" + "-"*40)
    else:
        print("\nautenticidade inválida: assinatura não conferiu (mensagem possa ter sido alterada ou chave incorreta).\n" + "-"*40)

while True:
    print("\n" + "="*48)
    print("sistema de assinatura digital simulada")
    print("="*48)
    escolha = input("enviar (e) / listar (l) / verificar por id (v) / sair (s)? ").lower().strip()

    if escolha == "e":
        remetente = input("remetente: ").strip()
        destinatario = input("destinatario: ").strip()
        mensagem = input("mensagem: ").strip()
        enviar_mensagem_assinada(remetente, destinatario, mensagem)
    elif escolha == "l":
        usuario_filtro = input("filtrar por usuário (enter para todos): ").strip()
        listar_mensagens(usuario_filtro if usuario_filtro else None)
    elif escolha == "v":
        id_msg = input("id do documento mongodb: ").strip()
        verificar_mensagem(id_msg)
    elif escolha == "s":
        print("\nencerrando sistema de assinatura.")
        break
    else:
        print("\nopção inválida. tente novamente.\n" + "-"*40)
