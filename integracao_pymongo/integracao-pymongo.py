import pymongo as pym
import pprint

client = pym.MongoClient(
    "mongodb+srv://<mongodb_user>:<mongodb_pass>@clusterlearrn.z1cmxtg.mongodb.net/?retryWrites=true&w=majority"
)

# criando banco de dados
db = client.desafio

# criando a colecao bank
bank = db.bank

# preparando informacoes de cliente e conta
clientes = [
    {
        "nome": "Jonas",
        "cpf": "12312312312",
        "endereco": "Rua fulano, 12, caninde",
        "conta": [{
            "agencia": "1234",
            "numero": "0786-9",
            "tipo": "CC",
            "saldo": "0.0"
        }]
    },
    {
        "nome": "Jose",
        "cpf": "89789789800",
        "endereco": "Rua sicrano, 34, caninde",
        "conta": [{
            "agencia": "1234",
            "numero": "0234-1",
            "tipo": "CC",
            "saldo": "0.0"
        }]
    }
]

client_insert = bank.insert_many(clientes)
pprint.pprint(client_insert.inserted_ids)