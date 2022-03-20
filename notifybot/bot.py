from discord.ext import commands
import discord, asyncio, re

from notifybot.task import TaskId

handlers = {}

def register_handler(id):
    def inner_decorator(f):
        handlers[id] = f
        return f
    return inner_decorator

class DiscordBot:

    def __init__(self, task):
        intents = discord.Intents.default()
        intents.members = True
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.bot.loop.create_task(self.check_request())
        self.on_ready = self.bot.event(self.on_ready)
        self.echo = self.bot.command(name='echo')(self.echo)
        self.task = task

    def run(self, token):
        return self.bot.start(token)

    # events
    async def on_ready(self):
        print('bot login')
        
    # commands
    async def echo(self, ctx, arg):
        await ctx.send(arg)

    # request handler
    async def check_request(self):
        while True:
            await asyncio.sleep(0.1)

            while True:
                uid, id, data = self.task.get_request()
                if uid is None:
                    break
                else:
                    if id in handlers:
                        success, result = await handlers[id](self, data)
                        self.task.add_response(uid, success, result)
                    else:
                        self.task.add_response(uid, False, None)

    @register_handler(TaskId.GET_CHANNEL)
    async def get_channels(self, data):
        guilds = {}
        for guild in self.bot.guilds:
            channels = []
            guilds[guild.name] = channels
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):
                    channels.append(channel.name)

        return True, guilds

    @register_handler(TaskId.GET_MEMBER)
    async def get_members(self, data):
        guilds = {}
        for guild in self.bot.guilds:
            members = []
            guilds[guild.name] = members
            for member in guild.members:
                members.append(member.name)

        return True, guilds

    @register_handler(TaskId.SEND_TEXT)
    async def send_text(self, data):
        user_name_or_id = data.get("user") or ""
        guild_name_or_id = data.get("guild") or ""
        channel_name_or_id = data.get("channel") or ""

        result, target = self.get_send_target(user_name_or_id, guild_name_or_id, channel_name_or_id)
        if not result:
            return result, target

        message = data.get("message")
        if message is None:
            return False, "message not found"

        try:
            await target.send(self.replace_tag_name(message))
        except Exception as e:
            return False, str(e)

        return True, None

    @register_handler(TaskId.SEND_EMBED)
    async def send_embed(self, data):
        user_name_or_id = data.get("user") or ""
        guild_name_or_id = data.get("guild") or ""
        channel_name_or_id = data.get("channel") or ""

        result, target = self.get_send_target(user_name_or_id, guild_name_or_id, channel_name_or_id)
        if not result:
            return result, target

        message = data.get("message")
        if message is None:
            return False, "message not found"

        title = message.get("title") or ""
        description = message.get("description") or ""
        color = message.get("color") or "0xFFFFFF"
        fields = message.get("fields")

        embed = discord.Embed(title=title, description=self.replace_tag_name(description), color=int(color, 16))
        
        if isinstance(fields, list):
            for field in fields:
                if isinstance(field, dict):
                    name = field.get("name") or ""
                    value = field.get("value") or ""
                    inline = field.get("inline") or False
                    embed.add_field(name=name, value=self.replace_tag_name(value), inline=inline)
        
        try:
            await target.send(embed = embed)
        except Exception as e:
            return False, str(e)

        return True, None

    # utility
    def replace_tag_name(self, text):
        tags = re.findall(r'<@\w+>', text)
        for tag in tags:
            name = tag[2:-1]
            user = self.get_user(name)
            if user is None:
                text = text.replace(tag, name)
            else:
                text = text.replace(name, str(user.id))
        return text

    def get_guild(self, id_or_name):
        if isinstance(id_or_name, int):
            return self.bot.get_guild(id_or_name)
        elif isinstance(id_or_name, str):
            try:
                guild_id = int(id_or_name)
                return self.bot.get_guild(guild_id)
            except (ValueError, TypeError):
                guild = discord.utils.get(self.bot.guilds, name=id_or_name)
                return guild
        else:
            return None

    def get_channel(self, id_or_name, guild):
        if isinstance(id_or_name, int):
            return self.bot.get_channel(id_or_name)
        elif isinstance(id_or_name, str):
            try:
                channel_id = int(id_or_name)
                return self.bot.get_channel(channel_id)
            except (ValueError, TypeError):
                channel = discord.utils.get(guild.channels, name=id_or_name)
                return channel
        else:
            return None

    def get_user(self, id_or_name):
        if isinstance(id_or_name, int):
            return self.bot.get_user(id_or_name)
        elif isinstance(id_or_name, str):
            try:
                user_id = int(id_or_name)
                return self.bot.get_user(user_id)
            except (ValueError, TypeError):
                user = discord.utils.get(self.bot.users, name=id_or_name)
                return user
        else:
            return None

    def get_send_target(self, user_name_or_id, guild_name_or_id, channel_name_or_id):
        if not user_name_or_id:
            guild = self.get_guild(guild_name_or_id)
            if guild is None:
                return False, "guild " + str(guild_name_or_id) + " not found"

            channel = self.get_channel(channel_name_or_id, guild)
            if channel is None:
                return False, "channel " + str(channel_name_or_id) + " not found"

            return True, channel

        else:
            user = self.get_user(user_name_or_id)
            if user is None:
                return False, "user " + str(user_name_or_id) + " not found"

            return True, user
