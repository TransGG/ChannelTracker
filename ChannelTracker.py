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

version = "1.1.0"

intents = discord.Intents.default()
intents.members = True
intents.message_content = False
intents.emojis_and_stickers = True
intents.guilds = True


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    copyGuild: discord.Guild
    pasteGuild: discord.Guild
    is_dev: int

    tp_entry_allowed_roles = [
        993370301201129572,  # [Head Staff]
        981735525784358962,  # Admin
        1012954384142966807,  # Sr. Mod,
        981735650971775077,  # Moderator
        959916105294569503,  # Verifier
        1087869446707740773, # Supporter+
        1087871081634861117, # Supporter++
    ]
    tp_notable_roles = [
        959748411844874240,  # Verified
        1087868304565219420,  # Supporters
        # Custom roles
        1092822871413362783,  # The Princess (pink, Chroma)

        1087884342673543370,  # Sage green
        1087884432687497276,  # Turbo
        1087884433421516951,  # Viking
        1087884488547258409,  # Mauve
        1087884559091257455,  # Butterfly Bush
        1087884617589198939,  # Red Bud Cherry
        1087884664787705897,  # Carnation
        1087884705736695939,  # Mayochup
        1087884755221102762,  # Color rotation!
        # Color roles
        959562647978790912,  # Red
        959562648394039367,  # Purple
        959562648767328266,  # Green
        959562649274826824,  # Pink
        959562649727811595,  # Orange
        959562650143047680,  # Yellow
        959562650373734400,  # Blue
        964275547742031962,  # Dark Blue
        964275808057323580,  # Dark green
        # Pronoun roles
        959562682736988191,  # He/Him
        959562683085123624,  # She/Her
        959562683496149062,  # They/Them
        964299749236830308,  # It/Its
        959562683491950603,  # Ask Pronouns
        964299652113514506,  # Any Pronouns
    ]

    copy_entry_allowed_roles = [
        1085626136815476806,  # [Head Staff]
        1086348907530965022,  # Admin
        1085626122668097637,  # Sr. Mod,
        1085626108034170920,  # Moderator
        1085626093014364272,  # Verifier
        1089969043034865814,  # Supporter+
        1089969051788390511,  # Supporter++
    ]
    copy_notable_roles = [
        1085625471972159539,  # Verified
        1089969060441235506,  # Supporters
        # Custom roles
        1092852293755474000,  # The Princess (pink, Chroma)

        1089969347956576386,  # Sage green
        1089969337978343555,  # Turbo
        1089969326804705395,  # Viking
        1089969316742574171,  # Mauve
        1089969307099861022,  # Butterfly Bush
        1089969293376098324,  # Red Bud Cherry
        1089969281606885447,  # Carnation
        1089969269871218719,  # Mayochup
        1089969259045716123,  # Color rotation!
        # Color roles
        1085625867490840587,  # Red
        1085625860024967308,  # Purple
        1085625853066625184,  # Green
        1085625846083096638,  # Pink
        1085625839296720966,  # Orange
        1085625833059790898,  # Yellow
        1085625824889286827,  # Blue
        1085625814067978351,  # Dark Blue
        1085625807654891571,  # Dark green
        # Pronoun roles
        1085625778403819683,  # He/Him
        1085625770988294256,  # She/Her
        1085625763539210281,  # They/Them
        1085625757960765450,  # It/Its
        1085625790948978688,  # Ask Pronouns
        1085625784179363913,  # Any Pronouns
    ]

client = Bot(
        intents = intents,
        command_prefix = "/!\"@:\\#", #unnecessary, but needs to be set so.. uh.. yeah. Unnecessary terminal warnings avoided.
        case_insensitive=True,
        # activity = discord.Game(name="with slash (/) commands!"),
        allowed_mentions = discord.AllowedMentions(everyone = False)
    )


