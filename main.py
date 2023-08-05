# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='cfn!', intents=intents)

server1_id = 1102112870583521364
server2_id = 1071613385910792262

@bot.event
async def on_ready():
	print(f"Logged in as {bot.user}")

# Command: Ping
@bot.command()
async def ping(ctx):
	await ctx.send('pong')
	
#Command: Register
#@bot.command()
#

view = discord.ui.View()
item = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Click Me", url="https://google.com")
view.add_item(item=item)
# Command: Broadcast	
@bot.command(pass_context=True)
async def broadcast(ctx, *, msg):
	for guild in bot.guilds:
		for channel in guild.text_channels:
			try:
				print(f"sending message to "+str(channel))
				await channel.send(msg, view=view)
			except Exception:
				continue
			else:
				continue


bot.run(os.environ["DISCORD_TOKEN"])
