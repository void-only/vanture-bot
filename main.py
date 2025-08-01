import discord
import random
import os
import re
from discord import app_commands
from keep_alive import keep_alive

TRIGGER = "vanture"  # keyword to trigger 8ball-like replies

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

OWNER_ID = 756126826774134876

positive_responses = [
    "Absolutely!", "No doubt about it.", "Yeah, obviously.", "Obviously, duh.",
    "100%.", "For sure!", "Yep.", "You already know it.", "Of course!", "Clearly.",
    "That’s a yes with ✨style✨.", "Mmhmm.", "Facts.", "Obviously, king 👑",
    "You got this.", "Too easy.", "Simple.", "Yessir.", "Yaaas."
]

roast_responses = [
    "Bro what? No 💀", "That’s a fat no, champ.", "Not even close.", "Try again later, maybe.",
    "Don’t count on it.", "LMAO no.", "You wish.", "Stop embarrassing yourself.",
    "That’s wild... but no.", "Not in this universe.", "Hell no 😂", "Nah, be fr.",
    "Imagine thinking that.", "Not today, not ever.", "Pipe dream, buddy.", "You really asked that?"
]

roast_lines = [
    "You're like a cloud. When you disappear, it’s a beautiful day.",
    "You have something on your chin... no, the third one down.",
    "You bring everyone so much joy… when you leave the room.",
    "You're not stupid; you just have bad luck thinking.",
    "You're like a software update at 2 AM—nobody asked for you.",
    "You're the reason the gene pool needs a lifeguard.",
    "You’re the human version of a headache.",
    "If I wanted to hear from someone irrelevant, I’d unmute my toaster."
]

compliment_lines = [
    "You're sharper than a brand-new katana.",
    "You're the type who makes broken things work again—like magic.",
    "You bring main character energy wherever you go.",
    "You’re basically the human version of 'well played'.",
    "Your vibe is 100% rare loot tier.",
    "You're cooler than the other side of the pillow.",
    "You make smart look effortless.",
    "You radiate 'I got this' energy."
]

emojis = ["😈", "👽", "🤖", "✨", "😎", "🙃", "🔥", "🌌", "🎲", "🪐", "💀", "🧠"]

auto_replies = {
    "good morning": ["Good morning, legend ☀️", "Rise and grind 😤", "Mornin', what’s cookin’?"],
    "i’m sad": ["Tough day? You’ll bounce back. 💪", "Sad? Same. But let’s vibe anyway.", "Want a roast or a hug?"],
    "chat is dead": ["Just like your personality, huh?", "Your presence killed it fr.", "It was alive till you typed."],
    "i’m bored": ["Do something chaotic.", "Touch grass or code something idk 😭", "Try screaming into the void."],
    "hello": ["Yo.", "Wassup.", "Hey there.", "Yo. Speak fast, I got things to ignore.", "SYBAU"],
    "hi": ["Heyyy 👋", "Yo.", "Wassup.", "shuddup lil bro"],
    "what's up": ["The sky. And your delusions.", "your mum (jk)", "Not your IQ, that’s for sure."],
    "gm": ["GM! Let’s make chaos today ☕", "Mornin'. Don’t forget to slay."],
    "yo": ["YO! 🔥", "Wagwan.", "sybau"],
    "good night": ["Nighty night 😴", "Sleep well, chaotic one.", "no one's gonna reply lil bro"],
    "bye": ["Bye! Try not to break anything.", "See ya, legend.", "piece off"],
    "i’m tired": ["Go touch some grass kid, what do i do?", "Go recharge. You’ll wake up cooler."],
    "i hate you": ["Get in line. The queue's long bbg."],
    "kys": ["after you m'lady", "NO U", "Ts pmo Sybau"]
}

@client.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    msg = message.content.lower()

    # Use regex for strict phrase matching with word boundaries
    for phrase, replies in auto_replies.items():
        if re.search(rf"\b{re.escape(phrase)}\b", msg):
            await message.channel.typing()
            await message.reply(random.choice(replies))
            return

    # "vanture" command (8ball-style)
    if msg.startswith(TRIGGER):
        question = message.content[len(TRIGGER):].strip()
        if not question:
            await message.reply("Ask something after the keyword, bro 🤔")
            return

        await message.channel.typing()
        answer = random.choice(positive_responses + roast_responses)
        emoji = random.choice(emojis)
        await message.reply(f"{emoji} {answer}")
        return

# --- SLASH COMMANDS ---

@tree.command(name="roast", description="Roast a member")
@app_commands.describe(user="The member to roast")
async def roast_command(interaction: discord.Interaction, user: discord.Member):
    burn = random.choice(roast_lines)
    await interaction.response.send_message(f"{user.mention}, {burn}")

@tree.command(name="compliment", description="Compliment a member")
@app_commands.describe(user="The member to compliment")
async def compliment_command(interaction: discord.Interaction, user: discord.Member):
    praise = random.choice(compliment_lines)
    await interaction.response.send_message(f"{user.mention}, {praise}")

@tree.command(name="pfp", description="Get a user's profile picture")
@app_commands.describe(user="The member whose profile picture you want (leave blank for yourself)")
async def pfp_command(interaction: discord.Interaction, user: discord.Member = None):
    user = user or interaction.user
    embed = discord.Embed(title=f"{user.name}'s Profile Pic", color=discord.Color.blue())
    embed.set_image(url=user.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@tree.command(name="active", description="Trigger Active Developer Badge (if eligible)")
async def active_command(interaction: discord.Interaction):
    if interaction.user.id == OWNER_ID:
        await interaction.response.send_message("**Active Developer Badge triggered.** If you're eligible, you’ll get it soon. 🔥")
    else:
        await interaction.response.send_message("You’re not allowed to use this, lil bro 💀", ephemeral=True)

# Run the bot
keep_alive()
client.run(os.getenv("bot_token"))
