# iOS-device-to-Discord
A Python bot for discord using libimobiledevice to control connected devices through discord.

First and foremost!! Credit to the person who originally posted this script. This is a revision of that script using discord bot ext combined with some added functionality.
Requirements: Python 3.7.2
Mac OS (untested on linux or windows) 
some Ios devices connected via usb

Install Instructions:

1. install discord py for python 3.7

python3 -m pip install discord.py==0.16.12

python3 -m pip install -U https://github.com/Rapptz/discord.py/archive/async.zip#egg=discord.py[voice]

pip3 install --upgrade aiohttp
(ignore error "discord.py requires aiohttp <1.03 installing aiohttp which is incompatible with discord.py)

pip3 install --upgrade websockets
(ignore same error related to sockets)

2. Install Libimobiledevice

brew update

brew uninstall --ignore-dependencies libimobiledevice

brew uninstall --ignore-dependencies usbmuxd

brew install --HEAD usbmuxd

brew unlink usbmuxd

brew link usbmuxd

brew install --HEAD libimobiledevice

brew unlink libimobiledevice && brew link libimobiledevice

brew install --HEAD  ideviceinstaller

brew unlink ideviceinstaller && brew link ideviceinstaller

sudo chmod -R 777 /var/db/lockdown/

3. Create a discord bot at https://discordapp.com/developers/applications/

Get bot token. Invite bot to discord server

Open config.example.py and save as config.py - edit config values
