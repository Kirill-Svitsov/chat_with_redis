import flet as ft
from redis_client import ChatClient
import threading


class DualChatUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.setup_clients()
        self.setup_ui()

    def setup_page(self):
        self.page.title = "Двойной чат"
        self.page.window_width = 900
        self.page.window_height = 500
        self.page.padding = 10

    def setup_clients(self):
        # Создаем два клиента Redis
        self.client1 = ChatClient("Пупа")
        self.client2 = ChatClient("Лупа")

        # Запускаем получение сообщений для обоих клиентов
        threading.Thread(
            target=self.client1.receive_messages,
            args=(self.handle_message1,),
            daemon=True
        ).start()

        threading.Thread(
            target=self.client2.receive_messages,
            args=(self.handle_message2,),
            daemon=True
        ).start()

    def handle_message1(self, data):
        self.add_message(self.chat1_display, data['user'], data['text'])

    def handle_message2(self, data):
        self.add_message(self.chat2_display, data['user'], data['text'])

    def add_message(self, chat_display, user, text):
        color = "#4CAF50" if user == "Пупа" else "#2196F3"
        chat_display.controls.append(
            ft.Row([
                ft.Text(f"{user}:", color=color, weight="bold"),
                ft.Text(text)
            ], spacing=5)
        )
        self.page.update()

    def setup_ui(self):
        # Элементы для первого чата
        self.chat1_display = ft.ListView(expand=True, spacing=5, auto_scroll=True)
        self.message1_input = ft.TextField(hint_text="Сообщение...", expand=True)

        def send_message1(e):
            if self.message1_input.value:
                self.client1.send_message(self.message1_input.value)
                self.add_message(self.chat1_display, "Пупа", self.message1_input.value)
                self.message1_input.value = ""
                self.page.update()

        # Элементы для второго чата
        self.chat2_display = ft.ListView(expand=True, spacing=5, auto_scroll=True)
        self.message2_input = ft.TextField(hint_text="Сообщение...", expand=True)

        def send_message2(e):
            if self.message2_input.value:
                self.client2.send_message(self.message2_input.value)
                self.add_message(self.chat2_display, "Лупа", self.message2_input.value)
                self.message2_input.value = ""
                self.page.update()

        # Создаем контейнеры для чатов
        chat1 = ft.Container(
            content=ft.Column([
                ft.Text("Чат: Пупа", size=16, weight="bold"),
                self.chat1_display,
                ft.Row([
                    self.message1_input,
                    ft.ElevatedButton("Отправить", on_click=send_message1)
                ])
            ]),
            padding=10,
            border=ft.border.all(1),
            border_radius=10,
            width=400,
            expand=True
        )

        chat2 = ft.Container(
            content=ft.Column([
                ft.Text("Чат: Лупа", size=16, weight="bold"),
                self.chat2_display,
                ft.Row([
                    self.message2_input,
                    ft.ElevatedButton("Отправить", on_click=send_message2)
                ])
            ]),
            padding=10,
            border=ft.border.all(1),
            border_radius=10,
            width=400,
            expand=True
        )

        # Добавляем чаты на страницу
        self.page.add(
            ft.Row(
                [chat1, chat2],
                spacing=20,
                expand=True
            )
        )


def main(page: ft.Page):
    dual_chat = DualChatUI(page)


if __name__ == "__main__":
    ft.app(target=main)