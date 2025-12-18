import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    ContextTypes,
)
from dotenv import load_dotenv

WELCOME_MESSAGE = (
    "👋 Welcome to the group!\n\n"
    "📢 This is our official channel.\n"
    "Stay tuned for updates 🚀"
)


async def approve_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.chat_join_request.approve()

        await context.bot.send_message(
            chat_id=update.chat_join_request.chat.id,
            text=WELCOME_MESSAGE
        )

        print(
            f"✅ Approved join request & sent welcome message to "
            f"{update.chat_join_request.from_user.id}"
        )

    except Exception as e:
        print("❌ Error handling join request:", e)




def main():
    load_dotenv()

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN not found in .env file")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(ChatJoinRequestHandler(approve_join_request))

    print("✅ Bot is running and auto-approving join requests...")
    app.run_polling()

if __name__ == "__main__":
  main()
