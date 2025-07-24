import discord
import random
import os
from keep_alive import keep_alive

TRIGGER = "vanture"  # keyword to trigger text-based command

OWNER_ID = 756126826774134876  # Only you can use the /active command

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

positive_responses = [
    "Obviously.", "Hell yeah.", "Without a doubt.", "For sure.", "Bet.", "Yup.",
    "100%.", "All signs point to yes.", "That's a flex.", "No cap."
]

negative_responses = [
    "Bruh... no.", "Absolutely not.", "Nah fam.", "That's dumb.", "Try again, clown 🤡",
    "What are you even asking?", "L bozo.", "You serious?", "Nuh uh.", "Delete that thought."
]

emojis = ["😈", "👽", "🤖", "✨", "😎", "🙃", "🔥", "🌌", "🎲", "🪐"]

@client.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.lower().startswith(TRIGGER):
        question = message.content[len(TRIGGER):].strip()

        if not question:
            await message.reply("Bro you forgot to ask something 💀")
            return

        await message.channel.typing()

        if random.random() > 0.5:
            answer = random.choice(positive_responses)
        else:
            answer = random.choice(negative_responses)

        emoji = random.choice(emojis)
        reply = f"{emoji} {answer}"
        await message.reply(reply)

# /pfp command
@tree.command(name="pfp", description="Get someone's profile picture")
async def pfp_command(interaction: discord.Interaction, user: discord.User = None):
    user = user or interaction.user
    await interaction.response.send_message(f"🖼️ {user.mention}'s pfp:\n{user.avatar.url}")

# /active command (owner only)
@tree.command(name="active", description="Only the dev can use this")
async def active_command(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("🚫 You're not my dev, back off.", ephemeral=True)
    else:
        await interaction.response.send_message("👨‍💻 Active Developer badge moment.")

keep_alive()
client.run(os.getenv("bot_token"))
