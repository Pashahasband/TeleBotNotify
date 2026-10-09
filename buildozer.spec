[app]

# (str) Title of your application
title = Telegram Monitor

# (str) Use latest python-for-android from master
p4a.source = https://github.com/kivy/python-for-android.git
p4a.branch = master

# (str) Package name
package.name = tgmonitor

# (str) Package domain (needed for android/iOS packaging)
package.domain = org.tgmonitor

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,json,kv

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,telethon,aiogram,aiohttp,certifi,yarl

# (str) Supported orientation (landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25.2.9519653
# (str) Use NDK from ANDROID_NDK_HOME
p4a.ndk_version = 25.2.9519653

# (str) The Android arch to build for
android.archs = arm64-v8a,armeabi-v7a

# (bool) Use python-storage
python.storage = False

# (str) Android logcat filters
logcat.tags = *:D

# (int) Android package source version
version = 0.1.0

# (str) Comment
comment = Мониторинг Telegram-каналов

# (list) Author information
author = Your Name <your@email.com>
