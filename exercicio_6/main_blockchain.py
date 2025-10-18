import datetime
from db_blockchain import conectar_mongo
from blockchain_cripto import calcular_hash

colecao = conectar_mongo()

def obter_ultimo_bloco():
    ultimo = colecao.find_one(sort=[("index", -1)])
    return ultimo

def criar_bloco(dados: str):
    ultimo = obter_ultimo_bloco()
    if ultimo:
        index = ultimo["index"] + 1
        prev_hash = ultimo["hash"]
    else:
        index = 0
        prev_hash = "0" * 64

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    bloco = {
        "index": index,
        "timestamp": timestamp,
        "dados": dados,
        "prev_hash": prev_hash
    }
    bloco["hash"] = calcular_hash(bloco)
    colecao.insert_one(bloco)
    print(f"\nbloco {index} criado e armazenado.")
    print(f"hash: {bloco['hash']}\n" + "-"*40)

def listar_blocos():
    blocos = colecao.find().sort("index", 1)
    encontrou = False
    for b in blocos:
        encontrou = True
        print(f"\nindex: {b['index']}")
        print(f"timestamp: {b['timestamp']}")
        print(f"dados: {b['dados']}")
        print(f"prev_hash: {b['prev_hash']}")
        print(f"hash: {b['hash']}")
        print("-"*40)
    if not encontrou:
        print("\nnenhum bloco encontrado.\n" + "-"*40)

def validar_cadeia() -> bool:
    blocos = list(colecao.find().sort("index", 1))
    if not blocos:
        print("\ncadeia vazia (não há blocos para validar).\n" + "-"*40)
        return True

    for i in range(len(blocos)):
        bloco = blocos[i]
        calculado = calcular_hash(bloco)
        if bloco["hash"] != calculado:
            print(f"\nfalha: hash inválido no bloco index {bloco['index']}.")
            print(f"hash armazenado: {bloco['hash']}")
            print(f"hash calculado:  {calculado}\n" + "-"*40)
            return False
        if i > 0:
            prev = blocos[i-1]
            if bloco["prev_hash"] != prev["hash"]:
                print(f"\nfalha: prev_hash inconsistente no bloco index {bloco['index']}.")
                print(f"prev_hash armazenado: {bloco['prev_hash']}")
                print(f"hash do bloco anterior: {prev['hash']}\n" + "-"*40)
                return False
    print("\ncadeia válida. imutabilidade preservada.\n" + "-"*40)
    return True

while True:
    print("\n" + "="*48)
    print("blockchain simplificada")
    print("="*48)
    escolha = input("adicionar bloco (a) / listar (l) / validar (v) / sair (s)? ").lower().strip()

    if escolha == "a":
        dados = input("dados para o bloco: ").strip()
        criar_bloco(dados)
    elif escolha == "l":
        listar_blocos()
    elif escolha == "v":
        validar_cadeia()
    elif escolha == "s":
        print("\nencerrando blockchain.")
        break
    else:
        print("\nopção inválida. tente novamente.\n" + "-"*40)
