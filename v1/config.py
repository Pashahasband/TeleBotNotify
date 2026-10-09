"""
Конфигурация мониторинга Telegram-каналов.

ЗАПОЛНИ:
1. TELETHON_API_ID и TELETHON_API_HASH — из my.telegram.org
2. TELETHON_PHONE — номер телефона для авторизации в Telegram
3. BOT_TOKEN — токен бота от @BotFather
4. CHANNELS_TO_WATCH — юзернеймы каналов (без @)
5. TARGET_PHRASE — фраза для поиска
"""

# === MTProto (Telethon) — для чтения каналов ===
TELETHON_API_ID = 12345678  # Замени на свой api_id с my.telegram.org
TELETHON_API_HASH = '0123456789abcdef0123456789abcdef'  # Замени на свой api_hash
TELETHON_PHONE = '+79991234567'  # Твой номер телефона

# === Bot API — для отправки уведомлений ===
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'  # Токен от @BotFather

# === Настройки мониторинга ===
CHANNELS_TO_WATCH = [
    'channel1',  # Замени на юзернеймы каналов (без @)
    'channel2',
    'channel3',
]

TARGET_PHRASE = 'нужная фраза'  # Фраза для поиска (регистр не важен)

# === Дополнительные настройки ===
SESSION_NAME = 'monitor_session'  # Имя файла сессии (не передавай никому!)
LOG_LEVEL = 'INFO'  # Уровень логирования: DEBUG, INFO, WARNING, ERROR
NOTIFY_CHAT_ID = None  # Устанавливается автоматически при /start бота
