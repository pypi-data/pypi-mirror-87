  # -*- coding: utf-8 -*-
 
"""
“Commons Clause” License Condition Copyright Pirxcy/Mello 2019-2020 / 2020-202
 
The Software is provided to you by the Licensor under the
License, as defined below, subject to the following condition.
 
Without limiting other conditions in the License, the grant
of rights under the License will not include, and the License
does not grant to you, the right to Sell the Software.
 
For purposes of the foregoing, “Sell” means practicing any or
all of the rights granted to you under the License to provide
to third parties, for a fee or other consideration (including
without limitation fees for hosting or consulting/ support
services related to the Software), a product or service whose
value derives, entirely or substantially, from the functionality
of the Software. Any license notice or attribution required by
the License must also include this Commons Clause License
Condition notice.
 
Software: PirxcyBot (Nextry)
 
License: Apache 2.0
"""
 
__name__ = "PirxcyPackage"
__author__ = "Pirxcy"
__version__ = "18.0.4"
 
 
try:
    # System imports.
    from typing import Tuple, Any, Union
 
    import asyncio
    import sys
    import datetime
    import time
    import time as delay
    import json
    import sanic
    import functools
    import os
    import random as py_random
    import logging
    import uuid
 
    # Third party imports.
    from fortnitepy.ext import commands
 
    import crayons
    import fortnitepy
    import sanic
    import BenBotAsync
    import FortniteAPIAsync
    import aiohttp
    import pypresence
    import psutil
 
except ModuleNotFoundError as e:
    print(e)
    print('Failed to import 1 or more modules, running "INSTALL PACKAGES.bat"'
          'might fix the issue, if not please create an issue or join'
          'the support server.')
    sys.exit()
 
# Imports uvloop and uses it if installed (Unix only).
try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
 
def time() -> str:
    return datetime.datetime.now().strftime('%H:%M:%S')
 
 
def get_device_auth_details() -> dict:
    if os.path.isfile('device_auths.json'):
        with open('device_auths.json', 'r') as fp:
            return json.load(fp)
    else:
        with open('device_auths.json', 'w+') as fp:
            json.dump({}, fp, sort_keys=False, indent=4)
 
    return {}
 
 
def store_device_auth_details(email: str, details: dict) -> None:
    existing = get_device_auth_details()
    existing[email] = details
 
    with open('device_auths.json', 'w') as fp:
        json.dump(existing, fp, sort_keys=False, indent=4)
 
 
def check_if_process_running(name: str) -> bool:
    for process in psutil.process_iter():
        try:
            if name.lower() in process.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
 
    return False
 
 
async def set_vtid(variant_token: str) -> Tuple[str, str, int]:
    async with aiohttp.ClientSession() as session:
        request = await session.request(
            method='GET',
            url='https://benbotfn.tk/api/v1/assetProperties',
            params={
                'path': 'FortniteGame/Content/Athena/'
                        f'Items/CosmeticVariantTokens/{variant_token}.uasset'
            })
 
        response = await request.json()
 
    file_location = response['export_properties'][0]
 
    skin_cid = file_location['cosmetic_item']
    variant_channel_tag = file_location['VariantChanelTag']['TagName']
    variant_name_tag = file_location['VariantNameTag']['TagName']
 
    variant_type = variant_channel_tag.split(
        'Cosmetics.Variant.Channel.'
    )[1].split('.')[0]
 
    variant_int = int("".join(filter(
        lambda x: x.isnumeric(), variant_name_tag
    )))
 
    return skin_cid, variant_type if variant_type != 'ClothingColor' else 'clothing_color', variant_int
 
 
async def get_playlist(display_name: str) -> str:
    async with aiohttp.ClientSession() as session:
        request = await session.request(
            method='GET',
            url='http://scuffedapi.xyz/api/playlists/search',
            params={
                'displayName': display_name
            })
 
        response = await request.json()
 
    return response['id'] if 'error' not in response else None
async def set_and_update_member_prop(schema_key: str, new_value: Any) -> None:
    prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}
 
    await client.party.me.patch(updated=prop)
 
 
async def set_and_update_party_prop(schema_key: str, new_value: Any) -> None:
    prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}
 
    await client.party.patch(updated=prop)
 
print(crayons.red(f' ██▓███   ██▓ ██▀███  ▒██   ██▒ ▄████▄▓██   ██▓'))
print(crayons.red(f'▓██░  ██▒▓██▒▓██ ▒ ██▒▒▒ █ █ ▒░▒██▀ ▀█ ▒██  ██▒'))
print(crayons.red(f'▓██░ ██▓▒▒██▒▓██ ░▄█ ▒░░  █   ░▒▓█    ▄ ▒██ ██░'))
print(crayons.red(f'▒██▄█▓▒ ▒░██░▒██▀▀█▄   ░ █ █ ▒ ▒▓▓▄ ▄██▒░ ▐██▓░'))
print(crayons.red(f'▒██▒ ░  ░░██░░██▓ ▒██▒▒██▒ ▒██▒▒ ▓███▀ ░░ ██▒▓░'))
print(crayons.red(f'▒▓▒░ ░  ░░▓  ░ ▒▓ ░▒▓░▒▒ ░ ░▓ ░░ ░▒ ▒  ░ ██▒▒▒ '))
print(crayons.red(f'░▒ ░      ▒ ░  ░▒ ░ ▒░░░   ░▒ ░  ░  ▒  ▓██ ░▒░ '))
print(crayons.red(f'╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ' 'V18.0.4'))
print(crayons.green(f'Coded By Pirxcy \nJoin The Discord - https://discord.gg/P89rq5c\n'))
print(crayons.blue(f'Changelog: \n1. Fixed !shops Command\n2. Fixed !sleaks and !eleaks\nCredits To Sam From FortniteAPI.com\nRemoved !s !e etc Due to API Search Change!'))

 
with open('config.json') as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(Fore.RED + ' [ERROR] ' + Fore.RESET + "There was an error in one of the bot's files! (config.json). If you have problems trying to fix it, join the discord support server for help - https://discord.gg/88r2ShB")
        print(Fore.LIGHTRED_EX + f'\n {e}')
        exit(1)

with open('info.json') as f:
    try:
        info = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(Fore.RED + ' [ERROR] ' + Fore.RESET + "There was an error in one of the bot's files! (info.json) If you have problems trying to fix it, join the discord support server for help - https://discord.gg/88r2ShB")
        print(Fore.LIGHTRED_EX + f'\n {e}')
        exit(1)

def is_admin():
    async def predicate(ctx):
        return ctx.author.id in info['FullAccess']
    return commands.check(predicate)

 
if data['debug']:
    logger = logging.getLogger('fortnitepy.http')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('\u001b[36m %(asctime)s:%(levelname)s:%(name)s: %(message)s \u001b[0m'))
    logger.addHandler(handler)
 
    logger = logging.getLogger('fortnitepy.xmpp')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('\u001b[35m %(asctime)s:%(levelname)s:%(name)s: %(message)s \u001b[0m'))
    logger.addHandler(handler)
 
prefix = data['prefix']

device_auth_details = get_device_auth_details().get(data['email'], {})
client = commands.Bot(
    command_prefix=(data['prefix']),
    case_insensitive=True,
    auth=fortnitepy.AdvancedAuth(
        email=data['email'],
        password=data['password'],
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        **device_auth_details
    ),
    status=data['status'],
    platform=fortnitepy.Platform(data['platform']),
   avatar=fortnitepy.Avatar(
        asset=data['avatar'],
        background_colors="[\"#B35EEF\",\"#4D1397\",\"#2E0A5D\"]"
    )
)
  
from sanic import Sanic
from sanic.response import text
app = Sanic(__name__)
@app.route('/')
async def hello_world(request):
    return text(f'Congratulations {nickname} Your Bot is Online\n ███▄    █ ▓█████ ▒██   ██▒▄▄▄█████▓ ██▀███ ▓██   ██▓\n ██ ▀█   █ ▓█   ▀ ▒▒ █ █ ▒░▓  ██▒ ▓▒▓██ ▒ ██▒▒██  ██▒\n▓██  ▀█ ██▒▒███   ░░  █   ░▒ ▓██░ ▒░▓██ ░▄█ ▒ ▒██ ██░\n▓██▒  ▐▌██▒▒▓█  ▄  ░ █ █ ▒ ░ ▓██▓ ░ ▒██▀▀█▄   ░ ▐██▓░\n▒██░   ▓██░░▒████▒▒██▒ ▒██▒  ▒██▒ ░ ░██▓ ▒██▒ ░ ██▒▓░\n░ ▒░   ▒ ▒ ░░ ▒░ ░▒▒ ░ ░▓ ░  ▒ ░░   ░ ▒▓ ░▒▓░  ██▒▒▒ \n░ ░░   ░ ▒░ ░ ░  ░░░   ░▒ ░    ░      ░▒ ░ ▒░▓██ ░▒░\n   ░   ░ ░    ░    ░    ░    ░        ░░   ░ ▒ ▒ ░░  \n         ░    ░  ░ ░    ░              ░     ░ ░     \n                                             ░ ░    \n')

@client.event
async def event_ready():
    await app.create_server(host="0.0.0.0",port=8000, return_asyncio_server=True)
 
@client.event
async def event_device_auth_generate(details: dict, email: str) -> None:
    store_device_auth_details(email, details)
 
@client.event
async def event_ready() -> None:
    delay.sleep(2)
    os.system('clear')
    print(crayons.green(f'The Fun Is Just Bout To Get Started.'))
    delay.sleep(2)
    print(crayons.cyan(f'Your Slave Is Ready --> {client.user.display_name}')) 
    member = client.party.me
 
    await member.edit_and_keep(
 
        functools.partial(
 
            fortnitepy.ClientPartyMember.set_outfit,
 
            asset=data['cid']
 
        ),
 
        functools.partial(
 
            fortnitepy.ClientPartyMember.set_backpack,
 
            asset=data['bid']
 
        ),
 
        functools.partial(
 
            fortnitepy.ClientPartyMember.set_banner,
 
            icon="BRS10GRID",
 
            color="purple",
 
            season_level=999
 
        ),
 
        functools.partial(
 
            fortnitepy.ClientPartyMember.set_battlepass_info,
 
            has_purchased=True,
 
            level=data['bp_tier']
 
        )
 
    )
 
    discord_exists = await client.loop.run_in_executor(None, check_if_process_running, 'Discord')
 
    if discord_exists and (sys.platform == 'darwin' or 'linux' in sys.platform.lower()):
        client.loop.create_task(start_discord_rich_presence())
 
        if isinstance(pending, fortnitepy.IncomingPendingFriend):
            try:
                epic_friend = await pending.accept() if data["friend_accept"] else await pending.decline()
                if isinstance(epic_friend, fortnitepy.Friend):
                    print(f"[PirxcyBot] [{time()}] Accepted friend request from: {epic_friend.display_name}.")
                else:
                    print(f"[PirxcyBot] [{time()}] Declined friend request from: {pending.display_name}.")
            except fortnitepy.HTTPException as epic_error:
                if epic_error.message_code != 'errors.com.epicgames.common.throttled':
                    raise
 
                await asyncio.sleep(int(epic_error.message_vars[0] + 1))
                await pending.accept() if data["friend_accept"] else await pending.decline()
 
