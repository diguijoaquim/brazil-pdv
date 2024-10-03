import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models.modelos import Base,Produto,Usuario,produtoVenda,RelatorioVenda
from datetime import datetime
import re
import json

d="""
{
    "app":"PDV LITE",
    "key_code":"electro_code_097*$FDEAGRERSATHBNJGFFFRKCXDTGVCXDHJFDC<VTYDGHGHVjghgldxv.fTkvHLGdM",
    "data":{
        "nome":"ShopNow",
        "localizacao":"Av. filipe Samuel Magaia N 1104",
        "cidade":"Lichinga",
        "nuit":1667287375365,
        "valor":30000,
        "validade":"17-05-2020",
        "pago":true,
        "tipo":"Farmacia",
        "contacto":877136613,
        "codigo_fatura":"0786",
        "logo":"/assets/logo.png",
        "email":"admin@gmail.com"
    },
    "admin":{
        "nome":"Diqui Joaquim",
        "apelido":"Namueto",
        "email":"admin@gmail.com",
        "contacto":877136613,
        "username":"admin",
        "password":"1234"
    }

}
"""
info= json.loads(d)
#conectar ao banco de dados 
engine=sqlalchemy.create_engine('sqlite:///database/database.db',echo=False)
ano=datetime.now().year
mes=datetime.now().month
date=datetime.now().day

_validade_software=info['data']['validade']

#vamos verificar se a validade so software e menor que o ano atual
def AnoValido():
    #vamos dividir a string da data
    validade_software=re.split("-",_validade_software)
    print(mes)
    print(int(validade_software[1]))


    if(ano>int(validade_software[2])):
        print("ja expirou ")
        return False
    elif(ano==int(validade_software[2]) and mes<int(validade_software[1])):
        print("vai expirar este ano")
        return True
    elif(ano==int(validade_software[2]) and mes>int(validade_software[1])):
        print("Ja espirou")
        return False
    else:
        print("Ainda Nao espirou ")
        return True

#vamos criar as tabelas dos segintes modelos,"Produto e Usuario"
def CriarTabelas():
    Base.metadata.create_all(engine) 

#criar uma sessao  db
Session=sessionmaker(bind=engine)

db=Session()
def isDataBase():
    try:
        db.query(Usuario).all()
    except:
        CriarTabelas()
        CadastrarUsuario(n=info['admin']['nome'], 
                         c="admin",
                         u=info['admin']['username'],
                         s_=info['admin']['password']
                         )
#essas funcoes podem ser importadas em quarquer class

def CadastrarUsuario(n,c,u,s_):
    novoUsuario=Usuario(nome=n,cargo=c,username=u,senha=s_)
    db.add(novoUsuario)
    db.commit()
    print(f"O usuario {n} Foi Cadastrado com sucesso")

def CadastrarProduto(titulo, preco, descricao, image):
    if titulo != "" and preco is not None and descricao != "" and image != "":
        novoProduto = Produto(titulo=titulo, preco=preco, descricao=descricao, image=image)
        db.add(novoProduto)
        db.commit()
        print(f"O Produto {titulo} foi cadastrado com sucesso")
    else:
        print("Complete todos os campos")

def AtualisarProduto(id,data):
    produto=db.query(Produto).filter_by(id=data.id).first()
    produto.titulo=data.titulo
    produto.preco=data.preco
    produto.descricao=data.descricao
    db.commit()
    print(f"O produto {data.nome} foi atualizado com sucesso")
#funcoes para estoque
def incrementarStoque(id_produto,qtd):
    produto=db.query(Produto).filter_by(id=id_produto).first()
    if(produto):
        p=produto.estoque
        produto.estoque=produto.estoque+qtd
        db.commit()
        print(f"Estoque atualizado d {p} para {produto.estoque}")
    else:
        print("O produto nao foi encontrado")

def decrementarStoque(id_produto,qtd):
    produto=db.query(Produto).filter_by(id=id_produto).first()
    if(produto):
        p=produto.estoque
        produto.estoque=produto.estoque-qtd
        db.commit()
        print(f"Estoque atualizado d {p} para {produto.estoque}")
    else:
        print("O produto nao foi encontrado")


def verProdutos():
    return db.query(Produto).all()

def pegarporCategoria(categoria: str):
    return db.query(Produto).filter_by(categoria=categoria).all()

def pesquisaProduto(query):
    return db.query(Produto).filter(Produto.titulo.like(f"%{query}%")).all()
def todosUsers():
    return db.query(Usuario).all()
def verCaixa():
    return db.query(Usuario).filter_by(cargo="Caixa").all()
def acharUmProduto(id):
    return db.query(Produto).filter_by(id=id).first()
    
def deletarProduto(id):
    p=db.query(Produto).filter_by(id=id).first()
    db.delete(p)
    db.commit()
    print(f"O produto {p.nome} foi deletado com sucesso!")

def addVenda(venda):
    db.add(venda)
    db.commit()
    print("Venda Feita")

def verVendas():
    return db.query(produtoVenda).all()

