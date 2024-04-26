import discord
from discord.ext import commands


class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        mes = ["!create <task>: Create a task.",
        "!list_tasks: List all tasks with their indexes.",
        "!remove <index>: Remove a task.",
        "!set_time <index> <time>: Set daily reminder. Time format - <HH:MM>",
        "!remove_time <index>: Remove a timer."
        "!help: Show this help message."]

        channel = self.get_destination()
        await channel.send("\n".join(mes))