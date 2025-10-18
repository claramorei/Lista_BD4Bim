from db_biometrico import conectar_mongo
from seguranca_biometrico import gerar_hash_biometrico

colecao = conectar_mongo()

def registrar_usuario(nome: str, dado_biometrico: str):
    hash_bio = gerar_hash_biometrico(dado_biometrico)
    colecao.insert_one({
        "nome": nome,
        "hash_biometrico": hash_bio
    })
    print(f"\nusuario '{nome}' registrado com hash biometrico.\n" + "-"*40)

def autenticar_usuario(nome: str, dado_biometrico: str):
    doc = colecao.find_one({"nome": {"$regex": f"^{nome}$", "$options": "i"}})
    if not doc:
        print("\nusuario não encontrado.\n" + "-"*40)
        return

    hash_atual = gerar_hash_biometrico(dado_biometrico)
    if hash_atual == doc["hash_biometrico"]:
        print("\nautenticacao bem-sucedida.\n" + "-"*40)
    else:
        print("\nautenticacao falhou. hash nao corresponde.\n" + "-"*40)

while True:
    print("\n" + "="*48)
    print("cofre biometrico")
    print("="*48)
    escolha = input("registrar usuario (r) / autenticar (a) / sair (s)? ").lower().strip()

    if escolha == "r":
        nome = input("nome do usuario: ").strip()
        dado = input("dado biometrico (simulado): ").strip()
        registrar_usuario(nome, dado)
    elif escolha == "a":
        nome = input("nome do usuario: ").strip()
        dado = input("dado biometrico (simulado): ").strip()
        autenticar_usuario(nome, dado)
    elif escolha == "s":
        print("\nencerrando cofre biometrico.")
        break
    else:
        print("\nopcao invalida. tente novamente.\n" + "-"*40)
