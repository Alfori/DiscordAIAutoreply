import discord
from discord.ext import tasks
import asyncio
import random
import logging
import os
import schedule
import time

# user token
myToken = 'YourTokenHere' # enter your user token here so it can log into your account ################# FILL IN TOKEN HERE ###############

if myToken is None:
    raise ValueError("Token not set!")
# replace channel ID with who you want to send it to
myChannelID = 1324  # enter channel id you want to send to ############################################# FILL IN CHANNEL ID HERE ############### 

logging.basicConfig(level=logging.INFO)
morning_message_sent = False
client = discord.Client()

phrases = [  # you can change the phrases it replies, planning on incorporating an AI bot to reply for you where you can include how you type/speech patterns (maybe even voice for voicenotes in the future using a sampled version of my voice).
    "Interesting",
    "I get what you mean",
    "That makes sense",
    "I didn't consider that tbh",
    "I appreciate it",
    "I'll keep that in mind",
    "I get where you're coming from",
    "Let's explore it more"
]

@client.event
async def on_message(message):
    global morning_message_sent

    if message.author == client.user:
        return
    
    if message.channel.id in [myChannelID] and not morning_message_sent:
        try:
            waitTime = random.randint(5, 20)
            logging.info(f"Waiting for {waitTime} seconds before replying")

            for remaining in range(waitTime, 0, -1):
                logging.info(f"Time left: {remaining} seconds")
                await asyncio.sleep(1)
            
            # determine if the bot should reply or just send a message
            if random.randint(2, 5) == 1:  # 2/5 chance to reply
                reply = random.choice(phrases)
                await message.reply(reply)
                logging.info(f"Replied to {message.author} with: {reply}")
            else:  # 3/5 chance to just send a message
                random_message = random.choice(phrases)
                await message.channel.send(random_message)
                logging.info(f"Sent a message to {message.author} in the channel: {random_message}")

            morning_message_sent = True
        except Exception as e:
            logging.error(f"Error processing this message: {e}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    schedule.every().day.at("11:41").do(run_scheduled_task)  # schedule message to be sent at 8am
    asyncio.create_task(schedule_runner())

async def schedule_runner():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

async def sendScheduledMessage():
    global morning_message_sent
    myDMs = client.get_channel(myChannelID)

    # send message to myself
    if myDMs:
        await myDMs.send("Good morning!")
        print("Message sent")
        morning_message_sent = False
    else:
        print("Channel not found")

def run_scheduled_task():
    asyncio.create_task(sendScheduledMessage())

# run the bot
client.run(myToken)
