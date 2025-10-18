from db_login import conectar_mongo
from seguranca_login import gerar_salt, gerar_hash_senha, verificar_senha

colecao = conectar_mongo()

def cadastrar_usuario(usuario: str, senha: str):
    salt = gerar_salt()
    hash_senha = gerar_hash_senha(senha, salt)

    colecao.insert_one({
        "usuario": usuario,
        "salt": salt,
        "hash_senha": hash_senha
    })

    print(f"\nusuário '{usuario}' cadastrado com sucesso.")
    print(f"salt: {salt}")
    print(f"hash: {hash_senha}\n" + "-"*40)

def autenticar_usuario(usuario: str, senha_digitada: str):
    doc = colecao.find_one({"usuario": {"$regex": f"^{usuario}$", "$options": "i"}})
    if not doc:
        print("\nusuário não encontrado.\n" + "-"*40)
        return

    salt = doc["salt"]
    hash_armazenado = doc["hash_senha"]

    if verificar_senha(senha_digitada, salt, hash_armazenado):
        print("\nautenticação bem-sucedida.\n" + "-"*40)
    else:
        print("\nsenha incorreta. acesso negado.\n" + "-"*40)

while True:
    print("\n" + "="*48)
    print("sistema de login seguro com salt e hash")
    print("="*48)
    escolha = input("cadastrar (c) / autenticar (a) / sair (s)? ").lower().strip()

    if escolha == "c":
        usuario = input("usuário: ").strip()
        senha = input("senha: ").strip()
        cadastrar_usuario(usuario, senha)
    elif escolha == "a":
        usuario = input("usuário: ").strip()
        senha = input("senha: ").strip()
        autenticar_usuario(usuario, senha)
    elif escolha == "s":
        print("\nencerrando sistema.")
        break
    else:
        print("\nopção inválida. tente novamente.\n" + "-"*40)
