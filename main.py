import os
import re
import time
import json
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    ContextTypes,
    CommandHandler,
    ChatMemberHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(level=logging.WARNING)

USER_WARNINGS = {}
MAX_WARNINGS = 5
USER_MESSAGE_LOG = {}
FLOOD_THRESHOLD = 3
FLOOD_WINDOW = 10
OWNER_IDS = {8565631938, 6546783150}
CHATS_FILE = "chats.json"
AD_TARGET_CHATS = set()

def load_chats():
    global AD_TARGET_CHATS
    if os.path.exists(CHATS_FILE):
        try:
            with open(CHATS_FILE, "r") as f:
                AD_TARGET_CHATS = set(json.load(f))
        except:
            AD_TARGET_CHATS = set()

def save_chats():
    try:
        with open(CHATS_FILE, "w") as f:
            json.dump(list(AD_TARGET_CHATS), f)
    except Exception as e:
        logging.error(f"Save Error: {e}")

SPAM_KEYWORDS = [
    # Crypto & Scams
    "crypto", "bitcoin", "eth ", "btc ", "tether", "binance", "pump", "doubling",
    "mining", "forex", "trading signal", "investment", "passive income", "profit",
    "return on investment", "wallet", "seed phrase", "airdrop", "presale", "token",
    "earn money", "work from home", "salary", "hiring", "job offer", "remote work",
    "payment", "fast cash", "free money", "get rich", "financial freedom", "commission",
    "casino", "slots", "betting", "poker", "jackpot", "lottery", "winner", "prize",
    "official support", "admin support", "kyc verification", "claim now", "gift",
    "premium for free", "account hacked", "security alert", "verify your account",
    "dm me", "contact me", "check bio", "join channel", "click here", "limited offer",
    "whatsapp", "telegram.me", "t.me/", "fast profit", "guaranteed",

    # Vulgar & Adult Content
    "sex", "sexy", "pussy", "hot videos", "porn", "xxx", "nude",
    "18+", "nsfw", "adult", "uncensored", "leaked", "private tape",
    "dick", "cock", "boobs", "tits", "breast", "ass", "booty", "butt",
    "vagina", "clit", "cum", "squirt", "orgasm", "masturbate", "horny",
    "slut", "whore", "bitch", "fuck", "motherfucker",
    "hot girl", "cam girl", "live show", "dating", "hookup", "meetup",
    "incest", "milf", "teen sex", "hentai", "anime sex",
    "onlyfans", "fansly", "brazzers", "pornhub", "xvideos",
    "strip", "naked", "topless", "upskirt",
    "blowjob", "handjob", "anal", "deepthroat", "creampie",
    "erotic", "sensual", "kamasutra",
    "escort", "call girl", "massage happy ending",
    "viagra", "cialis", "enlarge"
]

