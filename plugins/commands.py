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
    text_start = ("This bot searches Apps in F-Droid repository, "
                  "works only in inline mode\n\n"
                  "Currently supported repositories:\n"
                  "- [F-Droid.org](https://f-droid.org/), "
                  "search directly\n"
                  "- [IzzyOnDroid]"
                  "(https://apt.izzysoft.de/fdroid/), search with `!i`\n\n"
                  "[Source Code]"
                  "(https://github.com/dashezup/FDroidSearchBot)"
                  " | [Developer](https://t.me/dashezup)"
                  " | [Support Chat](https://t.me/ezupdev)")
    await message.reply(
        text_start,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Select Chat to Use in inline Mode",
                        switch_inline_query=""
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Search on F-Droid",
                        switch_inline_query_current_chat="",
                    ),
                    InlineKeyboardButton(
                        "Search on IzzyOnDroid",
                        switch_inline_query_current_chat="!i ",
                    )
                ]
            ]
        ),
        quote=True,
        disable_web_page_preview=True
    )
