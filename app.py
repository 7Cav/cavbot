# This script requires the following environment variables to be set:
# - MESSAGE_IDS: A comma-separated list of message IDs to monitor for reactions
# - BOT_TOKEN: The API token for your Discord bot
# - GUILD_ID: The ID of the Discord guild the bot will operate in
# - PTERO_API: The API key for your Pterodactyl instance

# Load packages
import os
import requests
import asyncio
import aiohttp

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


env_vars = {
    "GUILD_ID": "No guild ID found in environment variable GUILD_ID\nPlease add a guild ID to the environment variable GUILD_ID",
    "PTERO_API": "No Pterodactyl API key found in environment variable PTERO_API\nPlease add a Pterodactyl API key to the environment variable PTERO_API",
    "SERVERS": "No servers found in environment variable SERVERS\nPlease add servers in the format of server1:server1_id,server2:server2_id",
    "BOT_TOKEN": "No bot token found in environment variable BOT_TOKEN\nPlease add a bot token to the environment variable BOT_TOKEN",
    "MESSAGE_IDS": "No message IDs found in environment variable MESSAGE_IDS\nPlease add a comma-separated list of message IDs to the environment variable MESSAGE_IDS",
}

for var, error_msg in env_vars.items():
    value = os.environ.get(var)
    if value is None:
        print(error_msg)
        exit(1)

# Set the main_guild_id variable to the guild ID stored in the GUILD_ID environment variable
# This environment variable is used to configure which guild the bot should operate in
main_guild_id = os.environ.get("GUILD_ID")


# Set the ptero_api variable to the Pterodactyl API key stored in the PTERO_API environment variable
# This environment variable is used to configure the Pterodactyl API key
ptero_api = os.environ.get("PTERO_API")


server_list = os.environ.get("SERVERS")
SERVERS = {
    server.split(":")[0]: server.split(":")[1] for server in server_list.split(",")
}


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


@tree.command(
    name="restart",
    description="Restarts/Updates the selected Arma Server",
    guild=discord.Object(id=main_guild_id),
)


    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://panel.7cav.us/api/application/servers/{server_id}/power",
            headers={
                "Authorization": f"Bearer {ptero_api}",
                "Content-Type": "application/json",
                "Accept": "Application/vnd.pterodactyl.v1+json",
            },
            json={"command": "restart"},
            timeout=10,
        ) as response:
            if response.status == 204:
                await interaction.followup.send("Server restarting...")
            else:
                await interaction.followup.send(
                    "Something went wrong, please try again later."
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
# Set the token variable to the bot token from the environment variables
token = client.run(os.getenv("BOT_TOKEN"))
# Run the client with the token
client.run(token)
