# This script requires the following environment variables to be set:
# - MESSAGE_IDS: A comma-separated list of message IDs to monitor for reactions
# - BOT_TOKEN: The API token for your Discord bot
# - GUILD_ID: The ID of the Discord guild the bot will operate in
# - PTERO_API: The API key for your Pterodactyl instance
# - SERVERS: A comma-separated list of servers in the format of server1:server1_id,server2:server2_id
# - COGS: A comma-separated list of cogs to load


# Load packages
import os

import discord
from discord.ext import commands

# Create a new Intents object with the default intents
intents = discord.Intents.all()

# Enable the intents to see reactions and members
intents.reactions = True
intents.members = True
intents.guild_messages = True

# Create a new Client object with the specified intents
bot = commands.Bot(command_prefix="!", intents=intents)

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
    "COGS": "No cogs found in environment variable COGS\nPlease add a comma-separated list of cogs to the environment variable COGS",
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

# Loop through all files in the cogs directory
for filename in os.listdir("./cogs"):
    # Check if the file is a Python file
    if filename.endswith(".py") and (
        # check if the cog is not in the COGS environment variable
        not os.environ.get("COGS")
        or filename[:-3] in os.environ["COGS"].split(",")
    ):
        # Load the cog
        bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def on_ready():
    """
    This function is called when the bot is connected to Discord and ready to receive messages.

    It sets the bot's status to the value of the `status` variable and prints a message to the console
    indicating that the bot is ready.
    """
    # Set the bot's activity status to the value of the `status` variable
    await bot.change_presence(activity=status)

    # Print a message to the console indicating that the bot is ready
    print("Bot ready")


# Bot Token
# Set the token variable to the bot token from the environment variables
token = bot.run(os.getenv("BOT_TOKEN"))
# Run the client with the token
bot.run(token)