@client.event
async def on_ready():
    client.copyGuild  = client.get_guild(959551566388547676) # TransPlace   # testing server: 1034084825482661939
    client.pasteGuild = client.get_guild(981615050664075404) # TransPlace [Copy]
    client.is_dev = 0
    if open('token.txt',"r").read().endswith("NEXPRir4\n"):
        client.is_dev = 1
        client.copyGuild = client.get_guild(981615050664075404)  # TransPlace [Copy]
        client.pasteGuild = client.get_guild(1034084825482661939)  # Dev Copy Copy testing server
    if client.copyGuild is None or client.pasteGuild is None:
        print("WARNINGGGG COULDN'T GET SERVER INFORMATION / ROLES ETC. STUFF THINGIES. SO CAN'T COMPARE SERVERS")
        raise Exception("WARNINGGGG COULDN'T GET SERVER INFORMATION / ROLES ETC. STUFF THINGIES. SO CAN'T COMPARE SERVERS")

    print(f"[#] Logged in as {client.user}, in version {version}" + " (Developer Mode)"*client.is_dev)#,color="green")
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
    if itx.user.id not in [262913789375021056, 317731855317336067, 280885861984239617]: #Mia, Minion, Cleo
        await itx.response.send_message("Only 3 people can update the slash commands (to prevent ratelimiting)", ephemeral=True)
        return
    await client.tree.sync()
    # commandList = await client.tree.fetch_commands()
    # client.commandList = commandList
    await itx.response.send_message("Updated commands")



def getMatch(snowflake: discord.abc.Snowflake | int, location):
    # try:
    #     collection = TrackerDB["blacklist"]
    #     query = {"id": snowflake.id}
    # except AttributeError:
    #     return None
    # item = collection.find_one(query)
    # if item is not None:
    #     return "Forbidden"
    if snowflake is None:
        return None
    collection = TrackerDB["ids"]
    if isinstance(snowflake, discord.abc.Snowflake):
        query = {"id": snowflake.id}
    else:
        query = {"id": int(snowflake)}
    item = collection.find_one(query)
    if item is None:
        return None

    if type(location) is list:
        try:
            for x in location:
                result = discord.utils.find(lambda r: r.id == query["id"], x)
                if result is not None:
                    return result
            return None
        except TypeError:
            pass
    result = discord.utils.find(lambda r: r.id == item["matchingid"], location)
    if result is None:
        return None
    else:
        return result #redundant: # TODO:

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

### Update Events
# on_guild_channel_create
# on_guild_channel_delete
# on_guild_channel_update
## on_guild_update
## on_guild_emojis_update
## on_guild_stickers_update
# on_guild_role_create
# on_guild_role_delete
# on_guild_role_update
# on_thread_create
# on_thread_update
# on_thread_remove
# on_thread_delete

guildUpdates = []

channeltracker = app_commands.Group(name='channeltracker', description='Interact with ChannelTracker commands')
client.tree.add_command(channeltracker)

