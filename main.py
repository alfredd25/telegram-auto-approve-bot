import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    ContextTypes,
)
from dotenv import load_dotenv

async def approve_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.chat_join_request.approve()
        print(
            f"✅ Approved join request from "
            f"{update.chat_join_request.from_user.id} "
            f"in chat {update.chat_join_request.chat.id}"
        )
    except Exception as e:
        print("❌ Error approving join request:", e)



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
