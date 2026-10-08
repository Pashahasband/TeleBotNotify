"""
Сервис мониторинга Telegram-каналов.
Запускает Telethon (чтение каналов) и aiogram (отправка уведомлений).
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Callable, List

from telethon import TelegramClient, events
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

import config as app_config


class MonitorService:
    """Сервис мониторинга каналов."""

    def __init__(self):
        self.telethon_client: TelegramClient | None = None
        self.bot: Bot | None = None
        self.dp: Dispatcher | None = None
        self.is_running = False
        self.is_authenticating = False
        self.notify_chat_id = None
        self.log_messages: List[str] = []
        self._on_log_callback: Callable[[str], None] | None = None
        self._on_status_callback: Callable[[str, bool], None] | None = None

    def set_callbacks(
        self,
        on_log: Callable[[str], None],
        on_status: Callable[[str, bool], None],
    ):
        """Устанавливает коллбеки для обновления UI."""
        self._on_log_callback = on_log
        self._on_status_callback = on_status

    def log(self, message: str):
        """Добавляет сообщение в лог и вызывает коллбек."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.log_messages.append(entry)
        # Храним не больше 500 записей
        if len(self.log_messages) > 500:
            self.log_messages = self.log_messages[-500:]
        if self._on_log_callback:
            self._on_log_callback(entry)

    def set_status(self, status: str, running: bool):
        """Устанавливает статус и вызывает коллбек."""
        self.is_running = running
        if self._on_status_callback:
            self._on_status_callback(status, running)

    def _get_config(self) -> dict:
        """Загружает конфигурацию."""
        return app_config.load_config()

    def validate_config(self) -> tuple[bool, str]:
        """Проверяет, что все поля заполнены."""
        cfg = self._get_config()
        missing = []
        if not cfg.get("telethon_api_id"):
            missing.append("API ID")
        if not cfg.get("telethon_api_hash"):
            missing.append("API Hash")
        if not cfg.get("telethon_phone"):
            missing.append("Номер телефона")
        if not cfg.get("bot_token") or cfg.get("bot_token") == "YOUR_BOT_TOKEN_HERE":
            missing.append("Токен бота")
        if not cfg.get("channels"):
            missing.append("Каналы")
        if not cfg.get("target_phrase"):
            missing.append("Целевая фраза")

        if missing:
            return False, f"Не заполнено: {', '.join(missing)}"
        return True, ""

    async def _parse_channels(self, channels_str: str) -> list:
        """Парсит строку каналов в список."""
        channels = [c.strip() for c in channels_str.split(",") if c.strip()]
        # Убираем @ если есть
        channels = [c.lstrip("@") for c in channels]
        return channels

    # ==================== BOT HANDLERS ====================

    async def _cmd_start(self, message):
        """Сохраняет ID пользователя для уведомлений."""
        self.notify_chat_id = message.from_user.id
        if self._on_log_callback:
            self._on_log_callback(
                f"✅ Бот активирован для @{message.from_user.username}"
            )

    async def _cmd_help(self, message):
        """Показывает справку."""
        await message.answer(
            "Доступные команды:\n"
            "/start — активировать уведомления\n"
            "/help — показать справку\n"
            "/status — статус мониторинга"
        )

    async def _cmd_status(self, message):
        """Показывает статус."""
        status = "🟢 Работает" if self.is_running else "🔴 Остановлен"
        await message.answer(f"Мониторинг: {status}")

    # ==================== CHANNEL HANDLER ====================

    async def _on_channel_message(self, event):
        """Обрабатывает новое сообщение из канала."""
        text = event.message.message
        if not text:
            return

        cfg = self._get_config()
        target = cfg.get("target_phrase", "").strip().lower()

        if target and target in text.lower():
            # Формируем ссылку
            if event.chat.username:
                link = f"https://t.me/{event.chat.username}/{event.message.id}"
            else:
                link = "Ссылка недоступна (канал частный)"

            alert_text = (
                f"🚨 <b>Найдено совпадение!</b>\n\n"
                f"📢 <b>Канал:</b> {event.chat.title}\n"
                f"📝 <b>Текст:</b> {text[:250]}{'...' if len(text) > 250 else ''}\n"
                f"🔗 <b>Ссылка:</b> {link}"
            )

            if self.notify_chat_id and self.bot:
                try:
                    await self.bot.send_message(
                        chat_id=self.notify_chat_id,
                        text=alert_text,
                        parse_mode="HTML",
                    )
                    self.log(f"📨 Уведомление отправлено в канал '{event.chat.title}'")
                except Exception as e:
                    self.log(f"❌ Ошибка отправки: {e}")
            else:
                self.log("⚠️ Notify chat ID не установлен. Отправь /start боту")

    # ==================== MAIN LOOP ====================

    async def start_monitoring(self):
        """Запускает мониторинг."""
        # Проверяем конфиг
        valid, msg = self.validate_config()
        if not valid:
            self.set_status(msg, False)
            self.log(f"❌ Ошибка конфигурации: {msg}")
            return

        cfg = self._get_config()
        self.set_status("Подключение...", False)

        try:
            # === Telethon ===
            self.log("📡 Подключение к Telegram (MTProto)...")
            api_id = int(cfg["telethon_api_id"])
            self.telethon_client = TelegramClient(
                cfg.get("session_name", "monitor_session"),
                api_id,
                cfg["telethon_api_hash"],
            )

            # Авторизация
            self.is_authenticating = True
            self.set_status("Авторизация...", False)
            self.log("🔐 Авторизация...")

            await self.telethon_client.start(phone=cfg["telethon_phone"])
            self.log("✅ Авторизация успешна!")

            # Настраиваем обработчик каналов
            channels = await self._parse_channels(cfg["channels"])
            self.log(f"👀 Мониторинг: {', '.join(channels)}")
            self.log(f"🔍 Фраза: '{cfg['target_phrase']}'")

            @self.telethon_client.on(events.NewMessage(chats=channels))
            async def handler(event):
                await self._on_channel_message(event)

            # === Bot API ===
            self.log("🤖 Запуск бота уведомлений...")
            self.bot = Bot(token=cfg["bot_token"])
            self.dp = Dispatcher()

            @self.dp.message(Command("start"))
            async def cmd_start(message):
                await self._cmd_start(message)

            @self.dp.message(Command("help"))
            async def cmd_help(message):
                await self._cmd_help(message)

            @self.dp.message(Command("status"))
            async def cmd_status(message):
                await self._cmd_status(message)

            self.set_status("✅ Мониторинг активен", True)
            self.log("🚀 Мониторинг запущен!")

            # Запускаем оба цикла параллельно
            await asyncio.gather(
                self.telethon_client.run_until_disconnected(),
                self.dp.start_polling(self.bot),
            )

        except ValueError as e:
            self.log(f"❌ Ошибка данных: {e}")
            self.set_status("Ошибка данных", False)
        except Exception as e:
            self.log(f"❌ Ошибка: {e}")
            self.set_status(f"Ошибка: {str(e)[:50]}", False)
        finally:
            self.is_running = False
            self.is_authenticating = False

    async def stop_monitoring(self):
        """Останавливает мониторинг."""
        self.log("🛑 Остановка мониторинга...")
        if self.telethon_client:
            self.telethon_client.stop()
        if self.bot:
            # Dispatcher нужно остановить через event loop
            pass
        self.set_status("Остановлен", False)
        self.log("🛑 Остановлено")

    def get_log(self) -> List[str]:
        """Возвращает последние сообщения лога."""
        return list(self.log_messages)

    def clear_log(self):
        """Очищает лог."""
        self.log_messages.clear()
