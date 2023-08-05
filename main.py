import os
import discord
from discord.ext import commands

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Print when Logged In
@bot.event
async def on_ready():
	print(f"Logged in as {bot.user}")

# Command: Ping
@bot.command()
async def ping(ctx):
	await ctx.send('pong')
	
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

@bot.command(name="sendban", description="Send an embed message with a ban button")
async def send_ban(ctx, name: str, userid: int):
	embed = discord.Embed(title="Ban User", description=f"Are you sure you want to ban {name}?", color=discord.Color.red())

	view = View()

	async def ban_button_callback(button, interaction):
		await interaction.response.send_message("User banned.", ephemeral=True)
		await interaction.user.ban(reason="Banned through bot command")

	ban_button = Button(label="Ban", custom_id="ban_button")
	ban_button.callback = ban_button_callback
	view.add_item(ban_button)

	await ctx.send(embed=embed, view=view)
		
bot.run(os.environ["DISCORD_TOKEN"])