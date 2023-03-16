import discord

from responses import get_response


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


def run_game_step(message, user_message, is_private=False):
    if user_message == "/play":
        dm = DM()
        print("Initializing DM...")
        dm.initialize_dm()
        export_output(self.introduction)
        self.history.append({"source": "output", "text": self.introduction})
        output = self.run_dm_step("I look around and take in my surroundings.")
        export_output(output)
        self.history.append({"source": "output", "text": output})
    elif user_message == "quit":
        # Quit the game
        pass
    else:
        # Run the game
        pass