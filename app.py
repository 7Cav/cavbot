# Load packages
import discord

# from dotenv import load_dotenv
import os

# Credentials
# load_dotenv('.env')

# Grant necessary intents to see reactions/member list
intents = discord.Intents.default()
intents.reactions = True
intents.members = True
client = discord.Client(intents=intents)
# Sets status text and type (1=playing, 2=listening, 3=watching)
status = discord.Activity(name="https://7cav.us", type=3)


# Output success message when connected and add status
@client.event
async def on_ready():
    await client.change_presence(activity=status)
    print("Bot ready")


# Add role based on Emoji Name - - Emoji name and Role name MUST MATCH
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    # Change Message ID to the ID of the message you want the bot to look at
    if message_id == 829823580099182612:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        role = discord.utils.get(guild.roles, name=payload.emoji.name)
        if role is not None:
            member = payload.member
            if member is not None:
                await member.add_roles(role)
                print("Role Added")
            else:
                print("Member Not Found")
        else:
            print("Role Not Found")
    if message_id == 947278394712797224:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        role = discord.utils.get(guild.roles, name=payload.emoji.name)
        if role is not None:
            member = payload.member
            if member is not None:
                await member.add_roles(role)
                print("Role Added")
            else:
                print("Member Not Found")
        else:
            print("Role Not Found")


# Remove role based on Emoji Name - - Emoji name and Role name MUST MATCH
@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 829823580099182612:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        role = discord.utils.get(guild.roles, name=payload.emoji.name)
        if role is not None:
            member = guild.get_member(payload.user_id)
            if member is not None:
                await member.remove_roles(role)
                print("Role Removed")
            else:
                print("Member Not Found")
        else:
            print("Role Not Found")
    if message_id == 947278394712797224:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        role = discord.utils.get(guild.roles, name=payload.emoji.name)
        if role is not None:
            member = guild.get_member(payload.user_id)
            if member is not None:
                await member.remove_roles(role)
                print("Role Removed")
            else:
                print("Member Not Found")
        else:
            print("Role Not Found")


# Bot Token
token = client.run(os.getenv("BOT_TOKEN"))
client.run(token)
