import flet as ft 

def MutxutxuApp(page:ft.page):
    page.title="Ponto de venda - Mutxutxu"
    page.theme_mode=ft.ThemeMode.LIGHT
    page.padding=0
    user='Ghost'
    header=ft.Row(
        [ft.Container(content=ft.Text("Mutxutxu PDV",weight='bold',size=50,color=ft.colors.ORANGE_600),padding=ft.Padding(0,100,0,0))]
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

        card.content=login_perfil
        login_perfil.offset = ft.transform.Offset(0, 0)
        page.update()

    def back_to_perfil(e):
        card.content=choice_perfil
        page.update()
        
    for i in range(3):
        perfiles.controls.append(
            ft.Container(height=200,width=200,bgcolor='#fefce8',border_radius=10,
                          content=ft.Column([
                        
                        ft.Row([ft.Image(src='image.png',width=100,height=100)],alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([ft.Text('Admin',weight='bold')],alignment=ft.MainAxisAlignment.CENTER)
             ]),alignment=ft.alignment.center,padding=20,on_hover=hovercard,on_click=enter)
        )
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
        ft.ElevatedButton(text="ok",on_click=write),
        ])
    ])
    login_input=ft.TextField(label='Digite a sua senha')
    login=ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[
        ft.Container(height=300,width=300,bgcolor='grey',border_radius=10),
        ft.Column([
            login_input
            ,
            keyboard
        ],expand=True)
    ])
    login_label=ft.Row([ft.IconButton(icon=ft.icons.ARROW_BACK,on_click=back_to_perfil),ft.Text(f"Ola,{user} digite o seu pin")])
    login_perfil=ft.Column(
        [login_label,
         login

        ])
    card=ft.Container(padding=10,content=choice_perfil,
         bgcolor=ft.colors.ORANGE_100,border_radius=10
        )
    body=ft.Container(content=ft.Column(controls=[header,ft.Row([card],alignment=ft.MainAxisAlignment.CENTER),
                                                  ft.Row([ft.CupertinoButton(text="Fechar",bgcolor=ft.colors.RED_400)],
                                                         alignment=ft.MainAxisAlignment.CENTER)]),bgcolor='#fefce8',expand=True)
    page.add(body)
    
    

ft.app(target=MutxutxuApp)