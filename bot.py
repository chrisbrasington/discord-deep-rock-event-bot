#!/usr/bin/env python3
import datetime, discord, json, random
from datetime import timedelta
from discord.ext import commands
from pytz import timezone

class GuildConfiguration:
    def __init__(self, guild_id: int, voice_channel_id: int, notify_channel_id: int):
        self.guild_id = guild_id
        self.voice_channel_id = voice_channel_id
        self.notify_channel_id = notify_channel_id

    def to_json(self):
        return json.dumps({
            "guild_id": self.guild_id,
            "voice_channel_id": self.voice_channel_id,
            "notify_channel_id": self.notify_channel_id
        })

    @classmethod
    def from_json(cls, json_string: str):
        data = json.loads(json_string)
        return cls(**data)

# create a discord client
client = discord.Client(intents=discord.Intents.all())

event_names = [
    'Deep Rockin\' Wednesdays',
    'Deep Rock Hump Day',
    'oh SH$# it\'s DEEP ROCK WEDNESDAYS',
    'Stony Rock Extrapalooza'
]

event_images = [
    'eventgals_banner.png',
    'promo.jpg', 
    'meme1.jpg',
    'meme2.jpg'
]

# define the event creation function
async def create_event(guild, name, event_time, image):
    print(f'creating event on {guild} at {event_time}')

    event = await guild.create_scheduled_event(
        name=name, start_time=event_time,
        channel = guild.get_channel(guild_config.voice_channel_id), 
        entity_type = discord.EntityType.voice,
        description = 'Come hang out, deep rock and chill.\n\nRepeats every Wednesday afternoon.',
        image = image
        )

    gaming = guild.get_channel(guild_config.notify_channel_id)

    await gaming.send(event.url)

# handle the ready event
@client.event
async def on_ready():
    # get the current guild
    guild = client.get_guild(guild_config.guild_id)

    if not await has_event():
        name = random.choice(event_names)

        image_pick = random.choice(event_images)
        print(image_pick)
        with open(image_pick, "rb") as image_file:
            image_bytes = image_file.read()

        next_wed = await get_next_wed()

        await create_event(guild, name, 
            next_wed, image_bytes)

async def get_next_wed():
    # Get the current date and time
    now = datetime.datetime.now().astimezone()

    # Get the current day of the week (0 is Monday, 6 is Sunday)
    day_of_week = now.date().weekday()

    # Calculate the number of days to add to get to the next Wednesday
    days_to_add = 2 - day_of_week
    if days_to_add < 0:
        # If the current day is already Wednesday, add 7 days to get to the next Wednesday
        days_to_add += 7

    # Add the necessary number of days to get to the next Wednesday
    next_wednesday = now + timedelta(days=days_to_add)

    next_wednesday = next_wednesday.replace(hour=20,minute=0)

    return next_wednesday

# check if guild has event
async def has_event():
    guild = client.get_guild(guild_config.guild_id)
    found = False

    for event in guild.scheduled_events:
        print(event.name)
        if event.name in event_names:
            found = True
    
    return found

# load config from file
def load_config_from_file(filename: str):
    with open(filename, "r") as f:
        json_string = f.read()
        return GuildConfiguration.from_json(json_string)

# on message respond
@client.event
async def on_message(message):
    respond = False
    # if the message is not from a bot
    if not message.author.bot and client.user in message.mentions:
        respond = True
    elif 'rock' in message.content and 'ston' in message.content:
        respond = True

    # respond with "rock and stone"
    if respond:
        response = f"Rock and Stone! {message.author.mention}"
        print(response)
        await message.channel.send(response)

guild_config = load_config_from_file('settings.json')

# read the token from the file
with open("bot_token.txt", "r") as f:
    token = f.read()

# run the bot
client.run(token)