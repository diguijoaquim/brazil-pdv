#Criado por Ghost 04- Diqui Joaquim
import flet as ft 
import os
from controler import *
from models.modelos import produtoVenda
import re
from datetime import datetime
from pdv2pdf import*
from time import sleep

isDataBase()
current_date = datetime.now()
quantidade_item=0
preco_total=0.00
carrinho = []
carrinho_s=[]
day = current_date.strftime("%d-%m-%Y")
hora=current_date.strftime("%H:%M")
data_view="00-00-0000"
vendas_view=0
total_view=0.00
produtos_em_json=[]

relatorios=ft.Column(controls=[
                ft.Text(f"Data: {data_view}",size=11),
                ft.Text(f"Vendas: {vendas_view}",size=11),
                ft.Text(f"Total: {total_view} MT",size=11)
                               ])


def main(page:ft.Page):
    page.title="PDV MOBILE"
    page.window_width=350
    selected_file_path = None
    imagens=os.path.expanduser("~/Documents/pdvlite")
    e_nome_input = ft.TextField(label="Nome", width=400)
    e_marca_input = ft.TextField(label="Marca", width=400)
    e_preco_input = ft.TextField(label="Preço", width=400)
    e_estoque_input = ft.TextField(label="Estoque", width=400,)
    select_button = ft.ElevatedButton(text="Selecionar Foto", on_click=lambda _: file_picker.pick_files(allow_multiple=False))
    e_categoria_input = ft.Dropdown(
        label="Categoria",
        width=400,
        options=[
            ft.dropdown.Option("Comida"),
            ft.dropdown.Option("Material de Construção"),
            ft.dropdown.Option("Sapatos"),
            ft.dropdown.Option("Vestuarios"),
            ft.dropdown.Option("Medicamentos"),
            ft.dropdown.Option("Tecnologia"),
            ft.dropdown.Option("Moda e Acessórios"),
            ft.dropdown.
            Option("Casa e Jardim"),
            ft.dropdown.Option("Beleza e Cuidados Pessoais"),
            ft.dropdown.Option("Esportes e Lazer"),
            ft.dropdown.Option("Livros e Papelaria"),
            ft.dropdown.Option("Automóveis e Acessórios"),
            ft.dropdown.Option("Saúde e Bem-estar"),
      
        ],
        
    )
    selects=ft.Dropdown(
            label="Tipo de movimento",
            options=[
                ft.dropdown.Option("Aumentar"),
                ft.dropdown.Option("Diminuir"),
            ]
        )
    e_descricao_input = ft.TextField(label="Descrição", multiline=True, width=400,)
    def open_stoque(e):
        produto_selencionado = acharUmProduto(e.control.bgcolor)
        print(produto_selencionado.nome)
        def mod_stck(e):
            dl.open=False
            page.update()
            if(selects.value =="Aumentar"):
                incrementarStoque(produto_selencionado.id,int(estoque_input_x.value))
                estoque_update()
            elif(selects.value =="Diminuir"):
                decrementarStoque(produto_selencionado.id,int(estoque_input_x.value))
                estoque_update()    
            else:
                print("Selencione o tipo de movimento")
        dl=ft.AlertDialog(
        title=ft.Text("Gerir o Estoque",size=24),
        content=ft.Column(
            controls=[
                estoque_input_x,
                selects,
                ft.Text("Note: Antes de concluir a sua transicao \nverifique se esta realizando o tipo de movimento\ndezejado!",color=ft.colors.YELLOW_900),
                
                ft.ElevatedButton(text="Confirmar",width=300,height=50,on_click=mod_stck),
                ft.Row(controls=[
                    ft.Text(f"O estoque atual  de "),
                    ft.Text(f"{produto_selencionado.nome}",size=20,weight="bold"),
                    ft.Text(f"e de: "),
                    ft.Text(f"{produto_selencionado.estoque}",size=18,weight="bold"),

                ])
            ]
            ))
        
        
        page.dialog=dl
        dl.open=True
        page.update()
    def cancelar_atualizacao(e):
        dlg_edit.open=False
        page.update()

    def cancel_dlg(event):
        dlg.open=False
        page.update()
    # Diálogo de cadastro
    dlg_edit = ft.AlertDialog(
        title=ft.Text("Atualizar o Produto", size=24),
        content=ft.Column([
            e_nome_input,
            e_marca_input,
            e_preco_input,
            e_estoque_input,
            e_categoria_input,
            e_descricao_input,
            select_button
        ], scroll=True),  # Permite rolagem se o conteúdo for maior que o espaço disponível
        actions=[
            ft.TextButton("Cancelar", on_click=cancel_dlg),
        ],
        
    )
    c_nome=ft.TextField(label="Nome do Caixa")
    c_apelido=ft.TextField(label="Apelido do Caixa")
    c_cell=ft.TextField(label="Telefone do Caixa")
    c_email=ft.TextField(label="Email do Caixa")
    c_senha=ft.TextField(label="Senha do Caixa")
    c_endereco=ft.TextField(label="Endereco do Caixa")
    def update_produto(e):
        if not selected_file_path:
            status_text.value = "Por favor, selecione um arquivo primeiro."
            page.update()
            return

        # Caminho para a pasta "Documentos/pdvlite" do usuário
        destination_dir = os.path.expanduser("~/Documents/pdvlite")

        # Certifique-se de que a pasta de destino existe, caso contrário, crie-a
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Nome do arquivo selecionado
        filename = os.path.basename(selected_file_path)

        # Caminho completo para o arquivo de destino
        destination_path = os.path.join(destination_dir, filename)

        try:
            #shutil.copy(selected_file_path, destination_path)
            status_text.value = "Foto copiada com sucesso!"
        except Exception as ex:
            status_text.value = f"Erro ao copiar a foto: {ex}"
        page.update()
        pdt=acharUmProduto(e.control.bgcolor)
        pdt.nome=e_nome_input.value
        pdt.preco=e_preco_input.value
        pdt.marca=e_marca_input.value
        pdt.categoria=e_categoria_input.value
        pdt.descricao=e_descricao_input.value
        pdt.estoque=e_estoque_input.value
        pdt.image=filename
        AtualisarProduto(int(e.control.bgcolor),pdt)
        estoque_update()
        dlg_edit.open=False
        page.update()
    lista_vendas=ft.ListView(height=300)

    def deletar_produto(e):
        #vamos achar o id do produto
        #guardado no bgcolor do IconButton
        id=e.control.bgcolor
        #print(int(id))
        deletarProduto(int(id))
        estoque_update()   
    aviso=ft.AlertDialog(title=ft.Text("PDV LITE - AVISO"))
    
    def deletar_(e):
       
        funcionario=db.query(Usuario).filter_by(id=e.control.key).first()
        if(funcionario.cargo=="admin"):
            aviso.title=ft.Text("O ADMIN DO SISTEMA NAO PODE SER DELETADO")
            page.update()
            sleep(3)
            aviso.open=False
            page.update()
        else:
            db.delete(funcionario)
            db.commit()
            aviso.open=False
            page.update()

    def cancelar(e):
        aviso.open=False
        page.update()
    def deletar(e):
        page.dialog=aviso
        funcionario=db.query(Usuario).filter_by(id=e.control.key).first()
        aviso.content=ft.Text(f"Tens certeza que queres eliminar o Funcionario?")
        aviso.actions=[
            ft.ElevatedButton("Cancelar",bgcolor="blue",on_click=cancelar),
            ft.ElevatedButton("Deletar",bgcolor="red",on_click=deletar_,key=f"{funcionario.id}")
        ]
        aviso.open=True
        page.update()
        aviso.content=ft.Text()
    def add(e):
        if not selected_file_path:
            status_text.value = "Por favor, selecione um arquivo primeiro."
            page.update()
            return

        # Caminho para a pasta "Documentos/pdvlite" do usuário
        destination_dir = os.path.expanduser("~/Documents/pdvlite")

        # Certifique-se de que a pasta de destino existe, caso contrário, crie-a
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Nome do arquivo selecionado
        filename = os.path.basename(selected_file_path)
        

        # Caminho completo para o arquivo de destino
        destination_path = os.path.join(destination_dir, filename)

        try:
            #shutil.copy(selected_file_path, destination_path)
            status_text.value = "Foto copiada com sucesso!"
        except Exception as ex:
            status_text.value = f"Erro ao copiar a foto: {ex}"
        page.update()

        CadastrarProduto(nome_input.value,marca_input.value,preco_input.value,int(estoque_input.value),categoria_input.value,descricao_input.value,filename)
        dlg.open=False
        page.update()
        #update_menu()

    def cadastrar(e):
        CadastrarUsuario(name.value,name2.value,Telefone.value,email.value,"caixa","Lichinga",u=username.value,s_=senha.value)
        name.value=""
        name2.value=""
        Telefone.value=""
        email.value=""
        senha.value=""
        username.value=""
        page.update()
    def dropdown_changed(e):
        selected_item = categoria_input.value
        page.update()
     # Definindo as opções do Dropdown para categorias
    e_categoria_input = ft.Dropdown(
        label="Categoria",
        width=400,
        options=[
            ft.dropdown.Option("Comida"),
            ft.dropdown.Option("Material de Construção"),
            ft.dropdown.Option("Sapatos"),
            ft.dropdown.Option("Vestuarios"),
            ft.dropdown.Option("Medicamentos"),
            ft.dropdown.Option("Tecnologia"),
            ft.dropdown.Option("Moda e Acessórios"),
            ft.dropdown.
            Option("Casa e Jardim"),
            ft.dropdown.Option("Beleza e Cuidados Pessoais"),
            ft.dropdown.Option("Esportes e Lazer"),
            ft.dropdown.Option("Livros e Papelaria"),
            ft.dropdown.Option("Automóveis e Acessórios"),
            ft.dropdown.Option("Saúde e Bem-estar"),
      
        ],
        on_change=dropdown_changed
    )
    relatorio_alert=ft.AlertDialog(title=ft.Text("Sem Relatorio"),content=ft.Text("Nao tem um Relatorio diario para Hoje! Voce deseja criar?"),actions=[
    ft.TextButton('Cancelar'),
    ft.ElevatedButton("Criar Relatorio")
    ])
    def novo_relatorio(e):
        relatorio_alert.open=False
        page.update()
        rlt=db.query(RelatorioVenda).filter_by(nome=f"relatorio{day}").count()
        if rlt>0:
            page.dialog=dialogo
            dialogo.open=True
            page.update()
            print("So pode Ter Novo Relatorio Amanha")
        else:
            addRelatorio(day)
    def fecha(e):
        dialogo.open=False
        page.update()
    def relatorio_pdf(e):
        id=e.control.key
        RelatorioToPDF(getRelatorioUnicoByID(id))
    lista=ft.Column()
    dal=ft.AlertDialog(title=ft.Text("Produtos Da Venda:"),content=ft.Container(content=lista))
    def verMaisProdutos(e):
        lista.controls.clear()
        page.update()
        page.dialog=dal
        dal.open=True
        page.update()
        venda=db.query(produtoVenda).filter_by(id=e.control.key).first()
        print(venda.produtos)
        for p in venda.produtos:
            lista.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(f"Nome: ",size=11),ft.Text(p['nome'],weight="bold",size=11),
                        ft.Text(f"Marca: ",size=11),ft.Text(p['marca'],weight="bold",size=11),
                        ft.Text(f"Prc: ",size=11),ft.Text(f"{p['preco']}0 MT",size=11),
                        ft.Text(f"Qtd: ",size=11),ft.Text(p['quantidade'],weight="bold",size=11),
                        ft.Text(f"T: ",size=11),ft.Text(f"{p['total']}0 MT",weight="bold",size=11)
                    ]
                )
            )
        lista.controls.append(
            ft.CupertinoButton("Imprimir",key=f"{venda.id}",on_click=print_fatura_pdf,bgcolor="blue")
        )
        page.update()
    relatorio_alert=ft.AlertDialog(title=ft.Text("Sem Relatorio"),content=ft.Text("Nao tem um Relatorio diario para Hoje! Voce deseja criar?"),actions=[
        ft.TextButton('Cancelar'),
        ft.ElevatedButton("Criar Relatorio",on_click=novo_relatorio)
    ])
    def print_fatura_pdf(e):
        id=e.control.key
        venda =getOneSale(id)
        SaleToPDF(venda)
        #chamamar funcoes para gerar PDF
    funcionario_list=ft.ListView(height=500)
    
    usname=ft.TextField(label="Nome do usuario")
    uspass=ft.TextField(label="Senha do Usuario")

    vendas=ft.ListView(height=500)
    def see_more(e):
        vendas.controls.clear()
        global total_view
        global vendas_view
        global data_view
        rel=getRelatorioUnicoByID(e.control.bgcolor)
        total_view=totalVendaMoneyRelatorio(rel.data)
        vendas_view=len(rel.vendas)
        data_view=rel.data
        relatorios.controls.clear()
        relatorios.controls.append(ft.Text(f"Data: {data_view}",size=11))
        relatorios.controls.append(ft.Text(f"Vendas: {vendas_view}",size=11))
        relatorios.controls.append(ft.Text(f"Total: {total_view} MT",size=11))
        relatorios.controls.append(vendas)
        for i in rel.vendas:
            total=totalVendaMoney(i.id)
            total_tipo=totalVendaProdutos(i.id)
            vendas.controls.append(ft.Card(content=ft.Container(padding=10,
                content=ft.Column(controls=[
                    ft.Row(controls=[
                    ft.Column(controls=[
                        ft.Row(controls=[
                            ft.Column(controls=[
                        ft.Text(f"tipo: {total_tipo}",size=10),
                        ft.Text(f"{total_tipo}",size=10,weight="bold")
                    ]),
                    ft.Column(controls=[
                        ft.Text(f"Qtd: ",size=10),
                        ft.Text(f"{i.total_item}",size=10,weight="bold")
                    ]),
                    ft.Column(controls=[
                        ft.Text(f"Total:",size=10),
                        ft.Text(f" {total}0 MT",size=9,weight="bold")
                    ]),
                        ]),
                        ft.Row(controls=[
                            ft.IconButton(ft.icons.LIST,key=f"{i.id}",on_click=verMaisProdutos),
                    ft.Column(controls=[
                        ft.Text(f"Cliente: ",size=10),
                        ft.Text(f"{i.cliente}",size=10,weight="bold")
                    ]),
                    ft.Column(controls=[
                        ft.Text(f"Caixa: ",size=10),
                        ft.Text(f"{i.funcionario}",size=10,weight="bold")
                    ]),
                    
                    ft.IconButton(icon=ft.icons.PRINT,key=f"{i.id}",on_click=print_fatura_pdf)
                        ])
                        
                    ]),
                    

                ]),
        
                
                ])
            )))


        page.update()


    dialogo=ft.AlertDialog(title=ft.Text("PDV LITE"),
                           content=ft.Text("So pode criar um Relatorios por dia"),
                           actions=[
                               ft.TextButton('intendi',on_click=fecha)
                           ] )


    def print_fatura_pdf(e):
        id=e.control.key
        venda =getOneSale(id)
        SaleToPDF(venda)
        #chamamar funcoes para gerar PDF

    def guardar(e):
        global carrinho
        global preco_total
        global carrinho_s
        for p in carrinho:
            preco_total+=p.preco
    
        for i in carrinho_s:
                print(i)
        if(len(carrinho)>=1):
            if(getRelatorioUnico(day)):
                if(cliente.value !=""):
                    venda=produtoVenda(
                    data=datetime.now(),
                    produtos=carrinho_s,
                    total_item=quantidade_item,
                    total_money=preco_total,
                    relatorio_id=getRelatorioUnico(day).id,
                    cliente=cliente.value,
                    funcionario=logedUserId()
                )
                    if(checkCartStock(carrinho_s)['resultado']):
                        addVenda(venda)
                        deduceStockCart(carrinho_s)
                        limpar(e)
                else:
                    venda=produtoVenda(
                    data=datetime.now(),
                    hora=hora,
                    produtos=carrinho_s,
                    total_item=quantidade_item,
                    total_money=preco_total,
                    relatorio_id=getRelatorioUnico(day).id,
                    funcionario=logedUserId()
                   )
                    
                    if(checkCartStock(carrinho_s)['resultado']):
                        addVenda(venda)
                        deduceStockCart(carrinho_s)
                        limpar(e)
                    
            else:
                print("nao tem relatorio")
                page.dialog=relatorio_alert
                relatorio_alert.open=True
                page.update()
    def limpar(e):
        global carrinho
        global quantidade_item
        global carrinho_s
        carrinho_s=[]
        carrinho=[]
        quantidade_item=0
        total_text.controls.clear()
        total_text.controls.append(ft.Row(controls=[
            ft.Column(controls=[
                ft.Text(f"Quantidade: 0",size=13),
                ft.Text(f"Tipos: 0",size=13),
                ft.Text(f"Total: 0.00 MT",size=13),
            ]),
            ft.Column(controls=[
                    ft.Row(controls=[


                    ]),
                    ft.CupertinoButton("Salvar",bgcolor=ft.colors.BLUE_400,on_click=guardar)
            ])
            ]))
        lista_vendas.controls.clear()
        page.update()
    total_text=ft.Row(controls=[
        ft.Column(controls=[
                ft.Text(f"Quantidade: 0",size=17),
                ft.Text(f"Tipos: 0",size=17),
                ft.Text(f"Total: 0.00 MT",size=17),
            ]),
        ft.Column(controls=[
                    ft.TextButton("limpar",on_click=limpar),
                    ft.CupertinoButton("Salvar",bgcolor=ft.colors.BLUE_400)
                ])
    ]) 
    dl_m=ft.AlertDialog(title=ft.Text('Adicionar Mais'),
                    content=ft.Column(controls=[

                    ]))
    quantidade=ft.TextField(label=f"Quantidade")
    e_descricao_input = ft.TextField(label="Descrição", multiline=True, width=400,)
    def cancelar_atualizacao(e):
        dlg_edit.open=False
        page.update() 
    def dl_more_carinho(e):
        page.dialog=dl_m
        dl_m.open=True
        prod=acharUmProduto(e.control.bgcolor)
        sub=ft.ElevatedButton(text="Adicionar",bgcolor=f'{prod.id}',on_click=adicionar_Carinho_m)
        dl_m.title=ft.Text(f'Edit Qtd:  {prod.nome}')
        dl_m.content=ft.Column(controls=[
            quantidade,sub
        ])
        page.update()

    def adicionar_Carinho_m(e):
        global quantidade_item
        id=e.control.bgcolor
        produto=acharUmProduto(id)
        quantidade_valor=int(quantidade.value)
        Existe=False


        for i in carrinho:
            if str(i.id) ==id:
                i.quantidade_venda+=quantidade_valor
                Existe=True
                print("O Produto existe no carinho")
                page.update()
                break
        if(Existe==False):
            carrinho.append(produto)
            carrinho_s.append(
                {
                "nome":produto.nome,
                "marca":produto.marca,
                "preco":produto.preco,
                "quantidade":int(quantidade.value),
                "total":produto.preco*int(quantidade.value)
            })
            lista_vendas.controls.clear()
            page.update()
            quantidade_item+=int(quantidade.value)  
            quantidade.value=""
            total_text.controls.clear()
            total_text.controls.append(ft.Row(controls=[
                ft.Column(controls=[
                ft.Text(f"Quantidade: {getTotalQuantCart(carrinho_s)}",size=17),
                ft.Text(f"Tipos: {getTotalTipoCart(carrinho_s)}",size=17),
                ft.Text(f"Total: {getTotalMoneyCart(carrinho_s)}0 MT",size=17),
            ]),
            ft.Column(controls=[
                    ft.TextButton("limpar",on_click=limpar),
                    ft.CupertinoButton("Salvar",bgcolor=ft.colors.BLUE_400,on_click=guardar)
            ])
            ]))
            dl_m.open=False
            for i in carrinho:
                lista_vendas.controls.append(ft.Container(padding=10,height=80,
                        content=ft.Card(content=ft.Row(
                        controls=[
                                ft.Row(controls=[
                                    ft.Text(f"{i.nome} - {i.marca}",size=14),
                                    ft.Text(f"{i.preco} MT",size=12)]),
                                    ft.Text(f"Qtd: {quantidade_valor}"),
                                    ft.IconButton(icon=ft.icons.DELETE)
                                    
                                    ]),
                                    )))
            page.update()
            
    def adicionar_Carinho(e):
        global quantidade_item
        id=e.control.bgcolor
        produto=acharUmProduto(id)
        quantidade_valor=1
        quantidade.value=1
        Existe=False

        for i in carrinho:
            if str(i.id) ==id:
                i.quantidade_venda+=quantidade_valor
                Existe=True
                print("O Produto existe no carinho")
                page.update()
                break
        if(Existe==False):
            
            carrinho.append(produto)
            carrinho_s.append(
                {
                "nome":produto.nome,
                "marca":produto.marca,
                "preco":produto.preco,
                "quantidade":int(quantidade.value),
                "total":produto.preco*int(quantidade.value)
            }
            )
            lista_vendas.controls.clear()
            page.update()
            quantidade_item+=int(quantidade.value)
            quantidade.value=""
            total_text.controls.clear()
            total_text.controls.append(ft.Row(controls=[
            ft.Column(controls=[
                ft.Text(f"Quantidade: {getTotalQuantCart(carrinho_s)}",size=17),
                ft.Text(f"Tipos: {getTotalTipoCart(carrinho_s)}",size=17),
                ft.Text(f"Total: {getTotalMoneyCart(carrinho_s)}0 MT",size=17),
            ]),
            ft.Column(controls=[
                   ft.TextButton("limpar",on_click=limpar),
                   ft.CupertinoButton("Salvar",bgcolor=ft.colors.BLUE_400,on_click=guardar)
            ])
            ]))

            for i in carrinho:
                
                lista_vendas.controls.append(ft.Container(padding=10,height=80,
                        content=ft.Card(content=ft.Row(
                        controls=[
                                ft.Row(controls=[
                                    ft.Text(f"{i.nome} - {i.marca}",size=14),
                                    ft.Text(f"{i.preco} MT",size=12)]),
                                    ft.Text(f"Qtd: {quantidade_valor}"),
                                    ft.IconButton(icon=ft.icons.DELETE)
                                    
                                    ]) 
                                    )))
                
            page.update()
            
    def update_menu_c(e):
        items_menu.controls.clear()
        page.update()
        for i in pegarporCategoria(category.value):
            
            items_menu.controls.append(
                            ft.Card(
                                content=ft.Container(padding=6,
                                    content=ft.Stack(
                                        controls=[
                                        ft.Row(top=10,controls=[
                                        ft.Container(height=68,padding=ft.Padding(6,6,0,0),content=ft.Image(src=f'{imagens}/{i.image}',border_radius=6)),
                                        ft.Column(controls=[
                                            ft.Text(i.nome,weight="bold",size=16),
                                            ft.Text(i.descricao)
                                        ])
                                    ]),
                                    ft.Container(padding=ft.Padding(6,0,0,0),bottom=4,content=ft.Row(controls=[
                                        ft.Text(f"{i.preco} MT",weight="bold",size=15),
                                        ft.ElevatedButton(icon=ft.icons.ADD,text="more",bgcolor=f'{i.id}',on_click=dl_more_carinho),
                                        ft.IconButton(icon=ft.icons.PLUS_ONE,on_click=adicionar_Carinho,bgcolor=f'{i.id}')
                                    ]))
                                        ]
                                    )
                                    )),) 
        page.update() 
    def submit(e):
        items_menu.controls.clear()
        page.update()
        for i in pesquisaProduto(e.control.value):
            items_menu.controls.append(
                            ft.Card(
                                content=ft.Container(padding=6,
                                    content=ft.Stack(
                                        controls=[
                                        ft.Row(top=10,controls=[
                                        ft.Container(height=68,padding=ft.Padding(10,10,0,0),content=ft.Image(f'{imagens}/{i.image}',border_radius=6)),
                                        ft.Column(controls=[
                                            ft.Text(i.nome,weight="bold",size=16),
                                            ft.Text(i.descricao)
                                        ])
                                    ]),
                                    ft.Container(padding=ft.Padding(10,0,0,0),bottom=8,content=ft.Row(controls=[
                                        ft.Text(f"{i.preco} MT",weight="bold"),
                                        ft.ElevatedButton(icon=ft.icons.ADD,text="more",bgcolor=f'{i.id}',on_click=dl_more_carinho),
                                        ft.IconButton(icon=ft.icons.PLUS_ONE,on_click=adicionar_Carinho,bgcolor=f'{i.id}')
                                    ]))
                                        ]
                                    )
                                    )),) 
        page.update()    
    def update(e):
        page.dialog=dlg_edit
        produto_selencionado = acharUmProduto(e.control.bgcolor)
        dlg_edit.actions.clear()
        page.update()
        dlg_edit.actions.append(ft.TextButton("Cancelar", on_click=cancelar_atualizacao)),
        dlg_edit.actions.append(ft.ElevatedButton("Atualizar", on_click=update_produto,bgcolor=f"{produto_selencionado.id}")),
        #print(produto_selencionado)
        e_nome_input.value=produto_selencionado.nome
        e_marca_input.value=produto_selencionado.marca
        e_preco_input.value=produto_selencionado.preco
        e_estoque_input.value=produto_selencionado.estoque
        e_categoria_input.value=produto_selencionado.categoria
        e_descricao_input.value=produto_selencionado.descricao
        dlg_edit.open=True
        page.update()
    def update_menu():
        items_menu.controls.clear()
        page.update()
        for i in verProdutos():
            items_menu.controls.append(
                            ft.Card(
                                content=ft.Container(padding=6,
                                    content=ft.Stack(
                                        controls=[
                                        ft.Row(top=10,controls=[
                                        ft.Container(height=50,padding=ft.Padding(6,6,0,0),content=ft.Image(f'{imagens}/{i.image}',border_radius=6)),
                                        ft.Column(controls=[
                                            ft.Text(i.nome,weight="bold",size=14),
                                            ft.Text(i.descricao)
                                        ])
                                    ]),
                                    ft.Container(padding=ft.Padding(6,0,0,0),bottom=8,content=ft.Row(controls=[
                                        ft.Text(f"{i.preco} MT",weight="bold"),
                                        ft.CupertinoButton(icon=ft.icons.ADD,text="more",bgcolor=f'{i.id}',on_click=dl_more_carinho),
                                        ft.IconButton(icon=ft.icons.PLUS_ONE,on_click=adicionar_Carinho,bgcolor=f'{i.id}')
                                    ]))
                                        ]
                                    )
                                    )),) 
        page.update()
    def deletar_produto(e):
        #vamos achar o id do produto
        #guardado no bgcolor do IconButton
        id=e.control.bgcolor
        #print(int(id))
        deletarProduto(int(id))
        estoque_update()
    items_menu=ft.GridView(max_extent=350,spacing=10,height=400,child_aspect_ratio=2.5)
    search=ft.TextField(label="Procurar Produto",border_radius=12,on_change=submit,height=30,width=240)
    
    category=ft.Dropdown(
                            label="Categoria",
                            width=300,
                            border_radius=12,
                            options=[
                                ft.dropdown.Option("Comida"),
                                ft.dropdown.Option("Material de Construção"),
                                ft.dropdown.Option("Sapatos"),
                                ft.dropdown.Option("Vestuarios"),
                                ft.dropdown.Option("Medicamentos"),
                                ft.dropdown.Option("Tecnologia"),
                                ft.dropdown.Option("Moda e Acessórios"),
                                ft.dropdown.
                                Option("Casa e Jardim"),
                                ft.dropdown.Option("Beleza e Cuidados Pessoais"),
                                ft.dropdown.Option("Esportes e Lazer"),
                                ft.dropdown.Option("Livros e Papelaria"),
                                ft.dropdown.Option("Automóveis e Acessórios"),
                                ft.dropdown.Option("Saúde e Bem-estar"),
                        
                            ],
                          )
    lista_relatorio=ft.ListView(height=500,expand=True)
    relatoriosBody=ft.Container(
        content=ft.Column(controls=[
            ft.Row(controls=[
                ft.Text("Relatorios Diarios",weight="bold"),
                ft.ElevatedButton("Novo Relatorio",on_click=novo_relatorio)
            ]),
            ft.Row(
                controls=[
                    lista_relatorio,
                    ft.Container(expand=True,height=500,padding=10,content=ft.Column(
                    controls=[
                        ft.Text("Detalhes Do Relatorio",weight="bold",size=12),
                        relatorios
                    ]
                    ))

                ]
            )
        ])
    )
    cliente=ft.TextField(label="Nome do Cliente")
    home=ft.Container(
       ft.Column(controls=[
           ft.Row(controls=[
           ft.Text("Menu de itens"),
           search
           ]),
           ft.Column(controls=[
               ft.Container(height=340,content=items_menu),
               ft.Card(content=ft.Container(padding=6,content=total_text))
           ])
       ])
    )
    name=ft.TextField(label='Nome do funcionario')
    name2=ft.TextField(label='Apelido')
    Telefone=ft.TextField(label='Contacto')
    email=ft.TextField(label='email')
    username=ft.TextField(label='username')
    senha=ft.TextField(label='senha')
    userDialog=ft.AlertDialog(title=ft.Text("Adicionar Usuario"),
                              content=ft.Column(controls=[
                                  name,
                                  name2,
                                  username,
                                  Telefone,
                                  senha,
                                  ft.ElevatedButton("Cadastar Funcionario",on_click=cadastrar)
                              ]))
    def addUser(e):
        page.dialog=userDialog
        userDialog.open=True
        page.update()
    userBody=ft.Container(content=ft.Column(controls=[
        ft.ElevatedButton("Adicionar Funcionario",
                          on_click=addUser),
        ft.Container(content=ft.Column(controls=[funcionario_list],alignment=ft.MainAxisAlignment.CENTER))
    ]))
 



    def update_user_data(e):
        data={
            "nome":name.value,
            "apelido":name2.value,
            "telefone":Telefone.value,
            "email":email.value,
            "username":username.value
        }
        userUpdate(data)
    def update_user_data(e):
        data={
            "nome":name.value,
            "apelido":name2.value,
            "telefone":Telefone.value,
            "email":email.value,
            "username":username.value
        }
        userUpdate(data)

    user_update_form=ft.AlertDialog(title=ft.Text("Atualizar dados do usuario"),content=ft.Column(controls=[
        name,name2,Telefone,email,username,
        ft.FilledButton("Atualizar",on_click=update_user_data)
    ]))

    def dl_update_User(e):
        page.dialog=user_update_form
        user_update_form.open=True
        page.update()
    def confirm_change_password(e):
        if(loged().senha==cng_old.value):
            cng_old.label="Digite a senha anterior"
            cng_old.border_color=None
            page.update()
            print("senha certa")
            changePassword(cng_new.value)
            cng.open=False
            page.update()
        else:
            cng_old.label="por favor tente novamente"
            cng_old.border_color="red"
            page.update()
            print("a senha anterior nao e correta")
    cng_old=ft.TextField(label='Digite a senha anterior')
    cng_new=ft.TextField(label='Digite a nova senha ')
    cng=ft.AlertDialog(title=ft.Text('Mudar a senha do usuario'), content=ft.Column(controls=[
    cng_old,cng_new,ft.FilledButton("mudar a senha",on_click=confirm_change_password)
    ]))
    def chang_password(e):
        page.dialog=cng
        cng.open=True
        page.update()
    def chang_password(e):
        page.dialog=cng
        cng.open=True
        page.update()
  
    def estoque_update():
        estoqueBody.controls.clear()
        page.update()
        for i in verProdutos():
            estoqueBody.controls.append(
                ft.Card(
                content=ft.Container(padding=6,
                content=ft.Stack(
                controls=[
                ft.Row(top=10,controls=[
                ft.Container(height=55,padding=ft.Padding(6,6,0,0),content=ft.Image(src=f'{imagens}/{i.image}',border_radius=6)),
                ft.Column(controls=[
                ft.Text(i.nome,weight="bold",size=16),
                ft.Text(f"Quantidade: {i.estoque}")
                ]) ]),
                ft.Container(padding=ft.Padding(10,0,0,0),bottom=8,content=ft.Row(controls=[
                ft.Text(f"{i.preco} MT",weight="bold"),
                ft.CupertinoButton
                (f"Movimentar",on_click=open_stoque,bgcolor=f"{i.id}"),
                ft.IconButton(icon=ft.icons.DELETE,icon_color="red",bgcolor=f"{i.id}",on_click=deletar_produto),
                ft.IconButton(icon=ft.icons.EDIT,icon_color="green",bgcolor=f"{i.id}",on_click=update),
                                    ]))
                                        ]
                                    )
                                    ))
                   )
            body.content = estoqueBody
            page.update()
    imagens=os.path.expanduser("~/Documents/pdvlite")
    def file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal selected_file_path
        if e.files:
            selected_file_path = e.files[0].path
        else:
            selected_file_path = None
        page.update()
    status_text = ft.Text()
    file_picker = ft.FilePicker(on_result=file_picker_result)
    page.overlay.append(file_picker)
    

    def add_item(event):
        page.dialog=dlg
        dlg.open=True
        page.update()

    nome_input = ft.TextField(label="Nome",height=40)
    marca_input = ft.TextField(label="Marca",height=40)
    preco_input = ft.TextField(label="Preço",height=40 )
    estoque_input = ft.TextField(label="Estoque",height=40)
    estoque_input_x = ft.TextField(label="Nova Quantidade do Produto",height=40)
   
    categoria_input = ft.Dropdown(
        label="Categoria",
        height=40,
        options=[
            ft.dropdown.Option("Comida"),
            ft.dropdown.Option("Material de Construção"),
            ft.dropdown.Option("Sapatos"),
            ft.dropdown.Option("Vestuarios"),
            ft.dropdown.Option("Medicamentos"),
            ft.dropdown.Option("Tecnologia"),
            ft.dropdown.Option("Moda e Acessórios"),
            ft.dropdown.
            Option("Casa e Jardim"),
            ft.dropdown.Option("Beleza e Cuidados Pessoais"),
            ft.dropdown.Option("Esportes e Lazer"),
            ft.dropdown.Option("Livros e Papelaria"),
            ft.dropdown.Option("Automóveis e Acessórios"),
            ft.dropdown.Option("Saúde e Bem-estar"),
        ],
        
    )
    descricao_input = ft.TextField(label="Descrição", multiline=True,height=40)

    e_nome_input = ft.TextField(label="Nome",height=40)
    e_marca_input = ft.TextField(label="Marca",height=40)
    e_preco_input = ft.TextField(label="Preço",height=40)
    e_estoque_input = ft.TextField(label="Estoque", height=40)
    e_estoque_input_x = ft.TextField(label="Nova Quantidade do Produto",)
    def dropdown_changed(e):
        selected_item = categoria_input.value
        page.update()
     # Definindo as opções do Dropdown para categorias
    e_categoria_input = ft.Dropdown(
        label="Categoria",
        options=[
            ft.dropdown.Option("Comida"),
            ft.dropdown.Option("Material de Construção"),
            ft.dropdown.Option("Sapatos"),
            ft.dropdown.Option("Vestuarios"),
            ft.dropdown.Option("Medicamentos"),
            ft.dropdown.Option("Tecnologia"),
            ft.dropdown.Option("Moda e Acessórios"),
            ft.dropdown.
            Option("Casa e Jardim"),
            ft.dropdown.Option("Beleza e Cuidados Pessoais"),
            ft.dropdown.Option("Esportes e Lazer"),
            ft.dropdown.Option("Livros e Papelaria"),
            ft.dropdown.Option("Automóveis e Acessórios"),
            ft.dropdown.Option("Saúde e Bem-estar"),
      
        ],
        on_change=dropdown_changed
    )
    e_descricao_input = ft.TextField(label="Descrição", multiline=True,height=40)
    dlg = ft.AlertDialog(
        title=ft.Text("Novo Produto",),
        content=ft.Column([
            nome_input,
            marca_input,
            preco_input,
            estoque_input,
            categoria_input,
            descricao_input,
            select_button,
            
        ], scroll=True),  # Permite rolagem se o conteúdo for maior que o espaço disponível
        actions=[
            ft.TextButton("Cancelar", ),
            ft.TextButton("Cadastrar",),  # Fechar o diálogo sem ação adicional
        ],

    )
    page.floating_action_button=ft.FloatingActionButton(icon=ft.icons.ADD,on_click=add_item)
    page.floating_action_button_location=ft.FloatingActionButtonLocation.CENTER_DOCKED
    page.appbar=ft.AppBar(color="white",leading=ft.Icon(ft.icons.CODE,color="white"),bgcolor=ft.colors.BLUE_700,title=ft.Text("PDV LITE",color="white"),actions=[
                        ft.PopupMenuButton(icon_color="white"
                            ,
                        items=[
                        ft.PopupMenuItem("Sobre"),
                        ft.PopupMenuItem("Ajuda",),
                        ft.PopupMenuItem("Politica e Privacidade"),
                        ft.PopupMenuItem("Termos e Condicoes"),
                        ft.PopupMenuItem("Sair")
                                ],
                                
                                ),
                               
    ])
    
    estoqueBody=ft.GridView(
            height=550,runs_count=2,
            spacing=10,
            max_extent=350,
            child_aspect_ratio=2.0,
            run_spacing=5, 

        )
    
    if CheckIsLoged():
        funcionario_list.controls.clear()
        for c in getFuncionarios():
            funcionario_list.controls.append(
                    ft.Container(padding=10,content=ft.Card(
                    content=ft.Row(controls=[
                        ft.Text(f'{c.nome}, {c.apelido}, {c.cargo} ',size=20,weight="bold"), 
                        ft.IconButton(ft.icons.DELETE,key=f'{c.id}',on_click=deletar)
                        ]))))
        settingBody=ft.Container(content=ft.Column(controls=[ft.Text("Configuracoes",size=34,weight="bold"),
        ft.GridView(height=500,controls=[
            ft.Card(content=ft.Container(padding=10,content=ft.Column(controls=[
            ft.Row(controls=[
                ft.Text("UserName: "),ft.Text(loged().username,weight="bold")
            ]),
            ft.Row(controls=[
                ft.Text("Nome: "),ft.Text(loged().nome,weight="bold")
            ]),
            ft.Row(controls=[
                ft.Text("Apelido: "),ft.Text(loged().apelido,weight="bold")
            ]),
            ft.Row(controls=[
                ft.Text("Papel: "),ft.Text(loged().cargo,weight="bold")
            ]),
            ft.Row(controls=[
                ft.Text("Contacto: "),ft.Text(loged().telefone,weight="bold")
            ]),
            ft.Row(controls=[
                ft.Text("E-Mail: "),ft.Text(loged().telefone,weight="bold")
            ])
        ]))),
        ft.Card(content=ft.Container(padding=10,content=ft.Column(controls=[
            ft.Row(controls=[
                ft.Text("Empresa: "),ft.Text(info['data']['nome'],weight="bold")
            ]),
            ft.Row(controls=[
                ft.Text("Nuit: "),ft.Text(info['data']['nuit'],weight="bold")
            ]),
            ft.Row(controls=[
                ft.Text("Tipo de negocio: "),ft.Text(info['data']['tipo'],weight="bold")
            ]),
            ft.Row(controls=[
                ft.Text("Avenida: "),ft.Text(info['data']['localizacao'],weight="bold")
            ]),
            ft.Row(controls=[
                ft.Text("Cidade: "),ft.Text(info['data']['cidade'],weight="bold")
            ]),
            ft.Row(controls=[
                ft.Text("Valido Ate: "),ft.Text(info['data']['validade'],weight="bold")
            ]),            
        ]))),
          ft.Card(content=ft.Container(padding=40,content=ft.Column(controls=[
            ft.FilledButton(f"mudar a senha",on_click=chang_password),
            ft.FilledButton(f"mudar tudo",on_click=dl_update_User)     
        ]))),  ft.Card(content=ft.Container(padding=40,content=ft.Column(controls=[
              funcionario_list
        ]))),
        ]),]))
    else:
        settingBody=ft.Column()
    
    
    def relatorio_update():
        lista_relatorio.controls.clear()
        page.update()
        for i in getRelatorios():
            total=totalVendaMoneyRelatorio(i.data)
            lista_relatorio.controls.append(
                ft.Container(
                    content=ft.Card(
                ft.Container(padding=4,          
                content=ft.Column(  
                [
                    ft.Row(
                    [
                    ft.Text(i.data,size=13,weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Text(f"Total: {total} MT",weight="bold",size=13),
                    
                ft.Row(controls=[
            ft.ElevatedButton("ver mais",on_click=see_more,bgcolor=f"{i.id}"),
            ft.IconButton(ft.icons.PRINT,on_click=relatorio_pdf,key=f"{i.id}"),
            
                ],
                alignment=ft.MainAxisAlignment.CENTER
                ),
                
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ) )
            ))
                )
            body.content = relatoriosBody
            
            page.update()
    body=ft.Container()

    def homeBody(e):
        update_menu()
        body.content=home
        page.update()

    def estoque(e):
        estoque_update()
        body.content=estoqueBody
        page.update()
    estoque_update()
    update_menu()
    
    def relatorio(e):
        relatorio_update()
        page.update()

    def setting(e):
        body.content=settingBody
        page.update()
        
    body.content=home
    page.bottom_appbar=ft.BottomAppBar(bgcolor=ft.colors.BLUE_700,
                                       shape=ft.NotchShape.CIRCULAR,
                                       content=ft.Row(controls=[
                                           ft.IconButton(ft.icons.HOME,icon_color="white",on_click=homeBody),
                                           ft.IconButton(ft.icons.LIST,icon_color="white",on_click=estoque),
                                           ft.Container(expand=True),
                                           ft.IconButton(ft.icons.NOTIFICATIONS,icon_color="white",on_click=relatorio),
                                           ft.IconButton(ft.icons.SETTINGS,icon_color="white",on_click=setting)
                                       ]))
    page.add(body)
    
    

ft.app(target=main)