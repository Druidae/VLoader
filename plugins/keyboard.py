from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardAndText:
    START_TEXT = """
Hi {}

I am VLoader Bot
"""

    HELP_TEXT = """

# Send me the file links.

# Select the desired option.

# Then be relaxed your file will be uploaded soon..
"""

    ABOUT_TEXT = """
<b>♻️ My Name</b> : VLoader Bot

<b>📑 Language :</b> <a href="https://www.python.org/">Python 3.11.9</a>

<b>🇵🇲 Framework :</b> <a href="https://docs.pyrogram.org/">Pyrogram 2.0.106</a>

<b>👲 Developer :</b> <a href="https://t.me/koraki">@koraki</a>

"""

    FORMAT_SELECTION = "Now Select the desired formats"

    SET_CUSTOM_USERNAME_PASSWORD = """"""

    DOWNLOAD_START = "Trying to Download ⌛\n\n <i>{} </i>"

    UPLOAD_START = "\n📤 Uploading Please Wait "

    RCHD_TG_API_LIMIT = ("Downloaded in {} seconds.\nDetected File Size: {}\nSorry. But, I cannot upload files greater "
                         "than 2GB due to Telegram API limitations.")

    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = (
        "Tʜᴀɴᴋs fᴏʀ usɪɴɢ mᴇ\n\nDᴏᴡɴʟᴏᴀᴅᴇᴅ ɪɴ {} sᴇᴄᴏɴᴅs\n\nUᴘʟᴏᴀᴅᴇᴅ ɪɴ {} sᴇᴄᴏɴᴅs"
    )

    CUSTOM_CAPTION_UL_FILE = ""

    NO_VOID_FORMAT_FOUND = "ERROR... <code>{}</code>"

    FREE_USER_LIMIT_Q_SZE = "Cannot Process, Time OUT..."

    SLOW_URL_DECED = """
        Gosh that seems to be a very slow URL. Since you were screwing my home,
        I am in no mood to download this file. Meanwhile, why don't you try this:==> https://shrtz.me/PtsVnf6
        and get me a fast URL so that I can upload to Telegram, without me slowing down for other users."""

    START_BUTTONS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("❓ Help", callback_data="help"),
                InlineKeyboardButton("🦊 About", callback_data="about"),
            ],
            [InlineKeyboardButton("📛 Close", callback_data="close")],
        ]
    )
    HELP_BUTTONS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🏠 Home", callback_data="home"),
                InlineKeyboardButton("🦊 About", callback_data="about"),
            ],
            [InlineKeyboardButton("📛 Close", callback_data="close")],
        ]
    )
    ABOUT_BUTTONS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🏠 Home", callback_data="home"),
                InlineKeyboardButton("❓ Help", callback_data="help"),
            ],
            [InlineKeyboardButton("📛 Close", callback_data="close")],
        ]
    )
    BUTTONS = InlineKeyboardMarkup(
        [[InlineKeyboardButton("📛 Close", callback_data="close")]]
    )

