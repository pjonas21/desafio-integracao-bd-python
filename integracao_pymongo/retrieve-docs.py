import pymongo as pym
import pprint

client = pym.MongoClient(
    "mongodb+srv://<mongodb_user>:<mongodb_pass>@clusterlearrn.z1cmxtg.mongodb.net/?retryWrites=true&w=majority"
)

db = client.desafio
bank = db.bank

print("Clientes do banco")
pprint.pprint([cliente for cliente in bank.find()])

print("\nQtde de clientes na base de dados")
pprint.pprint(bank.count_documents({}))

print("\nFiltrando clientes pelo nome e contando")
pprint.pprint(bank.count_documents({"nome": "Jonas"}))

print("\nRecuperando clientes de forma ordenada pelo nome")
pprint.pprint([cliente for cliente in bank.find({}).sort("nome")])

# deletando registro da colecao de dados
bank.delete_one({"nome": "Jose"})

print("Clientes do banco")
pprint.pprint([cliente for cliente in bank.find()])