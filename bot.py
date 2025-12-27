import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

# ================== CONFIG ==================
TOKEN = "8142424304:AAHxfvq4scQPUS-j2d6k1pALTu5kFresfZY"   # 👈 BotFather token
API_URL = "https://tobi-tempmail-api.vercel.app/"
CHANNEL_USERNAME = "@Cyber_sagar"  # 👈 channel username
ADMIN_ID = 6076527622               # 👈 tumhara Telegram ID
# ============================================


# 🔒 Force Join Check
def is_joined(update, context):
    user_id = update.effective_user.id
    try:
        member = context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ▶️ /start command
def start(update, context):
    if not is_joined(update, context):
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url="https://t.me/Cyber_sagar")]
        ]
        update.message.reply_text(
            "❌ Pehle hamara channel join karo\n\n"
            "Join karne ke baad /start dobara likho",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    user = update.effective_user
    name = user.first_name
    username = f"@{user.username}" if user.username else "Not set"
    user_id = user.id

    # 📩 ADMIN NOTIFY
    context.bot.send_message(
        ADMIN_ID,
        f"🚀 New User Started Bot\n\n"
        f"👤 Name: {name}\n"
        f"🆔 ID: {user_id}\n"
        f"🏷 Username: {username}"
    )

    # 👋 Welcome
    update.message.reply_text(
        f"👋 Welcome {name}!\n\n"
        f"🆔 Username: {username}\n"
        f"🔢 User ID: {user_id}\n\n"
        f"/email likho aur temporary email pao 📧"
    )

    # 🔘 Buttons
    contact_btn = KeyboardButton("📞 Share Phone Number", request_contact=True)
    mail_btn = KeyboardButton("🔄 New Mail")

    reply_kb = ReplyKeyboardMarkup(
        [[contact_btn, mail_btn]],
        resize_keyboard=True
    )

    update.message.reply_text(
        "👇 Niche buttons use karo",
        reply_markup=reply_kb
    )


# 📞 Phone number receive
def get_contact(update, context):
    contact = update.message.contact
    phone = contact.phone_number
    name = contact.first_name
    user_id = contact.user_id

    # User reply
    update.message.reply_text(
        f"✅ Phone Number Received!\n\n"
        f"👤 Name: {name}\n"
        f"🆔 User ID: {user_id}\n"
        f"📞 Phone: {phone}\n\n"
        f"/email likho aur temporary email pao 📧"
    )

    # Admin notify
    context.bot.send_message(
        ADMIN_ID,
        f"📞 User Shared Phone Number\n\n"
        f"👤 Name: {name}\n"
        f"🆔 ID: {user_id}\n"
        f"📞 Phone: {phone}"
    )


# 📧 /email command
def email(update, context):
    if not is_joined(update, context):
        update.message.reply_text("❌ Pehle channel join karo")
        return

    try:
        r = requests.get(API_URL, timeout=10)
        data = r.json()
        mail = data.get("generated_email") or data.get("quick_email")

        if mail:
            update.message.reply_text(f"📧 Your Temp Email:\n\n{mail}")
        else:
            update.message.reply_text("❌ Email generate nahi hua")

    except:
        update.message.reply_text("⚠️ API error, baad me try karo")


# 🔄 New Mail Button
def new_mail_button(update, context):
    if update.message.text == "🔄 New Mail":
        try:
            r = requests.get(API_URL, timeout=10)
            data = r.json()
            mail = data.get("generated_email") or data.get("quick_email")

            if mail:
                update.message.reply_text(f"📧 Your New Temp Email:\n\n{mail}")
            else:
                update.message.reply_text("❌ Email generate nahi hua")

        except:
            update.message.reply_text("⚠️ API error, baad me try karo")


# 🚀 BOT START
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("email", email))
dp.add_handler(MessageHandler(Filters.contact, get_contact))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, new_mail_button))

print("🤖 Bot is running...")
updater.start_polling()
updater.idle()













