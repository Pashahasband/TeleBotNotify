# Telegram Monitor — Android App

Android-приложение для мониторинга Telegram-каналов на наличие определённой фразы.

## Что умеет

- ⚙️ Настройки прямо в приложении (API ID, Hash, токен бота, каналы, фраза)
- 📡 Фоновый мониторинг 3 каналов
- 🔔 Push-уведомления через бота при нахождении фразы
- 📋 Лог событий в реальном времени
- 🌙 Тёмная тема

## Установка

### Способ 1: Buildozer (Linux — рекомендуется)

Buildozer работает только на **Linux** (Ubuntu/Debian). На macOS/Windows — используй Way 2.

```bash
# 1. Установи зависимости
sudo apt update
sudo apt install -y python3-pip build-essential git \
    python3-dev ffmpeg libsdl2-dev libsdl2-image2.0-dev \
    libsdl2-mixer2.0-dev libsdl2-ttf2.0-dev libportmidi-dev \
    libswscale-dev libavformat-dev libavcodec-dev \
    zlib1g-dev libgstreamer1.0 gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good openjdk-17-jdk wget

# 2. Установи buildozer
pip install buildozer cython

# 3. Установи Android SDK/NDK (первый раз)
buildozer android sdk

# 4. Собери APK
buildozer android debug

# APK будет в: bin/TelegramMonitor-0.1.0-arm64-v8a-debug.apk
```

### Способ 2: GitHub Actions (любая ОС)

Используй готовый workflow:

1. Запушь проект на GitHub
2. Создай `.github/workflows/build-android.yml`:

```yaml
name: Build Android
on: [push, workflow_dispatch]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install buildozer cython
      - run: sudo apt update && sudo apt install -y python3-pip build-essential git python3-dev ffmpeg
      - run: buildozer android debug
      - uses: actions/upload-artifact@v4
        with:
          name: apk
          path: bin/*.apk
```

3. Скачай APK из Actions

### Способ 3: Termux (на самом Android)

Если не хочешь собирать APK, запусти прямо на телефоне:

```bash
# Установи Termux из F-Droid (не Play Market!)
pkg update
pkg upgrade
pkg install python git ffmpeg

# Установи зависимости
pip install telethon aiogram kivy

# Скопируй файлы проекта в Termux
# Запусти: python main.py
```

## Структура проекта

```
v2/
├── main.py              # Kivy-приложение (UI)
├── config.py            # Сохранение настроек (JSON)
├── monitor_service.py   # Логика мониторинга (Telethon + aiogram)
├── requirements.txt     # Python-зависимости для Android
├── buildozer.spec       # Конфигурация сборки APK
└── README.md            # Этот файл
```

## Как работает

```
┌──────────────────────────────────────┐
│         Android App (Kivy)           │
│  ┌────────────┐   ┌───────────────┐  │
│  │  Настройки │──▶│  Monitor      │  │
│  │  (JSON)    │   │  Service      │  │
│  └────────────┘   └───────┬───────┘  │
│                           │           │
│                    ┌──────▼───────┐   │
│                    │ Telethon     │   │
│                    │ (чтение     │   │
│                    │  каналов)    │   │
│                    └──────┬───────┘   │
│                           │           │
│                    ┌──────▼───────┐   │
│                    │ aiogram      │   │
│                    │ (уведомления)│   │
│                    └──────────────┘   │
└──────────────────────────────────────┘
```

## Настройка

1. Запусти приложение
2. Перейди в **Настройки**
3. Заполни поля:
   - **API ID** и **API Hash** → [my.telegram.org](https://my.telegram.org)
   - **Номер телефона** → твой номер для авторизации
   - **Токен бота** → от @BotFather
   - **Каналы** → через запятую, без @ (например: `chan1,chan2,chan3`)
   - **Целевая фраза** → что искать
4. Нажми **💾 Сохранить**
5. Перейди в **Мониторинг** → **▶ Старт**
6. При первом запуске введи код из Telegram
7. Напиши своему боту `/start` для активации уведомлений

## Возможные проблемы

| Проблема | Решение |
|----------|---------|
| Сборка падает с ошибкой NDK | Попробуй `android.ndk = 23b` |
| Приложение крашится при старте | Проверь лог: `adb logcat | grep python` |
| Не подключается к Telegram | Проверь API ID/Hash и номер телефона |
| Нет звука уведомлений | Разреши уведомления в настройках Android |
| Большой размер APK (~50-80MB) | Это нормально — включает Python-интерпретатор |

## Размер APK

Ожидаемый размер: **50-80 MB** (включает Python, все библиотеки и Kivy).

## Обновление

Чтобы обновить приложение:
1. Измени код
2. Запусти `buildozer android debug` снова
3. Установи новый APK поверх старого
