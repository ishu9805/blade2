import time
import asyncio
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)
from datetime import datetime

import speedtest
from pyrogram import Client, filters
from pyrogram.raw import functions

from config import CMD_HANDLER
from config import BOT_VER, BRANCH as brch
from BLADE import CMD_HELP, StartTime
from BLADE.helpers.basic import edit_or_reply
from BLADE.helpers.constants import WWW
from BLADE import app 
from BLADE.helpers.PyroHelpers import SpeedConvert
from BLADE.utils.tools import get_readable_time
from BLADE.modules.bot.inline import get_readable_time
from BLADE.helpers.adminHelpers import DEVS

from .help import *

modules = CMD_HELP

@Client.on_message(filters.command(["speed", "speedtest"], cmd) & filters.me)
async def speed_test(client: Client, message: Message):
    new_msg = await edit_or_reply(message, "`Running speed test . . .`")
    spd = speedtest.Speedtest()

    new_msg = await message.edit(
        f"`{new_msg.text}`\n" "`Getting best server based on ping . . .`"
    )
    spd.get_best_server()

    new_msg = await message.edit(f"`{new_msg.text}`\n" "`Testing download speed . . .`")
    spd.download()

    new_msg = await message.edit(f"`{new_msg.text}`\n" "`Testing upload speed . . .`")
    spd.upload()

    new_msg = await new_msg.edit(
        f"`{new_msg.text}`\n" "`Getting results and preparing formatting . . .`"
    )
    results = spd.results.dict()

    await message.edit(
        WWW.SpeedTest.format(
            start=results["timestamp"],
            ping=results["ping"],
            download=SpeedConvert(results["download"]),
            upload=SpeedConvert(results["upload"]),
            isp=results["client"]["isp"],
        )
    )




@Client.on_message(
    filters.command("cping", ["."]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command(["ping"], ".") & filters.me)
async def module_ping(client: Client, message: Message):
    cmd = message.command
    help_arg = ""
    bot_username = (await app.get_me()).username
    if len(cmd) > 1:
        help_arg = " ".join(cmd[1:])
    elif not message.reply_to_message and len(cmd) == 1:
        try:
            nice = await client.get_inline_bot_results(bot=bot_username, query="ping")
            await asyncio.gather(
                message.delete(),
                client.send_inline_bot_result(
                    message.chat.id, nice.query_id, nice.results[0].id
                ),
            )
        except BaseException as e:
            print(f"{e}")


@Client.on_message(filters.command("alive", cmd) & filters.me)
async def module_peler(client: Client, message: Message):
    cdm = message.command
    help_arg = ""
    bot_username = (await app.get_me()).username
    if len(cdm) > 1:
        help_arg = " ".join(cdm[1:])
    elif not message.reply_to_message and len(cdm) == 1:
        try:
            nice = await client.get_inline_bot_results(bot=bot_username, query="alive")
            await asyncio.gather(
                client.send_inline_bot_result(
                    message.chat.id, nice.query_id, nice.results[0].id),
            )
        except BaseException:
            pass


add_command_help(
    "•─╼⃝𖠁 ꜱᴘᴇᴇᴅᴛᴇꜱᴛ",
    [
        [
            f"speedtest `or` {cmd}speed",
            "Tᴏ ᴛᴇꜱᴛ ʏᴏᴜʀ ꜱᴇʀᴠᴇʀ ꜱᴘᴇᴇᴅ.",
        ],
    ],
)


add_command_help(
    "•─╼⃝𖠁 Pɪɴɢ",
    [
        ["ping", "Tᴏ Sʜᴏᴡ Yᴏᴜʀ Bᴏᴛ'ꜱ Pɪɴɢ."],
        ["pink", "Tᴏ Sʜᴏᴡ Yᴏᴜʀ Bᴏᴛ'ꜱ Pɪɴɢ ( Tʜᴇ ᴀɴɪᴍᴀᴛɪᴏɴ ɪꜱ ɪᴜꜱᴛ ᴅɪғғᴇʀᴇɴᴛ )."],
    ],
  )