@channeltracker.command(name="refresh",description="Copy paste TransPlace roles, channels, and stickers")
async def refresh(itx: discord.Interaction):
    try:
        global guildUpdates
        statusMessage = "Fetching id and blacklist data..."
        await itx.response.defer(ephemeral=True)
        await itx.followup.send(statusMessage)
        collection   = TrackerDB["ids"]
        blcollection = TrackerDB["blacklist"]
        blquery   = {"name": "blacklist"}
        search = blcollection.find_one(blquery)
        if search is None:
            blacklist = []
        else:
            blacklist = search['list']
        role: discord.Role


        if len(guildUpdates) < 2:
            #ignore but still continue the command
            pass
        elif guildUpdates[0]+600 > mktime(datetime.now().timetuple()):
            await itx.edit_original_response(content=f"You can't update the server more than twice in 10 minutes! (bcuz discord :P)\n" +
                                                     f"You can update it again <t:{guildUpdates[0]+600}:R> (<t:{guildUpdates[0]+600}:t>).")
            # ignore entirely, don't continue command
            return
        else:
            # clear and continue command
            guildUpdates = []
        guildUpdates.append(int(mktime(datetime.now().timetuple())))

        statusMessage += "\nCreating new roles"
        objectCreations = 0
        objectUpdates = 0
        await itx.edit_original_response(content=statusMessage)

        try:
            for role in client.copyGuild.roles:
                query     = {"id": role.id}
                print("role: ",role.name)
                if role.is_default():
                    zrole = None
                    for zrole in client.pasteGuild.roles:
                        if zrole.is_default():
                            break
                    assert zrole is not None
                else:
                    zrole = getMatch(role, client.pasteGuild.roles)
                if role.id in blacklist:
                    continue
                if zrole is not None:
                    if zrole.id in blacklist:
                        continue
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
                    await zrole.edit(position=role.position, reason="Set correct role position")
                    collection.update_one(query, {"$set":{"id":role.id,"matchingid":zrole.id}}, upsert=True)
                    objectCreations += 1
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
                        objectUpdates += 1
                    except Exception as ex:
                        print(repr(ex))
        except discord.errors.HTTPException:
            statusMessage += f" (stopped early because there are 250 roles in the server!!! :warning:) "
        # await itx.followup.send("Successfully updated the roles.",ephemeral=True)
        # return
        statusMessage += f" (Created {objectCreations} and updated {objectUpdates} roles)"
        statusMessage += "\nAdding new channels"
        objectCreations = 0
        objectUpdates = 0
        await itx.edit_original_response(content=statusMessage)
        for channel in client.copyGuild.channels:
            print("channel: ",channel)
            collection = TrackerDB["ids"]
            query = {"id": channel.id}
            zchannel: [discord.VoiceChannel | discord.StageChannel | discord.ForumChannel | discord.TextChannel | discord.CategoryChannel]
            zchannel                           = getMatch(channel, client.pasteGuild.channels)
            zcategory: discord.CategoryChannel = getMatch(channel.category, client.pasteGuild.categories)
            if channel.id in blacklist:
                continue
            if channel.category is not None:
                if channel.category.id in blacklist:
                    continue
            if zchannel is not None:
                if zchannel.id in blacklist:
                    continue
                if zchannel.category is not None:
                    if zchannel.category.id in blacklist:
                        continue
            zoverwrites = {}
            for target in channel.overwrites:
                ztarget = getMatch(target, client.pasteGuild.roles)
                if ztarget is None:
                    if target in client.pasteGuild.members:
                        ztarget = target
                    else:
                        continue
                    # ztarget = target#getMatch(target, client.pasteGuild.members)
                zoverwrites[ztarget] = channel.overwrites[target]
                # print(ztarget, channel.overwrites[target])
            # print(channel.overwrites, zoverwrites)
            # zoverwrites = {}

            if zchannel is None:
                print(channel,channel.category)
                if zcategory is None:
                    if type(channel) is not discord.CategoryChannel and channel.category is None:
                        zcategory: discord.Guild = client.pasteGuild
                    else:
                        if type(channel) is discord.CategoryChannel:
                            category = channel
                        else:
                            category = channel.category
                        zcategory = await client.pasteGuild.create_category(
                                category.name,
                                overwrites  = zoverwrites,
                                position    = category.position,
                                reason      = "Match TransPlace",
                            )
                        if type(channel) is not discord.CategoryChannel:
                            collection.update_one(query, {"$set":{"id":category.id,"matchingid":zcategory.id}}, upsert=True)
                        else:
                            nchannel = zcategory
                            objectCreations += 1
                if type(channel) is discord.TextChannel:
                    nchannel = await zcategory.create_text_channel(
                            channel.name,
                            overwrites      = zoverwrites,
                            position        = channel.position,
                            topic           = channel.topic,
                            slowmode_delay  = channel.slowmode_delay,
                            nsfw            = channel.nsfw,
                            news            = channel.is_news(),
                            default_auto_archive_duration = channel.default_auto_archive_duration,
                            reason          = "Match TransPlace",
                    )
                elif type(channel) is discord.VoiceChannel:
                    _bitrate = channel.bitrate
                    if _bitrate > 96000:
                        _bitrate = 96000
                    nchannel = await zcategory.create_voice_channel(
                            channel.name,
                            overwrites      = zoverwrites,
                            position        = channel.position,
                            bitrate         = _bitrate,
                            user_limit      = channel.user_limit,
                            rtc_region      = channel.rtc_region,
                            video_quality_mode = channel.video_quality_mode,
                            reason          = "Match TransPlace",
                    )
                elif type(channel) is discord.StageChannel:
                    nchannel = await zcategory.create_stage_channel(
                            channel.name,
                            overwrites      = zoverwrites,
                            position        = channel.position,
                            topic           = channel.topic,
                            reason          = "Match TransPlace",
                    )
                elif type(channel) is discord.ForumChannel:
                    ## zcategory should be the guild, aka channel.category is None
                    nchannel = await zcategory.create_forum(
                            channel.name,
                            topic           = channel.topic,
                            position        = channel.position,
                            nsfw            = channel.nsfw,
                            overwrites      = zoverwrites,
                            slowmode_delay  = channel.slowmode_delay,
                            reason          = "Match TransPlace",
                            default_auto_archive_duration = channel.default_auto_archive_duration,
                    )
                elif type(channel) is discord.CategoryChannel:
                    assert isinstance(nchannel, discord.CategoryChannel)
                    #already handled in zcategory is None, cause category.category is None.
                else:
                    raise Exception(f"Channel has type that was unaccounted for! (Type = {channel.__class__.__name__})")
                objectCreations += 1

                collection.update_one(query, {"$set":{"id":channel.id,"matchingid":nchannel.id}}, upsert=True)
            else:
                if channel.category is not None:
                    zcategory: discord.CategoryChannel = getMatch(channel.category, client.pasteGuild.categories)
                    if zcategory is None:
                        zcategory = await client.pasteGuild.create_category(
                                channel.category.name,
                                overwrites  = zoverwrites,
                                position    = channel.category.position,
                                reason      = "Match TransPlace",
                            )
                        query = {"id": channel.category.id}
                        collection.update_one(query, {"$set":{"matchingid":zcategory.id}}, upsert=True)
                        objectCreations += 1
                else:
                    zcategory = None
                if type(zchannel) is discord.TextChannel:
                    zchannel: discord.TextChannel
                    kwargs = dict()
                    for attr in ("name", "topic", "position", "nsfw","permissions_synced","slowmode_delay","type","default_auto_archive_duration"):
                        if getattr(zchannel, attr) != getattr(channel, attr):
                            if attr == "permissions_synced":
                                kwargs["sync_permissions"] = getattr(channel, attr)
                            else:
                                kwargs[attr] = getattr(channel,attr)
                    if zchannel.category != zcategory:
                        kwargs['category'] = zcategory
                    if zchannel.overwrites != zoverwrites:
                        kwargs['overwrites'] = zoverwrites
                    if len(kwargs) == 0:
                        continue
                    await zchannel.edit(
                        **kwargs,
                        reason          = "Match TransPlace",
                    )
                elif type(zchannel) is discord.VoiceChannel:
                    zchannel: discord.VoiceChannel
                    kwargs = dict()
                    for attr in ("name", "bitrate", "nsfw", "user_limit","position","rtc_region","permissions_synced","video_quality_mode"):
                        if getattr(zchannel, attr) != getattr(channel, attr):
                            if attr == "permissions_synced":
                                kwargs["sync_permissions"] = getattr(channel, attr)
                            elif attr == "bitrate":
                                _bitrate = getattr(channel, attr)
                                if _bitrate > 96000:
                                    _bitrate = 96000
                                kwargs["bitrate"] = _bitrate
                            else:
                                kwargs[attr] = getattr(channel,attr)
                    if zchannel.category != zcategory:
                        kwargs['category'] = zcategory
                    if zchannel.overwrites != zoverwrites:
                        kwargs['overwrites'] = zoverwrites
                    if len(kwargs) == 0:
                        continue
                    await zchannel.edit(
                        **kwargs,
                        reason          = "Match TransPlace",
                    )
                elif type(channel) is discord.StageChannel:
                    zchannel: discord.StageChannel
                    kwargs = dict()
                    for attr in ("name", "position", "nsfw","permissions_synced","rtc_region","video_quality_mode"):
                        if getattr(zchannel, attr) != getattr(channel, attr):
                            if attr == "permissions_synced":
                                kwargs["sync_permissions"] = getattr(channel, attr)
                            else:
                                kwargs[attr] = getattr(channel,attr)
                    if zchannel.category != zcategory:
                        kwargs['category'] = zcategory
                    if zchannel.overwrites != zoverwrites:
                        kwargs['overwrites'] = zoverwrites
                    if len(kwargs) == 0:
                        continue
                    await zchannel.edit(
                        **kwargs,
                        reason          = "Match TransPlace",
                    )
                elif type(channel) is discord.CategoryChannel:
                    zchannel: discord.CategoryChannel
                    kwargs = dict()
                    for attr in ("name", "position", "nsfw"):
                        if getattr(zchannel, attr) != getattr(channel, attr):
                            kwargs[attr] = getattr(channel,attr)
                    if zchannel.overwrites != zoverwrites:
                        kwargs['overwrites'] = zoverwrites
                    if len(kwargs) == 0:
                        continue
                    await zchannel.edit(
                        **kwargs,
                        reason          = "Match TransPlace",
                    )
                elif type(channel) is discord.ForumChannel:
                    zchannel: discord.ForumChannel
                    kwargs = dict()
                    for attr in ("name", "topic", "position", "nsfw","permissions_synced","slowmode_delay","default_auto_archive_duration"):
                        if getattr(zchannel, attr) != getattr(channel, attr):
                            if attr == "permissions_synced":
                                kwargs["sync_permissions"] = getattr(channel, attr)
                            else:
                                kwargs[attr] = getattr(channel,attr)
                    if zchannel.category != zcategory:
                        kwargs['category'] = zcategory
                    if zchannel.overwrites != zoverwrites:
                        kwargs['overwrites'] = zoverwrites
                    if len(kwargs) == 0:
                        continue
                    await zchannel.edit(
                        **kwargs,
                        reason          = "Match TransPlace",
                    )
                objectUpdates += 1

                # print(len(kwargs),kwargs)
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

        statusMessage += f" (Created {objectCreations} and updated {objectUpdates} channels)"
        statusMessage += "\nDeleting unused channels (if not in blacklist)"
        objectUpdates = 0
        objectUnused = 0
        await itx.edit_original_response(content=statusMessage)
        search = collection.find({})
        ids = {item['matchingid']: item['id'] for item in search}
        for zchannel in client.pasteGuild.channels:
            if zchannel.id not in blacklist:
                if zchannel.id in ids: # find if counterpart still exists
                    if not getMatch(ids[zchannel.id], [client.copyGuild.channels]):
                        query = {"matchingid": zchannel.id}
                        collection.delete_one(query)
                        objectUnused += 1
                else:
                    query = {"matchingid": zchannel.id}
                    collection.delete_one(query)
                    await zchannel.delete()
                    objectUpdates += 1

        statusMessage += f" (Deleted {objectUpdates} channels, and {objectUnused} vanished)"
        statusMessage += "\nDeleting unused roles (if not in blacklist)"
        objectUpdates = 0
        objectUnused = 0
        await itx.edit_original_response(content=statusMessage)
        for zrole in client.pasteGuild.roles:
            if zrole.id not in blacklist:
                if zrole.id in ids: # find if counterpart still exists
                    if not getMatch(ids[zrole.id], [client.copyGuild.roles]):
                        query = {"matchingid": zrole.id}
                        collection.delete_one(query)
                        objectUnused += 1
                else:
                    query = {"matchingid": zrole.id}
                    collection.delete_one(query)
                    try:
                        await zrole.delete()
                        objectUpdates += 1
                    except:
                        pass #can be their own role, or a role above their permission, or the @ everyone role
                # print(f"DELETED {zchannel.name}!")
        # for item in search:
        #     id = item['id']
        #     matchingid = item['matchingid']
        #     if id in blacklist or matchingid in blacklist:
        #         continue
        #     out = client.get_channel(matchingid)
        #     if out is None:
        #         out = client.pasteGuild.get_role(matchingid)
        #         if out is None:
        #             raise
        #     if out is None:
        #         await out.delete()
        statusMessage += f" (Deleted {objectUpdates} roles, and {objectUnused} vanished)"
        await itx.edit_original_response(content=statusMessage)

        await itx.followup.send("Successfully updated the server to the most recent layout and roles.",ephemeral=True)
    except Exception:
        import traceback  # , logging
        msg = f"\n\n\n\n[{datetime.now().strftime('%H:%M:%S.%f')}] [ERROR]:\n\n" + traceback.format_exc()
        msg = msg.replace("\\", "\\\\").replace("*", "\\*").replace("`", "\\`").replace("_", "\\_").replace("~~",                                                                                              "\\~\\~")
        embed = discord.Embed(color=discord.Colour.from_rgb(r=181, g=69, b=80), title='Error log', description=msg)
        await itx.followup.send("Couldn't update everything! Something went wrong!",embed=embed, ephemeral=True)
        raise

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
            await itx.response.send_message("The ID has to only contain numbers!")
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
            id = int(id)
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

        try:
            del blacklist[id]
        except IndexError:
            await itx.response.send_message(f"Couldn't delete that ID, because there isn't any item on the list with that ID.. Use `/channeltracker blacklist mode:Check` to see the IDs assigned to each item on the list",ephemeral=True)
            return
        collection.update_one(query, {"$set":{f"list":blacklist}}, upsert=True)
        await itx.response.send_message(f"Successfully removed '{id}' from the blacklist. It now contains {len(blacklist)} ID{'s'*(len(blacklist)!=1)}.", ephemeral=True)
    elif mode == 3:
        collection = TrackerDB["blacklist"]
        query = {"name": "blacklist"}
        search = collection.find_one(query)
        if search is None:
            await itx.response.send_message("There are no IDs in the blacklist, so.. nothing to list here....",ephemeral=True)
            return
        blacklist = search["list"]
        length = len(blacklist)

        ans = []
        for id in range(length):
            if blacklist[id] in [x.id for x in client.pasteGuild.channels] + [x.id for x in client.copyGuild.channels]:
                ans.append(f"`{id}`: <#{blacklist[id]}> (channel: {blacklist[id]})")
            elif blacklist[id] in [x.id for x in client.pasteGuild.roles] + [x.id for x in client.copyGuild.roles]:
                ans.append(f"`{id}`: <@&{blacklist[id]}> (role: {blacklist[id]})")
            else: # if it couldn't find the id in the roles or channels, send ID only
                ans.append(f"`{id}`: {blacklist[id]} (couldn't find type it was)")
        ans = '\n'.join(ans)
        await itx.response.send_message(f"Found {length} ID{'s'*(length!=1)}:\n{ans}",ephemeral=True)

