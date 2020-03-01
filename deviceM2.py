# Work with Python 3.7
import discord
import subprocess
from discord.utils import get
import os, fnmatch
from discord.ext import commands
from datetime import datetime as d
from config import bot_token, devices, bot_channel, bot_prefix, app_alias
import json

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
    await bot.change_presence(game=discord.Game(name='with all the connections.'),
                                 status=discord.Status('online'))
    msg = "**I'm alive again.**"
    await bot.send_message(discord.Object(id=bot_channel), msg)

#@bot.command(pass_context=True)
#async def ping(ctx):
#    start = d.timestamp(d.now())
#    message = bot.send_message(discord.Object(id=bot_channel), content='Pinging')
#    await message.edit(msg, content='Pong!\nPing time: {( d.timestamp( d.now() ) - start ) * 1000 }ms.')

@bot.command(pass_context=True)
async def help(ctx, *, cmd: None):
    cmd_help = str(cmd)
    if cmd_help is not None:
       if cmd_help == 'reboot':
           msg = "(p)reboot <device_name> or <all> Ex: !reboot device1 - reboots device1."       
       elif cmd_help == 'delete':
           msg = ("(p)delete [<device_name> | <all>] <app_alias> Ex: !delete device1 app3 - Delete app3 from device1." +
               "\nReplace device1 with all to delete app3 from all devices.")       
       elif cmd_help == 'sc':
           msg = "(p)sc <device_name> Ex: !sc device1 - Upload screen capture of device1."              
       elif cmd_help == 'mac':
           msg = "(p)mac Ex: !mac - Upload screen capture of Mac connected to devices."                     
       else:
           msg = "No command named " + cmd_help + " found."
    else:       
        msg = ("Type (p)help <commmand> for specific command help\n!delete <device_name> <app_alias> - delete app from device" +
            "\n!listapps <device_name> - list apps on device" +
            "\n!mac - screenshot of computer\n!reboot [<device_name> | <all>] - reboot single device or all" +
            "\n!sc <device_name> - screenshot of device")
    await bot.send_message(discord.Object(id=bot_channel), msg )

@bot.command(pass_context=True)
async def reboot(ctx, device):
    """(p)reboot <device_name> - reboot device. Replace <device_name> with <all> to reboot all devices."""
    name = str(device)
    if name == 'all':
        for d in devices:
            dname = devices[d]
            MyOut = subprocess.Popen(['idevicediagnostics', '-u', dname, 'restart'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            stdout,stderr = MyOut.communicate()
            await bot.send_message(discord.Object(id=bot_channel), stdout.decode("utf-8") )
    else:        
        try:
            MyOut = subprocess.Popen(['idevicediagnostics', '-u', devices.get(name), 'restart'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            stdout,stderr = MyOut.communicate()
            await bot.send_message(discord.Object(id=bot_channel), stdout.decode("utf-8") )
        except:
            await bot.send_message(discord.Object(id=bot_channel), "No device named " + name + " found.")
            
@bot.command(pass_context=True)
async def sc(ctx, device):
    """(p)sc <device_name> - Get screen capture of device and upload to channel."""
    name = str(device)
    if name == 'all':
        for k,v in devices.items():
            MyOut = subprocess.Popen(['idevicescreenshot', '-u', v, k+'.png'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            stdout = MyOut.communicate()
            await bot.send_file(discord.Object(id=bot_channel), k+'.png')
            await bot.send_message(discord.Object(id=bot_channel), k)
    else:
        try:
            MyOut = subprocess.Popen(['idevicescreenshot', '-u', devices.get(name), device+'.png'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            stdout = MyOut.communicate()
            await bot.send_file(discord.Object(id=bot_channel), name+'.png')
        except:
            await bot.send_message(discord.Object(id=bot_channel), "No device named " + name + " found.")

@bot.command(pass_context=True)
async def dl(ctx, message:str):
    try:
        url = (message)
        print(url, file=open('/Users/pokemon/Desktop/automation/ipa/url.txt', 'w'))
        MyOut = subprocess.Popen(['megadl', url],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout,stderr = MyOut.communicate()
        await bot.send_message(discord.Object(id=bot_channel), stdout.decode("utf-8") )
    except:
        await bot.send_message(discord.Object(id=bot_channel), "Download failed")        
        
@bot.command(pass_context=True)
async def listapps(ctx, device):
    name = str(device)
    try:
        MyOut = subprocess.Popen(['ideviceinstaller', '-u', devices.get(name), '--list-apps'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout,stderr = MyOut.communicate()
        await bot.send_message(discord.Object(id=bot_channel), stdout.decode("utf-8") )
    except:
        await bot.send_message(discord.Object(id=bot_channel), "No device named " + name + " found.")
    
@bot.command(pass_context=True)
async def delete(ctx, device, app):
    """(p)delete <device_name> <app_alias> - Delete app from device using alias defined in config. Replace <device_name> with <all> to delete app from all devices."""

    name = str(device)
    alias = app_alias[app]
    try:
        if name == 'all':
            for d in devices:
                dname = devices[d]
                print(dname)
                MyOut = subprocess.Popen(['ideviceinstaller', '-u', dname, '--uninstall',
                    str(alias)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                stdout,stderr = MyOut.communicate()
                await bot.send_message(discord.Object(id=bot_channel), stdout.decode("utf-8") )
        else:
            MyOut = subprocess.Popen(['ideviceinstaller', '-u', devices.get(name), '--uninstall',
                str(alias)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            stdout,stderr = MyOut.communicate()
            await bot.send_message(discord.Object(id=bot_channel), stdout.decode("utf-8") )
    except:    
        await bot.send_message(discord.Object(id=bot_channel), "Error in device name or app not found.")

@bot.command(pass_context=True)
async def mac(ctx):
   #MyOut2 = subprocess.run(['/path_to/sleepdisplay/dist/1.1/x64/SleepDisplay', '-wake'])
    MyOut = subprocess.Popen(['screencapture', 'mac.jpg'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout = MyOut.communicate()
    await bot.send_file(discord.Object(id=bot_channel), 'mac.jpg')

bot.run(TOKEN)
