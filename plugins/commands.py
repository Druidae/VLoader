from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.keyboard import KeyboardAndText


@Client.on_message(
    filters.command("start") & filters.private,
)
async def start_command(_bot, m: Message):
    return await m.reply_text(
        KeyboardAndText.START_TEXT.format(m.from_user.first_name),
        reply_markup=KeyboardAndText.START_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
    )


@Client.on_message(
    filters.command("help") & filters.private,
)
async def help_command(_bot, m: Message):
    return await m.reply_text(
        KeyboardAndText.HELP_TEXT,
        reply_markup=KeyboardAndText.HELP_BUTTONS,
        disable_web_page_preview=True,
    )


@Client.on_message(
    filters.command("about") & filters.private,
)
async def about_command(_bot, m: Message):
    return await m.reply_text(
        KeyboardAndText.ABOUT_TEXT,
        reply_markup=KeyboardAndText.ABOUT_BUTTONS,
        disable_web_page_preview=True,
    )
