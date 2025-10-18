import os
from main import conectar_mongo
from seguranca_senha import gerar_chave, criar_fernet, criptografar_texto, descriptografar_texto, gerar_hash_sha256

colecao = conectar_mongo()

def carregar_ou_criar_chave():
    if os.path.exists("chave_fernet.key"):
        with open("chave_fernet.key", "rb") as f:
            return f.read()
    else:
        chave = gerar_chave()
        with open("chave_fernet.key", "wb") as f:
            f.write(chave)
        return chave

chave = carregar_ou_criar_chave()
fernet = criar_fernet(chave)

def cadastrar_usuario(usuario: str, senha: str):
    senha_cript = criptografar_texto(senha, fernet)
    hash_senha = gerar_hash_sha256(senha)

    colecao.insert_one({
        "usuario": usuario,
        "senha_criptografada": senha_cript,
        "hash_senha": hash_senha
    })

    print(f"\nusuário '{usuario}' cadastrado com sucesso.")
    print(f"hash armazenado: {hash_senha}\n" + "-"*40)

def autenticar_usuario(usuario: str, senha_digitada: str):
    doc = colecao.find_one({"usuario": {"$regex": f"^{usuario}$", "$options": "i"}})
    if not doc:
        print("\nusuário não encontrado.\n" + "-"*40)
        return

    hash_digitada = gerar_hash_sha256(senha_digitada)
    if hash_digitada == doc["hash_senha"]:
        senha_real = descriptografar_texto(doc["senha_criptografada"], fernet)
        print(f"\nautenticação bem-sucedida.")
        print(f"senha original: {senha_real}\n" + "-"*40)
    else:
        print("\nsenha incorreta. acesso negado.\n" + "-"*40)

while True:
    print("\n" + "="*48)
    print("cofre de senhas criptografado")
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
        print("\nencerrando cofre.")
        break
    else:
        print("\nopção inválida. tente novamente.\n" + "-"*40)
