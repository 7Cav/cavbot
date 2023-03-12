# CavBot

General Discord Bot for =7Cav=

<hr>

## Set up .env file

<hr>

To use this script, you will need to set the following environment variables in a .env file:

- MESSAGE_IDS: A comma-separated list of message IDs to search for
- BOT_TOKEN: The API token for your Discord bot
- GUILD_ID: The ID of the Discord guild the bot will operate in
- PTERO_API: The API token for your Pterodactyl panel
- SERVERS: A comma-separated list of ptero server IDs to send commands to

To set these variables, create a file named .env in the root directory of this project and add the following lines:

MESSAGE_IDS=<insert message IDs here>
BOT_TOKEN=<insert bot token here>
GUILD_ID=<insert guild ID here>
PTERO_API=<insert Pterodactyl API token here>
SERVERS=<insert server IDs here>

Make sure to replace <insert ... here> with the appropriate values for your use case. For more information, see the README.md file in this repository.

<hr>

## Requirements

<hr>

See `requirements.txt` for requirements
