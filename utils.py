import discord
from config import CONFIG

def is_admin(user):
    """Check if user has admin privileges"""
    if isinstance(user, discord.Member):
        return user.name.lower() in ['mygelinabottle', 'cpjdrumgod247']
    return False

def validate_channel(bot, channel_name):
    """Validate and return channel object"""
    # Remove # if present at the start
    channel_name = channel_name.lstrip('#')

    # Search for channel in all guilds bot has access to
    for guild in bot.guilds:
        channel = discord.utils.get(guild.channels, name=channel_name)
        if channel:
            return channel

    return None