nickname=data['nickname']

@client.event
async def event_party_invite(invite):
    if data['joinoninvite'].lower() == 'true':
        try:
            await invite.accept()
            print(Fore.GREEN + ' [+] ' + Fore.RESET + f'Accepted party invite from {invite.sender.display_name}')
        except Exception:
            pass
    elif data['joinoninvite'].lower() == 'false':
        if invite.sender.id in info['FullAccess']:
            await invite.accept()
            print(Fore.GREEN + ' [+] ' + Fore.RESET + 'Accepted party invite from ' + Fore.LIGHTGREEN_EX + f'{invite.sender.display_name}')
        else:
            print(f'Never accepted party invite from {invite.sender.display_name}')

@client.event
async def event_party_member_join(message: Union[fortnitepy.FriendMessage, fortnitepy.PartyMessage]):
      if isinstance(message, fortnitepy.message.MessageBase):
        client = message.client
        client.add_cache(message.author)
        if "Lupus" in content:
            if isinstance(message, fortnitepy.PartyMessage):
                await message.author.block()
                await message.author.kick()
        elif "ReconBot" in content:
            if isinstance(message, fortnitepy.PartyMessage):
                await message.author.block()
                await message.author.kick()
        elif "Poki" in content:
            if isinstance(message, fortnitepy.PartyMessage):
                await message.author.block()
                await message.author.kick()
        elif "fnpy" in content:
            if isinstance(message, fortnitepy.PartyMessage):
                await message.author.block()
                await message.author.kick()
        elif "bot" in content:
            if isinstance(message, fortnitepy.PartyMessage):
                await message.author.block()
                await message.author.kick()
        elif "lobby bot" in content:
            if isinstance(message, fortnitepy.PartyMessage):
                await message.author.block()
                await message.author.kick()
        elif "hailey" in content:
            if isinstance(message, fortnitepy.PartyMessage):
                await message.author.block()
                await message.author.kick()              


@client.event
async def event_friend_request(request: fortnitepy.IncomingPendingFriend) -> None:
    print(f"[PirxcyBot] [{time()}] Received friend request from: {request.display_name}.")
 
    if data['friend_accept']:
        await request.accept()
        print(f"[PirxcyBot] [{time()}] Accepted friend request from: {request.display_name}.")
    else:
        await request.decline()
        print(f"[PirxcyBot] [{time()}] Declined friend request from: {request.display_name}.")
 
@client.event
async def event_party_member_join(member: fortnitepy.PartyMember) -> None:
    delay.sleep(0.1)
    await client.party.send(data['join_message'])
 
@client.event
async def event_party_member_join(member: fortnitepy.PartyMember) -> None:
    delay.sleep(0)
    await client.party.send(f'This Bot was Made For {nickname} and Made By Mello and Pirxcy\nTo Get Yours Join The Discord\nhttps://discord.gg/jXCfx9JEKz\nEnjoy!')
 
@client.event
async def event_party_member_join(member: fortnitepy.PartyMember) -> None:
    delay.sleep(0)
    await client.party.me.set_emote(
        asset=(data['eid'])
    )
 
@client.event
async def event_friend_message(message: fortnitepy.FriendMessage) -> None:
    print(crayons.magenta(f'[PirxcyBot] [{time()}] {message.author.display_name}: {message.content}'))
 
@client.event
async def event_friend_message(message: fortnitepy.FriendMessage) -> None:
    print(crayons.magenta(f'[PirxcyBot] [{time()}] {message.author.display_name}: {message.content}'))
 
 
@client.event
async def event_party_message(message: fortnitepy.FriendMessage) -> None:
    print(crayons.green(f'[PirxcyBot] [{time()}] {message.author.display_name}: {message.content}'))
 
 
 
@client.command()
async def skin(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No skin was given, try: {prefix}skin (skin name)')
    elif content.upper().startswith('CID_'):
        await client.party.me.set_outfit(asset=content.upper())
        await ctx.send(f'Skin set to: {content}')    
    elif content.upper().startswith('CID_'):
          await client.party.me.set_outfit(asset=content.upper())
          await ctx.send(f'Skin set to: {content}')
    elif content.lower() == 'joker':
          await client.party.me.set_outfit(asset='CID_922_Athena_Commando_M_ParcelPrank')
          await ctx.send(f'Skin Set To: Joker')
    elif content.lower() == 'midas rex':
          await client.party.me.set_outfit(asset='CID_923_Athena_Commando_M_ParcelGold')
          await ctx.send(f'Skin Set To: Joker')      
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                name=content,
                backendType="AthenaCharacter"
            )
            await client.party.me.set_outfit(asset=cosmetic.id)
            await ctx.send(f'Skin set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a skin named: {content}')
 
@client.command()
async def backpack(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaBackpack"
        )
 
        await ctx.send(f'Backpack set to {cosmetic.id}.')
        print(f"[PirxcyBot] [{time()}] Set backpack to: {cosmetic.id}.")
        await client.party.me.set_backpack(asset=cosmetic.id)
 
    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a backpack with the name: {content}.")
        print(f"[PirxcyBot] [{time()}] Failed to find a backpack with the name: {content}.")
 
 
@client.command()
async def b(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaBackpack"
        )
 
        await ctx.send(f'Backpack set to {cosmetic.id}.')
        print(f"[PirxcyBot] [{time()}] Set backpack to: {cosmetic.id}.")
        await client.party.me.set_backpack(asset=cosmetic.id)
 
    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a backpack with the name: {content}.")
        print(f"[PirxcyBot] [{time()}] Failed to find a backpack with the name: {content}.")
 
@client.command()
async def emote(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No emote was given, try: {prefix}emote (emote name)')
    elif content.lower() == 'floss':
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_Floss')
        await ctx.send(f'Emote set to: Floss')
    elif content.lower() == 'the flow':
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_THESHOW')
        await ctx.send(f'Emote set to: The Flow')
    elif content.lower() == 'jabba switchway':
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_JanuaryBop')
        await ctx.send(f'Emote set to: The Flow')
    elif content.lower() == 'go mufasa':
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_SandwichBop')
        await ctx.send(f'Emote set to: The Flow')    
    elif content.lower() == 'none':
        await client.party.me.clear_emote()
        await ctx.send(f'Emote set to: None')
    elif content.upper().startswith('EID_'):
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset=content.upper())
        await ctx.send(f'Emote set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await client.party.me.clear_emote()
            await client.party.me.set_emote(asset=cosmetic.id)
            await ctx.send(f'Emote set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find an emote named: {content}')
 
  
@client.command()
async def pickaxe(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaPickaxe"
        )
 
        await ctx.send(f'Pickaxe set to {cosmetic.id}.')
        print(f"[PirxcyBot] [{time()}] Set pickaxe to: {cosmetic.id}.")
        await client.party.me.set_pickaxe(asset=cosmetic.id)
 
    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a pickaxe with the name: {content}.")
        print(f"[PirxcyBot] [{time()}] Failed to find a pickaxe with the name: {content}.")
 
 
@client.command()
async def p(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaPickaxe"
        )
 
        await ctx.send(f'Pickaxe set to {cosmetic.id}.')
        print(f"[PirxcyBot] [{time()}] Set pickaxe to: {cosmetic.id}.")
        await client.party.me.set_pickaxe(asset=cosmetic.id)
 
    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a pickaxe with the name: {content}.")
        print(f"[PirxcyBot] [{time()}] Failed to find a pickaxe with the name: {content}.")
 
@client.command()
async def pet(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaPet"
        )
 
        await ctx.send(f'Pet set to {cosmetic.id}.')
        print(f"[PirxcyBot] [{time()}] Set pet to: {cosmetic.id}.")
        await client.party.me.set_pet(asset=cosmetic.id)
 
    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a pet with the name: {content}.")
        print(f"[PirxcyBot] [{time()}] Failed to find a pet with the name: {content}.")
 
 
@client.command()
async def emoji(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaEmoji"
        )
 
        await ctx.send(f'Emoji set to {cosmetic.id}.')
        print(f"[PirxcyBot] [{time()}] Set emoji to: {cosmetic.id}.")
        await client.party.me.set_emoji(asset=cosmetic.id)
 
    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find an emoji with the name: {content}.")
        print(f"[PirxcyBot] [{time()}] Failed to find an emoji with the name: {content}.")
 
 
@client.command()
async def contrail(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaSkyDiveContrail"
        )
 
        await ctx.send(f'Contrail set to {cosmetic.id}.')
        print(f"[PirxcyBot] [{time()}] Set contrail to: {cosmetic.id}.")
        await client.party.me.set_contrail(asset=cosmetic.id)
 
    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a contrail with the name: {content}.")
        print(f"[PirxcyBot] [{time()}] Failed to find an contrail with the name: {content}.")
 
 
@client.command()
async def purpleskull(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        clothing_color=1
    )
 
    await client.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants=skin_variants
    )
 
    await ctx.send('Skin set to Purple Skull Trooper!')
    print(f"[PirxcyBot] [{time()}] Skin set to Purple Skull Trooper.")
 
@client.command()
async def pinkghoul(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        material=3
    )
 
    await client.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=skin_variants
    )
 
    await ctx.send('Skin set to Pink Ghoul Trooper!')
    print(f"[PartyBot] [{time()}] Skin set to Pink Ghoul Trooper.")
 
 
 
@client.command()
async def test2(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        material=100
    )
 
    await client.party.me.set_outfit(
        asset='CID_853_athena_commando_f_sniperhoodcorrupt',
        variants=skin_variants
    )
 
    await ctx.send('Test!')
    print(f"[PirxcyBot] [{time()}] Test!")
 
@client.command()
async def purpleportal(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        item='AthenaBackpack',
        particle_config='Particle',
        particle=1
    )
 
    await client.party.me.set_backpack(
        asset='BID_105_GhostPortal',
        variants=skin_variants
    )
 
    await ctx.send('Backpack set to Purple Ghost Portal!')
    print(f"[PirxcyBot] [{time()}] Backpack set to Purple Ghost Portal.")
 
@client.command()
async def recon(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_022_Athena_Commando_F',
        )
 
        await ctx.send('Outfit set to Recon Expert!')
 
 
 
@client.command()
async def wonder(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_434_Athena_Commando_F_StealthHonor',
        )
 
        await ctx.send('Outfit set to Wonder')
 
