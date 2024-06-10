#!/usr/bin/env python3
import asyncio
import datetime
import discord
import json
import random
from datetime import timedelta
from discord.ext import commands
from discord import app_commands
import pytz

# Configure Discord bot
class bot_client(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')

        await self.wait_until_ready()
        if not self.synced:
            with open("config.json") as config_file:
                config = json.load(config_file)

            guild = self.get_guild(config['guild_id'])

            print(f'Syncing commands to {guild.name}...')
            await tree.sync(guild=guild)
            self.synced = True

        commands = await tree.fetch_commands(guild=guild)

        if len(commands) == 0:
            print('No commands registered.')
        else:
            print('Registered commands:')

        for command in commands:
            print(f' {command.name}')

        print('Bot is ready!')

async def setup():
    global bot, tree, guild, guild_id
    
    # Define the guild using the ID from the config file
    with open("config.json") as config_file:
        config = json.load(config_file)
        guild_id = config['guild_id']
    
        guild = discord.Object(id=guild_id)
        # guild = bot.get_guild(guild_id)

# Define bot and tree as global variables
event_name = 'Game Night'
bot = bot_client()
tree = app_commands.CommandTree(bot)
asyncio.run(setup())

# check if guild has event
async def has_event():
    global bot, guild_id

    guild = bot.get_guild(guild_id)

    print('Checking if guild has event')

    found = []

    events = await guild.fetch_scheduled_events()

    print(len(events))

    for event in events:
        print(event.name)

        if event.start_time.astimezone(pytz.UTC) < datetime.datetime.now(pytz.UTC):
            print(f'\talready passed: {event.name} at {event.start_time}')    
        else:
            print(f'\texists: {event.name} at {event.start_time}')

            # if starts with event_name
            if event.name.startswith(event_name):
                print(f'\tfound: {event.name} at {event.start_time}')
                found.append(event)
            else:
                print('\tother event, ignoring')
    
    # sort found by start time
    found.sort(key=lambda x: x.start_time)

    return found

# on message respond
@bot.event
async def on_message(message):
    respond = False
    appendEvent = False
    eventUrl = ''

    # if the message is not from a bot
    if not message.author.bot and bot.user in message.mentions:
        respond = True
        # selectively respond with event url in check
        if 'check' in message.content and await has_event():
            appendEvent = True
            eventUrl = await get_event_url()
    elif 'rock' in message.content and 'ston' in message.content:
        respond = True

    # respond with "rock and stone"
    if respond:
        response = f"Rock and Stone! {message.author.mention}"
        if appendEvent:
            response += f'\n{eventUrl}'
        print(response)
        await message.channel.send(response)

@tree.command(guild=guild, description="Check all events")
async def all(interaction):
    await interaction.response.send_message("Checking all events...")

    events = await has_event()

    if len(events) > 0:
        for event in events:
            await interaction.followup.send(f'{event.name} {event.url}')
    else:
        await interaction.followup.send("No events found.")

@tree.command(guild=guild, description="Check next event")
async def remind(interaction):
    await interaction.response.send_message("Checking for next event...")

    events = await has_event()

    if len(events) > 0:
        # respond with event url
        await interaction.followup.send(f'{events[0].name} {events[0].url}')
    else:
        await interaction.followup.send("No event found.")

@tree.command(guild=guild, description="Start next event")
async def start(interaction):
    await interaction.response.send_message("Starting next event...")

    events = await has_event()

    if len(events) > 0:

        event = events[0]
        await event.edit(status=discord.EventStatus.active)

        print(event.status)
        await interaction.followup.send(f'Started event: {event.name} {event.url}')
    else:
        await interaction.followup.send("No event found.")

@tree.command(guild=guild, description="end event")
async def goodnight(interaction):
    await interaction.response.send_message("End next event...")

    events = await has_event()

    if len(events) > 0:

        event = events[0]
        await event.edit(status=discord.EventStatus.completed)

        print(event.status)
        await interaction.followup.send(f'Ended event: {event.name}')
    else:
        await interaction.followup.send("No event found.")

# read the token from the file
with open("bot_token.txt", "r") as f:
    token = f.read()

bot.run(token)