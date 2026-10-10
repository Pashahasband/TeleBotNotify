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
requirements = python3==3.14.2,hostpython3==3.14.2,kivy==2.3.1,telethon==1.36.0,pyaes==1.6.1,rsa==4.9.1,pyasn1==0.6.1,aiogram==3.31.0,aiohttp==3.14.4,certifi,yarl==1.25.1,pydantic==2.12.3,pydantic-core==2.41.4,frozenlist==1.8.0,propcache==0.5.4

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
android.ndk = 25b
# (str) Use NDK from ANDROID_NDK_HOME
p4a.ndk_version = 25b
# (str) Use pre-installed NDK
p4a.force_android_sdk_clone = 0

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

# Non-interactive, reproducible Android build configuration.
android.accept_sdk_license = True
p4a.source_dir = .p4a
p4a.local_recipes = ./recipes
source.exclude_dirs = recipes,scripts,.git,.github