@channeltracker.command(name="relink", description="Link two channels or roles together (prevent overwriting)")
@app_commands.describe(id="ID from the copied server",matchingid="ID from the pasted server")
async def relink(itx: discord.Interaction, id: str, matchingid: str):
    try:
        id = int(id)
    except ValueError:
        await itx.response.send_message(f"Your `ID` has to be a channel or role ID! (not '{id}')",ephemeral=True)
        return
    try:
        matchingid = int(matchingid)
    except ValueError:
        await itx.response.send_message(f"Your `Matching ID` has to be a channel or role ID! (not '{matchingid}')",ephemeral=True)
        return
    if id == matchingid:
        await itx.response.send_message("Warning! Your `ID` and `Matching ID` shouldn't be the same!", ephemeral=True)
        return

    collection = TrackerDB["ids"]
    query   = {"id":id}
    # search = collection.find_one(query)
    # if search is not None:
    #     if search['id'] == search['matchingid']:


    collection.update_one(query, {"$set":{"matchingid":matchingid}}, upsert=True)
    await itx.response.send_message(f"Successfully re-linked `{id}` to `{matchingid}`.",ephemeral=True)

@channeltracker.command(name="fix",description="Delete all roles in the guild")
async def fix(itx: discord.Interaction):
    await itx.response.defer(ephemeral=True)
    try:
        unavailable = []
        for role in client.pasteGuild.roles:
            print(repr(role))
            try:
                await role.delete()
            except Exception as ex:
                unavailable.append(repr(role))
                print(repr(ex))
        spacer = "\n " # required cause f-strings can't have backslashes
        await itx.followup.send(f"Successfully deleted all the roles, except for:\n {spacer.join(unavailable)[:1500]}")
    except:
        await itx.followup.send(f"Something went horribly wrong, it seems.")

