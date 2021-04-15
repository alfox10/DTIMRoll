import discord
import os
import random
from wserver import keep_alive
import re

client = discord.Client()

author = ""

async def usage(channel):
    usage = "```COME USARE IL TOOL\n\t/roll xdY\n\tx è uguale al numero di dadi che si vuole lanciare\n\tY è uguale alle facce del dado da lanciare\n\tEsempio:\n\t/roll 3d6\n\tlancia 3 dadi da 6 facce\n\tOpzionale\n\tè possibile aggiungere un modificatore ad ogni lancio attraverso\n\tsimboli matematici + (addizione) e - (sottrazione)\n\tEsempio\n\t/roll 2d10-1\n\tlancia 2 dadi da 10 facce e sottrai ad ogni risultato 1\n```"
    await channel.send(usage)


async def readCommand(command, channel):
    # divide dice commands
    diceList = command.split(" ")
    if len(diceList) > 0:
        for i in range(len(diceList)):
            # print dice throw results
            await channel.send(throwDices(diceList[i]))
    else:
        await usage(channel)


def validateDiceCommand(count, data):
    global author
    if int(count) == 0:
        # invalid dice count
        return str(author)+" Scusa, non tiro!"
    if int(data.split("+")[0].split("-")[0]) == 0:
        return str(author)+" Nessuno sa dove sia il leggendario d0..."
    if int(data.split("+")[0].split("-")[0]) == 1:
        return str(author)+" Come si tira un punto?!"
    return None


def throwDices(dice):
    global author
    reg = re.search('[0-9]+d[0-9]+((\+|\-)[0-9]+){0,1}', str(dice))
    # command validation
    if not reg:
        # invalid dice, cucumber thrown!
        return str(author)+" Stai tirando un cetriolo? :cucumber:"

    diceCount = dice.split("d")[0]
    diceData = dice.split("d")[1]

    validation = validateDiceCommand(diceCount, diceData)
    if validation is not None:
        return validation

    result = ""
    for i in range(int(diceCount)):
        # dice data parsing
        diceValue = diceData.split("-")[0]
        diceValue = diceValue.split("+")[0]

        # additive modifier
        if "+" in diceData:
            diceModifier = diceData.split("+")[1]
            # dice throw
            baseValue = random.randint(1, int(diceValue))
            finalValue = baseValue + int(diceModifier)
            # value limiter
            if finalValue > int(diceValue):
                finalValue = int(diceValue)
            # emoji addition
            # if finalValue == int(diceValue):
            #     finalValue = str(finalValue) + " :tada:"
            result += str(finalValue) + " (" + str(baseValue) + ")\t"
        # subtractive modifier
        elif "-" in diceData:
            diceModifier = diceData.split("-")[1]
            # dice throw
            baseValue = random.randint(1, int(diceValue))
            finalValue = baseValue - int(diceModifier)
            # value limiter
            if finalValue < 1:
                finalValue = 1
            # emoji addition
            # if finalValue == 1:
            #     finalValue = str(finalValue) + " :skull:"
            result += str(finalValue) + " (" + str(baseValue) + ")\t"
        # no modifier
        else:
            # dice throw
            baseValue = random.randint(1, int(diceData))
            finalValue = baseValue
            # emoji addition
            # if baseValue == 1:
            #     finalValue = str(baseValue) + " :skull:"
            # if baseValue == int(diceValue):
            #     finalValue = str(baseValue) + " :tada:"
            result += str(finalValue) + "\t"
    return str(author)+" ```d" + diceData + ":   " + result + "```"

async def reroll(message):
  global author
  author = "<@" + str(message.author.id) + ">"
  async for m in message.channel.history(limit=20):
    if m.author == message.author:
        if m.content.startswith('/roll'):
          cleanMessage = m.content[6:]
          await readCommand(cleanMessage, m.channel)
          break
  await message.channel.send(str(author)+" Non riesco a recuperare i tuoi tiri, usa /roll per questa volta")

  

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '/reroll':
        await reroll(message)
        return

    if message.content.startswith('/roll '):
        global author
        author = "<@" + str(message.author.id) + ">"
        cleanMessage = message.content[6:]
        await readCommand(cleanMessage, message.channel)


keep_alive()
client.run(os.getenv('TOKEN'))
