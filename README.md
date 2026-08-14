INFO !!!

This is a little project for gaining git, python knowledge amongst other technologies, and to have a "simple" bot for my streams.

This project is published for people who want to:

-Host their own Twitch bot.

-Look through the source code.

-Use it as a starting point for a larger project.

If you don't have programming experience, there are many existing bots with a graphical UI that are considerably easier to configure and use.




This project mainly uses TwitchIO, obs-websocket and SQLite.




This program is capable of:

-Reading chat and executing commands from chat.

-Sub/Cheer/Channelpoints interaction.

-Playing Images/Sounds/Videos obs with size and position customization.

-Storing Commands/Chat keywords , Media info , Tokens on an SQLite database.




        CAUTION !!!

NEVER share your .env file as it contains private information.

The database file is created by the code upon its first run. Before that, create a .env file with this structure (you can create a txt file and rename it .env):


BOT_USERNAME=The Twitch username of the bot account.
BOT_TOKEN=The Twitch access token for the bot account.
BOT_REFRESH=The Twitch refresh token for the bot account.

CLIENT_ID=The Client ID of the Twitch application.
CLIENT_SECRET=The Client Secret of the Twitch application.

CHANNEL=The Twitch user ID of the streamer/channel (CAUTION not username, it needs the number id).
CHANNEL_TOKEN=The Twitch access token for the streamer/channel account.
CHANNEL_REFRESH=The Twitch refresh token for the streamer/channel account.

BOT_ID=The Twitch user ID of the bot account (CAUTION not username, it needs the number id).
OWNER_ID=The Twitch user ID of the bot/application owner (CAUTION not username, it needs the number id).

OBS_HOST=The IP address or hostname of the computer running OBS (if this is all done on the same pc you can put localhost).
OBS_PORT=The WebSocket port used by OBS.
OBS_PASSWORD=The password used to authenticate with the OBS WebSocket server.

SCENENAME=The name of the OBS scene that the bot uses to display media.




        BEFORE SETUP !!!

The SETUP part only concerns the files. There is additional setup needed as for example the .env guide we have before, this applies beside getting the .env info the only thing needed is the creation of a Twitch application (needed for .env), and the setup of the obs WebSocket.

For the obs websocket the options are on Tools -> Websocket Server settings -> Then enable the WebSocket Server and input a port (i reccommend also enabling the authentication and creating a password).


As for the tokens for the bot token i used these scopes:
user:read:chat user:write:chat

And for the channel token i used these scopes:
channel:read:redemptions bits:read channel:read:subscriptions moderator:read:followers moderator:read:chatters channel:manage:redemptions


If you make a Twitch account for the bot (HEAVILY RECOMMENDED) then you must make it moderator in the channel (CHANNEL in .env).




        SETUP !!!

Down here i explain how to set up this for the first time and what you need to do to run it:


(Installation)

Install your python version of choice, for the development of this project i used version 3.11.9 .

Create virtual environment
python -m venv .venv

Activate virtual environment
.venv\Scripts\activate

Install project dependencies
pip install -r requirements.txt

Run the bot
python main.py

Deactivate virtual environment
deactivate


(To run the code)

Activate virtual environment
.venv\Scripts\activate

Run the bot
python main.py

Deactivate virtual environment (after you have shut off the bot)
deactivate




        AFTER SETUP !!!

This code takes most of its information from an SQLite database, which means that a tool to view/change the information is almost needed (You can do it all by programming your own queries), there are tons of free SQLite-compatible database viewers. I used DB Browser for SQLite while developing this program.