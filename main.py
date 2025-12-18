import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    ContextTypes,
    CommandHandler,
    ChatMemberHandler,
)

from dotenv import load_dotenv

WELCOME_MESSAGE = (
    "👋 Welcome to the group!\n\n"
    "📢 This is our official channel.\n"
    "Stay tuned for updates 🚀"
)

OWNER_USER_ID = 6092408919

AD_TARGET_CHATS = set()

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



async def track_bot_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.my_chat_member.chat
    new_status = update.my_chat_member.new_chat_member.status

    if new_status in ("administrator", "creator"):
        AD_TARGET_CHATS.add(chat.id)
        print(f"📌 Bot added as admin in chat {chat.id}")

    if new_status in ("left", "kicked"):
        AD_TARGET_CHATS.discard(chat.id)
        print(f"❌ Bot removed from chat {chat.id}")



async def post_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if chat.type != "private":
        return

    if OWNER_USER_ID is not None and user.id != OWNER_USER_ID:
        await update.message.reply_text("❌ You are not authorized to post ads.")
        return


    if not context.args:
        await update.message.reply_text(
            "⚠️ Usage:\n/post_ad Your ad message here"
        )
        return

    ad_text = " ".join(context.args)

    sent = 0
    failed = 0

    for chat_id in AD_TARGET_CHATS:
        try:
            await context.bot.send_message(chat_id=chat_id, text=ad_text)
            sent += 1
        except Exception as e:
            failed += 1
            print(f"❌ Failed to send ad to {chat_id}: {e}")

    await update.message.reply_text(
        f"📢 Ad broadcast completed.\n"
        f"✅ Sent: {sent}\n"
        f"❌ Failed: {failed}"
    )




def main():
    load_dotenv()

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN not found in .env file")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(ChatJoinRequestHandler(approve_join_request))
    app.add_handler(ChatMemberHandler(track_bot_status, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(CommandHandler("post_ad", post_ad))



    print("✅ Bot is running and auto-approving join requests...")
    app.run_polling()

if __name__ == "__main__":
  main()
