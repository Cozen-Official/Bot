import logging
import os
import aiosqlite
import discord
from discord import Client, Interaction, app_commands
from discord.app_commands import Range
from embeds import error_embed, success_embed

os.environ["NIXPACKS_PYTHON_VERSION"] = 3.11

discord.utils.setup_logging()

log = logging.getLogger()


class BanView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @staticmethod
    def get_user_id_from_message(message: discord.Message) -> int | None:
        """Gets the user id from the embed in the message."""

        if not message.embeds:
            return

        embed = message.embeds[0]
        if not embed.fields:
            return

        mention = embed.fields[0].value

        return mention[2:-1]

    @discord.ui.button(label='Ban', style=discord.ButtonStyle.red, custom_id='share_ban')
    async def ban(self, interaction: Interaction, button: discord.ui.Button):
        """Bans the user."""

        user_id = self.get_user_id_from_message(interaction.message)
        if user_id is None:
            return await error_embed(interaction, 'Couldn\'t find the user to ban!')

        try:
            await interaction.guild.ban(discord.Object(id=user_id))
        except discord.Forbidden:
            return await error_embed(interaction, 'I don\'t have permission to ban the user!')

        button.disabled = True
        await interaction.response.edit_message(view=self)

        await success_embed(interaction, 'Successfully banned the user!')


class CustomClient(Client):
    db: aiosqlite.Connection
    tree: app_commands.CommandTree

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        """Sets up the database, syncs the app commands and adds the Ban view."""

        self.db = await aiosqlite.connect('database.db')
        await self.db.execute(
            '''CREATE TABLE IF NOT EXISTS ban_sharing_channels (
                guild_id INT NOT NULL PRIMARY KEY,
                channel_id INT NOT NULL
            )'''
        )
        await self.db.commit()

        await self.tree.sync()

        self.add_view(BanView())

    async def close(self):
        """Closes the database connection and the bot."""

        if hasattr(self, 'db'):
            await self.db.close()

        await super().close()


client = CustomClient()


@client.event
async def on_ready():
    print('-------------------- Bot is ready! --------------------')


@client.tree.error
async def on_app_command_error(interaction: Interaction, error: app_commands.AppCommandError):
    """Error handler."""

    if isinstance(error, app_commands.MissingPermissions):
        return await error_embed(interaction, 'You don\'t have permission to use this command!')

    raise error


async def get_ban_sharing_channel_id(guild_id: int) -> int | None:
    """Gets the ban sharing channel id for the guild."""

    sql = 'SELECT channel_id FROM ban_sharing_channels WHERE guild_id = ?'
    async with client.db.execute(sql, (guild_id,)) as cursor:
        async for row in cursor:
            return row[0]


async def get_ban_sharing_channels() -> list[discord.TextChannel]:
    """Gets all the ban sharing channels across all the discord servers."""

    channels = []

    sql = 'SELECT channel_id FROM ban_sharing_channels'
    async with client.db.execute(sql) as cursor:
        async for row in cursor:
            channel = client.get_channel(row[0])
            if channel is not None:
                channels.append(channel)

    return channels


@client.tree.command(name='setchannel')
@app_commands.default_permissions(administrator=True)
@app_commands.describe(channel='The channel to set as the ban sharing channel')
async def set_channel(interaction: Interaction, channel: discord.TextChannel):
    """Sets the ban sharing channel."""

    if interaction.guild_id is None:
        return await error_embed(interaction, 'You need to use this command in a server!')

    if not channel.permissions_for(interaction.guild.me).send_messages:
        return await error_embed(interaction, f'I need to have permissions to send messages {channel.mention}!')

    channel_id = await get_ban_sharing_channel_id(interaction.guild_id)
    if channel_id is not None:
        await client.db.execute(
            'UPDATE ban_sharing_channels SET channel_id = ? WHERE guild_id = ?',
            (channel.id, interaction.guild_id)
        )
    else:
        await client.db.execute(
            'INSERT INTO ban_sharing_channels VALUES (?, ?)',
            (interaction.guild_id, channel.id)
        )

    await client.db.commit()

    await success_embed(interaction, f'Successfully set {channel.mention} as the ban sharing channel!')


@client.tree.command(name='shareban')
@app_commands.default_permissions(administrator=True)
@app_commands.rename(user_text='user')
@app_commands.describe(
    user_text='The user to shareban (ID or username)',
    reason='The reason of the ban',
    evidence='The evidence of the ban'
)
async def share_ban(
    interaction: Interaction,
    user_text: Range[str, 2, 40],
    reason: Range[str, 1, 1000],
    evidence: discord.Attachment
):
    """Sets the ban sharing channel."""

    if interaction.guild_id is None:
        return await error_embed(interaction, 'You need to use this command in a server!')

    if 'image' not in evidence.content_type:
        return await error_embed(interaction, 'The evidence needs to be an image!')

    user = None
    is_banned = False
    try:
        user = interaction.guild.get_member(int(user_text))
    except ValueError:
        pass

    if user is None:
        user = interaction.guild.get_member_named(user_text)

    if user is None:
        async for entry in interaction.guild.bans():
            entry_text = str(entry.user)
            if entry_text.endswith('#0'):
                entry_text = entry_text[:-2]

            if entry_text.lower() == user_text.lower() or str(entry.user.id) == user_text:
                user = entry.user
                is_banned = True
                break

    if user is None:
        return await error_embed(interaction, f'Cannot find a user with ID or username **{user_text}**!')

    if not is_banned:
        try:
            await interaction.guild.ban(user, reason=reason)
        except discord.Forbidden:
            return await error_embed(interaction, f'I don\'t have permission to ban {user.mention}!')

    await success_embed(interaction, 'Successfully shared the ban!')

    embed = discord.Embed(title='Shared Ban', color=discord.Color.blue())
    embed.set_thumbnail(url=user.avatar.url)
    embed.set_image(url=evidence.url)
    embed.add_field(name='User', value=user.mention)
    embed.add_field(name='Member Status', value='-')
    embed.add_field(name='Ban Reason', value=reason)
    embed.add_field(name='Reporting User', value=interaction.user.mention)
    embed.add_field(name='Reporting Server', value=interaction.guild.name)

    for channel in await get_ban_sharing_channels():
        is_member = channel.guild.get_member(user.id) is not None
        embed.set_field_at(
            1,
            name='Member Status',
            value='In the server' if is_member else 'Not in the server'
        )

        try:
            await channel.send(embed=embed, view=BanView())
        except discord.Forbidden:
            pass


client.run(os.environ["DISCORD_TOKEN"], log_handler=None)
