"""
Telegram Channel Monitor — Android App
Kivy UI с двумя экранами: Настройки и Мониторинг
"""

import asyncio
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform

import config as cfg
from monitor_service import MonitorService

# === Цветовая схема ===
PRIMARY = (0.1, 0.4, 0.8)       # Синий
DARK_BG = (0.08, 0.08, 0.12)    # Тёмный фон
CARD_BG = (0.14, 0.14, 0.20)    # Фон карточек
SUCCESS = (0.2, 0.7, 0.3)       # Зелёный
WARNING = (0.9, 0.6, 0.1)       # Оранжевый
DANGER = (0.8, 0.2, 0.2)        # Красный
TEXT = (0.95, 0.95, 0.95)       # Белый текст
TEXT_DIM = (0.6, 0.6, 0.65)     # Серый текст


class SettingsScreen(Screen):
    """Экран настроек."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = MonitorService()
        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        layout = BoxLayout(orientation="vertical", padding=15, spacing=10)

        # Заголовок
        title = Label(
            text="⚙️ Настройки",
            font_size="20sp",
            color=TEXT,
            size_hint_y=None,
            height=50,
        )
        layout.add_widget(title)

        # Поля ввода
        fields = [
            ("API ID", "telethon_api_id", "Число с my.telegram.org"),
            ("API Hash", "telethon_api_hash", "Строка с my.telegram.org"),
            ("Номер телефона", "telethon_phone", "+79991234567"),
            ("Токен бота", "bot_token", "От @BotFather"),
            ("Каналы", "channels", "channel1,channel2,channel3"),
            ("Целевая фраза", "target_phrase", "Текст для поиска"),
        ]

        self.inputs = {}
        for label_text, key, hint in fields:
            row = BoxLayout(size_hint_y=None, height=50, spacing=10)
            lbl = Label(
                text=label_text,
                color=TEXT_DIM,
                size_hint_x=0.35,
                halign="right",
            )
            txt = TextInput(
                hint_text=hint,
                multiline=False,
                size_hint_x=0.65,
                font_size="14sp",
                background_color=CARD_BG,
                foreground_color=TEXT,
            )
            txt.bind(text=lambda instance, k=key: self.save_temp(k, instance.text))
            row.add_widget(lbl)
            row.add_widget(txt)
            self.inputs[key] = txt
            layout.add_widget(row)

        # Кнопка сохранения
        save_btn = Button(
            text="💾 Сохранить",
            size_hint_y=None,
            height=50,
            background_color=PRIMARY,
            color=TEXT,
            font_size="16sp",
        )
        save_btn.bind(on_press=lambda x: self.save_config())
        layout.add_widget(save_btn)

        # Кнопка перехода к мониторингу
        monitor_btn = Button(
            text="📡 К мониторингу →",
            size_hint_y=None,
            height=55,
            background_color=SUCCESS,
            color=(1, 1, 1),
            font_size="18sp",
            bold=True,
        )
        monitor_btn.bind(on_press=lambda x: self.go_to_monitor())
        layout.add_widget(monitor_btn)

        self.add_widget(layout)

    def load_config(self):
        """Загружает сохранённые настройки."""
        data = cfg.load_config()
        for key, txt in self.inputs.items():
            txt.text = data.get(key, "")

    def save_temp(self, key, value):
        """Временно сохраняет значение."""
        pass  # Сохраняем при нажатии кнопки

    def save_config(self):
        """Сохраняет настройки."""
        data = {}
        for key, txt in self.inputs.items():
            data[key] = txt.text
        cfg.save_config(data)
        self.show_snackbar("✅ Настройки сохранены")

    def go_to_monitor(self):
        """Переходит на экран мониторинга."""
        data = {}
        for key, txt in self.inputs.items():
            data[key] = txt.text
        cfg.save_config(data)
        self.manager.current = "monitor"
        # Передаём сервис на другой экран
        monitor_screen = self.manager.get_screen("monitor")
        monitor_screen.set_service(self.service)


class MonitorScreen(Screen):
    """Экран мониторинга — статус + лог."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = MonitorService()
        self.monitor_task = None
        self.setup_ui()

    def set_service(self, service):
        """Получает сервис из SettingsScreen (общий экземпляр)."""
        self.service = service

    def setup_ui(self):
        layout = BoxLayout(orientation="vertical", padding=15, spacing=10)

        # Верхняя панель: статус + кнопки
        top_bar = BoxLayout(size_hint_y=None, height=60, spacing=10)

        self.status_label = Label(
            text="⏸ Не запущен",
            color=TEXT_DIM,
            font_size="14sp",
        )
        top_bar.add_widget(self.status_label)

        self.start_btn = Button(
            text="▶ Старт",
            size_hint_x=None,
            width=100,
            background_color=SUCCESS,
            color=(1, 1, 1),
            font_size="14sp",
        )
        self.start_btn.bind(on_press=lambda x: self.start_monitoring())
        top_bar.add_widget(self.start_btn)

        self.stop_btn = Button(
            text="⏹ Стоп",
            size_hint_x=None,
            width=100,
            background_color=DANGER,
            color=TEXT,
            font_size="14sp",
            disabled=True,
        )
        self.stop_btn.bind(on_press=lambda x: self.stop_monitoring())
        top_bar.add_widget(self.stop_btn)

        layout.add_widget(top_bar)

        # Разделитель
        layout.add_widget(
            Label(
                text="",
                size_hint_y=None,
                height=5,
                background_color=TEXT_DIM,
            )
        )

        # Лог событий (скроллируемый)
        log_header = Label(
            text="📋 Лог событий",
            color=TEXT_DIM,
            size_hint_y=None,
            height=35,
            font_size="13sp",
        )
        layout.add_widget(log_header)

        # Кнопка очистки лога
        clear_btn = Button(
            text="🗑 Очистить",
            size_hint_y=None,
            height=35,
            background_color=CARD_BG,
            color=TEXT_DIM,
            font_size="12sp",
        )
        clear_btn.bind(on_press=lambda x: self.clear_log())
        layout.add_widget(clear_btn)

        # ScrollView для лога
        scroll = ScrollView(size_hint=(1, 0.85))
        self.log_layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.log_layout.bind(minimum_height=self.log_layout.setter("height"))
        self.log_labels = []
        scroll.add_widget(self.log_layout)
        layout.add_widget(scroll)

        # Кнопка назад
        back_btn = Button(
            text="← Назад к настройкам",
            size_hint_y=None,
            height=45,
            background_color=CARD_BG,
            color=TEXT_DIM,
            font_size="14sp",
        )
        back_btn.bind(on_press=lambda x: self.go_back())
        layout.add_widget(back_btn)

        self.add_widget(layout)

        # Периодическое обновление лога
        Clock.schedule_interval(self.update_log_display, 1.0)

    def set_service(self, service):
        """Устанавливает сервис и подключает коллбеки."""
        self.service = service
        self.service.set_callbacks(
            on_log=self.on_log_message,
            on_status=self.on_status_update,
        )

    def on_log_message(self, message: str):
        """Вызывается при новом сообщении в лог."""
        Clock.schedule_once(
            lambda dt: self.add_log_label(message), 0
        )

    def on_status_update(self, status: str, running: bool):
        """Вызывается при изменении статуса."""
        Clock.schedule_once(
            lambda dt: self.update_status_display(status, running), 0
        )

    def add_log_label(self, message: str):
        """Добавляет строку лога в UI."""
        lbl = Label(
            text=message,
            color=TEXT,
            font_size="11sp",
            text_size=(self.log_layout.width - 20, None),
            halign="left",
            valign="top",
            markup=True,
        )
        self.log_layout.add_widget(lbl)
        self.log_labels.append(lbl)
        # Убираем старые, если больше 200
        while len(self.log_labels) > 200:
            old = self.log_labels.pop(0)
            self.log_layout.remove_widget(old)

    def update_log_display(self, dt):
        """Периодически обновляет отображение (для совместимости)."""
        pass  # Обновление происходит через коллбеки

    def update_status_display(self, status: str, running: bool):
        """Обновляет отображение статуса."""
        if running:
            self.status_label.text = f"🟢 {status}"
            self.status_label.color = SUCCESS
            self.start_btn.disabled = True
            self.stop_btn.disabled = False
        else:
            self.status_label.text = f"⏸ {status}"
            self.status_label.color = TEXT_DIM
            self.start_btn.disabled = False
            self.stop_btn.disabled = True

    def start_monitoring(self):
        """Запускает мониторинг."""
        self.start_btn.text = "⏳ Запуск..."
        self.start_btn.disabled = True

        # Запускаем в отдельном event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.monitor_task = loop.create_task(self._run_async())
        loop.run_until_complete(self.monitor_task)

    async def _run_async(self):
        """Запускает сервис мониторинга."""
        try:
            await self.service.start_monitoring()
        except Exception as e:
            self.service.log(f"Критическая ошибка: {e}")
        finally:
            self.start_btn.text = "▶ Старт"
            self.start_btn.disabled = False

    def stop_monitoring(self):
        """Останавливает мониторинг."""
        self.service.log("🛑 Остановка по кнопке")
        # Telethon можно остановить через event
        if self.service.telethon_client:
            self.service.telethon_client.stop()
        self.update_status_display("Остановлен", False)

    def clear_log(self):
        """Очищает лог."""
        for lbl in self.log_labels:
            self.log_layout.remove_widget(lbl)
        self.log_labels.clear()
        self.service.clear_log()

    def go_back(self):
        """Возвращается к настройкам."""
        self.manager.current = "settings"


class ScreenManagerCustom(ScreenManager):
    """ScreenManager с анимацией перехода."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition(duration=0.2)


class MonitorApp(App):
    """Главное приложение."""

    def build(self):
        Window.clearcolor = DARK_BG
        Window.size = (400, 800)

        sm = ScreenManagerCustom()
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(MonitorScreen(name="monitor"))

        return sm


if __name__ == "__main__":
    MonitorApp().run()
