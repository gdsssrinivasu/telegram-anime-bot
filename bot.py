from pyrogram import Client, filters
import os
import asyncio

# =========================
# 🔁 MODE SWITCH
# =========================
LOCAL = False   # ❗ SET True only when using CMD locally

# =========================
# 🔐 CREDENTIALS
# =========================
if LOCAL:
    api_id = 39048142
    api_hash = "47574dc23e0733d0fee100d99723430f"
    bot_token = "8452766296:AAGCxTQTfrbGdW7nNxSDXiQ3rt20rZ22lGA"
    STORAGE_CHANNEL_ID = -1003432800289
else:
    api_id = int(os.getenv("API_ID"))
    api_hash = os.getenv("API_HASH")
    bot_token = os.getenv("BOT_TOKEN")
    STORAGE_CHANNEL_ID = int(os.getenv("STORAGE_CHANNEL_ID"))

# =========================
# 📦 EPISODE ID LISTS
# =========================
# Using list(range()) so we can loop safely

AOT_S1_480  = list(range(252, 277))
AOT_S1_720  = list(range(279, 304))
AOT_S1_1080 = list(range(306, 331))

AOT_S2_480  = list(range(757, 769))
AOT_S2_720  = list(range(771, 783))
AOT_S2_1080 = list(range(785, 797))

AOT_S3_480  = list(range(799, 821))
AOT_S3_720  = list(range(823, 845))
AOT_S3_1080 = list(range(847, 869))

AOT_S4P1_480  = list(range(871, 887))
AOT_S4P1_720  = list(range(889, 905))
AOT_S4P1_1080 = list(range(907, 923))

AOT_S4P2_480  = list(range(925, 937))
AOT_S4P2_720  = list(range(939, 951))
AOT_S4P2_1080 = list(range(953, 965))

# =========================
# 🤖 BOT INIT
# =========================
app = Client(
    "anime_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

# =========================
# ▶ START COMMAND
# =========================
@app.on_message(filters.command("start"))
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

    q = message.command[1]

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

    if q not in MAP:
        await message.reply("❌ Invalid option")
        return

    sent = 0
    failed = 0

    for msg_id in MAP[q]:
        try:
            await client.forward_messages(
                chat_id=message.chat.id,
                from_chat_id=STORAGE_CHANNEL_ID,
                message_ids=msg_id
            )
            sent += 1
            await asyncio.sleep(0.4)  # flood control
        except Exception:
            failed += 1
            continue

    await message.reply(
        f"✅ Done\n"
        f"Sent: {sent}\n"
        f"Skipped: {failed}"
    )

app.run()
