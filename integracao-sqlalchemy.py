import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Double
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

Base = declarative_base()


class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    nome = Column(String(150), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    endereco = Column(String, nullable=False)

    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cliente (id: {self.id}, nome: {self.nome}, cpf: {self.cpf})"


class Conta(Base):
    __tablename__ = "conta"

    id = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False, default="CC")
    agencia = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    saldo = Column(Double)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Conta (id: {self.id}, Agencia: {self.agencia}, Conta: {self.numero})"


engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

with Session(engine) as session:
    cliente_1 = Cliente(
        nome = "Paulo Jonas",
        cpf = "12312312312",
        endereco = "Rua fulano, 12, caninde",
        conta = [
            Conta(
                tipo = "CC",
                agencia = "1234",
                numero = "0789",
                saldo = 0.0,
            )
        ]
    )
    cliente_2 = Cliente(
        nome = "Luis da Silva",
        cpf = "23423423423",
        endereco = "Rua sicrano, 23, caninde",
        conta = [
            Conta(
                tipo = "CC",
                agencia = "1234",
                numero = "0675",
                saldo = 0.0,
            )
        ]
    )

    session.add_all([cliente_1, cliente_2])
    session.commit()

# filtragem e impressao de cliente pelo nome
stmt_select = select(Cliente).where(Cliente.nome.in_(["Paulo Jonas"]))
print([cliente for cliente in session.scalars(stmt_select)])

# busca e impressao de todos os clientes
stmt_all = select(Cliente)
print([cliente for cliente in session.scalars(stmt_all)])

# busca e impressao de todos os clientes ordenados pelo nome
stmt_ordered = select(Cliente).order_by(Cliente.nome.asc())
print([cliente for cliente in session.scalars(stmt_ordered)])

# busca e impressao do cliente, conta e agencia
stmt_join = select(Cliente.nome, Conta.agencia, Conta.numero).join_from(Conta, Cliente)
results = Session(engine).execute(stmt_join).fetchall()
print([res for res in results])

# impressao da quantidade de registros em uma tabela
stmt_count = select(func.count('*')).select_from(Cliente)
print("Total de instancias da tabela Cliente: ", end='')
for result in session.scalars(stmt_count):
    print(result)
