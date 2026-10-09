"""
Мониторинг Telegram-каналов на наличие определённой фразы.

Использует:
- Telethon (MTProto) для чтения сообщений из каналов
- aiogram (Bot API) для отправки уведомлений через бота

Запуск: python monitor.py
"""

import asyncio
import logging
from telethon import TelegramClient, events
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

import config

# === Настройка логирования ===
logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# === Глобальные объекты ===
telethon_client = TelegramClient(config.SESSION_NAME, config.TELETHON_API_ID, config.TELETHON_API_HASH)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

# ID пользователя, которому отправлять уведомления
# Устанавливается при отправке /start боту
notify_chat_id = None


# === Обработчик команд бота ===
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    """Сохраняет ID пользователя для уведомлений."""
    global notify_chat_id
    notify_chat_id = message.from_user.id
    
    # Сохраняем в config для удобства
    config.NOTIFY_CHAT_ID = notify_chat_id
    
    await message.answer(
        "✅ Бот уведомлений активирован!\n\n"
        f"Уведомления будут приходить сюда.\n"
        "Теперь бот будет мониторить каналы и присылать "
        "сообщения, когда найдёт целевую фразу."
    )
    logger.info(f"✅ Активирован для пользователя {message.from_user.username} (ID: {notify_chat_id})")


@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    """Показывает справку."""
    await message.answer(
        "Доступные команды:\n"
        "/start — активировать уведомления\n"
        "/help — показать справку"
    )


# === Обработчик новых сообщений из каналов ===
async def on_new_message(event):
    """Проверяет сообщение на наличие целевой фразы и отправляет уведомление."""
    text = event.message.message
    if not text:
        return

    # Проверяем совпадение (регистр не важен)
    if config.TARGET_PHRASE.lower() in text.lower():
        # Формируем ссылку на сообщение
        if event.chat.username:
            link = f"https://t.me/{event.chat.username}/{event.message.id}"
        else:
            link = "Ссылка недоступна (канал частный)"

        # Формируем уведомление
        alert_text = (
            f"🚨 <b>Найдено совпадение!</b>\n\n"
            f"📢 <b>Канал:</b> {event.chat.title}\n"
            f"📝 <b>Текст:</b> {text[:250]}{'...' if len(text) > 250 else ''}\n"
            f"🔗 <b>Ссылка:</b> {link}"
        )

        # Отправляем уведомление через бота
        if notify_chat_id:
            try:
                await bot.send_message(
                    chat_id=notify_chat_id,
                    text=alert_text,
                    parse_mode='HTML'
                )
                logger.info(f"Совпадение в '{event.chat.title}'!")
            except Exception as e:
                logger.error(f"Ошибка отправки уведомления: {e}")
        else:
            logger.warning("notify_chat_id не установлен. Отправь /start боту.")


# === Настройка обработчиков Telethon ===
def setup_telethon_handlers():
    """Регистрирует обработчик новых сообщений."""
    chats = list(config.CHANNELS_TO_WATCH)

    if not chats:
        logger.warning("Список каналов пуст! Добавь юзернеймы в config.CHANNELS_TO_WATCH")
        return

    logger.info(f"Мониторинг каналов: {', '.join(config.CHANNELS_TO_WATCH)}")
    logger.info(f"Целевая фраза: '{config.TARGET_PHRASE}'")

    @telethon_client.on(events.NewMessage(chats=chats))
    async def handler(event):
        await on_new_message(event)


# === Основная функция ===
async def main():
    """Запускает мониторинг каналов и бота."""
    setup_telethon_handlers()

    # Запуск Telethon (для первого входа запросит номер и код)
    logger.info("Авторизация в Telegram...")
    await telethon_client.start(phone=config.TELETHON_PHONE)
    logger.info("✅ Авторизация успешна!")

    # Запуск бота (polling)
    logger.info("✅ Запуск бота для уведомлений...")
    logger.info("👀 Мониторинг запущен. Ожидание сообщений...\n")

    # Запускаем оба цикла событий параллельно
    await asyncio.gather(
        telethon_client.run_until_disconnected(),
        dp.start_polling(bot),
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Остановлено пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
