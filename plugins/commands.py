"""Commands"""
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.text
                   & filters.private
                   & filters.incoming
                   & filters.command("start")
                   & ~filters.edited)
async def command_start(_, message: Message):
    """/start"""
    text_start = ("This bot searches Apps in F-Droid.org repo, "
                  "works only in inline mode.\n\n"
                  "**Source Code**: "
                  "[FDroidSearchBot]"
                  "(https://github.com/dashezup/FDroidSearchBot)\n"
                  "**Developer**: [Dash Eclipse](https://t.me/dashezup)")
    await message.reply(
        text_start,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Search in inline mode",
                        switch_inline_query=""
                    )
                ]
            ]
        ),
        quote=True,
        disable_web_page_preview=True
    )
