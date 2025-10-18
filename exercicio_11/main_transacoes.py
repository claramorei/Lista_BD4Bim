from db_transacoes import conectar_mongo
from seguranca_transacoes import gerar_hash_sha256
import datetime
import json

colecao = conectar_mongo()

def registrar_transacao(transacao: dict):
    transacao = transacao.copy()
    transacao["data_registro"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transacao["hash"] = gerar_hash_sha256(transacao)
    colecao.insert_one(transacao)
    print(f"\ntransacao registrada com hash: {transacao['hash']}\n" + "-"*40)

def listar_transacoes():
    transacoes = colecao.find()
    encontrou = False
    for t in transacoes:
        encontrou = True
        print(f"\nid: {t['_id']}")
        print(f"data_registro: {t['data_registro']}")
        print(f"hash: {t['hash']}")
        print(f"conteudo: {{ {', '.join(f'{k}: {v}' for k,v in t.items() if k not in ['_id','hash','data_registro'])} }}")
        print("-"*40)
    if not encontrou:
        print("\nnenhuma transacao encontrada.\n" + "-"*40)

def validar_integridade():
    transacoes = colecao.find()
    encontrou = False
    for t in transacoes:
        encontrou = True
        hash_atual = gerar_hash_sha256(t)
        if hash_atual == t["hash"]:
            print(f"id {t['_id']}: integridade ok")
        else:
            print(f"id {t['_id']}: falha de integridade! hash armazenado != hash atual")
    if not encontrou:
        print("\nnenhuma transacao para validar.\n" + "-"*40)

while True:
    print("\n" + "="*48)
    print("api de registro de transacoes seguras")
    print("="*48)
    escolha = input("registrar transacao (r) / listar (l) / validar (v) / sair (s)? ").lower().strip()

    if escolha == "r":
        dados_raw = input("digite os dados da transacao como json (ex: {\"campo1\":\"valor1\"}): ").strip()
        try:
            transacao = json.loads(dados_raw)
            registrar_transacao(transacao)
        except Exception as e:
            print(f"\nentrada inválida: {e}\n" + "-"*40)
    elif escolha == "l":
        listar_transacoes()
    elif escolha == "v":
        validar_integridade()
    elif escolha == "s":
        print("\nencerrando registro de transacoes.")
        break
    else:
        print("\nopção inválida. tente novamente.\n" + "-"*40)
