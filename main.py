import discord
from discord.ext import commands
from discord import app_commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

yes_no_responses = [
    "Absolutely.",
    "Nope.",
    "Yeah, sure…",
    "Not a chance.",
    "Definitely.",
    "Nah.",
    "You already know the answer.",
    "Ask again later.",
    "I'm not sure, honestly.",
    "Sure, why not."
]

emojis = ["😈", "✨", "💀", "🔥", "👀", "😎", "🤖", "🌀", "🚀", "🎯", "🍀"]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="ask", description="Ask a yes or no question")
@app_commands.describe(question="Your question")
async def ask(interaction: discord.Interaction, question: str):
    answer = random.choice(yes_no_responses)
    emoji = random.choice(emojis)
    await interaction.response.send_message(f"{emoji} {answer}")

@bot.tree.command(name="pfp", description="Get someone's profile picture")
@app_commands.describe(member="The member whose avatar you want")
async def pfp(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    await interaction.response.send_message(member.avatar.url)

@bot.tree.command(name="active", description="Developer-only command")
async def active(interaction: discord.Interaction):
    owner_id = interaction.client.application.owner.id if interaction.client.application.owner else None
    if interaction.user.id != owner_id:
        await interaction.response.send_message("You are not the owner of this bot.", ephemeral=True)
        return
    await interaction.response.send_message("🛠️ Developer is active and watching over this bot.")

# Run the bot
if __name__ == "__main__":
    import keep_alive
    keep_alive.keep_alive()
    bot.run(os.getenv("TOKEN"))
