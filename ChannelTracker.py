import discord # It's dangerous to go alone! Take this. /ref
from discord import app_commands # v2.0, use slash commands
from discord.ext import commands # required for client bot making

import pymongo # for online database
from pymongo import MongoClient

import sys # kill switch for ChannelTracker (search for :kill)

from datetime import datetime, timedelta
from time import mktime # for unix time code, tracking how often guilds were updated

mongoURI = open("mongo.txt","r").read()
cluster = MongoClient(mongoURI)
TrackerDB = cluster["TrackerDB"]

version = "0.1.0"

intents = discord.Intents.default()
intents.message_content = False
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


@client.event
async def on_ready():
    client.copyGuild  = client.get_guild(981615050664075404)
    client.pasteGuild = client.get_guild(1034084825482661939)
    print(f"[#] Logged in as {client.user}, in version {version}")#,color="green")
    # await client.logChannel.send(f":white_check_mark: **Started ChannelTracker** in version {version}")

@client.event
async def setup_hook():
    client.TrackerDB = TrackerDB

# @client.event
# async def on_message(message):
#     # kill switch, see cmd_addons for other on_message events.
#     if message.author.id == 262913789375021056:
#         if message.content == ":kill now please okay u need to stop.":
#             sys.exit(0)

@client.tree.command(name="update",description="Update slash-commands")
async def updateCmds(itx: discord.Interaction):
    # if not isStaff(itx):
    #     await itx.response.send_message("Only Staff can update the slash commands (to prevent ratelimiting)", ephemeral=True)
    #     return
    await client.tree.sync()
    # commandList = await client.tree.fetch_commands()
    # client.commandList = commandList
    await itx.response.send_message("Updated commands")



def getMatch(snowflake: discord.abc.Snowflake, location):
    try:
        collection = TrackerDB["blacklist"]
        query = {"id": snowflake.id}
    except AttributeError:
        return None
    item = collection.find_one(query)
    if item is not None:
        return "Forbidden"

    collection = TrackerDB["ids"]
    query = {"id": snowflake.id}
    item = collection.find_one(query)
    if item is None:
        return None

    result = discord.utils.find(lambda r: r.id == item["matchingid"], location)
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
## on_guild_channel_create
## on_guild_channel_delete
## on_guild_channel_update
# on_guild_update
# on_guild_emojis_update
# on_guild_stickers_update
# on_guild_role_create
# on_guild_role_delete
# on_guild_role_update
## on_thread_create
## on_thread_update
## on_thread_remove
## on_thread_delete

guildUpdates = []

channeltracker = app_commands.Group(name='channeltracker', description='Interact with ChannelTracker commands')
client.tree.add_command(channeltracker)

