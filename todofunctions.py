import logging, sys
import discord
from discord.ext import tasks
import asyncio
import json
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

import configcreator


def getConfigInfo(config):
    print("Please enter your discord bot information")
    config.set("DISCORD", "token", input("Token: "))
    print("Please enter your discord todo list channel id")
    insert = [[input("Channel ID: "), "none"]]
    config.set("DISCORD", "todo_list_channel_id", json.dumps(insert))
    print("Please enter ONE allowed users discord tag")
    insert2 = [input("Discord Tag: ")]
    config.set("DISCORD", "todo_list_allowed_users", json.dumps(insert2))
    print("Please enter ONE ADMIN users discord tag")
    insert3 = [input("Admin Discord Tag: ")]
    config.set("DISCORD", "todo_list_admins", json.dumps(insert3))
    configcreator.writeConfig(config)
    return configcreator.getConfig()

async def addChannelToSystem(client, channelid, msg):
    config = configcreator.getConfig()
    channels = json.loads(config.get("DISCORD", "todo_list_channel_id"))
    for channelelement in channels:
        if channelelement[0] == str(channelid):
            return
    try:
        channel = client.get_channel(int(channelid))
        logging.info(f"Channel {channel.name} found - channel added by {str(msg.author)} on server {str(msg.guild)}")
    except Exception:
        logging.warning(f"Channel not found - channel added by {str(msg.author)} on server {str(msg.guild)}")
        return
    channels.append([str(channelid), "none"])
    config.set("DISCORD", "todo_list_channel_id", json.dumps(channels))
    configcreator.writeConfig(config)
    msg = await channel.send(f"This channel got added to the ToDo List System by {str(msg.author)}")
    
async def removeChannelFromSystem(client, channelid, message):
    config = configcreator.getConfig()
    channels = json.loads(config.get("DISCORD", "todo_list_channel_id"))
    newchannels = []
    for channelelement in channels:
        if channelelement[0] == str(channelid):
            msg = 0
            try:
                channel = client.get_channel(int(channelelement[0]))
                logging.info(f"Channel {channel.name} found - channel removed by {str(message.author)} on server {str(message.guild)}")
                msg = await channel.fetch_message(int(channelelement[1]))
            except Exception:
                logging.error(f"Message {channelelement[1]} could not be fetched")
                logging.warning(f"Channel not found - channel removed by {str(message.author)} on server {str(message.guild)}")
                return
            if msg != 0:
                await msg.delete()
        else:
            newchannels.append(channelelement)
    config.set("DISCORD", "todo_list_channel_id", json.dumps(newchannels))
    configcreator.writeConfig(config)
    msg = await channel.send(f"This channel got removed from the ToDo List System by {str(message.author)}")




def strCleanup(string):
    string = string.replace('(', '')
    string = string.replace(')', '')
    string = string.replace(',', '')
    string = string.replace('\'', '')
    string = string.replace('§', ', ')
    return string

async def addtolist(client, channeldata, message, config, author):

    if channeldata[1] != "none":
        msg = 0
        try:
            channel = client.get_channel(int(channeldata[0]))
            msg = await channel.fetch_message(int(channeldata[1]))
        except Exception:
            logging.error(f"Message {channeldata[1]} could not be fetched")
        if msg != 0:
            edited_embed = discord.Embed(title="TO-DO-LIST", description=config.get("DISCORD", "description"), color=0xff0000)
            edited_embed.set_footer(text=config.get("GENERAL", "longprogramname"))
            embed = msg.embeds[0]
            embed_dict = embed.to_dict()
            counter = 0
            try:
                fields = embed_dict['fields']
            except Exception:
                counter = -1
            if counter != -1:
                for field in embed_dict['fields']:
                    edited_embed.add_field(name=field['name'], value=field['value'], inline=False)
                    counter += 1
                edited_embed.add_field(name=str(counter + 1), value=f":x: {message} - added by {author}", inline=False)
            else:
                edited_embed.add_field(name=str(1), value=f":x: {message} - added by {author}", inline=False)
            await msg.edit(embed=edited_embed) 
    else:
        edited_embed = discord.Embed(title="TO-DO-LIST", description=config.get("DISCORD", "description"), color=0xff0000)
        edited_embed.set_footer(text=config.get("GENERAL", "longprogramname"))
        edited_embed.add_field(name=str(1), value=f":x: {message}", inline=False)
        channel = client.get_channel(int(channeldata[0]))
        msg = await channel.send(embed=edited_embed)
        channels = json.loads(config.get("DISCORD", "todo_list_channel_id"))
        for channelelement in channels:
            if channelelement[0] == str(channeldata[0]):
                channelelement[1] = str(msg.id)
        config.set("DISCORD", "todo_list_channel_id", json.dumps(channels))
        configcreator.writeConfig(config)

