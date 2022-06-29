screen -XS todobot quit
sleep 1
source discord-to-do-bot_venv/bin/activate
screen -AmdS todobot python3.10 discord-bot.py
