from pyrogram import Client, filters
import os
import threading
from flask import Flask

# =========================
# 🔐 ENV VARIABLES (RENDER)
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

MAP = {
    "aot_s1_480": AOT_S1_480,
    "aot_s1_720": AOT_S1_720,
    "aot_s1_1080": AOT_S1_1080,
}

# =========================
# 🤖 PYROGRAM BOT
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
            "Attack on Titan Season 1\n\n"
            "/start aot_s1_480\n"
            "/start aot_s1_720\n"
            "/start aot_s1_1080"
        )
        return

    q = message.command[1]
    if q not in MAP:
        await message.reply("❌ Invalid option")
        return

    for msg_id in MAP[q]:
        await client.forward_messages(
            chat_id=message.chat.id,
            from_chat_id=STORAGE_CHANNEL_ID,
            message_ids=msg_id
        )

def run_bot():
    bot.run()

# =========================
# 🌐 FLASK WEB SERVER
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