@client.command()
async def galaxy(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_175_Athena_Commando_M_Celestial',
        )
 
        await ctx.send('Outfit set to Galaxy')
 
@client.command()    
async def eon(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_174_Athena_Commando_F_CarbideWhite',
        )
 
        await ctx.send('Outfit set to Eon')
 
@client.command()
async def glow(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_479_Athena_Commando_F_Davinci',
        )
 
        await ctx.send('Outfit set to Glow')
 
@client.command()
async def ikonik(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_313_Athena_Commando_M_KpopFashion',
        )
 
        await ctx.send('Outfit set to Ikonik')
 
@client.command()    
async def blackknight(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_035_Athena_Commando_M_Medieval',
        )
 
        await ctx.send('Outfit set to Black Knightt')
 
@client.command()    
async def aerialtrooper(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_017_Athena_Commando_M',
        )
 
        await ctx.send('Outfit set to Aerial assault trooper')
 
@client.command()
async def neoversa(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_441_Athena_Commando_F_CyberScavengerBlue',
        )
 
        await ctx.send('Skin set to Neo Versa')
 
@client.command()
async def bluestriker(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_138_Athena_Commando_M_PSBurnout',
        )
 
        await ctx.send('Skin set to Blue Striker')
 
@client.command()
async def roguespider(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_516_Athena_Commando_M_BlackWidowRogue',
        )
 
        await ctx.send('Skin set to Rogue Spider Knight')
 
@client.command()
async def honor(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_342_Athena_Commando_M_StreetRacerMetallic',
        )
 
        await ctx.send('Skin set to Honor Guard')
 
@client.command()
async def darkvertex(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_371_Athena_Commando_M_SpeedyMidnight',
        )
 
        await ctx.send('Skin set to Dark Vertex')
 
@client.command()
async def royalebomber(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_113_Athena_Commando_M_BlueAce',
        )
 
        await ctx.send('Skin set to Royale Bomber')
 
@client.command()
async def frostbite(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_261_Athena_Commando_M_RaptorArcticCamo',
        )
 
        await ctx.send('Skin set to Frost Bite')
 
@client.command()
async def doublehelix(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_183_Athena_Commando_M_ModernMilitaryRed',
        )
 
        await ctx.send('Skin set to Double Helix')
 
@client.command()
async def stealthreflex(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_386_Athena_Commando_M_StreetOpsStealth',
        )
 
        await ctx.send('Skin set to Stealth Reflex')
 
@client.command()
async def sparkle(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_039_Athena_Commando_F_Disco',
        )
 
        await ctx.send('Skin set to Sparkle Specialist')
 
@client.command()
async def wick(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_416_Athena_Commando_M_AssassinSuit',
        )
 
        await ctx.send('Skin set to John Wick')
 
@client.command()
async def ogwick(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_084_Athena_Commando_M_Assassin',
        )
 
        await ctx.send('Skin set to The Reaper')
 
@client.command()
async def widow(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_399_Athena_Commando_F_AshtonBoardwalk',
        )
 
        await ctx.send('Skin set to Black Widow')
 
@client.command()
async def starlord(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_400_Athena_Commando_M_AshtonSaltLake',
        )
 
        await ctx.send('Skin set to Star Lord')
 
@client.command()
async def shifu(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_509_Athena_Commando_M_WiseMaster',
        )
 
        await ctx.send('Skin set to Shifu')
 
@client.command()
async def air(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_432_Athena_Commando_M_BalloonHead',
        )
 
        await ctx.send('Skin set to Airhead')
 
@client.command()
async def bash(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_543_Athena_Commando_M_LlamaHero',
        )
 
        await ctx.send('Skin set to Bash')
 
@client.command()
async def blaster(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_553_Athena_Commando_M_BrightGunnerRemix',
        )
 
        await ctx.send('Skin set to Brite Blaster')
 
@client.command()
async def dab(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_emote(
            asset='EID_Dab',
        )
 
        await ctx.send('Emote set to Dab')
 
@client.command()
async def floss(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_emote(
            asset='EID_Floss',
        )
 
        await ctx.send('Emote set to Floss')
 
@client.command()
async def raidersrevenge(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_pickaxe(
            asset='Pickaxe_Lockjaw',
        )
        await client.party.me.clear_emote()
        await client.party.me.set_emote(
            asset='EID_IceKing',  
        )
        await ctx.send('Raiders Revenge axe') 
 
@client.command()
async def reaper(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_pickaxe(
            asset='HalloweenScythe',
        )
 
        await ctx.send('Pickaxe set to reaper')
 
@client.command()
async def wcfishstick(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           parts=3
        )
 
        await client.party.me.set_outfit(
            asset='CID_315_Athena_Commando_M_TeriyakiFish',
            variants=variants
        )
 
        await ctx.send('Skin set to WorldCup Fishstick')
 
@client.command()
async def maz(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           material=1
        )
 
        await client.party.me.set_outfit(
            asset='CID_466_Athena_Commando_M_WeirdObjectsCreature',
            variants=variants
        )
 
        await ctx.send('This is Maz  irl')
 
@client.command()
async def afishy(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_813_Athena_Commando_M_TeriyakiAtlantis',
        )
        await client.party.me.set_backpack(
            asset='BID_566_TeriyakiAtlantis',
        )
        await ctx.send('Atlantis Fishy, Use code: pirxcy')
 
@client.command()
async def astro(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_NPC_Athena_Commando_M_SpaceWanderer',
        )
        await ctx.send('Ancient Astronaut, Use code: pirxcy')        
 
@client.command()    
async def faris(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           parts=3
        )
 
        await client.party.me.set_outfit(
            asset='CID_315_Athena_Commando_M_TeriyakiFish',
            variants=variants
        )
 
        await ctx.send('Skin set to Faris favourite skin')
 
@client.command()
async def og(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_028_Athena_Commando_F',
        )
        delay.sleep(2)
        variants = client.party.me.create_variants(
           material=3
        )
 
        await client.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=variants
        )
        delay.sleep(2)
        variants = client.party.me.create_variants(
           clothing_color=1
        )
 
        await client.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=variants
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_022_Athena_Commando_F',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_017_Athena_Commando_M',
        )
        delay.sleep(2)
        await ctx.send('Use code: pirxcy')
 
@client.command()
async def defaults(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_005_Athena_Commando_M_Default',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_001_Athena_Commando_F_Default',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_002_Athena_Commando_F_Default',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_003_Athena_Commando_F_Default',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_004_Athena_Commando_F_Default',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_006_Athena_Commando_M_Default',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_007_Athena_Commando_M_Default',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_008_Athena_Commando_M_Default',
        )       
        await ctx.send(' enjoying this bot ? Please Support  Me By  Adding AlwayzExtremeMod')
 
@client.command()
async def npc(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_NPC_Athena_Commando_M_HenchmanBad',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_NPC_Athena_Commando_M_HenchmanGood',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_NPC_Athena_Commando_F_HenchmanSpyDark',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_NPC_Athena_Commando_F_HenchmanSpyGood',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_NPC_Athena_Commando_F_RebirthDefault_Henchman',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_NPC_Athena_Commando_M_HeistSummerIsland',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_NPC_Athena_Commando_M_PaddedArmorArctic',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_NPC_Athena_Commando_M_TacticalFishermanOil',
        )       
        await ctx.send(' enjoying this bot ? Please Support  Me By  Adding AlwayzExtremeMod')       
 
@client.command()
async def npcshorts(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_789_Athena_Commando_M_HenchmanGoodShorts_B',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_790_Athena_Commando_M_HenchmanGoodShorts_C',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_791_Athena_Commando_M_HenchmanGoodShorts_D',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_792_Athena_Commando_M_HenchmanBadShorts_B',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_793_Athena_Commando_M_HenchmanBadShorts_C',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_794_Athena_Commando_M_HenchmanBadShorts_D',
        )       
        await ctx.send(' enjoying this bot ? Please Support  Me By  Adding AlwayzExtremeMod')                 
 
@client.command()
async def npc2(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_NPC_Athena_Commando_F_MarauderElite',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_NPC_Athena_Commando_M_MarauderGrunt',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_NPC_Athena_Commando_M_Scrapyard',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_NPC_Athena_Commando_M_MarauderHeavy',
        )
        await ctx.send(' enjoying this bot ? Please Support  Me By  Adding AlwayzExtremeMod')      
 
@client.command()
async def aqua(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_772_Athena_Commando_M_Sandcastle',
        )
        await client.party.me.set_backpack(
            asset='BID_535_SandCastle',
        )
        await client.party.me.set_pickaxe(
            asset='Pickaxe_ID_415_SandcastleMale',
        )
        await client.party.me.clear_emote()
        await client.party.me.set_emote(
            asset='EID_IceKing',  
        )
        await ctx.send('Aquaman ! use code:pirxcy')
 
@client.command()
async def aqua2(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        progressive=2
    )
 
    await client.party.me.set_outfit(
        asset='CID_772_Athena_Commando_M_Sandcastle',
        variants=skin_variants
    )
 
    await ctx.send(' Aquaman second style use code: pirxcy')
 
@client.command()
async def gwildcard(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_787_Athena_Commando_M_Heist_Ghost',
        )
 
        await ctx.send('Ghost WildCard use code: pirxcy')    
 
@client.command()
async def swildcard(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        material=2
    )
 
    await client.party.me.set_outfit(
        asset='CID_787_Athena_Commando_M_Heist_Ghost',
        variants=skin_variants
    )
 
    await ctx.send(' Shadow WildCard use code: pirxcy')
 
@client.command()
async def gchaos(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_788_Athena_Commando_M_Mastermind_Ghost',
        )
 
        await ctx.send('Ghost Chaos Agent use code: pirxcy')    
 
@client.command()
async def schaos(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        material=2
    )
 
    await client.party.me.set_outfit(
        asset='CID_788_Athena_Commando_M_Mastermind_Ghost',
        variants=skin_variants
    )
 
    await ctx.send(' Shadow Chaos Agent use code: pirxcy')
 
@client.command()
async def ghush(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_786_Athena_Commando_F_CavalryBandit_Ghost',
        )
 
        await ctx.send('Ghost Hush use code: pirxcy')
 
@client.command()
async def shush(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        material=2
    )
 
    await client.party.me.set_outfit(
        asset='CID_786_Athena_Commando_F_CavalryBandit_Ghost',
        variants=skin_variants
    )
 
    await ctx.send(' Shadow Hush use code: pirxcy')
 
@client.command()
async def s2(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_032_Athena_Commando_M_Medieval',
        )
        await client.party.me.set_backpack(
            asset='BID_002_RoyaleKnight',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_033_Athena_Commando_F_Medieval',
        )
        await client.party.me.set_backpack(
            asset='BID_002_RoyaleKnight',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_039_Athena_Commando_F_Disco',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_035_Athena_Commando_M_Medieval',
        )
        await client.party.me.set_backpack(
            asset='BID_004_BlackKnight',
        )
        await ctx.send('Season 2 Skins')
 
@client.command()
async def fishy(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_315_Athena_Commando_M_TeriyakiFish',
        )
        delay.sleep(2)
        variants = client.party.me.create_variants(
           parts=2
        )
        await client.party.me.set_outfit(
            asset='CID_315_Athena_Commando_M_TeriyakiFish',
            variants=variants
        )
        variants = client.party.me.create_variants(
           parts=3
        )
 
        await client.party.me.set_outfit(
            asset='CID_315_Athena_Commando_M_TeriyakiFish',
            variants=variants
        )    
        delay.sleep(2)
        variants = client.party.me.create_variants(
           parts=1
        )
        await client.party.me.set_outfit(
            asset='CID_315_Athena_Commando_M_TeriyakiFish',
            variants=variants
        )    
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_624_Athena_Commando_M_TeriyakiWarrior',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_656_Athena_Commando_M_TeriyakiFishFreezerBurn',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_722_Athena_Commando_M_TeriyakiFishAssassin',
        )
        await ctx.send('Fishys Familly')
 
 
@client.command()
async def golden(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_701_Athena_Commando_M_BananaAgent',
            variants=client.party.me.create_variants(progressive=4),
            enlightenment=(2, 350)
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_690_Athena_Commando_F_Photographer',
            variants=client.party.me.create_variants(progressive=4),
            enlightenment=(2, 350)
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_691_Athena_Commando_F_TNTina',
            variants=client.party.me.create_variants(progressive=7),
            enlightenment=(2, 350)
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_692_Athena_Commando_M_HenchmanTough',
            variants=client.party.me.create_variants(progressive=4),
            enlightenment=(2, 350)
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_693_Athena_Commando_M_BuffCat',
            variants=client.party.me.create_variants(progressive=4),
            enlightenment=(2, 350)
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_694_Athena_Commando_M_CatBurglar',
            variants=client.party.me.create_variants(progressive=4),
            enlightenment=(2, 350)
        )               
        await ctx.send('Golden Edit Styles. Use code: pirxcy')
 
@client.command()
async def blaze(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           parts=2
        )
 
        await client.party.me.set_outfit(
            asset='CID_784_Athena_Commando_F_RenegadeRaiderFire',
            variants=variants
        )
        await client.party.me.set_backpack(
            asset='BID_545_RenegadeRaiderFire',
        )
        await ctx.send('outfit set to Blaze. Code: pirxcy')
 
@client.command()
async def agentj(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_756_Athena_Commando_M_JonesyAgent',
        )
 
        await ctx.send('Outfit set to Agent Jonesy')     
 
@client.command()
async def renegade(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_028_Athena_Commando_F',
        )
        await client.party.me.set_pickaxe(
            asset='Pickaxe_Lockjaw',
        )
        await client.party.me.clear_emote()
        await client.party.me.set_emote(
            asset='EID_IceKing',  
        )
        await ctx.send('Full Renegade set ! code: pirxcy')
 
@client.command()
async def jqc(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_028_Athena_Commando_F',
        )        
        await client.party.me.clear_emote()
        await client.party.me.set_emote(
            asset='EID_justhome',  
        )
        await ctx.send('This was made For Jqc Enjoy')
 
@commands.dm_only()
@client.command()
@is_admin()
async def hide(ctx, *, user = None):
    if client.party.me.leader:
        if user != "all":
            try:
                if user is None:
                    user = await client.fetch_profile(ctx.message.author.id)
                    member = client.party.members.get(user.id)
                else:
                    user = await client.fetch_profile(user)
                    member = client.party.members.get(user.id)

                raw_squad_assignments = client.party.meta.get_prop('Default:RawSquadAssignments_j')["RawSquadAssignments"]

                for m in raw_squad_assignments:
                    if m['memberId'] == member.id:
                        raw_squad_assignments.remove(m)

                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j',
                    {
                        'RawSquadAssignments': raw_squad_assignments
                    }
                )

                await ctx.send(f"Hid {member.display_name}")
            except AttributeError:
                await ctx.send("I could not find that user.")
            except fortnitepy.HTTPException:
                await ctx.send("I am not party leader.")
        else:
            try:
                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j',
                    {
                        'RawSquadAssignments': [
                            {
                                'memberId': client.user.id,
                                'absoluteMemberIdx': 1
                            }
                        ]
                    }
                )

                await ctx.send("Hid everyone in the party.")
            except fortnitepy.HTTPException:
                await ctx.send("I am not party leader.")
    else:
        await ctx.send("I need party leader to do this!")

