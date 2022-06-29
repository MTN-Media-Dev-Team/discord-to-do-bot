import nextcord
from nextcord.ext import tasks
import os
import sys
import time
import asyncio
import json
import logging

import configcreator
import todofunctions
logging.basicConfig(stream=sys.stderr, level=logging.INFO)


if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    logging.CRITICAL(f"Error: This program requires running python 3.6 or higher! You are running {str(sys.version_info[0])}.{str(sys.version_info[1])}")
    input("Press Enter to exit...")
    sys.exit()

version = "V0.1.3"
devchannel = "beta"
versiondate = "04.03.2022 18:00 UTC"
longversion = f"{version} {devchannel} {versiondate} - by MTN Media Dev Team"
programname = "To-Do Discord Bot"
longprogramname = f"{programname} - by MTN Media Dev Team"
print(longprogramname)
print(longversion)

configcreator.createSampleConfig(version, programname, devchannel, versiondate, longprogramname)

config = configcreator.getConfig()
if config.get("DISCORD", "token") == "none" or config.get("DISCORD", "todo_list_channel_id") == "none" or config.get("DISCORD", "todo_list_admins") == "none":
    config = todofunctions.getConfigInfo(config)

client = nextcord.Client()

@client.event
async def on_ready():
    logging.info(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    config = configcreator.getConfig()
    msg = message.content
    ischannel = 0
    channel = None
    channels = json.loads(config.get("DISCORD", "todo_list_channel_id"))
    allowedusers = None
    for channelelement in channels:
        if message.channel.id == int(channelelement[0]):
            ischannel = 1
            channel = channelelement
            allowedusers = channelelement[2]
            break
    if ischannel == 1 and not msg.startswith('[todoadmin'):
        if str(message.author) in allowedusers:
            if msg.startswith('[todo'):
                x = msg.split()
                try:
                    test = x[1] 
                    test2 = x[2] 
                except Exception:
                    logging.debug("No command found")
                    return
                if x[1] == "add":
                    config = configcreator.getConfig()
                    await todofunctions.addtolist(client, channel, msg.partition(' ')[2].partition(' ')[2], config, str(message.author))
                elif x[1] == "remove":
                    config = configcreator.getConfig()
                    await todofunctions.removefromlist(client, channel, x[2], config)
                elif x[1] == "edit":
                    config = configcreator.getConfig()
                    try:
                        test3 = x[3]
                    except Exception:
                        logging.debug("no edit text found - command ignored")
                        return
                    await todofunctions.editlist(client, channel, x[2], msg.partition(' ')[2].partition(' ')[2].partition(' ')[2], config, str(message.author))
                elif x[1] == "done":
                    config = configcreator.getConfig()
                    await todofunctions.markasdone(client, channel, x[2], config)
                elif x[1] == "undone":
                    config = configcreator.getConfig()
                    await todofunctions.markasundone(client, channel, x[2], config)
                await message.delete()
        else:
            if msg.startswith('[todo'):
                sending = await message.channel.send("You do not have permission to use this command")
                logging.warning(f"User {str(message.author)} tried to use a command but does not have permission")
                await message.delete()
    if msg.startswith('[todoadmin'):
        if (str(message.author) in json.loads(config.get("DISCORD", "todo_list_admins"))):
            x = msg.split()
            try:
                test = x[1] 
            except Exception:
                logging.debug("No command found")
                return
            config = configcreator.getConfig()
            if x[1] == "addchannel":
                await todofunctions.addChannelToSystem(client, message.channel.id, message)
                logging.warning(f"Channel {message.channel.id} added to system by {str(message.author)} on server {message.guild.id}")
            elif x[1] == "removechannel" and ischannel == 1:
                await todofunctions.removeChannelFromSystem(client, message.channel.id, message)
                logging.warning(f"Channel {message.channel.id} removed from system by {str(message.author)} on server {message.guild.id}")
            elif x[1] == "adduser" and ischannel == 1:
                await todofunctions.addAllowedUserToChannel(message.channel.id, message)
                logging.warning(f"User added to channel {message.channel.id} by {str(message.author)} on server {message.guild.id}")
            elif x[1] == "removeuser" and ischannel == 1:
                await todofunctions.removeAllowedUserFromChannel(message.channel.id, message)
                logging.warning(f"User removed from channel {message.channel.id} by {str(message.author)} on server {message.guild.id}")
        await message.delete()

token = config.get("DISCORD", "token")
client.run(token)
