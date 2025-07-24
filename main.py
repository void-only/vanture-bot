import discord
import random
import os
from keep_alive import keep_alive

TRIGGER = "vanture"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

positive_responses = [
    "Absolutely.", "Definitely.", "For sure.", "You know it.", "Of course.", "Without a doubt."
]

roast_responses = [
    "You wish.", "In your dreams.", "LOL no.", "As if!", "Try again, clown.", "😂 Not happening."
]

positive_gifs = [
    "https://media.giphy.com/media/111ebonMs90YLu/giphy.gif",
    "https://media.giphy.com/media/26BRQTezZrKak4BeE/giphy.gif"
]

roast_gifs = [
    "https://media.giphy.com/media/l3q2K5jinAlChoCLS/giphy.gif",
    "https://media.giphy.com/media/xT9IgG50Fb7Mi0prBC/giphy.gif"
]

emojis = ["😈", "👽", "🤖", "✨", "😎", "🙃", "🔥", "🌌", "🎲", "🪐"]

OWNER_ID = 756126826774134876

@client.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.lower().startswith(TRIGGER):
        await message.channel.typing()

        question = message.content[len(TRIGGER):].strip()
        if not question:
            await message.reply("Ask something after the keyword, bro 🤔")
            return

        is_positive = random.choice([True, False])
        answer = random.choice(positive_responses if is_positive else roast_responses)
        gif = random.choice(positive_gifs if is_positive else roast_gifs)
        color = 0x00ff99 if is_positive else 0xff0055

        embed = discord.Embed(
            title=answer,
            description=f"**{message.author.display_name} asked:** {question}",
            color=color
        )
        embed.set_image(url=gif)

        await message.reply(embed=embed)
        await message.add_reaction(random.choice(emojis))

# ---------------------------------------
# Slash Command: /pfp
# ---------------------------------------

@tree.command(name="pfp", description="Get someone’s profile picture")
async def pfp_command(interaction: discord.Interaction, user: discord.Member = None):
    user = user or interaction.user
    embed = discord.Embed(title=f"{user.display_name}'s Profile Picture", color=0x3498db)
    embed.set_image(url=user.avatar.url if user.avatar else user.default_avatar.url)
    await interaction.response.send_message(embed=embed)

# ---------------------------------------
# Slash Command: /active (Owner Only)
# ---------------------------------------

@tree.command(name="active", description="Get the Active Developer badge")
async def active_command(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("Only the chosen one may access the sacred badge 🧙", ephemeral=True)
        return

    embed = discord.Embed(
        title="🌟 Active Developer",
        description="You are an officially active developer!\nYou deserve the badge 💼✨",
        color=0xf1c40f
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1123903293603319808.png")  # Any icon you like
    await interaction.response.send_message(embed=embed)
