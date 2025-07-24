import discord
import random
import os
from discord import app_commands
from keep_alive import keep_alive

TRIGGER = "vanture"
OWNER_ID = 756126826774134876

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Cooldowns and Authorization
cooldowns = {}
allowed_channel_ids = set()
allowed_role_ids = set()

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

def is_authorized(ctx):
    if ctx.channel.id not in allowed_channel_ids:
        return False
    if any(role.id in allowed_role_ids for role in ctx.user.roles):
        return True
    return False if allowed_role_ids else True  # if no roles set, allow by channel

def on_cooldown(user_id):
    return user_id in cooldowns and cooldowns[user_id] > discord.utils.utcnow().timestamp()

def set_cooldown(user_id, seconds=3):
    cooldowns[user_id] = discord.utils.utcnow().timestamp() + seconds

@client.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if not is_authorized(message):
        return

    if on_cooldown(message.author.id):
        return
    set_cooldown(message.author.id)

    msg = message.content.lower()

    for phrase, replies in auto_replies.items():
        if phrase in msg:
            await message.channel.typing()
            await message.reply(random.choice(replies))
            return

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

    if message.content.startswith("/pfp"):
        await message.channel.typing()
        user = message.mentions[0] if message.mentions else message.author
        embed = discord.Embed(title=f"{user.name}'s Profile Pic", color=discord.Color.blue())
        embed.set_image(url=user.display_avatar.url)
        await message.reply(embed=embed)
        return

    if message.content.startswith("/roast"):
        if message.mentions:
            user = message.mentions[0]
            await message.channel.typing()
            await message.reply(f"{user.mention}, {random.choice(roast_lines)}")
        else:
            await message.reply("Mention someone to roast them 🔥")
        return

    if message.content.startswith("/compliment"):
        if message.mentions:
            user = message.mentions[0]
            await message.channel.typing()
            await message.reply(f"{user.mention}, {random.choice(compliment_lines)}")
        else:
            await message.reply("Mention someone to compliment them ✨")
        return

@tree.command(name="active", description="Trigger Active Developer Badge (if eligible)")
async def active_command(interaction: discord.Interaction):
    if interaction.user.id == OWNER_ID:
        await interaction.response.send_message("**Active Developer Badge triggered.** If you're eligible, you’ll get it soon. 🔥")
    else:
        await interaction.response.send_message("You’re not allowed to use this, lil bro 💀", ephemeral=True)

@tree.command(name="setauth", description="Set allowed channels and roles for bot responses (owner only)")
@app_commands.describe(channel="Channel to allow", role="Role to allow")
async def setauth(interaction: discord.Interaction, channel: discord.TextChannel = None, role: discord.Role = None):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("Only the bot owner can use this 🔒", ephemeral=True)
        return

    if channel:
        allowed_channel_ids.add(channel.id)
    if role:
        allowed_role_ids.add(role.id)

    msg = f"✅ Updated auth:\n"
    if channel:
        msg += f"- Allowed channel: {channel.mention}\n"
    if role:
        msg += f"- Allowed role: {role.mention}"
    await interaction.response.send_message(msg)

@tree.command(name="clearauth", description="Clear allowed channels and roles (owner only)")
async def clearauth(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("Only the bot owner can use this 🔒", ephemeral=True)
        return
    allowed_channel_ids.clear()
    allowed_role_ids.clear()
    await interaction.response.send_message("❌ Cleared all channel and role restrictions.")

keep_alive()
client.run(os.getenv("bot_token"))