def addRelatorio(day):
    relatorio=RelatorioVenda(nome=f"relatorio{day}",data=day,caixa="admin")
    db.add(relatorio)
    db.commit()
    print("Relatorio Cadastrado")

def RemoveRelatorio(day):
    relatorio=db.query(RelatorioVenda).filter_by(data=day).first()
    db.delete(relatorio)
    db.commit()
    print("Relatorio Deletado")


def getRelatorios():
    return db.query(RelatorioVenda).all()

def getRelatorioUnico(day):
    return db.query(RelatorioVenda).filter_by(data=day).first()

def getRelatorioUnicoByID(id):
    return db.query(RelatorioVenda).filter_by(id=id).first()

def totalRelatorioMoney(day):
    total=0.00
    for v in getRelatorioUnico(day).vendas:
        total+=v.total_money  
    return total
def deletarRelatorio(id):
    p=db.query(RelatorioVenda).filter_by(id=id).first()
    db.delete(p)
    db.commit()

def deletarVendas(id):
    p=db.query(produtoVenda).filter_by(id=id).first()
    db.delete(p)
    db.commit()

def totalVendaMoney(id):
    produto=db.query(produtoVenda).filter_by(id=id).first()
    total=0.00
    for i in produto.produtos:
        total+=i['total']   
    return total

def totalVendaMoneyRelatorio(day):
    relatorio=db.query(RelatorioVenda).filter_by(data=day).first()
    total=0.00
    for venda in relatorio.vendas:
        total+=totalVendaMoney(venda.id)
    money=f"{total:,.2f}".replace(",", " ").replace(".", ",")
    return money

def totalVendaProdutos(id):
    produto=db.query(produtoVenda).filter_by(id=id).first()
    total=0
    for i in produto.produtos:
        total+=1   
    return total

def getTotalMoneyCart(carrinho):
    total=0.00
    for i in carrinho:
        total+=i['total']
    return total


def getTotalTipoCart(carinho):
    tipo=0
    for i in carinho:
        tipo+=1
    return tipo

def getTotalQuantCart(carrinho):
    quant=0
    for i in carrinho:
        quant+=i["quantidade"]
    return quant

def itensListsimple(id):
    venda=db.query(produtoVenda).filter_by(id=id).first()
    
    produtos=[]
    for i in venda.produtos:
        produtos.append(f"{i['nome']}-{i['quantidade']}")
    novas_string=", ".join(produtos)
    return novas_string
def formatToMoney(data):
    money=f"{data:,.2f}".replace(",", " ").replace(".", ",")
    return money
def getOneSale(id):
    return db.query(produtoVenda).filter_by(id=id).first(

    )
def StartLogin(username,senha):
    user=db.query(Usuario).filter_by(username=username,senha=senha).first()
    if user != None:

        return user
    else:
        return False
    

def loged():
    return ''
def changePassword(nova):
    user=loged()
    user.senha=nova
    db.commit()
    print("senha foi modificada com sucesso")
def getFuncionarios():
    funcionarios=db.query(Usuario).all()
    return funcionarios

def excluir_funcionario(id):
    funcionario=db.query(Usuario).filter_by(id=id).first()
    db.delete(funcionario)
    print(funcionario)
    db.commit()
def userUpdate(data):
    user=loged()
    can=False
    if data['nome'] != "":
        user.nome=data['nome']
        can=True
    if data['apelido'] != "":    
        user.apelido=data['apelido']
        can=True
    if data['telefone'] != "":
        user.telefone=data["telefone"]
        can=True
    if data['email'] != "":
        user.email=data['email']
        can=True
    if data['username'] != "":
        user.username=data['username']
        can=True
    if can:
        db.commit()
        print("dados atualizados")
    else:
        print("Formaulario esta")


def formatar_dados(dados):
    import json

    # Verifica se 'dados' é uma string e precisa ser convertido
    if isinstance(dados, str):
        print(dados)
        dados = json.loads(dados)

    
    # Cria uma lista para armazenar as linhas da string de retorno
    linhas = []
    
    # Adiciona os dados formatados à lista
    linhas.append("-------RESTAURANTE MUTXUTXU------")
    linhas.append(f"Data: {dados['data']}")
    linhas.append("--------------------------")
    linhas.append("Produtos:")
    
    for produto in dados['produtos']:
        linhas.append(f"  Nome: {produto['nome']}")
        linhas.append(f"  Preço: {produto['preco']:.2f} MT")
        linhas.append(f"  Quantidade: {produto['quantidade']}")
        linhas.append("--------------------------")
        
    linhas.append(f"Subtotal: {dados['subtotal']:.2f} MT")
    linhas.append(f"Desconto: {dados['desconto']:.2f} MT")
    linhas.append(f"IVA: {dados['iva']:.2f} MT")
    linhas.append(f"Total: {dados['total']:.2f} MT")
    linhas.append("-------by--gulamo--devs-------")
    
    # Junta todas as linhas em uma única string
    return "\n".join(linhas)
