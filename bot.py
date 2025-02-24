import discord
from discord.ext import commands
import random
import os
from config import CONFIG
import json
from ai_responses import get_passive_aggressive_response
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('StewartBot')

# Load responses from JSON file
with open('responses.json', 'r') as f:
    RESPONSES = json.load(f)

# Set up bot with slash commands
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

@bot.tree.command(name="stweartbot", description="Repost a message to another channel")
async def stweartbot(interaction: discord.Interaction, channel: str, message: str):
    try:
        # Check if user has admin privileges
        if not any(name.lower() == interaction.user.name.lower() for name in ['mygelinabottle', 'cpjdrumgod247']):
            await interaction.response.send_message(
                "*Rolls eyes* Nice try, but you're not important enough for this command.",
                ephemeral=True
            )
            return

        # Extract channel ID if it's a mention (#channel-name format)
        if channel.startswith('<#') and channel.endswith('>'):
            channel_id = int(channel[2:-1])
            target_channel = interaction.guild.get_channel(channel_id)
        else:
            # Remove # if present at the start
            channel_name = channel.lstrip('#')
            target_channel = discord.utils.get(interaction.guild.channels, name=channel_name)

        if not target_channel:
            await interaction.response.send_message(
                f"*Sighs dramatically* I can't find a channel called {channel}. Did you even check if it exists?",
                ephemeral=True
            )
            return

        # Post the message
        await target_channel.send(message)
        await interaction.response.send_message(
            "Fine, I've reposted your message. Happy now?",
            ephemeral=True
        )
    except Exception as error:
        logger.error(f"Error in stweartbot command: {str(error)}")
        await interaction.response.send_message(f"Error: {str(error)}", ephemeral=True)

@bot.tree.command(name="stwearthelp", description="Shows help for Stewart's commands")
async def stwearthelp(interaction: discord.Interaction):
    help_text = """
*Rolls eyes and recites robotically*
Here are my commands, try to remember them this time:

/stweartbot [channel] [message]
    - Reposts your message to another channel
    - Only works if you're important enough (you know who you are)
    - Example: /stweartbot #announcements Hello everyone!

/stwearthelp
    - Shows this message
    - Though I don't know why you'd need it more than once

You can also just talk to me normally, but don't expect me to always respond...
    """
    await interaction.response.send_message(help_text, ephemeral=True)

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to the Discord!')
    logger.info("Version: YOUR_LATEST_CHANGES now active!")
    # Sync slash commands
    await bot.tree.sync()
    logger.info("Slash commands synced successfully!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Then handle normal messages
    if not message.content.startswith('/'):
        content_lower = message.content.lower()

        if 'stewart' in content_lower:
            # Initialize message_type outside try block
            message_type = None
            logger.info(f"Processing message containing 'stewart': {message.content}")

            try:
                # Determine message type
                if any(phrase in content_lower for phrase in ['where', 'been']):
                    message_type = "whereabouts"
                elif '?' in message.content:
                    message_type = "question"
                elif any(greeting in content_lower for greeting in ['hi', 'hello', 'hey', 'sup']):
                    message_type = "greeting"

                logger.info(f"Detected message_type: {message_type}")

                # Try to get AI response
                response = get_passive_aggressive_response(message.content, message_type)
                logger.info(f"AI Response received: {response}")

                # If AI response is received, use it
                if response:
                    await message.channel.send(response)
                    return

            except Exception as e:
                logger.error(f"Error with AI response: {str(e)}")
                # Fall back to default responses if AI fails
                if message_type == "whereabouts":
                    response = random.choice(RESPONSES['whereabouts'])
                elif message_type == "question":
                    response = random.choice(RESPONSES['questions'])
                elif message_type == "greeting":
                    response = random.choice(RESPONSES['greetings'])
                else:
                    response = random.choice(RESPONSES['general'])

                logger.info(f"Using fallback response: {response}")
                await message.channel.send(response)

# Use CONFIG['token'] instead of environment variable directly
bot.run(CONFIG['token'])