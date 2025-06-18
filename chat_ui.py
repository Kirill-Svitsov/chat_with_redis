import flet as ft
from redis_client import ChatClient
import threading


class ChatUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.setup_ui()

    def setup_page(self):
        self.page.title = "Простой чат"
        self.page.window_width = 300
        self.page.window_height = 400
        self.page.horizontal_alignment = "center"

    def setup_ui(self):
        self.MY_COLOR = "#4CAF50"  # Зеленый
        self.OTHER_COLOR = "#2196F3"  # Голубой
        self.username = ft.TextField(label="Ваше имя", width=250)
        self.chat_display = ft.ListView(expand=True, spacing=5, auto_scroll=True)
        self.message_input = ft.TextField(
            label="Сообщение",
            expand=True,
            on_submit=self.send_click
        )

        self.page.add(
            ft.Column([
                self.username,
                ft.ElevatedButton("Начать чат", on_click=self.start_chat)
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    def add_message(self, user, text):
        color = self.MY_COLOR if user == self.username.value else self.OTHER_COLOR
        self.chat_display.controls.append(
            ft.Row([
                ft.Text(f"{user}:", color=color, weight="bold"),
                ft.Text(text)
            ], spacing=5)
        )
        self.page.update()

    def start_chat(self, e):
        if not self.username.value:
            return

        self.client = ChatClient(self.username.value)
        self.page.session.set("client", self.client)

        self.page.clean()
        self.page.add(
            ft.Container(
                content=ft.Text(f"Чат: {self.username.value}", size=14),
                alignment=ft.alignment.center
            ),
            ft.Divider(height=1),
            self.chat_display,
            ft.Divider(height=1),
            ft.Row([
                self.message_input,
                ft.ElevatedButton(">", on_click=self.send_click, width=50)
            ], width=280)
        )

        threading.Thread(
            target=self.client.receive_messages,
            args=(lambda data: self.add_message(data['user'], data['text']),),
            daemon=True
        ).start()

    def send_click(self, e):
        if hasattr(self, 'client') and self.message_input.value:
            self.add_message(self.username.value, self.message_input.value)
            self.client.send_message(self.message_input.value)
            self.message_input.value = ""
            self.page.update()

    def create_content(self, username):
        """Создает содержимое для вкладки с заданным именем пользователя"""
        self.username.value = username
        self.start_chat(None)  # Программно "нажимаем" кнопку начала чата
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(f"Чат: {username}", size=14),
                    alignment=ft.alignment.center
                ),
                ft.Divider(height=1),
                self.chat_display,
                ft.Divider(height=1),
                ft.Row([
                    self.message_input,
                    ft.ElevatedButton(">", on_click=self.send_click, width=50)
                ], width=280)
            ],
            expand=True
        )
