from pymongo import MongoClient

def conectar_mongo():
    cliente = MongoClient("mongodb+srv://claramorei:ana0809@bancopymongo.m0mgjhc.mongodb.net/")
    
    db = cliente["meu_banco"]
    colecao_hashes = db["verificador_arquivos"]
    
    return colecao_hashes