async def removefromlist(client, channeldata, id, config):
    if channeldata[1] != "none":
        msg = None
        try:
            channel = client.get_channel(int(channeldata[0]))
            msg = await channel.fetch_message(int(channeldata[1]))
        except Exception:
            logging.error(f"Message {channeldata[1]} could not be fetched")
        if msg is not None:
            edited_embed = discord.Embed(title="TO-DO-LIST", description=config.get("DISCORD", "description"), color=0xff0000)
            edited_embed.set_footer(text=config.get("GENERAL", "longprogramname"))
            embed = msg.embeds[0]
            embed_dict = embed.to_dict()
            counter = 0
            for field in embed_dict['fields']:
                if field['name'] == str(id):
                    continue
                edited_embed.add_field(name=str(counter + 1), value=field['value'], inline=False)
                counter += 1

        await msg.edit(embed=edited_embed) 
    else:
        logging.warning("No to-do list message id found")

async def markasdone(client, channeldata, id, config):
    if channeldata[1] != "none":
        msg = None
        try:
            channel = client.get_channel(int(channeldata[0]))
            msg = await channel.fetch_message(int(channeldata[1]))
        except Exception:
            logging.error(f"Message {channeldata[1]} could not be fetched")
        if msg is not None:
            edited_embed = discord.Embed(title="TO-DO-LIST", description=config.get("DISCORD", "description"), color=0xff0000)
            edited_embed.set_footer(text=config.get("GENERAL", "longprogramname"))
            embed = msg.embeds[0]
            embed_dict = embed.to_dict()
            counter = 0
            for field in embed_dict['fields']:
                if field['name'] == str(id):
                    edited_embed.add_field(name=field['name'], value=f":white_check_mark: {str(field['value']).replace(':white_check_mark:', '').replace(':x:', '')}", inline=False)
                    continue
                edited_embed.add_field(name=field['name'], value=field['value'], inline=False)
                counter += 1

        await msg.edit(embed=edited_embed) 
    else:
        logging.warning("No to-do list message id found")

async def markasundone(client, channeldata, id, config):
    if channeldata[1] != "none":
        msg = None
        try:
            channel = client.get_channel(int(channeldata[0]))
            msg = await channel.fetch_message(int(channeldata[1]))
        except Exception:
            logging.error(f"Message {channeldata[1]} could not be fetched")
        if msg is not None:
            edited_embed = discord.Embed(title="TO-DO-LIST", description=config.get("DISCORD", "description"), color=0xff0000)
            edited_embed.set_footer(text=config.get("GENERAL", "longprogramname"))
            embed = msg.embeds[0]
            embed_dict = embed.to_dict()
            counter = 0
            for field in embed_dict['fields']:
                if field['name'] == str(id):
                    edited_embed.add_field(name=field['name'], value=f":x: {str(field['value']).replace(':white_check_mark:', '').replace(':x:', '')}", inline=False)
                    continue
                edited_embed.add_field(name=field['name'], value=field['value'], inline=False)
                counter += 1

        await msg.edit(embed=edited_embed) 
    else:
        logging.warning("No to-do list message id found")

async def editlist(client, channeldata, id, message, config, author):
    if channeldata[1] != "none":
        msg = 0
        try:
            channel = client.get_channel(int(channeldata[0]))
            msg = await channel.fetch_message(int(channeldata[1]))
        except Exception:
            logging.error(f"Message {channeldata[1]} could not be fetched")
        if msg != 0:
            edited_embed = discord.Embed(title="TO-DO-LIST", description=config.get("DISCORD", "description"), color=0xff0000)
            edited_embed.set_footer(text=config.get("GENERAL", "longprogramname"))
            embed = msg.embeds[0]
            embed_dict = embed.to_dict()
            counter = 0
            for field in embed_dict['fields']:
                if field['name'] == str(id):
                    edited_embed.add_field(name=field['name'], value=f":x: {message} - edited by {author}", inline=False)
                    continue
                edited_embed.add_field(name=field['name'], value=field['value'], inline=False)
                counter += 1

        await msg.edit(embed=edited_embed) 
    else:
        logging.warning("No to-do list message id found")