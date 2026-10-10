# Android build on VM 113

## Goal
Clone Pashahasband/TeleBotNotify main and run the documented Android debug APK build on VM 113.
Source commit: 6ad9e03f7a57c3b697b90607abe3429654a3e8c8.

## Facts and scope
Ubuntu 26.04, 4 vCPU, 7.3 GiB RAM; existing ubuntu account will execute builds.
The project workflow uses Python 3.11 and Java 17; buildozer.spec targets API 33,
NDK 25b, arm64-v8a and armeabi-v7a. v2 is a gitlink without .gitmodules;
build from the root files as the workflow does.
User approved expanding the root LV to 27 GiB using existing VG free space.
No app deployment, Telegram login or VPN changes are part of this build.

## Implementation
Install host compilation packages, isolated Python 3.11 and Buildozer environment.
Keep logs in /srv/builder-logs and APKs in bin/. Use the existing ubuntu account.
Fix only verified build blockers and record any deviations from upstream.

## Verification
Build process exit 0, APK exists, archive integrity and Android metadata check.
Report source revision, tool versions, artifact path and checksum.

## Rollback
Source/environment changes are confined to the checkout and user tool directories.
Original package list and apt logs are under /srv/builder-logs.
Do not automatically remove dependencies or shrink the expanded filesystem.

## Confirmed build failure and repair
The current pinned p4a revision builds CPython 3.14.2 while its aiohttp recipe
defaults to 3.8.3. Compilation fails on removed CPython C API fields.
Use a local PyProject aiohttp 3.14.4 recipe and its supported pure-Python mode.
Pin Android Python, p4a and application dependencies. Declare pydantic-core
explicitly so p4a cross-compiles the Rust extension for Android.
Install Rust under the existing ubuntu account. Pure-Python HTTP helpers trade
some throughput for portable packaging; application logic is unchanged.
Back up buildozer.spec and preserve failed build outputs before retry.
Verify both APK ABIs and package contents; device runtime testing is separate.

ARMv7 Rust compilation passed, but maturin could not infer the API level.
Set ANDROID_API_LEVEL=21 to match android.minapi and NDK target.

The top-level ANDROID_API_LEVEL was not inherited by maturin's isolated build.
A local pydantic-core recipe now injects it into the recipe build environment.

Pure package installation then failed because Telethon 1.36 has no Python 3.14
wheel and pyaes is sdist-only. Local pure-Python recipes now package both;
rsa 4.9.1 and pyasn1 0.6.1 are explicit wheel dependencies.

The p4a package-stage venv mixed bundled pip 25.3 with pip 26.2.1.
Pin and force-reinstall pip 25.3 in the pinned local p4a checkout before package
resolution. Preserve the failed generated venv for diagnosis.
