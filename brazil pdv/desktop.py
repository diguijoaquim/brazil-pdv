#Criado por Ghost 04- Diqui Joaquim
import os
import shutil
import flet as ft
from controler import *
from models.modelos import produtoVenda
import re
from datetime import datetime
from time import sleep
from pdv2pdf import*

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
desconto_p = 0.0
iva_p = 0.0
iva_label="Sem IVA"
desconto_label="Sem Desconto"
produtos_em_json=[]
ultima_venda={}
username=''



relatorios=ft.Column(controls=[
                ft.Text(f"Data: {data_view}"),
                ft.Text(f"Vendas: {vendas_view}"),
                ft.Text(f"Total: {total_view} MT")
                               ])

def main(page: ft.Page):
    page.title="PDV Niassa"
    page.title="Next Sistemas"
    page.theme_mode=ft.ThemeMode.LIGHT
    page.padding=0
    selected_file_path = None
    global ultima_venda

    def chage_nav(e):
        selected_index=e.control.selected_index
        if selected_index == 0:
            body.content = home
            update_menu()
            page.update()
        elif selected_index == 1:
            body.content = relatoriosBody
            relatorio_update()
            page.update()
        elif selected_index == 2:
            update_produtos()
            body.content = produtoBody
            produtoBody.content=produtos
            page.update()
        elif selected_index == 3:
            body.content = settingBody
            page.update()

        else:
            page.client_storage.set('user',[])
            page.client_storage.set('loged',False)
            page.window.close()

    def serialize_user(user):
        return {
            'id': user.id,
            'nome': user.nome,
            'cargo': user.cargo,
            'username': user.username,
            'senha':user.senha   
        }

    def CheckIsLoged():
        return page.client_storage.get("loged")

    imagens=os.path.expanduser("~/Documents/pdvlite")
    def file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal selected_file_path
        if e.files:
            selected_file_path = e.files[0].path
            status_text.value = f"Arquivo selecionado: {selected_file_path}"
        else:
            selected_file_path = None
            status_text.value = "Nenhum arquivo selecionado"
        page.update()

    status_text = ft.Text()
    file_picker = ft.FilePicker(on_result=file_picker_result)
    page.overlay.append(file_picker)
    select_button = ft.ElevatedButton(text="Selecionar Foto", on_click=lambda _: file_picker.pick_files(allow_multiple=False))
    usname=ft.TextField(label="Nome do usuario")
    uspass=ft.TextField(label="Senha do Usuario")
    vendas=ft.ListView(height=500)
    def entrar(e):
        global username
        result=StartLogin(username,login_input.value)
        if(result != False):
            page.client_storage.set("loged",True)
            username=e.control.key
            card.content=login_page
            login_perfil.offset = ft.transform.Offset(0, 0)
            login_input.value=''
            
            
            if (page.client_storage.get("user") =="" or page.client_storage.get("user")==None):
                page.client_storage.set("user",serialize_user(result))
            else:
                page.client_storage.set("user","")
                page.client_storage.set("user",serialize_user(result))

            page.controls.clear()
            page.update()
            page.add(
            ft.Row(
                [
                    nav_rail,
                    ft.VerticalDivider(width=1),
                    ft.Column([body], alignment=ft.MainAxisAlignment.START, expand=True),
                ],
                expand=True,
            )
        ) 
            
        usname.value=""
        uspass.value=""
        page.update()

    header=ft.Row(
        [ft.Container(content=ft.Text("Next Sistemas",weight='bold',size=50,color=ft.colors.ORANGE_600),padding=ft.Padding(0,100,0,0))]
        ,alignment=ft.MainAxisAlignment.CENTER,
        )
    def hovercard(e):
        if e.data == "true":  # mouse entra
            e.control.bgcolor='#fcf9d9'
        else: 
            e.control.bgcolor='#fefce8'
        page.update()
    perfiles=ft.Row(alignment=ft.MainAxisAlignment.CENTER)

    def enter(e):
        global username
        username=e.control.key
        card.content=login_perfil
        login_perfil.offset = ft.transform.Offset(0, 0)
        page.update()

    choice_perfil=ft.Column(
        [ft.Row([ft.Text("Escolha o seu perfil")]),
         perfiles

        ])
    def clear(e):
        login_input.value=''
        page.update()

    def write(e):
        if(e.control.text!='<'):
            holdtext=login_input.value
            newtext=holdtext+e.control.text
            login_input.value=newtext
        else:
            holdtext=login_input.value
            login_input.value = holdtext[:-1]
            
        page.update()
    
    def write_payment(e):
        
        if(e.control.text!='<'):
            holdtext=valor_pagar.value
            newtext=holdtext+e.control.text
            valor_pagar.value=newtext
        else:
            holdtext=valor_pagar.value
            valor_pagar.value = holdtext[:-1]

        recebido=valor_pagar.value
        subtotal = getTotalMoneyCart(carrinho_s)  # Exemplo: 1000 MZN
        desconto = round(subtotal * desconto_p)  # 5%
        subtotal_com_desconto = round(subtotal - desconto)
        iva = round(subtotal_com_desconto * iva_p)  # 16%
        total = round(subtotal_com_desconto + iva)
        if int(recebido)>total:
            troco=int(recebido)-total
            trocoView.value=f"O troco e de: {troco},00 MT"
        elif int(recebido)<total:
            resta=total-int(recebido)
            trocoView.value=f"falta: {resta},00 MT"
        elif int(recebido)==total:
            trocoView.value=f"sem troco"
        else:
            trocoView.value=f"occoreu um erro"
        global ultima_venda
        ultima_venda={
            'data':date,
            'produtos':carrinho_s,
            'subtotal':subtotal,
            'desconto':desconto,
            'iva':iva,
            'total':total
        }
        page.update()

    def write_payment2(e):

        recebido=valor_pagar.value
        subtotal = getTotalMoneyCart(carrinho_s)  # Exemplo: 1000 MZN
        desconto = round(subtotal * desconto_p)  # 5%
        subtotal_com_desconto = round(subtotal - desconto)
        iva = round(subtotal_com_desconto * iva_p)  # 16%
        total = round(subtotal_com_desconto + iva)
        if int(recebido)>total:
            troco=int(recebido)-total
            trocoView.value=f"O troco e de: {troco},00 MT"
        elif int(recebido)<total:
            resta=total-int(recebido)
            trocoView.value=f"falta: {resta},00 MT"
        elif int(recebido)==total:
            trocoView.value=f"sem troco"
        else:
            trocoView.value=f"occoreu um erro"

        global ultima_venda
        ultima_venda={
            'data':date,
            'produtos':carrinho_s,
            'subtotal':subtotal,
            'desconto':desconto,
            'iva':iva,
            'total':total,
            'cliente':f"{cliente.value}",
        }
        page.update()
    keyboard=ft.Column([
        ft.Row([
        ft.ElevatedButton(text="1",on_click=write),
        ft.ElevatedButton(text="2",on_click=write),
        ft.ElevatedButton(text="3",on_click=write),
        ])
        ,ft.Row([
        ft.ElevatedButton(text="4",on_click=write),
        ft.ElevatedButton(text="5",on_click=write),
        ft.ElevatedButton(text="6",on_click=write),
        ]),
        ft.Row([
        ft.ElevatedButton(text="7",on_click=write),
        ft.ElevatedButton(text="8",on_click=write),
        ft.ElevatedButton(text="9",on_click=write),
        ]),
        ft.Row([
        ft.ElevatedButton(text="<",on_click=write,on_long_press=clear),
        ft.ElevatedButton(text="0",on_click=write),
        ft.ElevatedButton(text="ok",on_click=entrar),
        ])
    ])
    def finalizar(e):
        global carrinho
        global preco_total
        global carrinho_s
        for p in carrinho:
            preco_total+=p.preco
    
        for i in carrinho_s:
                print(i)
        if(len(carrinho)>=1):
            if(getRelatorioUnico(day)):
                print("Tem Relatorio")
                if(cliente.value !=""):
                    venda=produtoVenda(
                    data=datetime.now(),
                    produtos=carrinho_s,
                    total_item=quantidade_item,
                    total_money=preco_total,
                    relatorio_id=getRelatorioUnico(day).id,
                    cliente=cliente.value,
                    funcionario=page.client_storage.get('user')['nome']
                    

                )
                    addVenda(venda)
                    limpar(e)
                    show_resumo()

                else:
                    venda=produtoVenda(
                    data=datetime.now(),
                    hora=hora,
                    produtos=carrinho_s,
                    total_item=quantidade_item,
                    total_money=preco_total,
                    relatorio_id=getRelatorioUnico(day).id,
                    funcionario=page.client_storage.get('user')['nome']
                   )
                    addVenda(venda)
                    limpar(e)
                    show_resumo()
                    
            else:
                page.open(relatorio_alert)
                
        
    keyboard2=ft.Column([
        ft.Row([
        ft.ElevatedButton(text="1",on_click=write_payment,scale=1.2),
        ft.ElevatedButton(text="2",on_click=write_payment,scale=1.2),
        ft.ElevatedButton(text="3",on_click=write_payment,scale=1.2),
        ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ,ft.Row([
        ft.ElevatedButton(text="4",on_click=write_payment,scale=1.2),
        ft.ElevatedButton(text="5",on_click=write_payment,scale=1.2),
        ft.ElevatedButton(text="6",on_click=write_payment,scale=1.2),
        ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN,spacing=5),
        ft.Row([
        ft.ElevatedButton(text="7",on_click=write_payment,scale=1.2),
        ft.ElevatedButton(text="8",on_click=write_payment,scale=1.2),
        ft.ElevatedButton(text="9",on_click=write_payment,scale=1.2),
        ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Row([
        ft.ElevatedButton(text="<",on_click=write_payment,scale=1.2,on_long_press=clear),
        ft.ElevatedButton(text="0",on_click=write_payment,scale=1.2),
        ft.ElevatedButton(text="ok",on_click=finalizar,scale=1.2),
        ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    ])

    login_input=ft.TextField(label='Digite a sua senha')
    login=ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[
        ft.Image(src='image.png',width=300,height=300,border_radius=10),
        ft.Column([
            login_input
            ,
            keyboard
        ],expand=True)
    ])
    def back_to_perfil(e):
        card.content=choice_perfil
        page.update()
    login_label=ft.Row([ft.IconButton(icon=ft.icons.ARROW_BACK,on_click=back_to_perfil),ft.Text(f"Dgite o seu pin")])
    login_perfil=ft.Column(
        [login_label,
         login

        ])

    
    
    for i in todosUsers():
        perfiles.controls.append(
            ft.Container(height=200,width=200,bgcolor='#fefce8',border_radius=10,
                          content=ft.Column([
                        
                        ft.Row([ft.Image(src='image.png',width=100,height=100)],alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([ft.Text(i.nome,weight='bold')],alignment=ft.MainAxisAlignment.CENTER)
             ]),alignment=ft.alignment.center,padding=20,on_hover=hovercard,on_click=enter,key=i.username)
        )

    card=ft.Container(padding=10,content=choice_perfil,
         bgcolor=ft.colors.ORANGE_100,border_radius=10
        )
    login_page=ft.Container(content=ft.Column(controls=[header,ft.Row([card],alignment=ft.MainAxisAlignment.CENTER),
                                                  ft.Row([ft.CupertinoButton(text="Fechar",bgcolor=ft.colors.RED_400,on_click=lambda e:page.window.close())],
                                                         alignment=ft.MainAxisAlignment.CENTER)]),bgcolor='#fefce8',expand=True)
        
    
    
    
    #CriarTabelas()
    def novo_relatorio(e):
        relatorio_alert.open=False
        page.update()
        rlt=db.query(RelatorioVenda).filter_by(nome=f"relatorio{day}").count()
        if rlt>0:
            page.open(dialogo)
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
        venda=db.query(produtoVenda).filter_by(id=e.control.key).first()

        for p in venda.produtos:
            #print("-----"*30)
            #print(p)
            lista.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(f"Nome: "),ft.Text(p['nome'],weight="bold"),
                        ft.Text(f"Preco: "),ft.Text(f"{p['preco']}0 MT"),
                        ft.Text(f"Quantidade: "),ft.Text(p['quantidade'],weight="bold"),
                        ft.Text(f"Total: "),ft.Text(f"{p['total']}0 MT",weight="bold")
                    ]
                )
            )
        
    relatorio_alert=ft.AlertDialog(title=ft.Text("Sem Relatorio"),content=ft.Text("Nao tem um Relatorio diario para Hoje! Voce deseja criar?"),actions=[
        ft.TextButton('Cancelar'),
        ft.ElevatedButton("Criar Relatorio",on_click=novo_relatorio)
    ])
    def print_fatura_pdf(e):
        id=e.control.key
        venda =getOneSale(id)
        SaleToPDF(venda)
        #chamamar funcoes para gerar PDF

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
        relatorios.controls.append(ft.Text(f"Data: {data_view}"))
        relatorios.controls.append(ft.Text(f"Vendas: {vendas_view}"))
        relatorios.controls.append(ft.Text(f"Total: {total_view} MT"))
        relatorios.controls.append(vendas)
        for i in rel.vendas:
            total=totalVendaMoney(i.id)
            total_tipo=totalVendaProdutos(i.id)
            vendas.controls.append(ft.Card(content=ft.Container(padding=10,
                content=ft.Column(controls=[
                    ft.Row(controls=[
                    ft.Text(f"Produtos: {total_tipo}"),
                    ft.Text(f"Qtd: {i.total_item}"),
                    ft.TextButton("Ver Produtos",key=f"{i.id}",on_click=verMaisProdutos),
                    ft.Row(controls=[
                        ft.Text(f"Total em Dinheiro:"),
                        ft.Text(f" {total}0 MT",size=20,weight="bold")
                    ]),
                    ft.Row(controls=[
                        ft.Text(f"Cliente: "),
                        ft.Text(f"{i.cliente}",size=15,weight="bold")
                    ]),
                    ft.Row(controls=[
                        ft.Text(f"Funcionario: "),
                        ft.Text(f"{i.funcionario}",size=15,weight="bold")
                    ]),
                    
                    ft.IconButton(icon=ft.icons.PRINT,key=f"{i.id}",on_click=print_fatura_pdf)

                ]),
     
               
                ])
            )))


        page.update()


    dialogo=ft.AlertDialog(title=ft.Text("PDV LITE"),
                           content=ft.Text("So pode criar um Relatorios por dia"),
                           actions=[
                               ft.TextButton('intendi',on_click=fecha)
                           ] )

    valor_pagar=ft.TextField(label="valor recebido",on_change=write_payment2)
    trocoView=ft.Text(weight='bold',size=24,col=ft.colors.ORANGE_600)
    
    def close_show(e):
        page.close(resumo_venda)
    pagament=ft.AlertDialog(title=ft.Text("Pagamento"),content=ft.Container(width=300,height=340,content=ft.Column([
        ft.Dropdown(label="metodo de pagamento",
                    options=[ft.dropdown.Option("Cash"),
                             ft.dropdown.Option("MPesa"),
                             ft.dropdown.Option("E-mola")
                             ]),
                    valor_pagar,
                    trocoView,
                    keyboard2
    ])))
    def guardar(e):
        page.open(pagament)
    def imprimir_fatuta(e):
        page.close(resumo_venda)

    
    resumo_venda=ft.AlertDialog(title=ft.Text('Resumo da Venda'),actions=[
        ft.TextButton('Cancelar',on_click=close_show),
        ft.ElevatedButton("imprimir",bgcolor=ft.colors.ORANGE_600,color='white',on_click=imprimir_fatuta)
    ])
    

    def show_resumo():
        dados=formatar_dados(ultima_venda)
        resumo_venda.content=ft.Text(dados)
        page.open(resumo_venda)
        
        


    def limpar(e):
        global carrinho
        global quantidade_item
        global carrinho_s
        carrinho_s=[]
        carrinho=[]
        quantidade_item=0
        total_text.controls.clear()
        total_text.controls.append(ft.Column(controls=[
                ft.Text(f"Subtotal: 0.0 MT", size=17),
                ft.Text(f"IVA: 0.0 MT", size=17),  
                ft.Text(f"Total : 0.0 MT", size=17),
                ft.Row(controls=[
                    ft.ElevatedButton("Limpar",bgcolor=ft.colors.RED_600,on_click=limpar,color='white'),
                    ft.ElevatedButton("Concluir",bgcolor=ft.colors.ORANGE_500,on_click=guardar,color='white')
                ])
            ]))
        lista_vendas.controls.clear()
        page.update()
    help_dialog=ft.AlertDialog(title=ft.Text("Ajuda"),content=ft.Container(padding=10,width=300,content=ft.Text(
        "O aplicativo PDV LITE e um sistema que facilitas as vendas das lojas, restaurantes e farmacias, o aplicativo tem uma documentacao na web e uma playlist de aulas gratis, clique nas seguintes accoes e aproveite , o novo futura de mocambique"
    )),actions=[
        ft.ElevatedButton("Documentacao",bgcolor="blue"),
        ft.ElevatedButton("YouTube",bgcolor="red")
    ])


    ####################################################### NAVBAR #############################################################
    if(CheckIsLoged()==True):
        pass
    total_text=ft.Column(controls=[
        ft.Column(controls=[
                ft.Text(f"Subtotal: 0.0 MT", size=17),
                ft.Text(f"IVA: 0.0 MT", size=17), 
                ft.Text(f"Total : 0.0 MT", size=17),

                ft.Row(controls=[
                    ft.ElevatedButton("Limpar",bgcolor=ft.colors.RED_600,on_click=limpar,color='white'),
                    ft.ElevatedButton("Concluir",bgcolor=ft.colors.ORANGE_500,color='white')
                ])
            ])
    ])       
    dl_m=ft.AlertDialog(title=ft.Text('Adicionar Mais'),
                    content=ft.Column(controls=[

                    ]))
    quantidade=ft.TextField(label=f"Quantidade")
    def dl_more_carinho(e):
        prod=acharUmProduto(e.control.key)
        sub=ft.ElevatedButton(text="Adicionar",bgcolor=f'{prod.id}',on_click=adicionar_Carinho_m,key=e.control.key)
        dl_m.title=ft.Text(f'Edit Qtd:  {prod.titulo}')
        dl_m.content=ft.Column(height=200,controls=[
            quantidade,sub
        ])
        page.open(dl_m)
    

    def adicionar_Carinho_m(e):
        global quantidade_item
        id = e.control.key
        produto = acharUmProduto(id)
        quantidade_valor = int(quantidade.value)
        Existe = False

        # Verifica se o produto já está no carrinho_s
        for i in range(len(carrinho_s)):
            if str(carrinho_s[i]['id']) == id:
                carrinho_s[i]['quantidade'] += quantidade_valor  # Aumenta a quantidade
                carrinho_s[i]['total'] = carrinho_s[i]['quantidade'] * produto.preco  # Atualiza o total
                Existe = True
                print("O Produto existe no carrinho, quantidade aumentada.")
                break

        if not Existe:
            # Se não existe, adiciona o novo produto ao carrinho
            carrinho.append(produto)  # Você ainda pode manter a referência ao produto
            carrinho_s.append(
                {
                    "id": produto.id,  # Adicionando o id para verificação futura
                    "nome": produto.titulo,
                    "preco": produto.preco,
                    "image": produto.image,
                    "quantidade": quantidade_valor,
                    "total": produto.preco * quantidade_valor
                }
            )

        lista_vendas.controls.clear()
        quantidade_item += quantidade_valor
        quantidade.value = ""
        total_text.controls.clear()

        total = getTotalMoneyCart(carrinho_s)  # Exemplo: 1000 MZN
        iva = total * 0.16  # 16% do total
        subtotal = total - iva  # Subtotal é o total menos o IVA

        total_text.controls.append(ft.Column(controls=[
            ft.Text(f"Subtotal: {subtotal} MT", size=17),
            ft.Text(f"IVA: {iva} MT", size=17), 
            ft.Text(f"Total: {total} MT", size=17),
            ft.Row(controls=[
                ft.ElevatedButton("Limpar", bgcolor=ft.colors.RED_600, on_click=limpar, color='white'),
                ft.ElevatedButton("Concluir", bgcolor=ft.colors.ORANGE_500, on_click=guardar, color='white')
            ])
        ]))

        dl_m.open = False  # Fecha a lista de produtos, se aplicável

        for i, item in enumerate(carrinho_s):
            lista_vendas.controls.append(ft.Container(
                padding=8,
                height=80,
                content=ft.Card(content=ft.Row(
                    controls=[
                        ft.Image(src=f'{imagens}/{item["image"]}', width=60, height=60, border_radius=8),
                        ft.Row(controls=[ft.Text(f"{item['preco']} MT", size=12)]),
                        ft.Text(f"Qtd: {item['quantidade']}"),  # Atualiza a quantidade aqui
                        ft.IconButton(icon=ft.icons.DELETE, on_click=delete_item, key=i)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ))
            ))

        page.update()

    def delete_item(e):
        index=int(e.control.key)
        carrinho.pop(index)
        carrinho_s.pop(index)
        global quantidade_item
        quantidade_valor=1
        quantidade.value=1
        e.control.bgcolor="orange"
        lista_vendas.controls.clear()
        page.update()
        quantidade_item+=int(quantidade.value)
        quantidade.value=""
        total_text.controls.clear()
        total = getTotalMoneyCart(carrinho_s)  # Exemplo: 1000 MZN
        iva = total * 0.16  # 16% do total
        subtotal = total - iva  # Subtotal é o total menos o IVA
        total_text.controls.append(ft.Column(controls=[
            ft.Text(f"Subtotal: {subtotal} MT", size=17),
            ft.Text(f"IVA: {iva} MT", size=17), 
            ft.Text(f"Total: {total} MT", size=17),
                            ft.Row(controls=[
                ft.ElevatedButton("Limpar",bgcolor=ft.colors.RED_600,on_click=limpar,color='white'),
                ft.ElevatedButton("Concluir",bgcolor=ft.colors.ORANGE_500,on_click=guardar,color='white')
            ])
        ]))

        for i, item in enumerate(carrinho):
            
            lista_vendas.controls.append(ft.Container(padding=8,height=80,
                    content=ft.Card(content=ft.Row(
                    controls=[
                        ft.Image(src=f'{imagens}/{item.image}',width=60,height=60,border_radius=8),
                            ft.Row(controls=[
                                ft.Text(f"{item.preco} MT",size=12)]),
                                ft.Text(f"Qtd: {quantidade_valor}"),
                                ft.IconButton(icon=ft.icons.DELETE,on_click=delete_item,key=i)
                                
                                ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN) 
                                )))
            
        page.update()
    
                  
    def adicionar_Carinho(e):
        global quantidade_item
        id = e.control.key
        produto = acharUmProduto(id)
        quantidade_valor = 1  # Pode ajustar conforme necessário
        quantidade.value = 1
        Existe = False
        e.control.bgcolor = "orange"

        for i in range(len(carrinho_s)):
            if str(carrinho_s[i]['id']) == id:
                # Aumenta a quantidade do item existente em carrinho_s
                carrinho_s[i]['quantidade'] += quantidade_valor
                carrinho_s[i]['total'] = carrinho_s[i]['quantidade'] * produto.preco  # Atualiza o total
                Existe = True
                print("O Produto existe no carrinho, quantidade aumentada.")
                break

        if not Existe:
            # Se não existe, adiciona o novo produto ao carrinho
            carrinho.append(produto)  # Você ainda pode manter a referência ao produto
            carrinho_s.append(
                {
                    "id": produto.id,  # Adicionando o id para verificação futura
                    "nome": produto.titulo,
                    "preco": produto.preco,
                    "image": produto.image,
                    "quantidade": quantidade_valor,
                    "total": produto.preco * quantidade_valor
                }
            )

        lista_vendas.controls.clear()
        quantidade_item += quantidade_valor
        quantidade.value = ""
        total_text.controls.clear()

        total = getTotalMoneyCart(carrinho_s)  # Exemplo: 1000 MZN
        iva = total * 0.16  # 16% do total
        subtotal = total - iva  # Subtotal é o total menos o IVA

        total_text.controls.append(ft.Column(controls=[
            ft.Text(f"Subtotal: {subtotal} MT", size=17),
            ft.Text(f"IVA: {iva} MT", size=17), 
            ft.Text(f"Total: {total} MT", size=17),
            ft.Row(controls=[
                ft.ElevatedButton("Limpar", bgcolor=ft.colors.RED_600, on_click=limpar, color='white'),
                ft.ElevatedButton("Concluir", bgcolor=ft.colors.ORANGE_500, on_click=guardar, color='white')
            ])
        ]))

        for i, item in enumerate(carrinho_s):
            lista_vendas.controls.append(ft.Container(
                padding=8,
                height=80,
                content=ft.Card(content=ft.Row(
                    controls=[
                        ft.Image(src=f'{imagens}/{item["image"]}', width=60, height=60, border_radius=8),
                        ft.Row(controls=[ft.Text(f"{item['preco']} MT", size=12)]),
                        ft.Text(f"Qtd: {item['quantidade']}"),  # Atualiza a quantidade aqui
                        ft.IconButton(icon=ft.icons.DELETE, on_click=delete_item, key=i)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ))
            ))

        page.update()


            
    def submit(e):
        items_menu.controls.clear()
        page.update()
        for i in pesquisaProduto(e.control.value):
            items_menu.controls.append(
                            ft.Card(
                                content=ft.Container(padding=7,
                                    content=ft.Column([
                                        ft.Image(f'{imagens}/{i.image}',border_radius=10,height=140,fit=ft.ImageFit.COVER,width=page.window.width / 3),
                                        ft.Text(i.titulo,weight="bold",size=20),
                                        ft.Text(i.descricao),
                                        ft.Text(f'{i.preco} MZN',weight="bold",size=18,color=ft.colors.ORANGE_700)
                                    ])
                                    ,on_hover=hovercard,on_click=adicionar_Carinho,on_long_press=dl_more_carinho,key=f'{i.id}')),) 
        page.update() 
    
    def hovercard(e):
        if e.data == "true":  # mouse entra
            e.control.bgcolor='#fefce8'
            e.control.border_radius=10

        else: 
            e.control.bgcolor=''
        page.update()
    def update_menu():
        items_menu.controls.clear()
        page.update()
        for i in verProdutos():
           
            items_menu.controls.append(
                            ft.Card(
                                content=ft.Container(padding=7,
                                    content=ft.Column([
                                        ft.Image(f'{imagens}/{i.image}',border_radius=10,height=140,fit=ft.ImageFit.COVER,width=page.window.width / 3),
                                        ft.Text(i.titulo,weight="bold",size=20),
                                        ft.Text(i.descricao),
                                        ft.Text(f'{i.preco} MZN',weight="bold",size=18,color=ft.colors.ORANGE_700)
                                    ])
                                    ,on_hover=hovercard,on_click=adicionar_Carinho,on_long_press=dl_more_carinho,key=f'{i.id}')),) 
        page.update()

    def update_produtos():
        produtos.controls.clear()
        page.update()
        for i in verProdutos():
           
            produtos.controls.append(
                            ft.Card(
                                content=ft.Container(padding=7,
                                    content=ft.Column([
                                        ft.Image(f'{imagens}/{i.image}',border_radius=10,height=140,fit=ft.ImageFit.COVER,width=page.window.width / 3),
                                        ft.Text(i.titulo,weight="bold",size=20),
                                        ft.Text(i.descricao),
                                        ft.Row([
                                            ft.Text(f'{i.preco} MZN',weight="bold",size=18,color=ft.colors.ORANGE_700),
                                            ft.PopupMenuButton(
                                            items=[
                                                ft.PopupMenuItem(text="Editar",on_click=update_produto),
                                                ft.PopupMenuItem(text="Deletar",on_click=deletarProduto),])
                                            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                                    ])
                                    ,on_hover=hovercard,key=f'{i.id}')),) 
        page.update() 
    lista_relatorio=ft.ListView(width=200,height=700)
        #atualizar o total
    def relatorio_update():
        lista_relatorio.controls.clear()
        page.update()
        for i in getRelatorios():
            total=totalVendaMoneyRelatorio(i.data)
            lista_relatorio.controls.append(
                ft.Container(
                    content=ft.Card(
                ft.Container(padding=10,        
                content=ft.Column(  
                [
                    ft.Row(
                    [
                    ft.Text(i.data,size=18,weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Text(f"Total: {total} MT",weight="bold",size=20),
                    
                ft.Row(controls=[
            ft.IconButton(ft.icons.MORE,on_click=see_more,bgcolor=f"{i.id}"),
             ft.IconButton(ft.icons.PRINT,on_click=relatorio_pdf,key=f"{i.id}"),
            ft.IconButton(ft.icons.SAVE)
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
        page.update()

    
    lista_vendas=ft.ListView(height=380)

    items_menu=ft.GridView(max_extent=240,spacing=10,width=1000,height=600,child_aspect_ratio=0.8)
    search=ft.TextField(label="Procurar Produto",border_radius=12,on_change=submit,width=180)
    produtos=ft.GridView(max_extent=240,spacing=10,width=1000,height=600,child_aspect_ratio=0.8)
    
    update_menu()

    relatoriosBody=ft.Container(
        content=ft.Column(controls=[
            ft.Row(controls=[
                ft.Text("Relatorios Diarios",weight="bold"),
                ft.ElevatedButton("Novo Relatorio",on_click=novo_relatorio)
            ]),
            ft.Row(
                controls=[
                    lista_relatorio,
                    ft.Container(expand=True,height=740,padding=10,content=ft.Column(
                    controls=[
                        ft.Text("Detalhes Do Relatorio",weight="bold",size=30),
                        relatorios
                    ]
                    ))

                ]
            )
        ])
    )
    produtoBody=ft.Container(
       
    )
    cliente=ft.TextField(label="Cliente",height=40,)
    
    home=ft.Container(
        bgcolor="#e1e0e0",
        content=ft.Column(
            [
                ft.Row(
                    controls=[
                
                ft.Container(expand=True,height=800,
                             padding=14,
                             content=ft.Column(controls=[
                    ft.Container(padding=10,border_radius=10,bgcolor="white",content=ft.Row(controls=[
                        ft.Text("Next Sistemas",size=33,weight="bold",color=ft.colors.ORANGE_800),
                        search
                    ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)),
                    items_menu
                ])),
                ft.Container(width=300,padding=10,bgcolor=ft.colors.WHITE,content=ft.Column(controls=[
                    ft.Text("Resumo da Veda:",size=20,weight="bold",color=ft.colors.ORANGE_500),
                     ft.Container(padding=10,margin=10,content=ft.Column(controls=[
                        ft.Row(controls=[
                                ft.Text("Data:",size=15),
                                ft.Text(day,size=15)
                            ]),
                        ft.Row(controls=[
                                ft.Text("Horas:",size=15),
                                ft.Text(hora,size=15),    
                            ]),
                        
                    ])),
                    ft.Card(content=ft.Container(padding=10,content=ft.Column([cliente]),)),
                    ft.Stack(width=300,height=650,controls=[
                    lista_vendas,
                    ft.Card(width=280,
                            bottom=150,
                            content=ft.Container(padding=10,content=ft.Column(controls=[
                                total_text
                                ])))
                                ])
                                ]))
             
                    ],)]))
    def addUser(e):
        page.open(userDialog)
        

    name=ft.TextField(label='Nome do funcionario')
    name2=ft.TextField(label='Apelido')
    Telefone=ft.TextField(label='Contacto')
    email=ft.TextField(label='email')
    username_input=ft.TextField(label='username')
    senha=ft.TextField(label='senha')
    
    def update_user_data(e):
        data={
            "nome":name.value,
            "apelido":name2.value,
            "telefone":Telefone.value,
            "email":email.value,
            "username":username_input.value
        }
        userUpdate(data)

    user_update_form=ft.AlertDialog(title=ft.Text("Atualizar dados do usuario"),content=ft.Column(controls=[
        name,name2,Telefone,email,username_input,
        ft.FilledButton("Atualizar",on_click=update_user_data)
    ]))

    def dl_update_User(e):
        page.open(user_update_form)
        
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
        page.open(cng)
    def cadastrar(e):
        if name.value != '' and senha.value !="":
            CadastrarUsuario(name.value,'simples',u=username_input.value,s_=senha.value)
            name.value=""
            senha.value=""
            username_input.value=""
            funcionarios=[]
            for i in getFuncionarios():
                funcionarios.append(ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(i.nome)),
                            ft.DataCell(ft.Text(i.username)),
                            ft.DataCell(ft.IconButton(icon=ft.icons.DELETE,key=i.id,on_click=deletar)),
                        ],
                    ),)
            tabela.rows=funcionarios
            page.update()


    userDialog=ft.AlertDialog(title=ft.Text("Adicionar Usuario"),
                              content=ft.Column(height=250,controls=[
                                  name,
                                  username_input,
                                  senha,
                                  ft.ElevatedButton("Cadastar Funcionario",on_click=cadastrar)
                              ]))
    

    def deletar(e):
        if(int(e.control.key)==1):
            def f(e):
                page.close(d)
            d=ft.AlertDialog(title=ft.Text("Aviso"),content=ft.Text("O Admin Nao pode ser eliminado"),actions=[ft.TextButton('fechar',on_click=f)])
            page.open(d)
        else:
            excluir_funcionario(e.control.key)
            funcionarios=[]
            for i in getFuncionarios():
                funcionarios.append(ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(i.nome)),
                            ft.DataCell(ft.Text(i.username)),
                            ft.DataCell(ft.IconButton(icon=ft.icons.DELETE,key=i.id,on_click=deletar)),
                        ],
                    ),)
            tabela.rows=funcionarios
            page.update()
            

    funcionarios=[]
    tabela=ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Nome do usuario")),
                ft.DataColumn(ft.Text("accoes"), numeric=True),
            ],
            )
    if CheckIsLoged():
        
        for i in getFuncionarios():
            funcionarios.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(i.nome)),
                        ft.DataCell(ft.Text(i.username)),
                        ft.DataCell(ft.IconButton(icon=ft.icons.DELETE,key=i.id,on_click=deletar)),
                    ],
                ),)
            tabela.rows=funcionarios
        ft.Text(page.client_storage.get('user')['username'],weight="bold")
        settingBody=ft.Container(content=ft.Column(controls=[
            ft.Text("Configuracoes",size=34,weight="bold"),
                ft.Row(controls=[
                    ft.Card(content=ft.Container(padding=10,content=ft.Column(controls=[
                    ft.Row(controls=[
                        ft.Text("UserName: "),ft.Text(page.client_storage.get('user')['username'],weight="bold")
                    ]),
                    ft.Row(controls=[
                        ft.Text("Nome: "),ft.Text(page.client_storage.get('user')['nome'],weight="bold")
                    ]),
                    ft.Row(controls=[
                        ft.Text("Papel: "),ft.Text(page.client_storage.get('user')['cargo'],weight="bold")
                    ]),
                    
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
            ft.FilledButton(f"mudar tudo",on_click=dl_update_User),
            ft.FilledButton(f"adicionar user",on_click=addUser)      
        ])))
        

        ]),
        tabela
        
        
        ]))
    else:
        settingBody=ft.Column()
        
    nome_input = ft.TextField(label="Nome", width=400)
    preco_input = ft.TextField(label="Preço", width=400)
    select_button = ft.ElevatedButton(text="Selecionar Foto", on_click=lambda _: file_picker.pick_files(allow_multiple=False))
    descricao_input = ft.TextField(label="Descrição", multiline=True, width=400,)
    e_nome_input = ft.TextField(label="Nome", width=400)
    e_preco_input = ft.TextField(label="Preço", width=400)
    e_descricao_input = ft.TextField(label="Descrição", multiline=True, width=400,)
    def cancelar_atualizacao(e):
        dlg_edit.open=False
        page.update()

    def cancel_dlg(event):
        dlg.open=False
        page.update()
    def update_produto(e):
        if not selected_file_path:
            status_text.value = "Por favor, selecione um arquivo primeiro."
            page.update()
            return
        destination_dir = os.path.expanduser("~/Documents/pdvlite")

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        filename = os.path.basename(selected_file_path)
        destination_path = os.path.join(destination_dir, filename)
        try:
            shutil.copy(selected_file_path, destination_path)
            status_text.value = "Foto copiada com sucesso!"
        except Exception as ex:
            status_text.value = f"Erro ao copiar a foto: {ex}"
        page.update()

        print(e.control.bgcolor)
        pdt=acharUmProduto(e.control.bgcolor)
        pdt.titulo=e_nome_input.value
        pdt.preco=e_preco_input.value
        pdt.descricao=e_descricao_input.value
        pdt.image=filename
        AtualisarProduto(int(e.control.bgcolor),pdt)
        dlg_edit.open=False
        page.update()
        
    def add(e):
        if not selected_file_path:
            status_text.value = "Por favor, selecione um arquivo primeiro."
            page.update()
            return
        destination_dir = os.path.expanduser("~/Documents/pdvlite")
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        filename = os.path.basename(selected_file_path)
        destination_path = os.path.join(destination_dir, filename)
        try:
            shutil.copy(selected_file_path, destination_path)
            status_text.value = "Foto copiada com sucesso!"
        except Exception as ex:
            status_text.value = f"Erro ao copiar a foto: {ex}"
        page.update()
        CadastrarProduto(nome_input.value, preco_input.value, descricao_input.value, filename)
        dlg.open=False
        page.update()
        update_menu()
        

    dlg = ft.AlertDialog(
        title=ft.Text("Cadastrar Novo Produto", size=24),
        content=ft.Column([
            nome_input,
            preco_input,
            descricao_input,
            select_button,
            status_text
            
        ], scroll=True),  # Permite rolagem se o conteúdo for maior que o espaço disponível
        actions=[
            ft.TextButton("Cancelar", on_click=cancel_dlg),
            ft.TextButton("Cadastrar", on_click=add),  # Fechar o diálogo sem ação adicional
        ],

    )
    # Diálogo de cadastro
    dlg_edit = ft.AlertDialog(
        title=ft.Text("Atualizar o Produto", size=24),
        content=ft.Column([
            e_nome_input,
            e_preco_input,
            e_descricao_input,
            select_button
        ], scroll=True),  # Permite rolagem se o conteúdo for maior que o espaço disponível
        actions=[
            ft.TextButton("Cancelar", on_click=cancel_dlg),
        ],
        
    )

    def add_item(event):
        page.open(dlg)
    

    
    # Criando o NavigationRail
    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        leading=ft.Container(padding=5,
                             content=ft.Icon(ft.icons.RESTAURANT_SHARP,size=40,color=ft.colors.ORANGE_500),
    ),
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.HOME_OUTLINED, selected_icon=ft.icons.HOME, label="Casa"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.TIMELINE_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.TIMELINE),
                label="Relatorios"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.MORE),
                selected_icon_content=ft.Icon(ft.icons.MORE),
                label="Produtos"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label="Definicoes"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.LOGOUT_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.LOGOUT),
                label="Log out"
            ),
        ],
        on_change=chage_nav,
    )
    def close_about(e):
        about.open=False
        page.update()
    about=ft.AlertDialog(
        title=ft.Text("Sobre PDV Lite v1.0 - Lichinga"),
        content=ft.Container(
            width=300,
            content=ft.Text("""O PDV Lite é um sistema de ponto de venda offline desenvolvido pela equipe BlueSpark da empresa Electro Gulamo. Este sistema tem como objetivo auxiliar a gestão de vendas em lojas e farmácias.
                                                                        Imagine um cenário onde todos os cálculos são realizados automaticamente e um relatório diário é gerado sem a necessidade de utilizar o Excel. O PDV Lite foi criado para oferecer muito mais, proporcionando uma solução completa e eficiente para a gestão de vendas.
        """,no_wrap=False)),actions=[
            ft.TextButton("Intendi!",on_click=close_about)
        ])
    # Conteúdo inicial do corpo da página
    body = ft.Container(content=home)
    body_config=ft.Row(
                [
                    nav_rail,
                    ft.VerticalDivider(width=1),
                    ft.Column([body], alignment=ft.MainAxisAlignment.START, expand=True),
                ],
                expand=True,
            )
    # Adicionando o NavigationRail ao layout da página
    if(CheckIsLoged()):
        page.floating_action_button=ft.FloatingActionButton(
                        icon=ft.icons.ADD, on_click=add_item
                    )
        page.add(
          body_config  
        ) 
        
        
    else:
        page.add(login_page)
# Inicializando o aplicativo
ft.app(target=main)
