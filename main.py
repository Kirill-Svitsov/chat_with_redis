import flet as ft
from chat_ui import ChatUI

def main(page: ft.Page):
    chat = ChatUI(page)

ft.app(target=main)