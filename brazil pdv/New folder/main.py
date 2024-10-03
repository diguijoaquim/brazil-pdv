import flet as ft

def main(page: ft.Page):
    page.title="Ponto de venda - Mutxutxu"
    page.theme_mode=ft.ThemeMode.LIGHT
    page.padding=0

    rail = ft.NavigationRail(
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
                icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                label="produtos"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label="Definicoes"
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.Column([ ft.Container(expand=True,bgcolor="#e1e0e0")], alignment=ft.MainAxisAlignment.START, expand=True),
            ],
            expand=True,
        )
    )

ft.app(main)