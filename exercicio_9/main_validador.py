from db_validador import conectar_mongo
from seguranca_validador import gerar_hash_sha512_registro
import datetime

colecao = conectar_mongo()

def inserir_registro(dados: dict):
   
    registro = dados.copy()
    registro["data_insercao"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    registro["hash"] = gerar_hash_sha512_registro(registro)
    colecao.insert_one(registro)
    print("\nregistro inserido com hash calculado.\n" + "-"*40)

def listar_registros():
    registros = colecao.find()
    encontrou = False
    for r in registros:
        encontrou = True
        print(f"\nid: {r['_id']}")
        print(f"data insercao: {r['data_insercao']}")
        print(f"hash: {r['hash']}")
        print(f"conteudo: {{ {', '.join(f'{k}: {v}' for k, v in r.items() if k not in ['_id','hash','data_insercao'])} }}")
        print("-"*40)
    if not encontrou:
        print("\nnenhum registro encontrado.\n" + "-"*40)

def validar_integridade():
    registros = colecao.find()
    encontrou = False
    for r in registros:
        encontrou = True
        hash_atual = gerar_hash_sha512_registro(r)
        if hash_atual == r["hash"]:
            print(f"id {r['_id']}: integridade ok")
        else:
            print(f"id {r['_id']}: falha de integridade! hash armazenado != hash atual")
    if not encontrou:
        print("\nnenhum registro para validar.\n" + "-"*40)

while True:
    print("\n" + "="*48)
    print("validador de integridade de banco de dados")
    print("="*48)
    escolha = input("inserir registro (i) / listar registros (l) / validar (v) / sair (s)? ").lower().strip()

    if escolha == "i":
        dados_raw = input("digite os dados do registro como json (ex: {\"campo1\":\"valor1\"}): ").strip()
        try:
            import json
            dados = json.loads(dados_raw)
            inserir_registro(dados)
        except Exception as e:
            print(f"\nentrada inválida: {e}\n" + "-"*40)
    elif escolha == "l":
        listar_registros()
    elif escolha == "v":
        validar_integridade()
    elif escolha == "s":
        print("\nencerrando validador de integridade.")
        break
    else:
        print("\nopção inválida. tente novamente.\n" + "-"*40)
