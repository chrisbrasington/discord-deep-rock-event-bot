#!/usr/bin/env python3
import asyncio, datetime, discord, json, signal, random
from datetime import timedelta
from discord.ext import commands
from pytz import timezone
import pytz

# guild configuration and channels
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

# has alerted (Wednesday only)
has_alerted = False

# create a discord client
client = discord.Client(intents=discord.Intents.all())

# event names
event_names = [
    'Deep Rockin\' Wednesdays',
    'Deep Rock Hump Day',
    'oh SH$# it\'s DEEP ROCK WEDNESDAYS',
    'Stony Rock Extrapalooza'
]

# event images
event_images = [
    'eventgals_banner.png',
    'promo.jpg', 
    'meme1.jpg',
    'meme2.jpg'
]

# alarm timer
alarm_timer = 360 #3600 seconds in an hour? 1 appears to be 10 seconds

# alarm handler
async def alarm_handler(signal):
    global guild_config, has_alerted

    print('Alarm triggered!')

    # every alarm check if event exists, if not create it
    await create_event_if_not_exists()
    
    if is_wed():
        if not has_alerted:
            print('alert check - Wednesday but before noon')
            
            # Set the timezone to Denver
            denver_tz = pytz.timezone('America/Denver')

            # Get the current time in Denver
            now = datetime.datetime.now(denver_tz)

            if await has_event() and now.hour >= 12:
                print('alerting to channel!!')
                has_alerted = True
                guild = client.get_guild(guild_config.guild_id)
                gaming = guild.get_channel(guild_config.notify_channel_id)
                await gaming.send(await get_event_url())
        else:
            print('alarm check - Wednesday already alerted')
    else:
        print('alert check - it is not Wednesday')
        has_alerted = False

    # re-signal alarm
    signal.alarm(alarm_timer)

# creation event 
async def create_event(guild, name, event_time, image):
    print(f'creating event on {guild} at {event_time} as {name}')

    event = await guild.create_scheduled_event(
        name=name, 
        start_time=event_time,
        channel = guild.get_channel(guild_config.voice_channel_id), 
        entity_type = discord.EntityType.voice,
        description = 'Come hang out, deep rock and chill.\n\nRepeats every Wednesday afternoon.',
        image = image
        )

# create event if not exists
async def create_event_if_not_exists():
    if not await has_event():

        # get the current guild
        guild = client.get_guild(guild_config.guild_id)

        # random name
        name = random.choice(event_names)
        # random image
        image_pick = random.choice(event_images)

        print(image_pick)
        with open(image_pick, "rb") as image_file:
            image_bytes = image_file.read()

        next_wed = await get_next_wed()

        await create_event(guild, name, 
            next_wed, image_bytes)

# get next Wednesday
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

# get event url
async def get_event_url():
    guild = client.get_guild(guild_config.guild_id)
    found = False

    for event in guild.scheduled_events:
        print(f'exists: {event.name}')
        if event.name in event_names:
            return event.url
    return ''


# check if guild has event
async def has_event():
    global guild_config

    print('Checking if guild has event')

    guild = client.get_guild(guild_config.guild_id)
    found = False

    for event in guild.scheduled_events:
        print(event.name)

    # for event in guild.scheduled_events:
    #     if event.start_time.astimezone(pytz.UTC) < datetime.datetime.now(pytz.UTC):
    #         print(f'already passed: {event.name} at {event.start_time}')    
    #     else:
    #         print(f'exists: {event.name} at {event.start_time}')
    #         if event.name in event_names:
    #             found = True
    
    return found

# is Wednesday now?
def is_wed():
    day_of_week = datetime.datetime.now().astimezone().date().weekday()
    return day_of_week == 2 #wed

# load config from file
def load_config_from_file(filename: str):
    with open(filename, "r") as f:
        json_string = f.read()
        return GuildConfiguration.from_json(json_string)

# on message respond
@client.event
async def on_message(message):
    respond = False
    appendEvent = False
    eventUrl = ''

    # if the message is not from a bot
    if not message.author.bot and client.user in message.mentions:
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
        if(appendEvent):
            response += f'\n{eventUrl}'
        print(response)
        await message.channel.send(response)
        await create_event_if_not_exists()

# handle the ready event
@client.event
async def on_ready():
    print('Bot is ready!')

    channel_id = 737797410041888829
    guild = client.get_guild(guild_config.guild_id)
    botChannel = guild.get_channel(channel_id)

    if botChannel is None:
        print(f"Channel with ID {channel_id} does not exist.")

    await create_event_if_not_exists()

guild_config = load_config_from_file('settings.json')

# read the token from the file
with open("bot_token.txt", "r") as f:
    token = f.read()

signal.signal(signal.SIGALRM, alarm_handler)
signal.setitimer(signal.ITIMER_REAL, 5, 5)
signal.signal(signal.SIGALRM, lambda signum, frame: 
    # alarm_handler(signal)
    asyncio.create_task(alarm_handler(signal))
)
signal.alarm(10)

# run the bot
client.run(token)