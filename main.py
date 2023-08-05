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

@bot.command()
async def send_embed(ctx, name: str, user_id: int):
	embed = discord.Embed(
		title=f'User Ban: {name}',
		description=f'Are you sure you want to ban {name}?',
		color=discord.Color.red()
	)

	async def ban_callback(interaction):
		await interaction.response.send_message('Banning user...')
		try:
			user = await bot.fetch_user(user_id)
			await ctx.guild.ban(user, reason='User ban requested')
			await interaction.followup.send_message(f'Successfully banned user {name}')
		except discord.NotFound:
			await interaction.followup.send_message('User not found.')

	action_row = discord.ui.ActionRow(
#	action_row = discord.ActionRow(
		discord.ui.Button(label='Ban User', custom_id='ban_user', style=discord.ButtonStyle.red)
	)

	view = discord.ui.View()
	view.add_item(action_row)

	await ctx.send(embed=embed, view=view)

@bot.event
async def on_button_click(interaction):
	if interaction.custom_id == 'ban_user':
		await interaction.defer()
		await ban_callback(interaction)
		
bot.run(os.environ["DISCORD_TOKEN"])