@channeltracker.command(name="refresh",description="Copy paste TransPlace roles, channels, and stickers")
async def refresh(itx: discord.Interaction):
    try:
        global guildUpdates
        await itx.response.defer(ephemeral=True)

        blcollection = TrackerDB["ids"]
        blquery   = {"name": "blacklist"}
        search = blcollection.find_one(blquery)
        if search is None:
            blacklist = []
        else:
            blacklist = search
        for role in client.copyGuild.roles:
            collection   = TrackerDB["ids"]
            query     = {"id": role.id}
            print(repr(role))
            if role.id in blacklist:
                continue

            zrole  = getMatch(role, client.pasteGuild.roles)
            if zrole is None:
                zrole = await client.pasteGuild.create_role(
                        name         = role.name,
                        permissions  = role.permissions,
                        colour       = role.colour,
                        hoist        = role.hoist,
                        # display_icon = role.display_icon,
                        mentionable  = role.mentionable,
                        reason       = "Match TransPlace",
                )

                collection.update_one(query, {"$set":{"id":role.id,"matchingid":zrole.id}}, upsert=True)
            else:
                kwargs = dict()
                for attr in ("name", "permissions", "colour","hoist","mentionable","position"):
                    if getattr(zrole, attr) != getattr(role, attr):
                        kwargs[attr] = getattr(role,attr)
                if len(kwargs) == 0:
                    continue
                try:
                    await zrole.edit(
                            **kwargs,
                            reason       = "Match TransPlace",
                    )
                except Exception as ex:
                    print(repr(ex))

        # await itx.followup.send("Successfully updated the roles.",ephemeral=True)
        # return

        if len(guildUpdates) < 2:
            #ignore but still continue the command
            pass
        elif guildUpdates[0]+600 > mktime(datetime.now().timetuple()):
            await itx.response.send_message("You can't update the server more than twice in 10 minutes! (bcuz discord :P)\n"+
            f"You can update it again <t:{guildUpdates[0]+600}:R> (<t:{guildUpdates[0]+600}:t>).", ephemeral = True)
            # ignore entirely, don't continue command
            return
        else:
            # clear and continue command
            guildUpdates = []
        guildUpdates.append(int(mktime(datetime.now().timetuple())))


        for channel in client.copyGuild.channels:
            collection = TrackerDB["ids"]
            query = {"id": channel.id}
            print(repr(channel))
            zchannel  = getMatch(channel, client.pasteGuild.channels)
            zcategory = getMatch(channel.category, client.pasteGuild.categories)
            if zchannel is None:
                if zcategory is None:
                    if type(channel) is not discord.CategoryChannel and channel.category is None:
                        zcategory = client.pasteGuild
                    else:
                        if type(channel) is discord.CategoryChannel:
                            category = channel
                        else:
                            category = channel.category
                        zcategory = await client.pasteGuild.create_category(
                                category.name,
                                position    = category.position,
                                reason      = "Match TransPlace",
                            )

                        if type(channel) is not discord.CategoryChannel:
                            collection.update_one(query, {"$set":{"id":category.id,"matchingid":zcategory.id}}, upsert=True)
                        else:
                            nchannel = zcategory
                if type(channel) is discord.TextChannel:
                    nchannel = await zcategory.create_text_channel(
                            channel.name,
                            # overwrites      = channel.overwrites,
                            position        = channel.position,
                            topic           = channel.topic,
                            slowmode_delay  = channel.slowmode_delay,
                            nsfw            = channel.nsfw,
                            news            = channel.is_news(),
                            default_auto_archive_duration = channel.default_auto_archive_duration,
                            reason          = "Match TransPlace",
                    )
                elif type(channel) is discord.VoiceChannel:
                    nchannel = await zcategory.create_voice_channel(
                            channel.name,
                            # overwrites      = channel.overwrites,
                            position        = channel.position,
                            bitrate         = channel.bitrate,
                            user_limit      = channel.user_limit,
                            rtc_region      = channel.rtc_region,
                            video_quality_mode = channel.video_quality_mode,
                            reason          = "Match TransPlace",
                    )
                elif type(channel) is discord.StageChannel:
                    nchannel = await zcategory.create_stage_channel(
                            channel.name,
                            # overwrites      = channel.overwrites,
                            position        = channel.position,
                            topic           = channel.topic,
                            reason          = "Match TransPlace",
                    )
                elif type(channel) is discord.ForumChannel:
                    ## zcategory should be the guild, aka channel.category is None
                    nchannel = await zcategory.create_forum(
                            channel.name,
                            topic           = channel.topic,
                            category        = channel.category,
                            position        = channel.position,
                            nsfw            = channel.nsfw,
                            slowmode_delay  = channel.slowmode_delay,
                            reason          = "Match TransPlace",
                            default_auto_archive_duration = channel.default_auto_archive_duration,
                    )
                elif type(channel) is discord.CategoryChannel:
                    pass #already handled in zcategory is None, cause category.category is None.
                else:
                    raise Exception("Channel has type that was unaccounted for!")

                collection.update_one(query, {"$set":{"id":channel.id,"matchingid":nchannel.id}}, upsert=True)
            else:
                if channel.category is not None:
                    zcategory = getMatch(channel.category, client.pasteGuild.categories)
                    if zcategory is None:
                        zcategory = await client.pasteGuild.create_category(
                                channel.category.name,
                                position    = channel.category.position,
                                reason      = "Match TransPlace",
                            )
                        collection.update_one(query, {"$set":{"id":channel.category.id,"matchingid":zcategory.id}}, upsert=True)
                else:
                    zcategory = None
                if type(zchannel) is discord.TextChannel:
                    kwargs = dict()
                    for attr in ("name", "topic", "position", "nsfw","permissions_synced","slowmode_delay","type","default_auto_archive_duration"):
                        if getattr(zchannel, attr) != getattr(channel, attr):
                            if attr == "permissions_synced":
                                kwargs["sync_permissions"] = getattr(channel, attr)
                            kwargs[attr] = getattr(channel,attr)
                    if zchannel.category != zcategory:
                        kwargs['category'] = zcategory
                    if len(kwargs) == 0:
                        continue
                    await zchannel.edit(
                        **kwargs,
                        reason          = "Match TransPlace",
                elif type(zchannel) is discord.VoiceChannel:
                    kwargs = dict()
                    for attr in ("name", "bitrate", "nsfw", "user_limit","position","rtc_region","permissions_synced","video_quality_mode"):
                        if getattr(zchannel, attr) != getattr(channel, attr):
                            if attr == "permissions_synced":
                                kwargs["sync_permissions"] = getattr(channel, attr)
                            kwargs[attr] = getattr(channel,attr)
                    if zchannel.category != zcategory:
                        kwargs['category'] = zcategory
                    if len(kwargs) == 0:
                        continue
                    await zchannel.edit(
                        **kwargs,
                        reason          = "Match TransPlace",
                    )
                elif type(channel) is discord.StageChannel:
                    await zchannel.edit(
                            name            = channel.name,
                            position        = channel.position,
                            nsfw            = channel.nsfw,
                            sync_permissions = channel.permissions_synced,
                            category        = zcategory,
                            reason          = "Match TransPlace",
                            rtc_region      = channel.rtc_region,
                            video_quality_mode = channel.video_quality_mode,
                    )
                elif type(channel) is discord.CategoryChannel:
                    await zchannel.edit(
                            name        = channel.name,
                            position    = channel.position,
                            nsfw        = channel.nsfw,
                            reason      = "Match TransPlace",
                            # overwrites = channel.overwrites,
                        )
                elif type(channel) is discord.ForumChannel:
                    await zchannel.edit(
                            names           = channel.name,
                            topic           = channel.topic,
                            position        = channel.position,
                            nsfw            = channel.nsfw,
                            sync_permissions = channel.permissions_synced,
                            category        = zcategory,
                            slowmode_delay  = channel.slowmode_delay,
                            # type            = type(channel),
                            reason          = "Match TransPlace",
                            # overwrites      = channel.overwrites,
                            default_auto_archive_duration = channel.default_auto_archive_duration,
                    )

            if type(zchannel) in [discord.TextChannel, discord.ForumChannel]:
                pass
                # for thread in channel.threads:
                #     zthread  = getMatch(thread, zchannel.threads)
                #     if zthread is None:
                #         await zchannel.create_thread(
                #                 thread.name,
                #                 auto_archive_duration = thread.auto_archive_duration,
                #                 slowmode_delay = thread.slowmode_delay,
                #                 content = "Thread created to match TransPlace's thread layout",
                #                 mention_author = False
                #                 reason = "Match TransPlace",
                #         )
                #         ## this only works for Forum channels. Gotta copy paste it with a text channel's threads too

        await itx.followup.send("Successfully updated the server to the most recent layout and roles.",ephemeral=True)
    except:
        await itx.followup.send("Couldn't update everything! Something went wrong!",ephemeral=True)
        raise

@channeltracker.command(name="fix",description="Delete all roles in the guild")
async def fix(itx:discord.Interaction):
    for role in client.pasteGuild.roles:
        print(repr(role))
        try:
            await role.delete()
        except Exception as ex:
            print(repr(ex))

@channeltracker.command(name="blacklist", description="Disable certain channel's updates")
@app_commands.choices(mode=[
    discord.app_commands.Choice(name="Blacklist a channel or role's update", value=1),
    discord.app_commands.Choice(name="Remove an id from the blacklist", value=2),
    discord.app_commands.Choice(name='Check the blacklisted IDs', value=3)
])
@app_commands.describe(id="What ID do you want to blacklist")
async def blacklist(itx: discord.Interaction, mode: int, id: str):
    if mode == 1: # add an item to the blacklist
        if len(id) > 150:
            await itx.response.send_message("Your ID shouldn't be *that* long...",ephemeral=True)
            return
        try:
            id = int(id)
        except ValueError:
            await itx.reponse.send_message("The ID has to only contain numbers!")
            return
        collection = TrackerDB["blacklist"]
        query = {"name":"blacklist"}
        search = collection.find_one(query)
        if search is None:
            blacklist = []
        else:
            blacklist = search['list']
        blacklist.append(id)
        collection.update_one(query, {"$set":{f"list":blacklist}}, upsert=True)
        await itx.response.send_message(f"Successfully added {repr(id)} to the blacklist. ({len(blacklist)} id{'s'*(len(blacklist)!=1)} in the blacklist now)",ephemeral=True)

    elif mode == 2: # Remove item from blacklist
        try:
            string = int(string)
        except ValueError:
            await itx.response.send_message("To remove an item from the blacklist, you must give the id of the item you want to remove. This should be a number... You didn't give a number...", ephemeral=True)
            return
        collection = TrackerDB["blacklist"]
        query = {"name":"blacklist"}
        search = collection.find_one(query)
        if search is None:
            await itx.response.send_message("There are no items on the blacklist, so you can't remove any either...",ephemeral=True)
            return
        blacklist = search["list"]
        length = len(blacklist)

        try:
            del blacklist[string]
        except IndexError:
            cmd_mention = self.client.getCommandMention("channeltracker blacklist")
            await itx.response.send_message(f"Couldn't delete that ID, because there isn't any item on the list with that ID.. Use {cmd_mention}` mode:Check` to see the IDs assigned to each item on the list",ephemeral=True)
            return
        collection.update_one(query, {"$set":{f"list":blacklist}}, upsert=True)
        await itx.response.send_message(f"Successfully removed '{string}' from the blacklist. It now contains {len(blacklist)} string{'s'*(len(blacklist)!=1)}.", ephemeral=True)
    elif mode == 3:
        collection = TrackerDB["blacklist"]
        query = {"user": itx.user.id}
        search = collection.find_one(query)
        if search is None:
            await itx.response.send_message("There are no IDs in the blacklist, so.. nothing to list here....",ephemeral=True)
            return
        blacklist = search["list"]
        length = len(blacklist)

        ans = []
        for id in range(length):
            ans.append(f"`{id}`: {blacklist[id]}, <#{blacklist[id]}>, <@{blacklist[id]}>, <@&{blacklist[id]}>")
        ans = '\n'.join(ans)
        await itx.response.send_message(f"Found {length} IDs{'s'*(length!=1)}:\n{ans}",ephemeral=True)

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


try:
    client.run(open('token.txt',"r").read())
except SystemExit:
    print("Exited the program forcefully using the kill switch")
