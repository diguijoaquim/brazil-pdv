from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy import Column, String, Integer, Float, DateTime,JSON,ForeignKey
#Criado por Ghost 04- Diqui Joaquim

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nome = Column(String(32))
    cargo = Column(String(100))
    username=Column(String(20))
    senha= Column(String(100))

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100))
    preco = Column(Float)
    descricao = Column(String(255))
    image=Column(String(100))
    quantidade_venda=Column(Integer)

class RelatorioVenda(Base):
    __tablename__="relatorios"
    id=Column(Integer,primary_key=True)
    nome=Column(String(20))
    data=Column(String(22))
    caixa=Column(String(50))
    vendas=relationship("produtoVenda", backref="relatorios")
    funcionario=Column(String(40))

class produtoVenda(Base):
    __tablename__="vendas"
    id=Column(Integer,primary_key=True)
    data=Column(DateTime)
    hora=Column(String(10),default="08:00")
    produtos = Column(JSON, nullable=False)
    total_item=Column(Integer)
    total_money=Column(Float)
    relatorio_id=Column(Integer, ForeignKey("relatorios.id"))
    cliente=Column(String(50),default="Desconhecido")
    funcionario=Column(String(40))

    