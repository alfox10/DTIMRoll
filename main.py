import discord
import os
import random
from wserver import keep_alive
import re

client = discord.Client()


async def usage(channel):
    usage = "```COME USARE IL TOOL\n\t/roll xdY\n\tx e' uguale al numero di dadi che si vuole lanciare\n\tY e' uguale alle facce del dado da lanciare\n\tEsempio:\n\t/roll 3d6\n\tlancia 3 dadi da 6 facce\n\tOpzionale\n\te' possibile aggiungere un modificatore ad ogni lancio attraverso\n\tsimboli matematici + (addizione) e - (sottrazione)\n\tEsempio\n\t/roll 2d10-1\n\tlancia 2 dadi da 10 facce e sottrai ad ogni risultato 1\n```"
    await channel.send(usage)


async def readCommand(command, channel):
    diceList = command.split(" ")
    if len(diceList) > 0:
        for i in len(diceList):
            channel.send(throwDices(diceList[i]))
    else:
        await usage(channel)


async def throwDices(dice):
    reg = re.search('[0-9]+d[0-9]+((\+|\-)[0-9]+){0,1}', str(dice))
    # command validation
    if not reg:
        # invalid dice, cucumber thrown!
        return "```Stai tirando un cetriolo? :cucumber:```"

    diceCount = dice.split("d")[0]
    diceData = dice.split("d")[1]
    result = ""
    for i in range(int(diceCount)):
        if "+" in diceData:
            diceValue = diceData.split("-")[0]
            diceModifier = diceData.split("+")[1]
            baseValue = random.randint(1, int(diceValue))
            finalValue = baseValue + int(diceModifier)
            if finalValue > diceValue:
                finalValue = diceValue
            if finalValue >= diceValue:
                finalValue = str(finalValue) + ":tada:"
            result += str(finalValue) + " (" + str(baseValue) + ")\t"
        elif "-" in diceData:
            diceValue = diceData.split("-")[0]
            diceModifier = diceData.split("-")[1]
            baseValue = random.randint(1, int(diceValue))
            finalValue = baseValue + int(diceModifier)
            if finalValue < 1:
                finalValue = 1
            if finalValue == 1:
                finalValue = str(finalValue) + ":skull:"
            result += str(finalValue) + " (" + str(baseValue) + ")\t"
        else:
            baseValue = random.randint(1, int(diceData[0]))
            finalValue = baseValue
            if finalValue == 1:
                finalValue = str(finalValue) + ":skull:"
            if finalValue >= diceValue:
                finalValue = str(finalValue) + ":tada:"
            result += finalValue + "\t"
    return "``` d" + diceData + ": " + result + "```"


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/roll '):
        cleanMessage = message.content.substr(0, 5)
        await readCommand(cleanMessage, message.channel)


keep_alive()
client.run(os.getenv('TOKEN'))
