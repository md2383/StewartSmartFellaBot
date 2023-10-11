import discord
from discord.ext import commands

from keep_alive import keep_alive

import random
import os

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

think_of = [
    "I be thinking about life", "Honestly got no clue what you just asked",
    "Thinking about deez nuts in that mouf",
    "Thinking about shithow Curtis needs to up his game next episode",
    "Thinking about how MyGel need's to stop yapping", "I be not thinking tbh"
]

greeting = [
    "Yo", "Whats up", "Whats good", "Hello", "Hi", "Howdy", "Hey",
    "what do you want", "shush"
]

bye = [
    "You're leaving?", "You just got here", "Where tf you goin?",
    "I thought we were smart fellas for life why are you leaving???",
    "no plis don go", "please don't", "stay por favor"
]

what = [
    "huh?", "idk", "what are you on abt rn", "wdym what",
    "stop playin you heard me the first time", "quit being dumb",
    "Yo mamma that's what", "what? what? what? That's what you sound like rn",
    "stfu you heard me"
]

confused = [
    "huh?", "tf did you just say?", "idk what you sayin", "blud spewing bs rn",
    "I don't speak whatever it is you're speaking", "No idea what you saying"
]

who = [
    "I'm Stewart Smart Fella", "Name's Fella, Stewart Smart Fella",
    "You know who I am", "You literally refered to me by name"
]

how_doing = [
    "I'm aight", "Would be better if you watched the new podcast episode",
    "I'd tell you but I don't know you",
    "About as good as Ted from Ted 1 was after he found out John Bennet didn't wanna be best friends no more",
    "I'm excited for the next upload", "Chillin"
]

random_yap = [
    "do not care about what you just said, but i do care about watching the Smart Fellas on Youtube (they have me at gunpoint)",
    "thats cool, buuuuut have you seen how fire my new look is?!?!?!?",
    "honestly wasn't paying attention, was too busy listening to the most recent podcast episode",
    "dont care but why am i an apple? honestly who thought this was a good idea?",
    "I would respond to you but ong you mad clapped so imma just ignore you",
    "SHUT UP. Sorry my you got on my nerves a tad"
]

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())


@bot.command()
async def stewartpost(ctx, channel, message):
  try:
    newchannel = discord.utils.get(ctx.guild.channels, id=int(channel[2:-1]))
    await newchannel.send(message)
  except Exception as error:
    print("error: " + str(error))
    await ctx.send("Error: " + str(error))


@bot.command()
async def stewarttest(ctx, arg):
  try:
    await ctx.send(arg)
  except Exception as error:
    print("error: " + str(error))
    await ctx.send("Improper use: /stewarttest [text]")


@bot.event
async def on_ready():
  print(f'{bot.user} has connected to the Discord!')


@bot.event
async def on_message(message):

  trim = message.content.upper()

  if message.author != bot.user and not message.content.startswith("/"):

    if "STEWART" in trim:
      if "THINK OF" in trim:
        ##randomly select a response from think_of
        await message.channel.send(think_of[random.randint(
            0,
            len(think_of) - 1)])
        return
      if "HELLO" in trim or ("HI" in trim and 'CHI' not in trim
        and 'THI' not in trim) or "HEY" in trim or (
        "YO" in trim and 'YOU' not in trim) or "SUP" in trim or (
        ("WHAT" in trim or "WHAT IS") and "UP" in trim):
        await message.channel.send(greeting[random.randint(
            0,
            len(greeting) - 1)])
        return
      if "BYE" in trim:
        await message.channel.send(bye[random.randint(0, len(bye) - 1)])
        return
      if "NEXT EPISODE" in trim or "NEXT VID" in trim:
        await message.channel.send(
            "You gotta either wait or check announcements")
        return
      if "WHATS" in trim or "WHAT IS" in trim:
        await message.channel.send(random_yap[random.randint(
            0,
            len(random_yap) - 1)])
        return
      if "WHAT" in trim:
        await message.channel.send(what[random.randint(0, len(what) - 1)])
        return
      if "WHO" in trim and "YOU" in trim:
        await message.channel.send(who[random.randint(0, len(who) - 1)])
        return
      if ("HOW" in trim and "DOIN" in trim) or "HBU" in trim or (
          ("YOU" in trim or "U" in trim) and
          ("OK" in trim or "GOOD" in trim or "GUD" in trim)) or (
              "HOW" in trim and ("ARE" in trim or "R" in trim) and
              ("YOU" in trim or "U" in trim)) or (
                  "HOW" in trim and ("ABOUT" in trim or "ABT" in trim) and
                  ("YOU" in trim or "U" in trim)):
        await message.channel.send(how_doing[random.randint(
            0,
            len(how_doing) - 1)])
        return
      else:
        if random.randint(0, 1) == 0:
          await message.channel.send(confused[random.randint(
              0,
              len(confused) - 1)])
        else:
          await message.channel.send(random_yap[random.randint(
              0,
              len(random_yap) - 1)])
        return

  if (message.content.startswith("/stewarttest")):
    await stewarttest(message.channel, message.content.split(" ")[1])
    return

  if (message.content.startswith("/stewartpost")):
    await stewartpost(message.channel,
                      message.content.split(" ")[1],
                      message.content.split(" ", 2)[2])
    return

  if (message.content.startswith("/stewarthelp")):
    await message.channel.send(
        "Commands: \n /stewarttest [text] \n /stewartpost [channel] [message] \n /stewarthelp"
    )
    return


my_secret = os.environ['DISCORD_BOT_SECRET']
keep_alive()
bot.run(my_secret)
