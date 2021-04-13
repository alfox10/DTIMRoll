import discord
import os
import random
from wserver import keep_alive
import re

client = discord.Client()


async def usage(message):
    usage = "```COME USARE IL TOOL\n\t/roll xdY\n\tx e' uguale al numero di dadi che si vuole lanciare\n\tY e' uguale alle facce del dado da lanciare\n\tEsempio:\n\t/roll 3d6\n\tlancia 3 dadi da 6 facce\n\tOpzionale\n\te' possibile aggiungere un modificatore ad ogni lancio attraverso\n\tsimboli matematici + (addizione) e - (sottrazione)\n\tEsempio\n\t/roll 2d10-1\n\tlancia 2 dadi da 10 facce e sottrai ad ogni risultato 1\n```"
    await message.channel.send(usage)


async def randomize(message):
    userText = message.content
    splitSpace = userText.split(" ", 1)
    if len(splitSpace) == 2:
        reg = re.search('[0-9]+d[0-9]+((\+|\-)[0-9]+){0,1}', str(splitSpace[1]))
        if not reg:
          await message.channel.send("```Testo non valido```")
          return
        diceData = str(splitSpace[1]).split("d")
        if len(diceData) == 2:
          result = ""
          for i in range(int(diceData[0].strip())):
            if "+" in diceData[1]:
                diceValues = str(diceData[1]).split("+")
                x = random.randint(1, int(diceValues[0].strip()))
                sum = x + int(diceValues[1].strip())
                result += str(x) + " + " + str(diceValues[1]) + " = " + str(sum)+"\n"
            elif "-" in diceData[1]:
              diceValues = str(diceData[1]).split("-")
              x = random.randint(1, int(diceValues[0].strip()))
              sum = x - int(diceValues[1])
              result +=str(x) + " - " + str(diceValues[1]) + " = " + str(sum)+"\n"
            elif diceData[1].strip().isdecimal():
              x = random.randint(1, int(diceData[1].strip()))
              result += str(x)+"\t"
            else:
              await usage(message)
              break
          await message.channel.send("```"+result+"```")
        else:
            await usage(message)
    else:
        await usage(message)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/roll'):
        await randomize(message)


keep_alive()
client.run(os.getenv('TOKEN'))
