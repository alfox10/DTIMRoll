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


async def readRollCommand(command, channel):
    global author
    # divide dice commands
    diceList = command.split(" ")
    if len(diceList) > 0:
        message = author
        for i in range(len(diceList)):
            # print dice throw results
            message += "\n" + throwDices(diceList[i])
        await channel.send(message)
    else:
        await usage(channel)


def validateDiceCommand(count, data):
    global author
    if int(count) == 0:
        # invalid dice count
        return "Scusa, non tiro!"
    if int(data.split("+")[0].split("-")[0]) == 0:
        return "Nessuno sa dove sia il leggendario d0..."
    if int(data.split("+")[0].split("-")[0]) == 1:
        return "Come si tira un punto?!"
    return None


def throwDices(dice):
    global author
    reg = re.search('[0-9]*(d|D)[0-9]+((\+|\-)[0-9]+){0,1}', str(dice))
    # command validation
    if not reg:
        # invalid dice, cucumber thrown!
        return "Stai tirando un cetriolo? :cucumber:"

    diceCount = dice.split("d")[0]
    if diceCount == "":
        diceCount = "1"
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
            result += str(finalValue) + " (" + str(baseValue) + ")\t"
        # no modifier
        else:
            # dice throw
            baseValue = random.randint(1, int(diceData))
            finalValue = baseValue
            result += str(finalValue) + "\t"
    return "```d" + diceData + ":   " + result + "```"


async def reroll(message):
    global author
    async for m in message.channel.history(limit=20):
        if m.author == message.author:
            if m.content.startswith('/roll'):
                cleanMessage = m.content[6:]
                await readRollCommand(cleanMessage, m.channel)
                break
    await message.channel.send(str(author)+" non riesco a recuperare i tuoi tiri, usa /roll per questa volta")


async def readTossCommand(command, channel):
    message = channel.send(str(author))
    message += "\n" + tossCoins(command)
    await channel.send(message)


def tossCoins(coin):
    result = ""
    for i in range(int(coin)):
        toss = random.randint(1, 2)
        if toss == 1:
            result += "testa" + "\t"
        if toss == 2:
            result += "croce" + "\t"
    return "```" + result + "```"


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global author
    author = "<@" + str(message.author.id) + ">"

    if message.author == client.user:
        return

    if message.content == '/reroll':
        await reroll(message)
        return

    if message.content.startswith('/roll '):
        cleanMessage = message.content[6:]
        await readRollCommand(cleanMessage, message.channel)

    if message.content.startswith('/toss'):
        cleanMessage = message.content[6:]
        await readTossCommand(cleanMessage, message.channel)


keep_alive()
client.run(os.getenv('TOKEN'))
