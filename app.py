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


@client.event
async def on_raw_reaction_add(payload):
    """
    Event triggered when a user reacts to a message with an emoji.

    If the message ID is in the specified list of message IDs, the function attempts to add a role to the user.

    Parameters:
        payload (discord.RawReactionActionEvent): The raw reaction event.

    Returns:
        None
    """
    await update_role(payload, True)


@client.event
async def on_raw_reaction_remove(payload):
    """
    Event triggered when a user removes a reaction from a message with an emoji.

    If the message ID is in the specified list of message IDs, the function attempts to remove a role from the user.

    Parameters:
        payload (discord.RawReactionActionEvent): The raw reaction event.

    Returns:
        None
    """
    await update_role(payload, False)


async def update_role(payload, add_role):
    """
    Attempts to add or remove a role to/from the user based on the provided payload and flag.

    If the message ID is in the specified list of message IDs, the function attempts to add or remove a role to/from the user
    based on the provided flag.

    Parameters:
        payload (discord.RawReactionActionEvent): The raw reaction event.
        add_role (bool): Flag indicating whether to add or remove the role.

    Returns:
        None
    """
    message_ids = os.environ.get("MESSAGE_IDS")
    message_ids_list = [int(id) for id in message_ids.split(",")]
    message_id = payload.message_id

    # Check if the message ID is in the specified list of message IDs
    if message_id in message_ids_list:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        # Get the role associated with the emoji
        role = discord.utils.get(guild.roles, name=payload.emoji.name)

        # If the role is found, try to add/remove it to/from the user
        if role is not None:
            member = guild.get_member(payload.user_id)
            if member is None:
                print("Member Not Found")
            elif add_role:
                await member.add_roles(role)
                print("Role Added")
            else:
                await member.remove_roles(role)
                print("Role Removed")
        else:
            print("Role Not Found")


# Bot Token
token = client.run(os.getenv("BOT_TOKEN"))
client.run(token)
