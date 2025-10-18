import os
import datetime
from db_backup import conectar_mongo
from seguranca_backup import gerar_chave, criar_fernet, criptografar_arquivo, descriptografar_arquivo, gerar_hash_sha256

colecao = conectar_mongo()

def carregar_ou_criar_chave():
    if os.path.exists("chave_backup.key"):
        with open("chave_backup.key", "rb") as f:
            return f.read()
    else:
        chave = gerar_chave()
        with open("chave_backup.key", "wb") as f:
            f.write(chave)
        return chave

chave = carregar_ou_criar_chave()
fernet = criar_fernet(chave)

def criar_backup(caminho_arquivo: str):
    if not os.path.exists(caminho_arquivo):
        print("\narquivo não encontrado.\n" + "-"*40)
        return

    dados_cript = criptografar_arquivo(caminho_arquivo, fernet)
    hash_arquivo = gerar_hash_sha256(dados_cript)
    nome_backup = os.path.basename(caminho_arquivo) + ".backup"
    data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(nome_backup, "wb") as f:
        f.write(dados_cript)

    colecao.insert_one({
        "arquivo_original": caminho_arquivo,
        "backup_nome": nome_backup,
        "hash_sha256": hash_arquivo,
        "data_backup": data
    })

    print(f"\nbackup '{nome_backup}' criado e metadados salvos no banco.\n" + "-"*40)

def restaurar_backup(nome_backup: str):
    if not os.path.exists(nome_backup):
        print("\nbackup não encontrado.\n" + "-"*40)
        return

    with open(nome_backup, "rb") as f:
        dados_cript = f.read()

    hash_atual = gerar_hash_sha256(dados_cript)
    registro = colecao.find_one({"backup_nome": nome_backup})

    if not registro:
        print("\nmetadados não encontrados no banco.\n" + "-"*40)
        return

    if registro["hash_sha256"] != hash_atual:
        print("\nfalha na integridade: o backup foi alterado.\n" + "-"*40)
        return

    destino = nome_backup.replace(".backup", "_restaurado.txt")
    descriptografar_arquivo(dados_cript, fernet, destino)
    print(f"\nbackup restaurado com sucesso em '{destino}'.\n" + "-"*40)

while True:
    print("\n" + "="*48)
    print("backup criptografado em nuvem")
    print("="*48)
    escolha = input("criar (c) / restaurar (r) / sair (s)? ").lower().strip()

    if escolha == "c":
        caminho = input("caminho do arquivo para backup: ").strip()
        criar_backup(caminho)
    elif escolha == "r":
        nome_backup = input("nome do arquivo .backup: ").strip()
        restaurar_backup(nome_backup)
    elif escolha == "s":
        print("\nencerrando sistema de backup.")
        break
    else:
        print("\nopção inválida. tente novamente.\n" + "-"*40)
