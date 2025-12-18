📢 Telegram Auto-Approve & Ads Posting Bot

This Telegram bot is designed to help group and channel owners automatically manage join requests and broadcast advertisements easily.

✅ Features

Automatically approves all pending and future join requests

Works for both groups and channels

Sends a welcome message after approval

Allows only the owner to post ads

Broadcasts ads to all groups/channels where the bot is admin

Lightweight and runs 24/7

No database required

🛠 Requirements

Python 3.10 or higher

A Telegram Bot Token (via BotFather)

⚙️ Installation & Setup
1️⃣ Download the project

Clone the GitHub repository OR

Download the ZIP and extract it

2️⃣ Install dependencies

Open a terminal inside the project folder and run:

pip install -r requirements.txt

3️⃣ Create .env file

Create a file named .env in the project folder and add:

BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN

4️⃣ Set the ad owner (important)

In main.py, update this line with your Telegram user ID:

OWNER_USER_ID = YOUR_TELEGRAM_USER_ID


You can get your Telegram user ID using @userinfobot.

5️⃣ Run the bot
python main.py


You should see:

Bot is running and auto-approving join requests...

🚀 How to Use
🔹 Add the bot to your group/channel

Promote the bot to Admin

Enable:

✅ Post messages

✅ Approve new members

🔹 Enable Join Requests

Turn ON Approve New Members

🔹 Post Ads

Open a private chat with the bot

Send:

/post_ad Your advertisement text here


The bot will automatically post the ad to all groups/channels where it has admin rights.

📝 Notes

Ads can be posted only by the configured owner

The bot must be running continuously for automation to work

Deployment to VPS/cloud can be done if required

📞 Support

For any setup or deployment help, feel free to reach out.