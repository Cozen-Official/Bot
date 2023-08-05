# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='cfn!', intents=intents)
# Initialize the DiscordComponents extension
DiscordComponents(bot)

# Server IDs
server1_id = 1102112870583521364
server2_id = 1071613385910792262

# Print when Logged In
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

# Command: Broadcast	
@bot.command(pass_context=True)
async def broadcast(ctx, *, msg):
	for guild in bot.guilds:
		for channel in guild.text_channels:
			try:
				print(f"sending message to "+str(channel))
				await channel.send(msg)
			except Exception:
				continue
			else:
				continue
				
# Command: Send message with a Google link button
@bot.command()
async def google(ctx):
	# Create a button that links to Google
	google_button = Button(
		label='Go to Google',
		style=ButtonStyle.URL,
		url='https://www.google.com'
	)

	# Send a message with the Google link button
	await ctx.send("Click the button to go to Google:", components=[google_button])


bot.run(os.environ["DISCORD_TOKEN"])
