# Load packages
import os

import discord
from discord import app_commands
from discord.ext import commands

# Credentials
# load_dotenv('.env')

# Grant necessary intents to see reactions/member list
intents = discord.Intents.default()
intents.reactions = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
# Sets status text and type (1=playing, 2=listening, 3=watching)
status = discord.Activity(name="https://7cav.us", type=3)


def can_manage_reps():
    return app_commands.checks.has_any_role(
        "S5 - Public Relations", "General Staff", "Administrator"
    )


@tree.error
async def on_command_error(
    interaction: discord.Interaction, error: discord.app_commands.AppCommandError
) -> None:
    if isinstance(error, app_commands.errors.MissingAnyRole):
        await interaction.response.send_message(
            f"You must have one of these roles: `{error.missing_roles}` in order to use this command",
            ephemeral=True,
        )
    elif isinstance(error, app_commands.errors.AppCommandError):
        await interaction.response.send_message(
            f"```{error.original}```Please ensure you are typing the name of a member who is currently \
on this server. This is easiest if you use a mention, otherwise it is case sensitive. If you need further \
help open an S6 Ticket.",
            ephemeral=True,
        )
    else:
        sypolt = await client.fetch_user(130158049968128000)
        await sypolt.send(
            f"Someone broke your bot, it was probably liber ```{error}```"
        )
        await interaction.response.send_message(
            "You managed to break the bot in a way I didn't expect, good job. If the Cav \
had an Army Bug Finder medal I'd give it to you. Anyway the error was forwarded to me, Sypolt.R. \
Why don't you try whatever that was again but with less breaking things this time?",
            ephemeral=True,
        )


# Create repadd command
@tree.command(
    name="add_clan_rep",
    description="For S5 Members to Add Clan Reps",
    guild=discord.Object(id=109869242148491264),
)
@can_manage_reps()
async def clan_rep_add(interaction, target: str):
    member = await commands.MemberConverter().convert(interaction.user, target)
    role = discord.utils.get(interaction.guild.roles, id=1080062973483163742)
    if role in member.roles:
        await interaction.response.send_message(
            f"{member.mention} already has the role {role.mention}", ephemeral=True
        )
    else:
        await interaction.response.send_message(
            f"{role.mention} added to {member.mention}", ephemeral=True
        )
        await member.add_roles(discord.Object(1080062973483163742))


@tree.command(
    name="remove_clan_rep",
    description="For S5 Members to Remove Clan Reps",
    guild=discord.Object(id=109869242148491264),
)
@can_manage_reps()
async def clan_rep_remove(interaction, target: str):
    member = await commands.MemberConverter().convert(interaction.user, target)
    role = discord.utils.get(interaction.guild.roles, id=1080062973483163742)
    if role not in member.roles:
        await interaction.response.send_message(
            f"{member.mention} doesn't have the role {role.mention}", ephemeral=True
        )
    else:
        await interaction.response.send_message(
            f"{role.mention} removed from {member.mention}", ephemeral=True
        )
        await member.remove_roles(discord.Object(1080062973483163742))


# Output success message when connected and add status
@client.event
async def on_ready():
    await client.change_presence(activity=status)
    await tree.sync(guild=discord.Object(id=109869242148491264))
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
