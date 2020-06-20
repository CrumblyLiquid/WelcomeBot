import discord
from discord.ext import commands
from pathlib import Path
import os
import json
import io
import aiohttp
from PIL import Image

def getConfig(element: str):
    with open(str(Path(__file__).parent.absolute()) + '/config.json') as json_file:
        config = json.load(json_file)
    return config[element]

bot = commands.Bot(command_prefix = '', help_command=None, description='WelcomeBot is a bot which welcomes everyone!')

@bot.event
async def on_ready():
    print('Bot is ready!')
    print(f'Logged in as {bot.user}')
    print('')
    print('Author: CrumblyLiquid (CrumblyLiquid#6668)')
    print('')
    print('If you find any bugs please report to:\n- https://github.com/CrumblyLiquid/WelcomeBot\n- crumblyliquid@gmail.com')
    print('')

@bot.event
async def on_member_join(member):
    # Finds channel specified in config.json under element 'channel'
    chname = getConfig('channel')
    for channel in member.guild.channels:
        if channel.name == chname:
            async with aiohttp.ClientSession() as session: # Gets the avatar of user
                async with session.get(str(member.avatar_url_as(format='png', size=256))) as response:
                    if response.status != 200:
                        print('[ERROR]: Couldn\'t get picture from the avatar url!')
                        return
                    data = io.BytesIO(await response.read())

                    # Loads the original avatar picture
                    avatar = Image.open(data)
                    # cavatar = Cropped avatar
                    cavatar = avatar.crop((int((avatar.size[0]-148)/2), int((avatar.size[1]-172)/2), int(avatar.size[0]-((avatar.size[0]-148)/2)), int(avatar.size[1]-((avatar.size[1]-172)/2))))
                    
                    # Pastes the avatar into the template.png creating <user_id>.png
                    template = Image.open(str(Path(__file__).parent.absolute()) + '/template.png')
                    template.paste(cavatar, (437, 40, 437 + cavatar.size[0], 40 + cavatar.size[1]))
                    template.paste(cavatar, (441, 381, 441 + cavatar.size[0], 381 + cavatar.size[1]))
                    byteimg = io.BytesIO()
                    template.save(byteimg)
                    byteimg.seek(0)
                    finalimg = discord.File(byteimg)

                    # Sends the <user_id>.png with the welcoming message
                    await channel.send(f'Welcome to {member.guild.name}, {member.mention}!', file=finalimg)
                    
                    # Deletes the <user_id>.png
                    os.remove((str(Path(__file__).parent.absolute()) + f'/{member.id}.png'))

@bot.event
async def on_member_leave(member):
    pass # When I get good picture for leave event I'll add it. 

bot.run(getConfig('token'), reconnect=True)