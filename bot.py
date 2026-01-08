from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
STORAGE_CHANNEL_ID = int(os.getenv("STORAGE_CHANNEL_ID"))

S1_480P = [252,253,254]
S1_720P = [279,280,281]
S1_1080P = [306,307,308]

app = Client(
    "anime_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@app.on_message(filters.command("start"))
async def start(client, message):
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🎬 480p", callback_data="480")],
            [InlineKeyboardButton("🎬 720p", callback_data="720")],
            [InlineKeyboardButton("🎬 1080p", callback_data="1080")]
        ]
    )
    await message.reply("Choose quality:", reply_markup=buttons)

@app.on_callback_query()
async def callback(client, query):
    q = query.data

    if q == "480":
        files = S1_480P
    elif q == "720":
        files = S1_720P
    elif q == "1080":
        files = S1_1080P
    else:
        await query.answer("Invalid option")
        return

    await query.message.delete()

    for msg_id in files:
        await client.forward_messages(
            chat_id=query.message.chat.id,
            from_chat_id=STORAGE_CHANNEL_ID,
            message_ids=msg_id
        )

app.run()
