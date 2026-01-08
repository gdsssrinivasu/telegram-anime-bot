from pyrogram import Client, filters
from flask import Flask
import os
import threading

# =========================
# 🔐 ENV VARIABLES (RENDER)
# =========================
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
STORAGE_CHANNEL_ID = int(os.getenv("STORAGE_CHANNEL_ID"))  # must start with -100

# =========================
# 📦 EPISODE ID RANGES
# (range(start, end+1))
# =========================

# -------- AOT SEASON 1 --------
AOT_S1_480  = range(252, 277)
AOT_S1_720  = range(279, 304)
AOT_S1_1080 = range(306, 331)

# -------- AOT SEASON 2 --------
AOT_S2_480  = range(757, 769)
AOT_S2_720  = range(771, 783)
AOT_S2_1080 = range(785, 797)

# -------- AOT SEASON 3 --------
AOT_S3_480  = range(799, 821)
AOT_S3_720  = range(823, 845)
AOT_S3_1080 = range(847, 869)

# -------- AOT S4 PART 1 --------
AOT_S4P1_480  = range(871, 887)
AOT_S4P1_720  = range(889, 905)
AOT_S4P1_1080 = range(907, 923)

# -------- AOT S4 PART 2 --------
AOT_S4P2_480  = range(925, 937)
AOT_S4P2_720  = range(939, 951)
AOT_S4P2_1080 = range(953, 965)

# =========================
# 🗺️ COMMAND MAP
# =========================
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
    text = message.text or ""
    print("RAW MESSAGE:", text)

    parts = text.split(maxsplit=1)

    # 👉 Show menu
    if len(parts) == 1:
        await message.reply(
            "Attack on Titan\n\n"
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

    # 👉 Parse parameter
    q = parts[1].strip().lower()
    print("PARSED PARAM:", q)

    if q not in MAP:
        await message.reply(f"❌ Invalid option: `{q}`")
        return

    sent = 0
    for msg_id in MAP[q]:
        try:
            await client.forward_messages(
                chat_id=message.chat.id,
                from_chat_id=STORAGE_CHANNEL_ID,
                message_ids=msg_id
            )
            sent += 1
        except Exception as e:
            print(f"FORWARD ERROR (msg_id={msg_id}):", e)

    await message.reply(f"✅ Sent {sent} files")

def run_bot():
    bot.run()

# =========================
# 🌐 FLASK (RENDER FREE)
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Anime bot is running"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
