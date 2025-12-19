✅ Features
🛡️ Moderation & Security

Auto-Approve Join Requests
Automatically approves pending join requests for groups and private channels.

Link Filter
Detects and deletes messages containing links (http, https, t.me) from non-admins.

Spam Keyword Filter
Blocks spam using a list of 40+ keywords (crypto, gambling, scams, etc.), including normalized text detection to prevent bypass attempts.

Flood Control
Automatically deletes messages if a user sends more than 3 messages within 10 seconds.

Warning System

Users are warned automatically for violations

5 warnings = automatic ban

📢 Management Tools

Welcome Messages
Sends a custom welcome message once a member is approved.

Advertisement Broadcasting (Owner Only)
Broadcast messages to all groups where the bot is an admin.

User Tagging
Reply to any message with /tag to mention the user using an inline link.

Admin Commands

/warn – Manually add a warning

/unwarn – Remove a warning

🛠 Requirements

Python: 3.10 or higher

Telegram Bot Token (from @BotFather)

Dependencies:

python-telegram-bot[job-queue]

python-dotenv

⚙️ Installation & Setup
1️⃣ Prepare the Environment

Extract the ZIP file and open a terminal/command prompt in the project folder.

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Configure the Bot
Create .env file

Add the following in the root directory:

BOT_TOKEN=your_telegram_bot_token_here

Set Owner ID

Open main.py and update:

OWNER_USER_ID = 123456789


(You can get your Telegram ID from @userinfobot)

4️⃣ Run the Bot
python main.py


You should see:

✅ Bot is running and moderation features are active...

🚀 How to Use
🔹 Group Setup

Add the bot to your Group or Channel

Promote it to Admin with these permissions:

Delete Messages

Ban Users

Invite Users via Link

Enable Join Requests:

Group Settings → Edit → Invite Links

Turn “Approve New Members” ON

🔹 Commands
Command	Description
/post_ad <text>	Broadcast an ad to all managed groups (Owner only)
/tag	Reply to a user to mention them
/warn	Reply to a user to add a warning
/unwarn	Reply to a user to remove a warning
📝 Technical Notes

Persistence
Warning counts are stored in-memory. Restarting the bot resets all warnings.

Admin Immunity
Admins and the group creator are never warned, muted, or moderated.

Auto-Cleanup
Bot warning messages are automatically deleted after 10 seconds to keep chats clean.