@channeltracker.command(name="check_link", description="Check if an ID is connected to the main server")
@app_commands.describe(id="ID from the copied server")
async def check_link(itx: discord.Interaction, id: str):
    try:
        id = int(id)
    except ValueError:
        await itx.response.send_message(f"Your `ID` has to be a channel or role ID! (not '{id}')",ephemeral=True)
        return
    collection = TrackerDB["blacklist"]
    query = {"name": "blacklist"}
    search = collection.find_one(query)
    if search is None:
        blacklist = []
    else:
        blacklist = search['list']

    collection = TrackerDB["ids"]
    query   = {"matchingid":id}
    search = collection.find(query)
    other_result = collection.find_one(query)
    results = []
    for result in search:
        blacklist_info = ""
        if result["id"] in blacklist or result["matchingid"] in blacklist:
            blacklist_info = " (blacklisted)"
        results.append(str(result["id"])+blacklist_info)
    if other_result is not None and len(results) > 1:
        other_result = f", but the first one is: `{other_result['id']}`"
    else:
        other_result = "."
    if len(results) > 0:
        await itx.response.send_message(
            f"`{id}` is linked to `{'`, `'.join(results)}`"+other_result+"\nBe sure to check if its category is blacklisted too.",
            ephemeral=True)
    else:
        await itx.response.send_message(f"I did not find any channels linked to this ID (`{id}`)",ephemeral=True)

    query = {"id": id}
    search = collection.find(query)
    other_result = collection.find_one(query)
    results = []
    for result in search:
        blacklist_info = ""
        if result['id'] in blacklist or result['matchingid'] in blacklist:
            blacklist_info = " (blacklisted)"
        results.append(str(result["matchingid"]) + blacklist_info)
    if other_result is not None and len(results) > 1:
        other_result = f", but the first one is: `{other_result['id']}`"
    else:
        other_result = "."
    if len(results) > 0:
        await itx.followup.send(
            content=f"For the reverse (if you swapped them around and want to see if a CopyServer channel connected to any PasteServer channel:\n" +
                    f"`{id}` is linked to `{', '.join(results)}`" + other_result + "\nBe sure to check if its category is blacklisted too.",
            ephemeral=True)

