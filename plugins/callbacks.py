"""Module for handling Pyrogram callback queries"""

import logging
from pyrogram import Client
from plugins.download_script import youtube_dl_call_back
from plugins.keyboard import KeyboardAndText

# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@Client.on_callback_query()
async def button(bot, update):
    if update.data == "home":
        await update.message.edit(
            text=KeyboardAndText.START_TEXT.format(update.from_user.mention),
            reply_markup=KeyboardAndText.START_BUTTONS,
        )
    elif update.data == "help":
        await update.message.edit(
            text=KeyboardAndText.HELP_TEXT,
            reply_markup=KeyboardAndText.HELP_BUTTONS,
        )
    elif update.data == "about":
        await update.message.edit(
            text=KeyboardAndText.ABOUT_TEXT,
            reply_markup=KeyboardAndText.ABOUT_BUTTONS,
        )
    elif "close" in update.data:
        await update.message.delete(True)
    elif "|" in update.data or "=" in update.data:
        await youtube_dl_call_back(bot, update)
    else:
        await update.message.delete()
