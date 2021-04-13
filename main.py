import discord
import os
import random
from wserver import keep_alive

client = discord.Client()

async def usage(message):
  usage = "```COME USARE IL TOOL\n\t/roll xdY\n\tx e' uguale al numero di dadi che si vuole lanciare\n\tY e' uguale alle facce del dado da lanciare\n\tEsempio:\n\t/roll 3d6\n\tlancia 3 dadi da 6 facce\n\tOpzionale\n\te' possibile aggiungere un modificatore ad ogni lancio attraverso\n\tsimboli matematici + (addizione) e - (sottrazione)\n\tEsempio\n\t/roll 2d10-1\n\tlancia 2 dadi da 10 facce e sottrai ad ogni risultato 1\n```"
  await message.channel.send(usage)
	
async def randomize(message):
	userText=message.content
	splitSpace = userText.split(" ",1)
	if len(splitSpace) == 2:
		diceData = str(splitSpace[1]).split("d")
		if len(diceData) == 2:
			for i in range(int(diceData[0].strip())):
				if "+" in diceData[1]:
					diceValues = str(diceData[1]).split("+")
					x = random.randint(1, int(diceValues[0].strip()))
					sum = x + int(diceValues[1].strip())
					await message.channel.send(str(x) + " + " + str(diceValues[1]) + " = " + str(sum))
				elif "-" in diceData[1]:
					diceValues = str(diceData[1]).split("-")
					x = random.randint(1, int(diceValues[0].strip()))
					sum = x - int(diceValues[1])
					await message.channel.send(str(x) + " - " + str(diceValues[1]) + " = " + str(sum))
				elif diceData[1].strip().isdecimal():
					x = random.randint(1, int(diceData[1].strip()))
					await message.channel.send(x)
				else:
					await usage(message)
					break
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