@commands.dm_only()
@client.command()
@is_admin()
async def unhide(ctx):
    if client.party.me.leader:
        user = await client.fetch_profile(ctx.message.author.id)
        member = client.party.members.get(user.id)

        await member.promote()

        await ctx.send("Unhid all players.")

    else:
        await ctx.send("I am not party leader.")


@commands.dm_only()
@client.command()
@is_admin()
async def say(ctx, *, message = None):
    if message is not None:
        await client.party.send(message)
        await ctx.send(f'Sent "{message}" to party chat')
    else:
        await ctx.send(f'No message was given. Try: {prefix}say (message)')

@commands.dm_only()
@client.command()
@is_admin()
async def status(ctx, *, status = None):
    if status is not None:
        await client.set_status(status)
        await ctx.send(f'Set status to: {status}')
        print(Fore.GREEN + ' [+] ' + Fore.RESET + 'Changed status to: ' + Fore.LIGHTBLACK_EX + f'{status}')
    else:
        await ctx.send(f'No status was given. Try: {prefix}status (status message)')


@client.command()
async def sweat(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_149_athena_commando_f_soccergirlb',
        )
        await client.party.me.set_pickaxe(
            asset='halloweenscythe',
        )
        await client.party.me.clear_emote()
        await client.party.me.set_emote(
            asset='EID_IceKing',
        )
        await asyncio.sleep(1)
        await client.party.me.clear_emote()
        await client.party.me.set_emote(
            asset='EID_takethel',  
        )
        await ctx.send('Full Sweats set ! code: pirxcy')
 
@client.command()
async def travis(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_703_athena_commando_m_cyclone',
            )
        await client.party.me.clear_emote()
        await client.party.me.set_emote(
            asset='EID_cyclone',
        )
        await client.party.me.clear_emote()
        await client.party.me.set_emote(
            asset='EID_cycloneheadbang',  
        )
        await ctx.send('Astronomical!')
 
 
@client.command()
async def rglitch(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_WAve'
    )
    await ctx.send('!randomize skin')
    await client.party.me.set_emote(
        asset='EID_HighTowerTomato'
    )
 
 
@client.command()
async def gmidas(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           progressive=2
        )
 
        await client.party.me.set_outfit(
            asset='CID_694_Athena_Commando_M_CatBurglar',
            variants=variants
        )
 
        await ctx.send('Ghost midas')          
 
@client.command()
async def smidas(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           progressive=3
        )
 
        await client.party.me.set_outfit(
            asset='CID_694_Athena_Commando_M_CatBurglar',
            variants=variants
        )
 
        await ctx.send('Shadow midas')
 
@client.command()
async def gskye(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           progressive=2
        )
 
        await client.party.me.set_outfit(
            asset='CID_690_Athena_Commando_F_Photographer',
            variants=variants
        )
 
        await ctx.send('Ghost Skye')
 
@client.command()
async def sskye(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           progressive=3
        )
 
        await client.party.me.set_outfit(
            asset='CID_690_Athena_Commando_F_Photographer',
            variants=variants
        )
 
        await ctx.send('shadow Skye')
 
@client.command()
async def gtntina(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           progressive=2
        )
 
        await client.party.me.set_outfit(
            asset='CID_691_Athena_Commando_F_TNTina',
            variants=variants
        )
 
        await ctx.send('Ghost tntina')
 
@client.command()
async def stntina(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           progressive=3
        )
 
        await client.party.me.set_outfit(
            asset='CID_691_Athena_Commando_F_TNTina',
            variants=variants
        )
 
        await ctx.send('Shadow tntina')
 
@client.command()
async def gpeely(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           progressive=2
        )
 
        await client.party.me.set_outfit(
            asset='CID_701_Athena_Commando_M_BananaAgent',
            variants=variants
        )
 
        await ctx.send('Ghost Peely')
 
@client.command()
async def speely(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           progressive=3
        )
 
        await client.party.me.set_outfit(
            asset='CID_701_Athena_Commando_M_BananaAgent',
            variants=variants
        )
 
        await ctx.send('Shadow Peely')
 
@client.command()
async def gmeow(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           progressive=2
        )
 
        await client.party.me.set_outfit(
            asset='CID_693_Athena_Commando_M_BuffCat',
            variants=variants
        )
 
        await ctx.send('Ghost mewoscles')
 
@client.command()
async def smeow(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           progressive=3
        )
 
        await client.party.me.set_outfit(
            asset='CID_693_Athena_Commando_M_BuffCat',
            variants=variants
        )
 
        await ctx.send('Ghost mewoscles')
 
@client.command()
async def gbrutus(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           progressive=2
        )
 
        await client.party.me.set_outfit(
            asset='CID_692_Athena_Commando_M_HenchmanTough',
            variants=variants
        )
 
        await ctx.send('Ghost Brutus') 
 
@client.command()
async def sbrutus(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           progressive=2
        )
 
        await client.party.me.set_outfit(
            asset='CID_692_Athena_Commando_M_HenchmanTough',
            variants=variants
        )
 
        await ctx.send('Shdadow Brutus')         
 
@client.command()
async def dp2(ctx: fortnitepy.ext.commands.Context) -> None:
        variants = client.party.me.create_variants(
           parts=2
        )
 
        await client.party.me.set_outfit(
            asset='CID_705_Athena_Commando_M_Donut',
            variants=variants
        )
 
        await ctx.send('Deadpools second style. Code: pirxcy')
 
