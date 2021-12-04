# discord-to-do-bot
Simple Discord toDo list bot using python 3.6 or higher

# Install and configuration
## Installation
Put all .py files into a folder and run the discord-bot.py using python 3.6 or higher. YOu will then automatically get asked by the system to input your Discord Bot token, one channel id where the bot should look for commands, one users discord tag and one administrators discord tag. This information will be saved in the config.cfg file. If you want to change this information at any time, just go into that file and change it, but make sure to keep the formatting of that file the same!

## Adding Users or Administrators
To add users or administrators you currently have to ad them manually to the list in the config file.

## Adding channels to the system
To add a channel just type into any channel of a server where the bot is a member the "\[todoadmin addchannel" command. You need to be a bot admin to do that. After this is done you can use all other command as usual. If you remove a channel type the "\[todoadmin removechannel" command. This will remove the channel and delete a ToDo list if there is one in that channel.

## Adding a todo list
The ToDo List will automaticall be created if you just add one thing to the list in a channel that is added to the bot configuration.

# Commands

\[todo add (message)      - This command adds the message to the todo list
\[todo remove (ID)        - This command removes the message with the given ID from the list
\[todo done (ID)          - This command marks the message with the given ID as done with a "white check mark"
\[todo undone (ID)        - This command marks the message with the given ID as NOT done with a "red X"

\[todoadmin addchannel    - This command adds this channel to the bot listening list
\[todoadmin removechannel - This command removed this channel from the bot listening list and removes the currently present To-Do-Lists
