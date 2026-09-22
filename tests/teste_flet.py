from cProfile import label

import flet as ft
from flet import app, LabelPosition, controls


def main(page: ft.Pagge):
    page.title = "Minhas Tarefas"
    page.window.width = 400
    page.window.height = 650
    page.padding = ft.Padding.only(top=20,left=20,right=20,bottom=20)
    #------------------------------------FUNCOES------------------------------------------------------------------------------------------------
    def add_task(e):
        print(new_task.value)
        page.add(ft.Checkbox(label=new_task.value))
        new_task.value = ''
        page.update()


    def button_click(e):
        page.controls.append(ft.Text("Eita como clicka"))
    #-----------------------------------------------------VARIAVEIS-----------------------------------------------------------------------------
    new_task = ft.TextField(hint_text='Insira uma tarefa', expand=True)
    novo_texto = ft.Text(value="Bem vindo clickador")
    new_button = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_task)
    task_list = ft.Column(border=ft.border.all)
    #---------------------------------------------------------------------------------------------------------------------------------------------

    page.controls.append(ft.Button("Click me", on_click=button_click))


    card = ft.Column(
        width=400,
            controls=[
                ft.Row(
                    controls=[
                        new_task,
                        new_button
                    ]
                ),
                task_list,
            ]
        )

    page.add(card)
ft.run(main)