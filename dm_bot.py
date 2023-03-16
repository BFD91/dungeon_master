import discord

from dm import DM, roll

import discord

dm = DM()
print("Initializing DM")
dm.initialize_dm()


async def send_message(message, to_send, is_private=False):
    try:
        response = to_send
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = "MTA3OTEwMTU1MDIzMzkxMTM1Nw.Ggf0IO.co5YCgwQIWzza5G2pK6yrr0fz39xE1vRX30rgc"
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author.name)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} in {channel}: {user_message}")

        if user_message[0] == "?":
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await run_game_step(message, user_message, is_private=False)

    client.run(TOKEN)


async def run_game_step(message, user_message, is_private=False, dm=dm):
    player_input = user_message
    if player_input == "/play":
        print("Initializing DM...")
        if len(dm.introduction) > 2000:
            await send_message(message, dm.introduction[:2000], is_private=False)
            await send_message(message, dm.introduction[2000:], is_private=False)
        await send_message(message, dm.introduction, is_private=False)
        dm.history.append({"source": "output", "text": dm.introduction})
        output = dm.run_dm_step("I look around and take in my surroundings.")
        await send_message(message, output, is_private=False)
        dm.history.append({"source": "output", "text": output})
        pass
    if player_input.startswith("/roll "):
        roll_input = player_input.split("/roll ")[1]
        roll_output = roll(roll_input)
        player_input = f"I roll a {roll_output}."

    output = dm.run_dm_step(user_message)
    await send_message(message, output, is_private=False)
    dm.history.append({"source": "output", "text": output})


print("Running Discord bot")
run_discord_bot()
