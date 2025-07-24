import discord
import random
import os
import asyncio  # For sleep
from keep_alive import keep_alive

TRIGGER = "vanture"  # Trigger word

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

positive_responses = [
    "Obviously.", "No doubt.", "Yep.", "100%", "Absolutely.", "For sure.", "Clearly.", "It was meant to be.", "Without a doubt."
]

negative_responses = [
    "LMAO no.", "In your dreams, loser.", "You wish 💀", "Bro, chill.", "Yeah... not happening.", "As if.", "Delulu alert 🚨", "Keep coping.", "You're funny."
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
            await message.channel.send("Ask something after the keyword, bro 🤔")
            return

        # Choose response
        if random.random() < 0.5:
            answer = random.choice(positive_responses)
        else:
            answer = random.choice(negative_responses)

        emoji = random.choice(emojis)
        reply = f"{emoji} {answer}"

        # Add typing effect for 1.5 seconds
        async with message.channel.typing():
            await asyncio.sleep(1.5)
            await message.channel.send(reply)

keep_alive()
client.run(os.getenv("bot_token"))
