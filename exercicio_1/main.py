from pymongo import MongoClient


def conectar_mongodb():
    con = MongoClient("mongodb+srv://claramorei:ana0809@bancopymongo.m0mgjhc.mongodb.net/")

    db = con.get_database("meu_banco")
    colecao = db.get_collection('credenciais')

    return colecao

