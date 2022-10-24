import discord # It's dangerous to go alone! Take this. /ref
from discord import app_commands # v2.0, use slash commands
from discord.ext import commands # required for client bot making

import pymongo # for online database
from pymongo import MongoClient

import sys # kill switch for ChannelTracker (search for :kill)

mongoURI = open("mongo.txt","r").read()
cluster = MongoClient(mongoURI)
TrackerDB = cluster["TrackerDB"]

version = "0.0.1"

intents = discord.Intents.default()
intents.members = True #apparently this needs to be additionally defined cause it's not included in Intents.default()?
intents.message_content = True #apparently it turned off my default intent or something: otherwise i can't send 1984, ofc.
#setup default discord bot client settings, permissions, slash commands, and file paths
intents.emojis_and_stickers = True
intents.guilds = True


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

client = Bot(
        intents = intents,
        command_prefix = "/!\"@:\#", #unnecessary, but needs to be set so.. uh.. yeah. Unnecessary terminal warnings avoided.
        case_insensitive=True,
        # activity = discord.Game(name="with slash (/) commands!"),
        allowed_mentions = discord.AllowedMentions(everyone = False)
    )

copyGuild  = client.get_guild(981615050664075404)
pasteGuild = client.get_guild(1034084825482661939)

@client.event
async def on_ready():
    print(f"[#] Logged in as {client.user}, in version {version}")#,color="green")
    # await client.logChannel.send(f":white_check_mark: **Started Rina** in version {version}")

@client.event
async def setup_hook():
    client.TrackerDB = TrackerDB

@client.event
async def on_message(message):
    # kill switch, see cmd_addons for other on_message events.
    if message.author.id == 262913789375021056:
        if message.content == ":kill now please okay u need to stop.":
            sys.exit(0)

def getMatch(snowflake: discord.abc.Snowflake):
    collection = TrackerDB["blacklist"]
    query = {"id": snowflake.id}
    item = collection.find_one(query)
    if item is not None:
        return "Forbidden"

    collection = TrackerDB["ids"]
    query = {"id": snowflake.id}
    item = collection.find_one(query)
    if item is None:
        return None

    result = discord.utils.find(lambda r: r.id == item["matchingid"], globals()[item["location"]])
    if result is None:
        return None
    else:
        return result #redundant: # TODO:

    old = {
    #
    # if type(snowflake) == discord.Guild:
    #     guild.id
    # if type(snowflake) == discord.abc.GuildChannel:
    #     if type(snowflake) == discord.CategoryChannel:
    #         pass
    #     if type(snowflake) == discord.ThreadChannel:
    #         pass
    # if type(snowflake) == discord.Emoji:
    #     pass
    # if type(snowflake) == discord.GuildSticker:
    #     pass
    }

### Update Events
# on_guild_channel_create
# on_guild_channel_delete
# on_guild_channel_update
# on_private_channel_update
# on_guild_update
# on_guild_emojis_update
# on_guild_stickers_update
# on_guild_role_create
# on_guild_role_delete
# on_guild_role_update
# on_thread_create
# on_thread_update
# on_thread_remove
# on_thread_delete


@client.tree.command(name="updateChannels",description="Copy paste TransPlace channels")
for channel in copyGuild.channels:
    zchannel  = getMatch(channel)
    zcategory = getMatch(channel.category)
    if zchannel is None:
        zcategory
    else:
        if channel.name != zchannel.name:
            pass
        if channel.description != zchannel.description:
            pass
        if channel.slowmode != zchannel.slowmode:
            pass
        if channel.position != zchannel.permission:
            pass
        if channel.category != zcategory:
            pass





# @client.event
# async def on_guild_channel_create(channel):
#     zchannel = getMatch(channel)
#     if zchannel is not None:
#         return # channel seems to have been created already it seems?
#     zcategory = getMatch(channel)
#     if zcategory is None:
#         return # channel seems to have been created already it seems?
#     pasteGuild.
#     pass
#
# @client.event
# async def on_guild_channel_delete(channel):
#     pass
#
# @client.event
# async def on_guild_channel_update(before, after):
#     pass
#
# @client.event
# async def on_private_channel_update(before, after):
#     pass
#
# @client.event
# async def on_guild_update(before, after):
#     pass
#
# @client.event
# async def on_guild_emojis_update(guild, before, after):
#     pass
#
# @client.event
# async def on_guild_stickers_update(guild, before, after):
#     pass
#
# @client.event
# async def on_guild_role_create(role):
#     pass
#
# @client.event
# async def on_guild_role_delete(role):
#     pass
#
# @client.event
# async def on_guild_role_update(role):
#     pass
#
# @client.event
# async def on_thread_create(thread):
#     pass
#
# @client.event
# async def on_thread_update(before, after):
#     pass
#
# @client.event
# async def on_thread_remove(thread):
#     pass
#
# @client.event
# async def on_thread_delete(thread):
#     pass


try:
    client.run(open('token.txt',"r").read())
except SystemExit:
    print("Exited the program forcefully using the kill switch")
