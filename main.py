import os
from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv

def main():
    load_dotenv()

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN not found in .env file")

    app = ApplicationBuilder().token(token).build()

    print("✅ Bot is running and connected to Telegram...")
    app.run_polling()

if __name__ == "__main__":
    main()
