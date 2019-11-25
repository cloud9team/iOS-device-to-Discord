# Work with Python 3.7
import discord
import subprocess
from discord.utils import get
import os, fnmatch
from discord.ext import commands
from config import bot_token, devices, bot_channel, bot_prefix
#import json

TOKEN = bot_token

bot = commands.Bot(command_prefix=bot_prefix)
bot.remove_command('help')

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(pass_context=True)
async def help(ctx):
    msg = "!delete <device_name> - delete RDM-UIC from device\n!listapps <device_name> - list apps on device\n!mac - screenshot of computer\n!reboot <device_name> - reboot device\n!sc <device_name> - screenshot of device"
    await bot.send_message(discord.Object(id=bot_channel), msg )

@bot.command(pass_context=True)
async def reboot(ctx, device):
    name = str(device)
    MyOut = subprocess.Popen(['idevicediagnostics', '-u', devices.get(name), 'restart'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = MyOut.communicate()
    await bot.send_message(discord.Object(id=bot_channel), stdout.decode("utf-8") )

@bot.command(pass_context=True)
async def sc(ctx, device):
    # take screenshot of device
    name = str(device)
    MyOut = subprocess.Popen(['idevicescreenshot', '-u', devices.get(name), device+'.png'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout = MyOut.communicate()
    await bot.send_file(discord.Object(id=bot_channel), name+'.png')

@bot.command(pass_context=True)
async def listapps(ctx, device):
    name = str(device)
    MyOut = subprocess.Popen(['ideviceinstaller', '-u', devices.get(name), '--list-apps'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = MyOut.communicate()
    await bot.send_message(discord.Object(id=bot_channel), stdout.decode("utf-8") )

@bot.command(pass_context=True)
async def delete(ctx, device):
    name = str(device)
    MyOut = subprocess.Popen(['ideviceinstaller', '-u', devices.get(name), '--uninstall', 'com.apple.test.RealDeviceMap-UIControlUITests-Runner'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = MyOut.communicate()
    await bot.send_message(discord.Object(id=bot_channel), stdout.decode("utf-8") )

@bot.command(pass_context=True)
async def mac(ctx):
    MyOut = subprocess.Popen(['screencapture', 'mac.jpg'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout = MyOut.communicate()
    await bot.send_file(discord.Object(id=bot_channel), 'mac.jpg')

bot.run(TOKEN)