# async def on_voice_state_update(member_copy: discord.Member, _before: discord.VoiceState, _after: discord.VoiceState):
@client.event
async def on_member_join(member_copy: discord.Member):
    if member_copy.guild.id != client.pasteGuild.id:
        return
    member_tp = client.copyGuild.get_member(member_copy.id)
    automate_role_update = False
    roles_to_add_buffer = []
    if client.is_dev == 0:
        entry_allowed_roles = client.tp_entry_allowed_roles
        notable_roles = client.tp_notable_roles
    else:
        entry_allowed_roles = client.copy_entry_allowed_roles
        notable_roles = client.copy_notable_roles

    if member_tp is not None: # if the user *is* in the main server
        collection = TrackerDB["ids"]
        search = collection.find({})
        if search is None: # get all copied/logged roles and channels
            return
        for item in search:
            for role_tp in member_tp.roles:
                if item['id'] == role_tp.id:
                    if role_tp.id in entry_allowed_roles:
                        automate_role_update = True
                    if role_tp.id in notable_roles + entry_allowed_roles:
                        role_copy = member_copy.guild.get_role(item['matchingid'])
                        roles_to_add_buffer.append(role_copy)

    if len(roles_to_add_buffer) > 0:
        await member_copy.add_roles(*roles_to_add_buffer)

    welcome_channel = None
    if client.is_dev == 0:
        welcome_channel = client.get_channel(1046086440011964487)
    elif client.is_dev == 1:
        welcome_channel = client.get_channel(1085625766089326602)
    if welcome_channel is None:
        raise Exception("Couldn't find welcome channel!")

    if automate_role_update is False:
        await welcome_channel.send(f":x: **{member_copy.mention} might not be allowed to be here...** (still gave them their corresponding roles tho...)",
                                   allowed_mentions=discord.AllowedMentions.none())
    else:
        await welcome_channel.send(f":white_check_mark: {member_copy.mention} is valid. Welcome!",
                                   allowed_mentions=discord.AllowedMentions.none())