@client.command()
async def axe(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.clear_emote()
        await client.party.me.set_emote(
            asset='EID_IceKing',  
        )
        await ctx.send('Emote set to Point it out ')
 
@client.command()
async def minty(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_pickaxe(
            asset='Pickaxe_ID_294_CandyCane',
        )
        await client.party.me.clear_emote()
        await client.party.me.set_emote(
            asset='EID_IceKing',  
        )
        await ctx.send(' Visit our discord  https://discord.gg/CgKRmwz / Minty axe') 
 
@client.command()
async def default(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_NPC_Athena_Commando_F_RebirthDefault_Henchman',
        )
 
        await ctx.send('Skin set to Secret Default')
 
@client.command()
async def poof(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_034_Athena_Commando_M_Medieval',
        )
 
        await ctx.send('Magic trick  Bot is gone')
 
@client.command()
async def stw(ctx: fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_outfit(
            asset='CID_TBD_Athena_Commando_M_ConstructorTest',
        )
        delay.sleep(2)
        await client.party.me.set_outfit(
            asset='CID_TBD_Athena_Commando_F_ConstructorTest',
        )
        await ctx.send('STW Skins  Please Support  Me By  Adding AlwayzExtremeMod')
 
@client.command()
async def banner(ctx: fortnitepy.ext.commands.Context, icon: str, colour: str, banner_level: int) -> None:
    await client.party.me.set_banner(icon=icon, color=colour, season_level=banner_level)
 
    await ctx.send(f'Banner set to: {icon}, {colour}, {banner_level}.')
    print(f"[PirxcyBot] [{time()}] Banner set to: {icon}, {colour}, {banner_level}.")
 
 
@client.command()
async def cid(ctx: fortnitepy.ext.commands.Context, character_id: str) -> None:
    await client.party.me.set_outfit(
        asset=character_id,
        variants=client.party.me.create_variants(profile_banner='ProfileBanner')
    )
 
    await ctx.send(f'Skin set to {character_id}')
    print(f'[PirxcyBot] [{time()}] Skin set to {character_id}')
 
 
@client.command()
async def vtid(ctx: fortnitepy.ext.commands.Context, variant_token: str) -> None:
    variant_id = await set_vtid(variant_token)
 
    if variant_id[1].lower() == 'particle':
        skin_variants = client.party.me.create_variants(particle_config='Particle', particle=1)
    else:
        skin_variants = client.party.me.create_variants(**{vtid[1].lower(): int(vtid[2])})
 
    await client.party.me.set_outfit(asset=vtid[0], variants=skin_variants)
    print(f'[PirxcyBot] [{time()}] Set variants of {vtid[0]} to {vtid[1]} {vtid[2]}.')
    await ctx.send(f'Variants set to {variant_token}.\n'
                   '(Warning: This feature is not supported, please use !variants)')
 
 
@client.command()
async def variants(ctx: fortnitepy.ext.commands.Context, cosmetic_id: str, variant_type: str, variant_int: str) -> None:
    if 'cid' in cosmetic_id.lower() and 'jersey_color' not in variant_type.lower():
        skin_variants = client.party.me.create_variants(
            **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
        )
 
        await client.party.me.set_outfit(
            asset=cosmetic_id,
            variants=skin_variants
        )
 
    elif 'cid' in cosmetic_id.lower() and 'jersey_color' in variant_type.lower():
        cosmetic_variants = client.party.me.create_variants(
            pattern=0,
            numeric=69,
            **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
        )
 
        await client.party.me.set_outfit(
            asset=cosmetic_id,
            variants=cosmetic_variants
        )
 
    elif 'bid' in cosmetic_id.lower():
        cosmetic_variants = client.party.me.create_variants(
            item='AthenaBackpack',
            **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
        )
 
        await client.party.me.set_backpack(
            asset=cosmetic_id,
            variants=cosmetic_variants
        )
    elif 'pickaxe_id' in cosmetic_id.lower():
        cosmetic_variants = client.party.me.create_variants(
            item='AthenaPickaxe',
            **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
        )
 
        await client.party.me.set_pickaxe(
            asset=cosmetic_id,
            variants=cosmetic_variants
        )
 
    await ctx.send(f'Set variants of {cosmetic_id} to {variant_type} {variant_int}.')
    print(f'[PirxcyBot] [{time()}] Set variants of {cosmetic_id} to {variant_type} {variant_int}.')
 
 
@client.command()
async def checkeredrenegade(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        material=2
    )
 
    await client.party.me.set_outfit(
        asset='CID_028_Athena_Commando_F',
        variants=skin_variants
    )
 
    await ctx.send('Skin set to Checkered Renegade!')
    print(f'[PirxcyBot] [{time()}] Skin set to Checkered Renegade.')
 
 
@client.command()
async def mintyelf(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        material=2
    )
 
    await client.party.me.set_outfit(
        asset='CID_051_Athena_Commando_M_HolidayElf',
        variants=skin_variants
    )
 
    await ctx.send('Skin set to Minty Elf!')
    print(f'[PirxcyBot] [{time()}] Skin set to Minty Elf.')
 
 
@client.command()
async def eid(ctx: fortnitepy.ext.commands.Context, emote_id: str) -> None:
    await client.party.me.clear_emote()
    await client.party.me.set_emote(
        asset=emote_id
    )
 
    await ctx.send(f'Emote set to {emote_id}!')
 
 
@client.command()
async def stop(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.clear_emote()
    await ctx.send('Stopped emoting.')
 
 
@client.command()
async def bid(ctx: fortnitepy.ext.commands.Context, backpack_id: str) -> None:
    await client.party.me.set_backpack(
        asset=backpack_id
    )
 
    await ctx.send(f'Backbling set to {backpack_id}!')
 
 
@client.command()
async def _help(ctx: fortnitepy.ext.commands.Context) -> None:
    await ctx.send('DM me on Discord pirxcy#9999')
 
 
@client.command(aliases=['legacypickaxe'])
async def pickaxe_id(ctx: fortnitepy.ext.commands.Context, pickaxe_id_: str) -> None:
    await client.party.me.set_pickaxe(
        asset=pickaxe_id_
    )
 
    await ctx.send(f'Pickaxe set to {pickaxe_id_}')
 
 
@client.command()
async def pet_carrier(ctx: fortnitepy.ext.commands.Context, pet_carrier_id: str) -> None:
    await client.party.me.set_pet(
        asset=pet_carrier_id
    )
 
    await ctx.send(f'Pet set to {pet_carrier_id}!')
 
 
@client.command()
async def emoji_id(ctx: fortnitepy.ext.commands.Context, emoji_: str) -> None:
    await client.party.me.clear_emote()
    await client.party.me.set_emoji(
        asset=emoji_
    )
 
    await ctx.send(f'Emoji set to {emoji_}!')
 
 
@client.command()
async def trails(ctx: fortnitepy.ext.commands.Context, trails_: str) -> None:
    await client.party.me.set_contrail(
        asset=trails_
    )
 
    await ctx.send(f'Contrail set to {trails}!')
 
 
@client.command()
async def ready(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_ready(fortnitepy.ReadyState.READY)
    await ctx.send('Ready!')
 
@commands.dm_only()
@client.command()
@is_admin()
async def kick(ctx, *, member = None):
    if member is not None:
        if member.lower() == 'all':
            members = client.party.members

            for m in members:
                try:
                    member = await client.get_user(m)
                    await member.kick()
                except fortnitepy.Forbidden:
                    await ctx.send("I am not party leader.")

            await ctx.send("Kicked everyone in the party")

        else:
            try:
                user = await client.fetch_profile(member)
                member = client.party.members.get(user.id)
                if member is None:
                    await ctx.send("Couldn't find that user. Are you sure they're in the party?")

                await member.kick()
                await ctx.send(f'Kicked: {member.display_name}')
            except fortnitepy.Forbidden:
                await ctx.send("I can't kick that user because I am not party leader")
            except AttributeError:
                await ctx.send("Couldn't find that user.")
    else:
        await ctx.send(f'No member was given. Try: {prefix}kick (user)')
 
@commands.dm_only()
@client.command()
async def blockx(ctx: fortnitepy.ext.commands.Context, *, epic_username: str) -> None:
    user = await client.fetch_profile(epic_username)
    member = client.party.members.get(user.id)
 
    if member is None:
        await ctx.send("Failed")
    else:
        try:
            await member.block()
            await member.kick()
            await ctx.send(f"Blocked and Kicked: {member.display_name}.")
            print(f"[PirxcyBot] [{time()}] Blocked and Kicked: {member.display_name}")
        except fortnitepy.errors.Forbidden:
            await ctx.send(f"Failed to Block and Kick {member.display_name}, as I'm not party leader.")
            print(crayons.red(f"[PirxcyBot] [{time()}] [ERROR] "
                              "Failed to kick member as I don't have the required permissions."))
 
@commands.dm_only()
@client.command()
@is_admin()
async def promote(ctx, *, member = None):
    if member is None:
        user = await client.fetch_profile(ctx.message.author.id)
        member = client.party.members.get(user.id)
    if member is not None:
        user = await client.fetch_profile(member.display_name)
        member = client.party.members.get(user.id)
    try:
        await member.promote()
        await ctx.send(f"Promoted: {member.display_name}")
    except fortnitepy.Forbidden:
        await ctx.send("Client is not party leader")
    except fortnitepy.PartyError:
        await ctx.send("That person is already party leader")
    except fortnitepy.HTTPException:
        await ctx.send("Something went wrong trying to promote that member")
    except AttributeError:
        await ctx.send("I could not find that user")

@commands.dm_only()
@client.command()
@is_admin()
async def block(ctx, *, user = None):
    if user is not None:
        try:
            user = await client.fetch_profile(user)
            friends = client.friends

            if user.id in friends:
                try:
                    await user.block()
                    await ctx.send(f"Blocked {user.display_name}")
                except fortnitepy.HTTPException:
                    await ctx.send("Something went wrong trying to block that user.")

            elif user.id in client.blocked_users:
                await ctx.send(f"I already have {user.display_name} blocked.")
        except AttributeError:
            await ctx.send("I can't find a player with that name.")
    else:
        await ctx.send(f"No user was given. Try: {prefix}block (friend)")


@commands.dm_only()
@client.command()
@is_admin()
async def blocked(ctx):

    blockedusers = []

    for b in client.blocked_users:
        user = client.get_blocked_user(b)
        blockedusers.append(user.display_name)
    
    await ctx.send(f'Client has {len(blockedusers)} users blocked:')
    for x in blockedusers:
        if x is not None:
            await ctx.send(x)


@commands.dm_only()
@client.command()
@is_admin()
async def unblock(ctx, *, user = None):
    if user is not None:
        try:
            member = await client.fetch_profile(user)
            blocked = client.blocked_users
            if member.id in blocked:
                try:
                    await client.unblock_user(member.id)
                    await ctx.send(f'Successfully unblocked {member.display_name}')
                except fortnitepy.HTTPException:
                    await ctx.send('Something went wrong trying to unblock that user.')
            else:
                await ctx.send('That user is not blocked')
        except AttributeError:
            await ctx.send("I can't find a player with that name.")
    else:
        await ctx.send(f'No user was given. Try: {prefix}unblock (blocked user)')
    

@commands.dm_only()
@client.command()
@is_admin()
async def friends(ctx):
    cfriends = client.friends
    onlineFriends = []
    offlineFriends = []

    try:
        for f in cfriends:
            friend = client.get_friend(f)
            if friend.is_online():
                onlineFriends.append(friend.display_name)
            else:
                offlineFriends.append(friend.display_name)
        
        await ctx.send(f"Client has: {len(onlineFriends)} friends online and {len(offlineFriends)} friends offline")
        await ctx.send("(Check cmd for full list of friends)")

        print(" [+] Friends List: " + Fore.GREEN + f'{len(onlineFriends)} Online ' + Fore.RESET + "/" + Fore.LIGHTBLACK_EX + f' {len(offlineFriends)} Offline ' + Fore.RESET + "/" + Fore.LIGHTWHITE_EX + f' {len(onlineFriends) + len(offlineFriends)} Total')
        
        for x in onlineFriends:
            if x is not None:
                print(Fore.GREEN + " " + x)
        for x in offlineFriends:
            if x is not None:
                print(Fore.LIGHTBLACK_EX + " " + x)
    except Exception:
        pass


@commands.dm_only()
@client.command()
@is_admin()
async def members(ctx):
    pmembers = client.party.members
    partyMembers = []
    
    for m in pmembers:
        member = client.get_user(m)
        partyMembers.append(member.display_name)
    
    await ctx.send(f"There are {len(partyMembers)} members in {client.user.display_name}'s party:")
    for x in partyMembers:
        if x is not None:
            await ctx.send(x)
 
@client.command(aliases=['sitin'])
async def unready(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('Unready!')
 
 
@client.command()
async def sitoutingm(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    await ctx.send('Sitting Out!')
 
 
@client.command()
async def bp(ctx: fortnitepy.ext.commands.Context, tier: int) -> None:
    await client.party.me.set_battlepass_info(
        has_purchased=True,
        level=tier,
    )
 
    await ctx.send(f'Set battle pass tier to {tier}.')
 
 
@client.command()
async def level(ctx: fortnitepy.ext.commands.Context, banner_level: int) -> None:
    await client.party.me.set_banner(
        season_level=banner_level
    )
 
    await ctx.send(f'Set level to {level}.')
 
 
 
@client.command()
async def playlist_id(ctx: fortnitepy.ext.commands.Context, playlist_: str) -> None:
    try:
        await client.party.set_playlist(playlist=playlist_)
        await ctx.send(f'Gamemode set to {playlist_}')
    except fortnitepy.errors.Forbidden:
        await ctx.send(f"Failed to set gamemode to {playlist_}, as I'm not party leader.")
        print(crayons.red(f"[PirxcyBot] [{time()}] [ERROR] "
                          "Failed to set gamemode as I don't have the required permissions."))
 
 
@client.command()
async def starwars(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
    )
 
    await ctx.send('Skin set to Star Wars Hologram!')
    print(f'[PirxcyBot] [{time()}] Skin set to Star Wars')
 
 
@client.command()
async def gift(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.clear_emote()
 
    await client.party.me.set_emote(
        asset='EID_NeverGonna'
    )
 
    await ctx.send('What did you think would happen?')
 
 
@client.command()
async def matchmakingcode(ctx: fortnitepy.ext.commands.Context, *, custom_matchmaking_key: str) -> None:
    await client.party.set_custom_key(
        key=custom_matchmaking_key
    )
 
    await ctx.send(f'Custom matchmaking code set to: {custom_matchmaking_key}')
 
 
@client.command()
async def ponpon(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_TourBus'
    )
 
    await ctx.send('Emote set to Ninja Style!')

@client.command()
async def mufasa(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_SandwichBop'
    )
 
    await ctx.send('Emote set to Go Mufasa!')

@client.command()
async def jabba(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_JanuaryBop'
    )
 
    await ctx.send('Emote set to Go Jabba Switchway!')
 
@client.command()
async def glitch(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_HighTowerTomato'
    )
 
    await ctx.send('Emote set to Glitchiest Emote!')
 
@client.command()
async def twerk(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_securityguard'
    )
 
    await ctx.send('Work it!')
 
@client.command()
async def fixglitch(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_hightowertomato_npc'
    )
 
    await ctx.send('Emote set to Glitchiest Emote!')
 
@client.command()
async def tiktok(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_JustHome'
    )
 
    await ctx.send('Emote set to Cringiest Emote!')
 
@client.command()
async def whatsnew(ctx: fortnitepy.ext.commands.Context) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://pastebin.com/raw/qtGL6vX3") as res:
                text = await res.text(encoding="utf-8")
        await ctx.send(text)
 
@client.command()
async def upcoming(ctx: fortnitepy.ext.commands.Context) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://pastebin.com/raw/HHxs9hNg") as res:
                text = await res.text(encoding="utf-8")
        await ctx.send(text)
 
 
 
 
@client.command()
async def publicbots(ctx: fortnitepy.ext.commands.Context) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://pastebin.com/raw/k8N15Br2") as res:
                text = await res.text(encoding="utf-8")
        await ctx.send(text)
 
@client.command()
async def float(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_Davinci'
    )
 
    await ctx.send('Made For I float uツ')
 
@client.command()
async def tiktok2(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_JulyBooks'
    )
 
    await ctx.send('Emote set to Cringiest Emote!')
 
@client.command()
async def tiktok3(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_HotPink'
    )
 
    await ctx.send('Emote set to Cringiest Emote!')
 
@client.command()
async def tiktok4(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_twistdaytona'
    )
 
    await ctx.send('Emote set to Cleanest Emote!')
 
 
@client.command()
async def tiktok5(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_twisteternity'
    )
 
    await ctx.send('Emote set to Cleanest Emote!')
 
@client.command()
async def tiktok5v2(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_twisteternity_sync'
    )
 
    await ctx.send('Emote set to Cleanest Emote!')
 
@client.command()
async def diamond(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_keeperdreamchorus'
    )
 
    await ctx.send('Emote set to BTS Emote!')
 
@client.command()
async def dynamite(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_keeperdreamhook'
    )
 
    await ctx.send('Emote set to BTS Emote!')
 
@client.command()
async def simp(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_IndigoApple'
    )
 
@client.command()
async def madd(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_Alien'
    )
 
    await ctx.send('POG')
 
@client.command()
async def coco(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_Floss'
    )
 
    await ctx.send('Made For coco .exe')
 
@client.command()
async def pirxcy(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_NeverGonna'
    )
 
    await ctx.send('LMAO GET SHlT  ON!')
 
@client.command()
async def blind(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_autumntea'
    )
 
    await ctx.send('Oh im Blinded By The Lights!')
 
 
async def Seven(self) -> None:
            while True:
                mes = "Hey, \r\nTo Get Your Own Bot Follow These Steps\r\n Join The Discord on discord.gg/wxEBMTZ/ \r\nDM Me To Get A Bot\r\nEnjoy!"
                for friend in client.friends:
                    try:
                        await friend.send(mes)
                        await friend.invite()
                    except fortnitepy.HTTPException as e:
                        if e.message_code != "errors.com.epicgames.common.throttled":
                            raise
                        if "Operation access is limited by throttling policy" not in e.message:
                            raise
                        await asyncio.sleep(int(e.message_vars[0]) + 1)
                        await friend.send(mes)
                        await friend.invite()
                await asyncio.sleep(150)
 
@client.command()
async def crash(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote(
        asset='EID_WAve'
    )
 
    await ctx.send('aavaaaaaaaaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaavaaaaaaaaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaaaaavaavaaaaaaaaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaaaaavaavaaaaaaaaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaaaaavaavaaaaaaaaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaaaaavaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaavaaaaaaaaaaaaav')
 
@client.command()
async def enlightened(ctx: fortnitepy.ext.commands.Context, cosmetic_id: str, season: int, skin_level: int) -> None:
    if 'cid' in cosmetic_id.lower():
        await client.party.me.set_outfit(
            asset=cosmetic_id,
            variants=client.party.me.create_variants(progressive=4),
            enlightenment=(season, level)
        )
 
        await ctx.send(f'Skin set to {character_id} at level {skin_level} (for Season 1{season}).')
    elif 'bid' in cosmetic_id.lower():
        await client.party.me.set_backpack(
            asset=cosmetic_id,
            variants=client.party.me.create_variants(progressive=2),
            enlightenment=(season, level)
        )
        await ctx.send(f'Backpack set to {character_id} at level {skin_level} (for Season 1{season}).')
 
    print(f'[PirxcyBot] [{time()}] Enlightenment for {cosmetic_id} set to level {skin_level} (for Season 1{season}).')
 
 
@client.command()
async def ninja(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_605_Athena_Commando_M_TourBus'
    )
 
    await ctx.send('Skin set to Ninja!')
    print(f'[PirxcyBot] [{time()}] Skin set to Ninja.')
 
@client.command()
async def midas2(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_923_Athena_Commando_M_ParcelGold'
    )
 
    await ctx.send('Skin set to Midas Rex!')
    print(f'[PirxcyBot] [{time()}] Skin set to Joker.')

@client.command()
async def midas3(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_NPC_Athena_Commando_M_CatBurglar_Ghost'
    )
 
    await ctx.send('Skin set to Midas CPU!')
    print(f'[PirxcyBot] [{time()}] Skin set to Joker.')

@client.command()
async def mince(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_958_Athena_Commando_M_PieMan'
    )
 
    await ctx.send('Skin set to Mincemeat!')
    print(f'[PirxcyBot] [{time()}] Skin set to Joker.')

@client.command()
async def lachlan(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_891_Athena_Commando_M_LunchBox'
    )
 
    await ctx.send('Skin set to Mincemeat!')
    print(f'[PirxcyBot] [{time()}] Skin set to Joker.')

@client.command()
async def bedhead(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_927_Athena_Commando_M_NauticalPajamas'
    )
 
    await ctx.send('Skin set to Mincemeat!')
    print(f'[PirxcyBot] [{time()}] Skin set to Joker.')

@client.command()
async def bedhead2(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_928_Athena_Commando_M_NauticalPajamas_B'
    )
 
    await ctx.send('Skin set to Mincemeat!')
    print(f'[PirxcyBot] [{time()}] Skin set to Joker.')

@client.command()
async def bedhead3(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_929_Athena_Commando_M_NauticalPajamas_C'
    )
 
    await ctx.send('Skin set to Mincemeat!')
    print(f'[PirxcyBot] [{time()}] Skin set to Joker.')

@client.command()
async def joker(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_922_Athena_Commando_M_ParcelPrank'
    )
 
    await ctx.send('Skin set to Joker!')
    print(f'[PirxcyBot] [{time()}] Skin set to Joker.')
 
@client.command()
async def bigchungus(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='cid_npc_athena_commando_m_marauderheavy'
    )

    await ctx.send('Skin set to Bigchungus!')
    print(f'[PirxcyBot] [{time()}] Skin set to Ninja.')
 
@client.command()
async def randomize(ctx: fortnitepy.ext.commands.Context, cosmetic_type: str = 'skin') -> None:
    if cosmetic_type == 'skin':
        all_outfits = await BenBotAsync.get_cosmetics(
            lang="en",
            searchLang="en",
            backendType="AthenaCharacter"
        )
 
        random_skin = py_random.choice(all_outfits).id
 
        await client.party.me.set_outfit(
            asset=random_skin,
            variants=client.party.me.create_variants(profile_banner='ProfileBanner')
        )
 
        await ctx.send(f'Skin randomly set to {skin}.')
 
    elif cosmetic_type == 'backpack':
        all_backpacks = await BenBotAsync.get_cosmetics(
            lang="en",
            searchLang="en",
            backendType="AthenaBackpack"
        )
 
        random_backpack = py_random.choice(all_backpacks).id
 
        await client.party.me.set_backpack(
            asset=random_backpack,
            variants=client.party.me.create_variants(profile_banner='ProfileBanner')
        )
 
        await ctx.send(f'Backpack randomly set to {backpack}.')
 
    elif cosmetic_type == 'emote':
        all_emotes = await BenBotAsync.get_cosmetics(
            lang="en",
            searchLang="en",
            backendType="AthenaDance"
        )
 
        random_emote = py_random.choice(all_emotes).id
 
        await client.party.me.set_emote(
            asset=random_emote
        )
 
        await ctx.send(f'Emote randomly set to {emote}.')
 
    elif cosmetic_type == 'all':
        all_outfits = await BenBotAsync.get_cosmetics(
            lang="en",
            searchLang="en",
            backendType="AthenaCharacter"
        )
 
        all_backpacks = await BenBotAsync.get_cosmetics(
            lang="en",
            searchLang="en",
            backendType="AthenaBackpack"
        )
 
        all_emotes = await BenBotAsync.get_cosmetics(
            lang="en",
            searchLang="en",
            backendType="AthenaDance"
        )
 
        random_outfit = py_random.choice(all_outfits).id
        random_backpack = py_random.choice(all_backpacks).id
        random_emote = py_random.choice(all_emotes).id
 
        await client.party.me.set_outfit(
            asset=random_outfit
        )
 
        await ctx.send(f'Skin randomly set to {random_outfit}.')
 
        await client.party.me.set_backpack(
            asset=random_backpack
        )
 
        await ctx.send(f'Backpack randomly set to {random_backpack}.')
 
        await client.party.me.set_emote(
            asset=random_emote
        )
 
        await ctx.send(f'Emote randomly set to {random_emote}.')
 
 
@client.command()
async def nobackpack(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.clear_backpack()
    await ctx.send('Removed backpack.')
 
 
@client.command()
async def nopet(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.clear_pet()
    await ctx.send('Removed pet.')
 
 
@client.command()
async def nocontrail(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.clear_contrail()
    await ctx.send('Removed contrail.')
 
 
@client.command()
async def match(ctx: fortnitepy.ext.commands.Context, players: Union[str, int] = 0, inputted_time: int = 0) -> None:
    if players == 'progressive':
        await set_and_update_member_prop('Location_s', 'InGame')
        await set_and_update_member_prop('HasPreloadedAthena_b', True)
        await set_and_update_member_prop('SpectateAPartyMemberAvailable_b', 'true')
        await set_and_update_member_prop('NumAthenaPlayersLeft_U', '100')
 
        match_time = str(fortnitepy.Client.to_iso(
            datetime.datetime.utcnow()
        ))[slice(23)]
 
        await set_and_update_member_prop('UtcTimeStartedMatchAthena_s', f'{str(match_time)}Z')
 
        await ctx.send(f'Set state to in-game in a match with progressive players drop starting from 100.'
                       '\nUse the command: !lobby to revert back to normal.')
 
        while (100 >= client.party.me.meta.get_prop('NumAthenaPlayersLeft_U') > 0
               and client.party.me.meta.get_prop('Location_s') == 'InGame'):
            await set_and_update_member_prop(
                'NumAthenaPlayersLeft_U',
                client.party.me.meta.get_prop('NumAthenaPlayersLeft_U') - random.randint(3, 6)
            )
 
            await asyncio.sleep(random.randint(45, 65))
 
    else:
        await set_and_update_member_prop('Location_s', 'InGame')
        await set_and_update_member_prop('NumAthenaPlayersLeft_U', players)
        await set_and_update_member_prop('HasPreloadedAthena_b', True)
        await set_and_update_member_prop('SpectateAPartyMemberAvailable_b', 'true')
 
        match_time = str(fortnitepy.Client.to_iso(
            datetime.datetime.utcnow() - datetime.timedelta(minutes=inputted_time)
        ))[slice(23)]
 
        await set_and_update_member_prop('UtcTimeStartedMatchAthena_s', f'{str(match_time)}Z')
 
        await ctx.send(f' Currently Displaying in game match with  {players} players.'
                       '\nUse the command: !lobby to revert back to the lobby.')
 
 
@client.command()
async def lobby(ctx: fortnitepy.ext.commands.Context) -> None:
    await set_and_update_member_prop('Location_s', 'PreLobby')
    await set_and_update_member_prop('NumAthenaPlayersLeft_U', '0')
    await set_and_update_member_prop('HasPreloadedAthena_b', False)
    await set_and_update_member_prop('SpectateAPartyMemberAvailable_b', 'false')
    await set_and_update_member_prop('UtcTimeStartedMatchAthena_s', '0001-01-01T00:00:00.000Z')
 
    await ctx.send('Current state in Lobby.')
 
 
 
@client.command()
async def playlist(ctx: fortnitepy.ext.commands.Context, *, playlist_name: str) -> None:
    try:
        scuffedapi_playlist_id = await get_playlist(playlist_name)
 
        if scuffedapi_playlist_id is not None:
            await client.party.set_playlist(playlist=scuffedapi_playlist_id)
            await ctx.send(f'Playlist set to {scuffedapi_playlist_id}.')
            print(f'[PirxcyBot] [{time()}] Playlist set to {scuffedapi_playlist_id}.')
 
        else:
            await ctx.send(f'Failed to find a playlist with the name: {playlist_name}.')
            print(crayons.red(f"[PirxcyBot] [{time()}] [ERROR] "
                              f"Failed to find a playlist with the name: {playlist_name}."))
 
    except fortnitepy.errors.Forbidden:
        await ctx.send(f"Failed to set playlist to {playlist_namet}, as I'm not party leader.")
        print(crayons.red(f"[PirxcyBot] [{time()}] [ERROR] "
                          "Failed to set playlist as I don't have the required permissions."))
 
 
@client.command()
async def ghost(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        skin_variants = client.party.me.create_variants(
            progressive=2
        )
 
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaCharacter"
        )
 
        await client.party.me.set_outfit(
            asset=cosmetic.id,
            variants=skin_variants
        )
 
        await ctx.send(f'Skin set to Ghost {cosmetic.name}!')
        print(f'[PirxcyBot] [{time()}] Skin set to Ghost {cosmetic.name}.')
 
    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a skin with the name: {content}.")
        print(f"[PirxcyBot] [{time()}] Failed to find a skin with the name: {content}.")
 
 
@client.command()
async def shadow(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        skin_variants = client.party.me.create_variants(
            progressive=3
        )
 
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaCharacter"
        )
 
        await client.party.me.set_outfit(
            asset=cosmetic.id,
            variants=skin_variants
        )
 
        await ctx.send(f'Skin set to Shadow {cosmetic.name}!')
        print(f'[PirxcyBot] [{time()}] Skin set to Ghost {cosmetic.name}.')
 
    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a skin with the name: {content}.")
        print(f"[PirxcyBot] [{time()}] Failed to find a skin with the name: {content}.")
 
 
 
@client.command()
async def set(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    cosmetic_types = {
        "AthenaBackpack": client.party.me.set_backpack,
        "AthenaCharacter": client.party.me.set_outfit,
        "AthenaEmoji": client.party.me.set_emoji,
        "AthenaDance": client.party.me.set_emote
    }
 
    set_items = await BenBotAsync.get_cosmetics(
        lang="en",
        searchLang="en",
        matchMethod="contains",
        set=content
    )
 
    await ctx.send(f'Equipping all cosmetics from the {set_items[0].set} set.')
    print(f'[PirxcyBot] [{time()}] Equipping all cosmetics from the {set_items[0].set} set.')
 
    for cosmetic in set_items:
        if cosmetic.backend_type.value in cosmetic_types:
            await cosmetic_types[cosmetic.backend_type.value](asset=cosmetic.id)
 
            await ctx.send(f'{cosmetic.short_description} set to {cosmetic.name}!')
            print(f'[PirxcyBot] [{time()}] {cosmetic.short_description} set to {cosmetic.name}.')
 
            await asyncio.sleep(3)
 
    await ctx.send(f'Finished equipping all cosmetics from the {set_items[0].set} set.')
    print(f'[PirxcyBot] [{time()}] Fishing equipping  all cosmetics from the {set_items[0].set} set.')
 
 
@client.command()
async def style(ctx: fortnitepy.ext.commands.Context, cosmetic_name: str, variant_type: str, variant_int: str) -> None:
    # cosmetic_types = {
    #     "AthenaCharacter": client.party.me.set_outfit,
    #     "AthenaBackpack": client.party.me.set_backpack,
    #     "AthenaPickaxe": client.party.me.set_pickaxe
    # }
 
    cosmetic = await BenBotAsync.get_cosmetic(
        lang="en",
        searchLang="en",
        matchMethod="contains",
        name=cosmetic_name,
        backendType="AthenaCharacter"
    )
 
    cosmetic_variants = client.party.me.create_variants(
        # item=cosmetic.backend_type.value,
        **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
    )
 
    # await cosmetic_types[cosmetic.backend_type.value](
    await client.party.me.set_outfit(
        asset=cosmetic.id,
        variants=cosmetic_variants
    )
 
    await ctx.send(f'Set variants of {cosmetic.id} to {variant_type} {variant_int}.')
    print(f'[PirxcyBot] [{time()}] Set variants of {cosmetic.id} to {variant_type} {variant_int}.')
 
 
@client.command()
async def sleaks(ctx: fortnitepy.ext.commands.Context) -> None:
    async with aiohttp.ClientSession() as session:
        request = await session.request(
            method='GET',
            url='https://fortnite-api.theapinetwork.com/upcoming/get',
        )
 
        response = await request.json()
 
    for new_skin in [new_cid for new_cid in response if new_cid.split('/')[-1].lower().startswith('cid_')]:
        await client.party.me.set_outfit(
            asset=new_skin.split('/')[-1].split('.uasset')[0]
        )
 
        await ctx.send(f"Skin set to {new_skin.split('/')[-1].split('.uasset')[0]}!")
        print(f"[PirxcyBot] [{time()}] Skin set to: {new_skin.split('/')[-1].split('.uasset')[0]}!")
 
        await asyncio.sleep(5)
 
    await ctx.send(f'Displayed All Leaked Skins\nThis Might Not Up to date As PAK/AESs Are Fuked')
    print(f'[PirxcyBot] [{time()}] New Leaked skins')

@client.command()
async def shops(ctx: fortnitepy.ext.commands.Context) -> None:
    async with aiohttp.ClientSession() as session:
        request = await session.request(
            method='GET',
            url='https://fortnite-api.theapinetwork.com/store/get',
        )
 
        response = await request.json()
 
    for new_skin in [new_cid for new_cid in response if new_cid.split('/')[-1].lower().startswith('cid_')]:
        await client.party.me.set_outfit(
            asset=new_skin.split('/')[-1].split('.uasset')[0]
        )
 
        await ctx.send(f"Skin set to {new_skin.split('/')[-1].split('.uasset')[0]}!")
        print(f"[PirxcyBot] [{time()}] Skin set to: {new_skin.split('/')[-1].split('.uasset')[0]}!")
 
        await asyncio.sleep(5)
 
    await ctx.send(f'Displayed All item shop Skins')
    print(f'[PirxcyBot] [{time()}] New Leaked skins')
 
@client.command()
async def shopem(ctx: fortnitepy.ext.commands.Context) -> None:
    async with aiohttp.ClientSession() as session:
        request = await session.request(
            method='GET',
            url='https://fortnite-api.com/v2/shop/br',
        )
 
        response = await request.json()
 
    for new_emoji in [new_emoji for new_emoji in response if new_emoji.split('/')[-1].lower().startswith('emoji_')]:
        client.party.me.set_emoji(
            asset=new_emoji.split('/')[-1].split('.uasset')[0]
        )
 
        await ctx.send(f"Emoji set to {new_emoji.split('/')[-1].split('.uasset')[0]}!")
        print(f"[PirxcyBot] [{time()}] Emoji set to: {new_emoji.split('/')[-1].split('.uasset')[0]}!")
 
        await asyncio.sleep(5)
 
    await ctx.send(f'Displayed All item shop Emoji')
    print(f'[PirxcyBot] [{time()}] New Leaked Emojis')
 
 
@client.command()
async def eleaks(ctx: fortnitepy.ext.commands.Context) -> None:
    async with aiohttp.ClientSession() as session:
        request = await session.request(
            method='GET',
            url='https://fortnite-api.theapinetwork.com/upcoming/get',
        )
 
        response = await request.json()
 
    for new_emote in [new_eid for new_eid in response if new_eid.split('/')[-1].lower().startswith('eid_')]:
        await client.party.me.set_emote(
            asset=new_emote.split('/')[-1].split('.uasset')[0]
        )
 
        await ctx.send(f"Emote set to {new_emote.split('/')[-1].split('.uasset')[0]}!")
        print(f"[PirxcyBot] [{time()}] Emote set to: {new_emote.split('/')[-1].split('.uasset')[0]}!")
 
        await asyncio.sleep(5)
 
    await ctx.send(f'Displayed All Leaked Emotes')
    print(f'[PirxcyBot] [{time()}] New Leaked Emotes')
 
@client.command()
async def emotes(ctx: fortnitepy.ext.commands.Context) -> None:
    async with aiohttp.ClientSession() as session:
        request = await session.request(
            method='GET',
            url='https://benbotfn.tk/api/v1/files/added',
        )
 
        response = await request.json()
 
    for new_emote in [new_eid for new_eid in response if new_eid.split('/')[-1].lower().startswith('eid_')]:
        await client.party.me.set_emote(
            asset=new_emote.split('/')[-1].split('.uasset')[0]
        )
 
        await ctx.send(f"Skin set to {new_emote.split('/')[-1].split('.uasset')[0]}!")
        print(f"[PirxcyBot] [{time()}] Skin set to: {new_emote.split('/')[-1].split('.uasset')[0]}!")
 
        await asyncio.sleep(5)
 
    await ctx.send(f'Displayed All Leaked Emotes')
    print(f'[PirxcyBot] [{time()}] New Leaked Emotes')
 
 
@client.command()
async def shopon(ctx: fortnitepy.ext.commands.Context) -> None:
    store = await client.fetch_item_shop()
 
    await ctx.send(f"Currently displaying itemshop rotation")
    print(f"[PirxcyBot] [{time()}] Equipping all skins in today's item shop.")
 
    for item in store.featured_items + store.daily_items:
        for grant in item.grants:
            if grant['type'] == 'AthenaCharacter':
                await client.party.me.set_outfit(
                    asset=grant['asset']
                )
 
                await ctx.send(f"Skin set to {item.display_names[0]}!")
                print(f"[PirxcyBot] [{time()}] Skin set to: {item.display_names[0]}!")
 
                await asyncio.sleep(3)
 
    await ctx.send(f'Displayed Current Itemshop Rotation')
    print(f'[PirxcyBot] [{time()}] Finished equipping all skins in the item shop.')
 
 
 
@client.command()
async def recon2(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        parts=2
    )
 
    await client.party.me.set_outfit(
        asset='CID_022_Athena_Commando_F',
        variants=skin_variants
    )
 
    await ctx.send('Recon Experts Second Style')
    print(f'[PirxcyBot] [{time()}] Skin set to Hatless Recon Expert.')
 
@client.command()
async def bulls2(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        parts=2
    )
 
    await client.party.me.set_outfit(
        asset='CID_242_athena_commando_f_bullseye',
        variants=skin_variants
    )
 
    await ctx.send('Bullseye Second Style')
    print(f'[PirxcyBot] [{time()}] Skin set to Second. Bullseye Style!.')
 
@is_admin()
@client.command()
async def leave(ctx: 
  fortnitepy.ext.commands.Context) -> None:
        await client.party.me.set_emote(asset=(data['leave_emote']))
        await asyncio.sleep(2)
        await client.party.me.leave()
        await ctx.send(data['leave_message'])
 
 
commands.dm_only()
@client.command()
async def pbp(ctx: fortnitepy.ext.commands.Context) -> None:
     async def privacy(self, ctx: fortnitepy.ext.commands.Context, privacy_type: str) -> None:
        try:
            if privacy_type.lower() == 'public':
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            elif privacy_type.lower() == 'private':
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE)
            elif privacy_type.lower() == 'friends':
                await self.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS)
            elif privacy_type.lower() == 'friends_allow_friends_of_friends':
                await self.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS_ALLOW_FRIENDS_OF_FRIENDS)
            elif privacy_type.lower() == 'private_allow_friends_of_friends':
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE_ALLOW_FRIENDS_OF_FRIENDS)
 
            await ctx.send(f'Party privacy set to {self.party.privacy}.')
            print(f'Party privacy set to {self.party.privacy}.')
 
        except fortnitepy.errors.Forbidden:
            await ctx.send(f"Failed to set party privacy to {privacy_type}, as I'm not party leader.")
            print(crayons.red(f"[ERROR] "
                              "Failed to set party privacy as I don't have the required permissions."))
@client.command()
async def maxtier(ctx: fortnitepy.ext.commands.Context, br_season: int) -> None:
    max_tier_skins = {
        1: "CID_028_Athena_Commando_F",
        2: "CID_035_Athena_Commando_M_Medieval",
        3: "CID_084_Athena_Commando_M_Assassin",
        4: "CID_116_Athena_Commando_M_CarbideBlack",
        5: "CID_165_Athena_Commando_M_DarkViking",
        6: "CID_230_Athena_Commando_M_Werewolf",
        7: "CID_288_Athena_Commando_M_IceKing",
        8: "CID_352_Athena_Commando_F_Shiny",
        9: "CID_407_Athena_Commando_M_BattleSuit",
        10: "CID_484_Athena_Commando_M_KnightRemix",
        11: "CID_572_Athena_Commando_M_Viper",
        12: "CID_694_Athena_Commando_M_CatBurglar"
    }
 
    await client.party.me.set_outfit(asset=max_tier_skins[br_season])
 
    await ctx.send(f'Displaying Max Tier Skins')
    print(f"[PirxcyBot] [{time()}] Skin set to {max_tier_skins[br_season]}.")
 

@commands.dm_only()
@client.command()
async def admin(ctx, setting = None, *, user = None):
    if (setting is None) and (user is None):
        await ctx.send(f"Missing one or more arguments. Try: {prefix}admin (add, remove, list) (user)")
    elif (setting is not None) and (user is None):

        user = await client.fetch_profile(ctx.message.author.id)

        if setting.lower() == 'add':
            if user.id in info['FullAccess']:
                await ctx.send("You are already an admin")

            else:
                await ctx.send("Password?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if content == data['AdminPassword']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("Incorrect Password.")

        elif setting.lower() == 'remove':
            if user.id not in info['FullAccess']:
                await ctx.send("You are not an admin.")
            else:
                await ctx.send("Are you sure you want to remove yourself as an admin?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if (content.lower() == 'yes') or (content.lower() == 'y'):
                    info['FullAccess'].remove(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send("You were removed as an admin.")
                        print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                elif (content.lower() == 'no') or (content.lower() == 'n'):
                    await ctx.send("You were kept as admin.")
                else:
                    await ctx.send("Not a correct reponse. Cancelling command.")
                
        elif setting == 'list':
            if user.id in info['FullAccess']:
                admins = []

                for admin in info['FullAccess']:
                    user = await client.fetch_profile(admin)
                    admins.append(user.display_name)

                await ctx.send(f"The bot has {len(admins)} admins:")

                for admin in admins:
                    await ctx.send(admin)

            else:
                await ctx.send("You don't have permission to this command.")

        else:
            await ctx.send(f"That is not a valid setting. Try: {prefix}admin (add, remove, list) (user)")
            
    elif (setting is not None) and (user is not None):
        user = await client.fetch_profile(user)

        if setting.lower() == 'add':
            if ctx.message.author.id in info['FullAccess']:
                if user.id not in info['FullAccess']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("That user is already an admin.")
            else:
                await ctx.send("You don't have access to add other people as admins. Try just: !admin add")
        elif setting.lower() == 'remove':
            if ctx.message.author.id in info['FullAccess']:
                if user.id in info['FullAccess']:
                    await ctx.send("Password?")
                    response = await client.wait_for('friend_message', timeout=20)
                    content = response.content.lower()
                    if content == data['AdminPassword']:
                        info['FullAccess'].remove(user.id)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send(f"{user.display_name} was removed as an admin.")
                            print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                    else:
                        await ctx.send("Incorrect Password.")
                else:
                    await ctx.send("That person is not an admin.")
            else:
                await ctx.send("You don't have permission to remove players as an admin.")
        else:
            await ctx.send(f"Not a valid setting. Try: {prefix}admin (add, remove) (user)")
 
if (data['email'] and data['password']) and (data['email'] != 'email@email.com' and data['password'] != 'password1'):
    try:
        client.run()
    except fortnitepy.errors.AuthException as e:
        print(crayons.red(f"[PirxcyBot] [{time()}] [ERROR] {e}"))
else:
    print(crayons.red(f"[PirxcyBot] [{time()}] [ERROR] Failed to login as no (or default) account details provided."))
