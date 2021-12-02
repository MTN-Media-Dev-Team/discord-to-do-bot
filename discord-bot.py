import discord
from discord.ext import tasks
import os
import sys
import mysql.connector
import hashlib
import time
import asyncio
import json

import configcreator

version = "V0.1.0-bot"
devchannel = "dev"
versiondate = "02.12.2021 22:00 UTC"
longversion = f"{version} {devchannel} {versiondate} - by MTN Media Dev Team"
programname = "To-Do Discord Bot"
longprogramname = f"{programname} - by MTN Media Dev Team"
print(longprogramname)
print(longversion)

configcreator.createSampleConfig(version, programname, devchannel, versiondate)

def getConfigInfo(config):
    print("Please enter your discord bot information")
    config.set("DISCORD", "token", input("Token: "))
    print("Please enter your discord todo list channel id")
    insert = [[input("Channel ID: "), "none"]]
    config.set("DISCORD", "todo_list_channel_id", json.dumps(insert))
    configcreator.writeConfig(config)
    return configcreator.getConfig()

config = configcreator.getConfig()
if config.get("DISCORD", "token") == "none" or config.get("DISCORD", "todo_list_channel_id") == "none":
    config = getConfigInfo(config)

#ask if user wants to add channel
print("Do you want to add a channel? (y/n)")
addchannel = input()
if addchannel == "y":
    print("Please enter channel id to add")
    channelid = input()
    config = configcreator.getConfig()
    channels = json.loads(config.get("DISCORD", "todo_list_channel_id"))
    channels.append([channelid, "none"])
    config.set("DISCORD", "todo_list_channel_id", json.dumps(channels))
    configcreator.writeConfig(config)

client = discord.Client()



def strCleanup(string):
    string = string.replace('(', '')
    string = string.replace(')', '')
    string = string.replace(',', '')
    string = string.replace('\'', '')
    string = string.replace('§', ', ')
    return string

async def addtolist(channeldata, message, config, author):

    if channeldata[1] != "none":
        msg = 0
        try:
            channel = client.get_channel(int(channeldata[0]))
            msg = await channel.fetch_message(int(channeldata[1]))
        except Exception:
            print(f"Message {channeldata[1]} could not be fetched")
        if msg != 0:
            edited_embed = discord.Embed(title="TO-DO-LIST", description=config.get("DISCORD", "description"), color=0xff0000)
            edited_embed.set_footer(text=longprogramname)
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
        edited_embed.set_footer(text=longprogramname)
        edited_embed.add_field(name=str(1), value=f":x: {message}", inline=False)
        channel = client.get_channel(int(channeldata[0]))
        msg = await channel.send(embed=edited_embed)
        channels = json.loads(config.get("DISCORD", "todo_list_channel_id"))
        for channelelement in channels:
            if channelelement[0] == str(channeldata[0]):
                channelelement[1] = str(msg.id)
        config.set("DISCORD", "todo_list_channel_id", json.dumps(channels))
        configcreator.writeConfig(config)

async def removefromlist(channeldata, id, config):
    if channeldata[1] != "none":
        msg = None
        try:
            channel = client.get_channel(int(channeldata[0]))
            msg = await channel.fetch_message(int(channeldata[1]))
        except Exception:
            print(f"Message {channeldata[1]} could not be fetched")
        if msg is not None:
            edited_embed = discord.Embed(title="TO-DO-LIST", description=config.get("DISCORD", "description"), color=0xff0000)
            edited_embed.set_footer(text=longprogramname)
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
        print("No to-do list message id found")

async def markasdone(channeldata, id, config):
    if channeldata[1] != "none":
        msg = None
        try:
            channel = client.get_channel(int(channeldata[0]))
            msg = await channel.fetch_message(int(channeldata[1]))
        except Exception:
            print(f"Message {channeldata[1]} could not be fetched")
        if msg is not None:
            edited_embed = discord.Embed(title="TO-DO-LIST", description=config.get("DISCORD", "description"), color=0xff0000)
            edited_embed.set_footer(text=longprogramname)
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
        print("No to-do list message id found")

async def markasundone(channeldata, id, config):
    if channeldata[1] != "none":
        msg = None
        try:
            channel = client.get_channel(int(channeldata[0]))
            msg = await channel.fetch_message(int(channeldata[1]))
        except Exception:
            print(f"Message {channeldata[1]} could not be fetched")
        if msg is not None:
            edited_embed = discord.Embed(title="TO-DO-LIST", description=config.get("DISCORD", "description"), color=0xff0000)
            edited_embed.set_footer(text=longprogramname)
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
        print("No to-do list message id found")

async def editlist(channeldata, id, message, config, author):
    if channeldata[1] != "none":
        msg = 0
        try:
            channel = client.get_channel(int(channeldata[0]))
            msg = await channel.fetch_message(int(channeldata[1]))
        except Exception:
            print(f"Message {channeldata[1]} could not be fetched")
        if msg != 0:
            edited_embed = discord.Embed(title="TO-DO-LIST", description=config.get("DISCORD", "description"), color=0xff0000)
            edited_embed.set_footer(text=longprogramname)
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
        print("No to-do list message id found")


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    config = configcreator.getConfig()
    msg = message.content
    ischannel = 0
    channel = None
    channels = json.loads(config.get("DISCORD", "todo_list_channel_id"))
    for channelelement in channels:
        if message.channel.id == int(channelelement[0]):
            ischannel = 1
            channel = channelelement
            break
    if ischannel == 1:
        if str(message.author) == 'Mats#2002' or str(message.author) == 'Asher (They|Them)#4931' or str(message.author) == 'Laurenzo#7927':
            if msg.startswith('[todo'):
                x = msg.split()
                try:
                    test = x[1] 
                    test2 = x[2] 
                except Exception:
                    print("No command found")
                    return
                if x[1] == "add":
                    config = configcreator.getConfig()
                    await addtolist(channel, msg.partition(' ')[2].partition(' ')[2], config, str(message.author))
                    config = configcreator.getConfig()
                elif x[1] == "remove":
                    config = configcreator.getConfig()
                    await removefromlist(channel, x[2], config)
                elif x[1] == "edit":
                    try:
                        test3 = x[3]
                    except Exception:
                        print("no text found")
                        return
                    config = configcreator.getConfig()
                    await editlist(channel, x[2], msg.partition(' ')[2].partition(' ')[2].partition(' ')[2], config, str(message.author))
                    config = configcreator.getConfig()
                elif x[1] == "done":
                    config = configcreator.getConfig()
                    await markasdone(channel, x[2], config)
                elif x[1] == "undone":
                    config = configcreator.getConfig()
                    await markasundone(channel, x[2], config)
                await message.delete()

token = config.get("DISCORD", "token")
client.run(token)