@channeltracker.command(name="update_member_roles", description="Update a member's roles to match the main server")
@app_commands.rename(member_copy="user")
@app_commands.describe(member_copy="Whose roles do you want to update?")
async def update_member(itx: discord.Interaction, member_copy: discord.Member = None):
    if member_copy is None:
        member_copy = itx.user
    member_tp = client.copyGuild.get_member(member_copy.id)
    roles_final = []
    if client.is_dev == 0:
        updatable_roles = client.tp_entry_allowed_roles + client.tp_notable_roles
    else:
        updatable_roles = client.copy_entry_allowed_roles + client.copy_notable_roles

    ### Make a list of roles that the member *should* have
    if member_tp is None:  # if the user *is* in the main server
        await itx.response.send_message("Couldn't update your roles because you aren't in the main server! (?)", ephemeral=True)
        return
    collection = TrackerDB["ids"]
    search = collection.find({})
    if search is None:  # get all copied/logged roles and channels
        return
    for item in search:
        for role_tp in member_tp.roles:
            if item['id'] == role_tp.id:
                if role_tp.id in updatable_roles:
                    role_copy = member_copy.guild.get_role(item['matchingid'])
                    roles_final.append(role_copy)

    ### Makes a list of roles that the member doesn't have but *should* have
    roles_to_add = []
    for role in roles_final:
        if role not in member_copy.roles and role.name != "@everyone":
            roles_to_add.append(role)

    ### Makes a list of roles that the member has but *shouldn't* have
    roles_to_remove = []
    for role in member_copy.roles:
        if role not in roles_final and role.name != "@everyone":
            roles_to_remove.append(role)

    class Confirm(discord.ui.View):
        class RemoveItem(discord.ui.Modal, title="What role do you not wanna update?"):
            def __init__(self, target, role_updates, role_update_index, timeout=300):
                super().__init__()
                self.value = None
                self.timeout = timeout
                self.target = target
                self.role_updates = role_updates
                self.role_update_index = role_update_index
                self.max_index = len(role_updates[role_update_index]) - 1
                self.id = None
                self.question_text = discord.ui.TextInput(label='Item index',
                                                          placeholder=f"[A number from 0 to {self.max_index} ]",
                                                          # style=discord.TextStyle.short,
                                                          # required=True
                                                          )
                self.add_item(self.question_text)

            @staticmethod
            def gen_embed(target, add_roles, remove_roles, color = None, keep_description=True):
                if color is None:
                    color = [0.6666,0.4,1]
                color = discord.Colour.from_hsv(h=color[0],s=color[1],v=color[2])
                if keep_description:
                    description = f"You're about to update {target.mention}'s roles. The bot plans to add/remove the following roles. " + \
                                  f"Please check and make sure you want to make these updates (like removing Admin, or adding channel-blocking roles"
                else:
                    description = None
                embed = discord.Embed(
                    color=color,
                    title="Update a member's role",
                    description=description
                )
                add_roles    = [f"`{i}` | {add_roles[i].mention   }" for i in range(len(add_roles   ))]
                remove_roles = [f"`{i}` | {remove_roles[i].mention}" for i in range(len(remove_roles))]
                embed.add_field(name="Add:",    value='\n'.join(add_roles)    + "None!"*(len(add_roles)    < 1))
                embed.add_field(name="Remove:", value='\n'.join(remove_roles) + "None!"*(len(remove_roles) < 1))
                return embed

            async def on_submit(self, itx: discord.Interaction):
                self.value = 9  # failed; placeholder
                try:
                    self.id = int(self.question_text.value)
                except ValueError:
                    await itx.response.send_message(
                        content=f"Couldn't send entry: '{self.question_text.value}' is not an integer. "
                                "It has to be an index number from the `/channeltracker update_member_roles` command response.",
                        ephemeral=True)
                    return
                if self.id < 0 or self.id > self.max_index:
                    await itx.response.send_message(
                        content=f"Couldn't send intry: '{self.id}' is not a possible index to remove from the changed roles. "
                                "It has to be an index number from the `/channeltracker update_member_roles` command response.",
                        ephemeral=True)
                    return
                del self.role_updates[self.role_update_index][self.id]
                self.value = 1  # succeeded
                await itx.response.edit_message(embed=self.gen_embed(self.target, self.role_updates[0], self.role_updates[1]))
                self.stop()

        def __init__(self, target, role_adds, role_removes, timeout=300):
            super().__init__()
            self.target = target
            self.role_adds = role_adds
            self.role_removes = role_removes
            self.timeout = timeout

        @discord.ui.button(label="Don't add: roleID", style=discord.ButtonStyle.blurple)
        async def unadd(self, itx: discord.Interaction, _button: discord.ui.Button):
            if len(self.role_adds) < 1:
                await itx.response.send_message("You can't un-add a role for this user, because it already wasn't going to...", ephemeral=True)
                return
            send_one = Confirm.RemoveItem(self.target, [self.role_adds, self.role_removes], 0)
            await itx.response.send_modal(send_one)
            await send_one.wait()
            self.role_adds = send_one.role_updates[0]

        @discord.ui.button(label="Don't remove: roleID", style=discord.ButtonStyle.blurple)
        async def unremove(self, itx: discord.Interaction, _button: discord.ui.Button):
            if len(self.role_removes) < 1:
                await itx.response.send_message("You can't un-remove a role for this user, because it already wasn't going to...", ephemeral=True)
                return
            send_one = Confirm.RemoveItem(self.target, [self.role_adds, self.role_removes], 1)
            await itx.response.send_modal(send_one)
            await send_one.wait()
            self.role_removes = send_one.role_updates[1]

        @discord.ui.button(label="Confirm", style=discord.ButtonStyle.red)
        async def confirm(self, itx: discord.Interaction, _button: discord.ui.Button):
            if len(self.role_adds) > 0:
                await self.target.add_roles(*self.role_adds, reason="Update member to match TP (kinda)")
            if len(self.role_removes) > 0:
                await self.target.remove_roles(*self.role_removes, reason="Update member to match TP (kinda)")

            embed = Confirm.RemoveItem.gen_embed(self.target, self.role_adds, self.role_removes, color=[0.3333,0.4,1], keep_description=False)

            await itx.response.edit_message(view=None, embed=embed)
            self.stop()

    view = Confirm(member_copy, roles_to_add, roles_to_remove)
    await itx.response.send_message(embed=Confirm.RemoveItem.gen_embed(member_copy, roles_to_add, roles_to_remove),
                                    view=view,
                                    ephemeral=True)

try:
    client.run(open('token.txt',"r").read())
except SystemExit:
    print("Exited the program forcefully using the kill switch")
