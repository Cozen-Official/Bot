from discord import Embed, TextChannel, VoiceChannel, Interaction, Message, Member, User
from discord.ext.commands import Context

__all__ = (
    'error_embed',
    'success_embed'
)

ValidContext = Context | TextChannel | VoiceChannel | Member | User | Interaction | Message


async def error_embed(ctx: ValidContext, text: str, delete_after: int | None = 60, **kwargs) -> Message | None:
    """Sends an error embed."""

    embed = Embed(color=0xeb4034, description=f'❌ {text}')

    if isinstance(ctx, Context):
        return await ctx.message.reply(embed=embed, delete_after=delete_after, **kwargs)

    if isinstance(ctx, Interaction):
        if not ctx.response.is_done():
            return await ctx.response.send_message(embed=embed, ephemeral=True, **kwargs)
        else:
            return await ctx.followup.send(embed=embed, ephemeral=True, **kwargs)

    if isinstance(ctx, Message):
        return await ctx.reply(embed=embed, delete_after=delete_after, **kwargs)

    return await ctx.send(embed=embed, delete_after=delete_after, **kwargs)


async def success_embed(ctx: ValidContext, text: str, delete_after: int | None = 60, **kwargs) -> Message | None:
    """Sends a success embed."""

    embed = Embed(color=0x32a852, description=f'✅ {text}')

    if isinstance(ctx, Context):
        return await ctx.message.reply(embed=embed, delete_after=delete_after, **kwargs)

    if isinstance(ctx, Interaction):
        if not ctx.response.is_done():
            return await ctx.response.send_message(embed=embed, ephemeral=True, **kwargs)
        else:
            return await ctx.followup.send(embed=embed, ephemeral=True, **kwargs)

    if isinstance(ctx, Message):
        return await ctx.reply(embed=embed, delete_after=delete_after, **kwargs)

    return await ctx.send(embed=embed, delete_after=delete_after, **kwargs)
