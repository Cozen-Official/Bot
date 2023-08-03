# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='cfn', intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Command: Ping
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

# Command: Share ban
@bot.command()
async def shareban(ctx, user_id: int, reason: str):
    # Get the member object for the given user ID
    member = bot.get_user(user_id)

    if not member:
        await ctx.send("User not found.")
        return

    # Share the ban to both servers
    server1 = bot.get_guild(server1_id)
    server2 = bot.get_guild(server2_id)

    if server1 and server2:
        # Ban the user on both servers
        await server1.ban(member, reason=reason)
        await server2.ban(member, reason=reason)
        await ctx.send(f"{member.mention} has been banned on both servers for: {reason}")
    else:
        await ctx.send("Could not find both servers.")


bot.run(os.environ["DISCORD_TOKEN"])
