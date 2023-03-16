import os

import discord
from discord.ext import commands, tasks
from discord.ext.commands import cog_ext


class react_roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.update_role(payload, True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.update_role(payload, False)

    async def update_role(self, payload, add_role):
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
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

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


def setup(bot):
    bot.add_cog(react_roles(bot))
