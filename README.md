INFO !!!

This is a little project for gaining git, python and SQLite knowledge amongst other technologies, and to have a "simple" bot for my streams.

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

-Storing Commands/Chat keywords , Media info , Tokens in an SQLite database.




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


BOT_TOKEN, BOT_REFRESH, CHANNEL_TOKEN, CHANNEL_REFRESH get loaded into the database and future tokens will be stored in the database. So PLEASE, in case you need to delete the database, change these values in .env to the current values stored in the database, as .env holds the last values you wrote, not necessarily the current valid tokens.




        TAKE INTO ACCOUNT BEFORE SETUP !!!

The SETUP part only concerns the files. There is additional setup needed, such as the .env setup explained above. Besides getting the .env information, the only things needed are the creation of a Twitch application (needed for .env) and the setup of the OBS WebSocket.

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

Deactivate virtual environment
deactivate


(To run the code) CAUTION: you need to complete the AFTER SETUP section to be able to run the code

Activate virtual environment
.venv\Scripts\activate

Run the bot
python main.py

Deactivate virtual environment (after you have shut off the bot)
deactivate




        AFTER SETUP !!!

This part contains the information on the files not created by the SETUP process.

The file structure is (inside the folder you have created the virtual environment, NOT the virtual environment folder):

.env
main.py
database.db (created automatically by main.py & database.py)
database.py
obs/
├── obs.py
├── obsmanager.py
├── images/
├── sounds/
└── videos/

This code takes most of its information from an SQLite database, which means that a tool to view/change the information is needed (or you can do it all by programming your own queries), there are tons of free SQLite-compatible database viewers. I used DB Browser for SQLite while developing this program.