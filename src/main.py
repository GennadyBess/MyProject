import discord
import logging
import asyncio
import time
from discord.ext import commands
from help_command import MyHelp

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

TOKEN = "MTIzMzEyODYzMTM3OTgyMDU3NA.GO_dGB.eJUDq3uXw1v4NhRpoF3Q-rgNHYjbRzTc4CsmLY" 

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.help_command = MyHelp()


tasks = {}
timers = {}


# def update_list_tasks():
#     new_list = {}
#     for index, task in enumerate(tasks.values()):
#         new_list[index + 1] = task
#     tasks.clear()
#     for index, task in enumerate(new_list.values()):
#         tasks[index + 1] = task

@bot.command()
async def create(ctx, task):
    tasks[len(tasks) + 1] = task
    await ctx.send(f"Task created: {task}")


@bot.command()
async def list_tasks(ctx):
    if tasks:
        task_list = "\n".join([f"{index}. {task}" for index, task in tasks.items()])
        await ctx.send(f"Tasks:\n{task_list}")
    else:
        await ctx.send("No tasks currently.")


@bot.command()
async def remove(ctx, index: int):
    if index in tasks:
        task = tasks.pop(index)
        #update_list_tasks()
        await ctx.send(f"Task removed: {task}")
    else:
        await ctx.send("Task not found.")


def check_time(time_str):
    try:
        time.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False


@bot.command()
async def set_time(ctx, index: int, time_str: str):
    if index not in tasks:
        await ctx.send("Task index not found.")
        return
    if not check_time(time_str):
        await ctx.send("Incorrect time format. Please use HH:MM format.")
        return

    timers[index] = (time_str, ctx.author.id)
    await ctx.send(f"Task scheduled at {time_str}.")


@bot.command()
async def remove_time(ctx, index):
    if index in timers:
        tmr = timers.pop(index)
        await ctx.send("Timer removed.")
    else:
        await ctx.send("Index is not found.")

@bot.command()
async def list_timers(ctx):
    if timers:
        timer_list = "\n".join([f"{index}. {task}" for index, (task, ids) in timers.items()])
        await ctx.send(f"Timers:\n{timer_list}")
    else:
        await ctx.send("No timers currently.")

async def check_tasks():
    while True:
        current_time = time.strftime("%H:%M")
        for index, (time_str, user_id) in list(timers.items()):
            if time_str == current_time:
                user = bot.get_user(user_id)
                if user:
                    await user.send(f"Reminder: {tasks[index]}")  # Send a private message to the user
                del timers[index]  # Remove the timer after sending the reminder
        await asyncio.sleep(60)  # Check every minute
        
@bot.event
async def on_ready():
    bot.loop.create_task(check_tasks())

if __name__ == "__main__":
    bot.run(TOKEN)

