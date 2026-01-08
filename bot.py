from pyrogram import Client, filters
from flask import Flask
import threading
import os

# =========================
# 🌐 FLASK KEEP-ALIVE (RENDER FREE FIX)
# =========================
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "Bot is running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()

# =========================
# 🔐 CREDENTIALS (PRODUCTION)
# =========================
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
STORAGE_CHANNEL_ID = int(os.getenv("STORAGE_CHANNEL_ID"))

# =========================
# 📦 EPISODE RANGES
# =========================
AOT_S1_480  = range(252, 277)
AOT_S1_720  = range(279, 304)
AOT_S1_1080 = range(306, 331)

AOT_S2_480  = range(757, 769)
AOT_S2_720  = range(771, 783)
AOT_S2_1080 = range(785, 797)

AOT_S3_480  = range(799, 821)
AOT_S3_720  = range(823, 845)
AOT_S3_1080 = range(847, 869)

AOT_S4P1_480  = range(871, 887)
AOT_S4P1_720  = range(889, 905)
AOT_S4P1_1080 = range(907, 923)

AOT_S4P2_480  = range(925, 937)
AOT_S4P2_720  = range(939, 951)
AOT_S4P2_1080 = range(953, 965)

# =========================
# 🤖 TELEGRAM BOT
# =========================
bot = Client(
    "anime_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@bot.on_message(filters.command("start"))
async def start(client, message):

    if len(message.command) < 2:
        await message.reply(
            "Choose:\n\n"
            "Season 1\n"
            "/start aot_s1_480\n"
            "/start aot_s1_720\n"
            "/start aot_s1_1080\n\n"
            "Season 2\n"
            "/start aot_s2_480\n"
            "/start aot_s2_720\n"
            "/start aot_s2_1080\n\n"
            "Season 3\n"
            "/start aot_s3_480\n"
            "/start aot_s3_720\n"
            "/start aot_s3_1080\n\n"
            "Season 4 Part 1\n"
            "/start aot_s4p1_480\n"
            "/start aot_s4p1_720\n"
            "/start aot_s4p1_1080\n\n"
            "Season 4 Part 2\n"
            "/start aot_s4p2_480\n"
            "/start aot_s4p2_720\n"
            "/start aot_s4p2_1080"
        )
        return

    MAP = {
        "aot_s1_480": AOT_S1_480,
        "aot_s1_720": AOT_S1_720,
        "aot_s1_1080": AOT_S1_1080,
        "aot_s2_480": AOT_S2_480,
        "aot_s2_720": AOT_S2_720,
        "aot_s2_1080": AOT_S2_1080,
        "aot_s3_480": AOT_S3_480,
        "aot_s3_720": AOT_S3_720,
        "aot_s3_1080": AOT_S3_1080,
        "aot_s4p1_480": AOT_S4P1_480,
        "aot_s4p1_720": AOT_S4P1_720,
        "aot_s4p1_1080": AOT_S4P1_1080,
        "aot_s4p2_480": AOT_S4P2_480,
        "aot_s4p2_720": AOT_S4P2_720,
        "aot_s4p2_1080": AOT_S4P2_1080,
    }

    key = message.command[1]
    if key not in MAP:
        await message.reply("❌ Invalid option")
        return

    for msg_id in MAP[key]:
        await client.forward_messages(
            chat_id=message.chat.id,
            from_chat_id=STORAGE_CHANNEL_ID,
            message_ids=msg_id
        )

bot.run()
