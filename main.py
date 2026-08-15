import asyncio
import logging

import twitchio
from twitchio import eventsub
from twitchio.ext import commands

from dotenv import load_dotenv
import os
from database import (initialisedb, loadtokens, inserttokens, updatetokens, loadpointsreward, chatorcommands ,randommedia)

from obs.obsmanager import OBSMANAGER




load_dotenv()

OWNER_ID = os.getenv("OWNER_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_REFRESH = os.getenv("BOT_REFRESH")
BOT_ID = os.getenv("BOT_ID")
BOT_USERNAME = os.getenv("BOT_USERNAME")
CHANNEL = os.getenv("CHANNEL")
CHANNEL_TOKEN = os.getenv("CHANNEL_TOKEN")
CHANNEL_REFRESH = os.getenv("CHANNEL_REFRESH")
SCENE_NAME = os.getenv("SCENENAME")

if CLIENT_ID is None or CLIENT_SECRET is None or BOT_TOKEN is None or BOT_ID is None or BOT_USERNAME is None or CHANNEL is None or OWNER_ID is None or BOT_REFRESH is None or CHANNEL_TOKEN is None or CHANNEL_REFRESH is None or SCENE_NAME is None:
    raise ValueError("Error in .env (MAIN).")




class Bot(commands.Bot):

    def __init__(self):  # We initialise the class.

        super().__init__(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            bot_id=BOT_ID,
            owner_id=OWNER_ID,
            prefix="!"
        )

        self.obsmanager = OBSMANAGER()


    async def setup_hook(self) -> None: #We execute this whilee setup of the bot.
        await self.add_component(Commands())
        print("Setup complete")

        await self.subscribe_websocket(eventsub.ChatMessageSubscription(broadcaster_user_id=CHANNEL, user_id=BOT_ID))

        await self.subscribe_websocket(eventsub.ChannelPointsRedeemAddSubscription(broadcaster_user_id=CHANNEL, token_for=CHANNEL))

        await self.subscribe_websocket(payload=eventsub.ChannelFollowSubscription(broadcaster_user_id=CHANNEL, moderator_user_id=CHANNEL,), as_bot=False, token_for=CHANNEL)

        await self.subscribe_websocket(eventsub.ChannelCheerSubscription(broadcaster_user_id=CHANNEL, token_for=CHANNEL))

        await self.subscribe_websocket(eventsub.ChannelSubscribeSubscription(broadcaster_user_id=CHANNEL, token_for=CHANNEL))


    async def event_ready(self) -> None: #Indicator of succsesfull setup.
        print(f"Logged in as: ", self.user)


    async def event_message(self, message):

        if message.chatter.id == self.bot_id: #Ignore messages from the bot..
            return
        
        print("CHAT:", message)

        chat = chatorcommands(message.text)

        if chat is not None:
            await message.channel.send(chat)

        await self.process_commands(message)#Activate commands(done automatically in TwitchIO method but we are overrriding it).


    async def add_token(self, token: str, refresh: str) -> twitchio.authentication.ValidateTokenPayload:
        response = await super().add_token(token, refresh)
        print("ADD_TOKEN CALLED")

        if response.user_id == BOT_ID:
            updatetokens("bot", token, refresh)

        elif response.user_id == CHANNEL:
            updatetokens("streamer", token, refresh)

        return response


    async def event_custom_redemption_add(self, payload):

        media = loadpointsreward(payload.reward.id) # media (image, sound, video, duration, x, y, width, height, name)

        print(payload.reward.id)

        if media is not None and media[8] == "randommedia":
            media = randommedia()

        if media is None: # Reward not found on DB
            return
        
        if media[0] is not None:
            await self.obsmanager.showimage(SCENE_NAME, media[0], media[3], media[4], media[5], media[6], media[7])

        if media[1] is not None:
            await self.obsmanager.playsoundorvideo(SCENE_NAME, media[1], media[3])

        if media[2] is not None:
            await self.obsmanager.playsoundorvideo(SCENE_NAME, media[2], media[3], media[4], media[5], media[6], media[7], True)
        
        print("Received.")
        print(payload)


    async def event_custom_channel_follow(self, payload):
        print("NEW FOLLOW:", payload)

    async def event_custom_channel_cheer(self, payload):
        print("CHEER:", payload)


    async def event_custom_channel_subscribe(self, payload):
        print("NEW SUB:", payload)




class Commands(commands.Component):

    @commands.command() # Is an label to the method, like a decorator.
    async def hi(self, ctx: commands.Context[Bot]) -> None:
        print("COMMAND FIRED")
        await ctx.reply(f"Hi {ctx.chatter}!")


    @commands.command()
    async def scene(self, ctx):
        print("scene")
        ctx.bot.obsmanager.setscene(SCENE_NAME) # The bot class is passed like a pointer in the context parameter.




if __name__ == "__main__":

    twitchio.utils.setup_logging(level=logging.INFO)

    initialisedb()

    bot_tokens = loadtokens("bot")
    channel_tokens = loadtokens("streamer")

    if bot_tokens is None:
        inserttokens("bot", BOT_TOKEN, BOT_REFRESH)
        bot_tokens = (BOT_TOKEN, BOT_REFRESH)

    if channel_tokens is None:
        inserttokens("streamer", CHANNEL_TOKEN, CHANNEL_REFRESH)
        channel_tokens = (CHANNEL_TOKEN, CHANNEL_REFRESH)


    async def runner() -> None:
        async with Bot() as bot:
            await bot.add_token(bot_tokens[0], bot_tokens[1]) #We input the tokens so TwitchIO can auto-refresh them.
            await bot.add_token(channel_tokens[0], channel_tokens[1])
            await bot.start(load_tokens=False)


    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        print("Shutting down due to KeyboardInterrupt")