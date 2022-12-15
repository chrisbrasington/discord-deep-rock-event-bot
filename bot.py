#!/usr/bin/env python3
import datetime, discord, random
from datetime import timedelta
from discord.ext import commands
from pytz import timezone

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

# define the event name, time, and image
# event_name = "Deep Rockin' Wednesdays"
# event_time = datetime.now() + timedelta(days=7, hours=20)
# event_image = 'eventgalsbanner.png'

# define the event creation function
async def create_event(guild, name, event_time, image):
    global channel_id, gaming_id

    print('creating event')
    print(guild)
    # create the event
    # https://discordpy.readthedocs.io/en/stable/api.html#discord.Guild.create_scheduled_event
    # channel_type = discord.Entiy
    # print(channel_type)
    print(f'channel_id: {channel_id}')
    print(event_time)

    event = await guild.create_scheduled_event(
        name=name, start_time=event_time,
        channel = guild.get_channel(channel_id), 
        entity_type = discord.EntityType.voice,
        description = 'Come hang out, deep rock and chill.\n\nRepeats every Wednesday afternoon.',
        image = image
        )
    # set the event thumbnail
    # await event.set_thumbnail(url=image)
    # send a confirmation message
    # await event.send(f"Event '{name}' has been created at {time} with image {image}")

    # print(event)

    gaming = guild.get_channel(gaming_id)

    await gaming.send(event.url)


# handle the ready event
@client.event
async def on_ready():
    global guild_id

    # get the current guild
    guild = client.get_guild(guild_id)

    if not await has_event():
        name = random.choice(event_names)

        image_pick = random.choice(event_images)
        print(image_pick)
        with open(image_pick, "rb") as image_file:
            image_bytes = image_file.read()

        next_wed = await get_next_wed()
        print(next_wed)

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


async def has_event():
    guild = client.get_guild(guild_id)
    print(f'{guild.name} events')

    found = False

    for event in guild.scheduled_events:
        print(event.name)
        if event.name in event_names:
            found = True
    
    if found:
        print('Event exists')
    else:
        print('Event not found')
    return found



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

# read the token from the file
with open("bot_token.txt", "r") as f:
    token = f.read()

with open("guild_id.txt", "r") as f:
    guild_id = int(f.read())

with open("channel.txt", "r") as f:
    channel_id = int(f.read())

with open("channel_gaming.txt", "r") as f:
    gaming_id = int(f.read())

# run the bot
client.run(token)