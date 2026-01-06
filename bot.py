from pyrogram import Client, filters
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

STORAGE_CHANNEL_ID = int(os.getenv("STORAGE_CHANNEL_ID"))

S1_480P = [252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276]
S1_720P = [279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303]
S1_1080P = [306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330]

app = Client(
    "anime_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@app.on_message(filters.command("start"))
async def start(client, message):
    if len(message.command) < 2:
        await message.reply(
            "Choose quality:\n"
            "👉 /start 480\n"
            "👉 /start 720\n"
            "👉 /start 1080"
        )
        return

    q = message.command[1]

    if q == "480":
        files = S1_480P
    elif q == "720":
        files = S1_720P
    elif q == "1080":
        files = S1_1080P
    else:
        await message.reply("❌ Invalid option")
        return

    for msg_id in files:
        await client.forward_messages(
            chat_id=message.chat.id,
            from_chat_id=STORAGE_CHANNEL_ID,
            message_ids=msg_id
        )

app.run()
