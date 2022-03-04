from configparser import ConfigParser
from pathlib import Path

def createSampleConfig(version, programname, channel, date, longprogramname):
    config = ConfigParser()
    config["GENERAL"] = {
        "version": version,
        "versionchannel": channel,
        "versiondate": date,
        "programname": programname,
        "longprogramname": longprogramname,
    }
    config["DISCORD"] = {
        "token": "none",
        "todo_list_channel_id": "none",
        "todo_list_admins": "none",
        "description": "To add to to-do list write [todo add 'your message'\nTo remove from to-do list write [todo remove 'id as number'\nTo mark as done/undone, write [todo done 'id'\nTo edit a message, write [todo edit 'id' 'new message'",
    }
    with open('configsample.cfg', 'w+') as conf:
        config.write(conf)

    configfile = Path("config.cfg")
    if not configfile.is_file():
        print("NewFile")
        newconfig = resetConfig()

def getSampleConfig():
    config = ConfigParser()
    config.read('configsample.cfg')
    return config

def getVersion():
    config = getSampleConfig()
    return config.get('GENERAL','version')

def getProgramName():
    config = getSampleConfig()
    return config.get('GENERAL','programname')

def getVersionAndProgramName():
    config = getSampleConfig()
    return config.get('GENERAL','version'), config.get('GENERAL','programname')

def resetConfig():
    config = getSampleConfig()
    with open('config.cfg', 'w+') as conf:
        config.write(conf)
    return config

def getAltPW():
    return "jE-AtR&fahuC?lGUsw0t"

def getConfig():
    config = ConfigParser()
    config.read('config.cfg')
    return config

def writeConfig(config):
    with open('config.cfg', 'w+') as conf:
        config.write(conf)
