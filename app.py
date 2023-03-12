# Load packages
import os

import discord
from discord import app_commands

# Create a new Intents object with the default intents
intents = discord.Intents.default()

# Enable the intents to see reactions and members
intents.reactions = True
intents.members = True

# Create a new Client object with the specified intents
client = discord.Client(intents=intents)

# Create a new CommandTree object for registering slash commands
tree = app_commands.CommandTree(client)

# Set the bot's status to a custom message
# The Activity object takes a name and a type parameter
# The type can be set to 1 (playing), 2 (listening), or 3 (watching)
status = discord.Activity(name="https://7cav.us", type=3)

# Set the main_guild_id variable to the bot token from the environment variables
main_guild_id = os.environ.get("GUILD_ID")

@client.event
async def on_ready():
    """
    This function is called when the bot is connected to Discord and ready to receive messages.

    It sets the bot's status to the value of the `status` variable and prints a message to the console
    indicating that the bot is ready.
    """
    # Set the bot's activity status to the value of the `status` variable
    await client.change_presence(activity=status)
    
    await tree.sync(guild=discord.Object(id=main_guild_id))

    # Print a message to the console indicating that the bot is ready
    print("Bot ready")


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
# Set the token variable to the bot token from the environment variables
token = client.run(os.getenv("BOT_TOKEN"))
# Run the client with the token
client.run(token)
