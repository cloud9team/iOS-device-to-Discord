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
    msg = "!sc <device_name> - screenshot of device\n!reboot <device_name> - reboot device\n!log <device_name> tail last 10 lines of device"
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

#@bot.command(pass_context=True)
#async def log(ctx, device):
# in progress: Send last 10 lines of full log of device
#    args = message.content.split(" ")
#    name = '"*'+args[1]+'*"'
#    fulllog = '"*full*"'
#    MyOut = subprocess.Popen(['find', '.', '-amin' , '1', '-name', name, '!', '-name', fulllog, '-print'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#    stdout,stderr = MyOut.communicate()
        #await client.send_message(message.channel, r[0] )


bot.run(TOKEN)
