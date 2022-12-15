import discord
from datetime import datetime, timedelta

# create a discord client
client = discord.Client(intents=discord.Intents.all())

event_names = [
    'Deep Rockin\' Wednesdays',
    'DEEP ROCK WEDnesdays',
    'Deep Rock Hump Day',
    'oh SH$# it\'s DEEP ROCK WEDNESDAYS'
]

# define the event name, time, and image
# event_name = "Deep Rockin' Wednesdays"
# event_time = datetime.now() + timedelta(days=7, hours=20)
# event_image = 'eventgalsbanner.png'

# define the event creation function
# async def create_event(guild, name, time, image):
#     # create the event
#     event = await guild.create_event(name=name, tz=time.tzinfo, start=time, end=time+timedelta(hours=1))
#     # set the event thumbnail
#     await event.set_thumbnail(url=image)
#     # send a confirmation message
#     await event.send(f"Event '{name}' has been created at {time} with image {image}")

# handle the ready event
# @client.event
# async def on_ready():
    # # get the current guild
    # guild = discord.utils.get(client.guilds, name="My Guild")
    # # check if the event exists
    # event_exists = False
    # for event in guild.events:
    #     if event.name == event_name:
    #         event_exists = True
    #         break
    # # if the event does not exist, create it
    # if not event_exists:
    #     await create_event(guild, event_name, event_time, event_image)

async dev has_event():


@client.event
async def on_message(message):
    respond = False
    # if the message is not from a bot
    if not message.author.bot and client.user in message.mentions:
        respond = True
    elif 'rock' in message.content and 'stone' in message.content:
        respond = True

    # respond with "rock and stone"
    if respond:
        await message.channel.send(f"Rock and Stone! {message.author.mention}")

# read the token from the file
with open("bot_token.txt", "r") as f:
    token = f.read()

# run the bot
client.run(token)