import discord
import random
import os
from keep_alive import keep_alive

TRIGGER = "vanture"  # change this to anything you want

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

responses = [
    "Absolutely!", "Not really...", "Yeah, sure", "Doubtful 🤨", "Totally!", "No way!",
    "Maybe.", "Of course!", "Nuh uh.", "You wish.", "For sure!", "Unlikely."
]

emojis = ["😈", "👽", "🤖", "✨", "😎", "🙃", "🔥", "🌌", "🎲", "🪐"]

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.lower().startswith(TRIGGER):
        question = message.content[len(TRIGGER):].strip()

        if not question:
            await message.reply("Ask something after the keyword, bro 🤔")
            return

        answer = random.choice(responses)
        emoji = random.choice(emojis)

        reply = f"{emoji} **You asked:** {question}\n**Answer:** {answer}"
        await message.reply(reply)

keep_alive()
client.run(os.getenv("bot_token"))
