import os

CONFIG = {
    'token': os.environ.get('DISCORD_BOT_TOKEN'),  # Using environment variable
    'admin_roles': ['Admin', 'Moderator'],
    'response_chance': 0.2,  # 20% chance to respond passive-aggressively
}