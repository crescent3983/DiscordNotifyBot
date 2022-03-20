import asyncio, os, argparse
from threading import Thread
from dotenv import load_dotenv

from notifybot.bot import DiscordBot
from notifybot.web import WebServer
from notifybot.cmd import CommandLine
from notifybot.task import TaskQueue

load_dotenv()

# argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--daemon', action='store_true', help='daemonized')

args = parser.parse_args()

# task
task = TaskQueue()

# web server
port = os.getenv("WEB_PORT") or 5000
user = os.getenv("WEB_USER")
password = os.getenv("WEB_PASSWORD")

def web_thread_run():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    web = WebServer(task)
    if user is not None and password is not None:
        web.set_auth(user, password)
    web.run(port)

Thread(target=web_thread_run, daemon=True).start()

# discord bot
token = os.getenv("BOT_TOKEN")

def bot_thread_run():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot = DiscordBot(task)
    loop.create_task(bot.run(token))
    loop.run_forever()

Thread(target=bot_thread_run, daemon=True).start()

# interactive shell
if args.daemon:
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    finally:
        loop.close()
else:
    cmd = CommandLine()
    cmd.prompt = '> '
    cmd.cmdloop('Starting prompt...')