async def delete_warning_message(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    try:
        await context.bot.delete_message(chat_id=job.data["chat_id"], message_id=job.data["message_id"])
    except:
        pass

async def approve_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.chat_join_request.approve()
        await context.bot.send_message(chat_id=update.chat_join_request.chat.id)
    except Exception as e:
        logging.error(f"Join Request Error: {e}")

async def track_bot_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.my_chat_member.chat
    status = update.my_chat_member.new_chat_member.status
    if status in ("administrator", "creator"):
        AD_TARGET_CHATS.add(chat.id)
        save_chats()
    elif status in ("left", "kicked"):
        AD_TARGET_CHATS.discard(chat.id)
        save_chats()

async def post_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private" or update.effective_user.id not in OWNER_IDS:
        return
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /post_ad <message>")
        return
    ad_text, sent, failed = " ".join(context.args), 0, 0
    for chat_id in AD_TARGET_CHATS:
        try:
            await context.bot.send_message(chat_id=chat_id, text=ad_text)
            sent += 1
        except:
            failed += 1
    await update.message.reply_text(f"📢 Broadcast: {sent} sent, {failed} failed.")

async def tag_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply to a message.")
        return
    user = update.message.reply_to_message.from_user
    await update.message.reply_text(f"🔔 Attention <a href='tg://user?id={user.id}'>{user.first_name}</a>", parse_mode="HTML")

async def add_warning(update: Update, context: ContextTypes.DEFAULT_TYPE, reason: str = "Rule violation"):
    user, chat = update.effective_user, update.effective_chat
    USER_WARNINGS[user.id] = USER_WARNINGS.get(user.id, 0) + 1
    count = USER_WARNINGS[user.id]
    if count >= MAX_WARNINGS:
        try:
            await chat.ban_member(user.id)
            await context.bot.send_message(chat.id, f"🚫 {user.mention_html()} banned ({MAX_WARNINGS}/{MAX_WARNINGS} warns).", parse_mode="HTML")
            USER_WARNINGS[user.id] = 0
        except Exception as e:
            logging.error(f"Ban Error: {e}")
    else:
        msg = await context.bot.send_message(chat.id, f"⚠️ {user.mention_html()} warned [{count}/{MAX_WARNINGS}].\nReason: {reason}", parse_mode="HTML")
        if context.job_queue:
            context.job_queue.run_once(delete_warning_message, 10, data={"chat_id": chat.id, "message_id": msg.message_id})

async def flood_control(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    uid, now = update.effective_user.id, time.time()
    chat = update.effective_chat
    member = await chat.get_member(uid)
    if member.status in ["administrator", "creator"]: return False
    
    if uid not in USER_MESSAGE_LOG: USER_MESSAGE_LOG[uid] = []
    USER_MESSAGE_LOG[uid] = [t for t in USER_MESSAGE_LOG[uid] if now - t < FLOOD_WINDOW]
    USER_MESSAGE_LOG[uid].append(now)
    
    if len(USER_MESSAGE_LOG[uid]) > FLOOD_THRESHOLD:
        await update.effective_message.delete()
        if len(USER_MESSAGE_LOG[uid]) == FLOOD_THRESHOLD + 1:
            await add_warning(update, context, "Flooding/Spamming")
        return True
    return False

async def filter_links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    msg, chat, user = update.effective_message, update.effective_chat, update.effective_user
    member = await chat.get_member(user.id)
    if member.status in ["administrator", "creator"]: return False
    
    text = (msg.text or msg.caption or "").lower()
    entities = msg.entities or msg.caption_entities
    has_link = any(e.type in ["url", "text_link"] for e in entities) if entities else False
    if not has_link: has_link = any(x in text for x in ["t.me", "http://", "https://"])
    
    if has_link:
        await msg.delete()
        await add_warning(update, context, "Posting links")
        return True
    return False

async def spam_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    msg, chat, user = update.effective_message, update.effective_chat, update.effective_user
    member = await chat.get_member(user.id)
    if member.status in ["administrator", "creator"]: return False
    
    raw = (msg.text or msg.caption or "").lower()
    norm = re.sub(r'[^a-zA-Z0-9]', '', raw)
    if any(k in raw or k.replace(" ", "") in norm for k in SPAM_KEYWORDS):
        await msg.delete()
        await add_warning(update, context, "Spam keywords")
        return True
    return False

async def global_moderator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]: return
    if await flood_control(update, context): return
    if await filter_links(update, context): return
    await spam_filter(update, context)

async def warn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = await update.effective_chat.get_member(update.effective_user.id)
    if m.status not in ["administrator", "creator"] or not update.message.reply_to_message: return
    update._effective_user = update.message.reply_to_message.from_user
    await add_warning(update, context, "Manual admin warn")

async def unwarn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = await update.effective_chat.get_member(update.effective_user.id)
    if m.status not in ["administrator", "creator"] or not update.message.reply_to_message: return
    target_id = update.message.reply_to_message.from_user.id
    USER_WARNINGS[target_id] = max(0, USER_WARNINGS.get(target_id, 0) - 1)
    await update.message.reply_text(f"✅ Warning removed. Current: {USER_WARNINGS[target_id]}/{MAX_WARNINGS}")

def main():
    load_chats()
    load_dotenv()

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN not found in .env file")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(ChatJoinRequestHandler(approve_join_request))
    app.add_handler(ChatMemberHandler(track_bot_status, ChatMemberHandler.MY_CHAT_MEMBER))

    app.add_handler(CommandHandler("post_ad", post_ad))
    app.add_handler(CommandHandler("tag", tag_user))
    app.add_handler(CommandHandler("warn", warn_command))
    app.add_handler(CommandHandler("unwarn", unwarn_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, global_moderator))

    print("✅ Bot is running and moderation features are active..")
    
    app.run_polling()

if __name__ == "__main__":
    main()