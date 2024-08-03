import time
import json
import asyncio
import logging

from pyrogram.types import Thumbnail
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from plugins.keyboard import KeyboardAndText
from plugins.functions.rand_text import random_char
from plugins.functions.display_progress import convert_to_human_bytes

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(filters.private & filters.regex(pattern=".*http.*"))
async def echo(bot, update):
    logger.info(update.from_user)
    url = update.text
    youtube_dl_username = None
    youtube_dl_password = None
    file_name = None

    if "youtu.be" in url:
        return await update.reply_text(
            "**Choose Download type**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Audio 🎵", callback_data="ytdl_audio"),
                        InlineKeyboardButton("Video 🎬", callback_data="ytdl_video"),
                    ]
                ]
            ),
            quote=True,
        )

    if "|" in url:
        url_parts = url.split("|")
        if len(url_parts) == 2:
            url = url_parts[0]
            file_name = url_parts[1]
        elif len(url_parts) == 4:
            url = url_parts[0]
            file_name = url_parts[1]
            youtube_dl_username = url_parts[2]
            youtube_dl_password = url_parts[3]
        else:
            for entity in update.entities:
                if entity.type == "text_link":
                    url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    length = entity.length
                    url = url[o: o + length]
        if url is not None:
            url = url.strip()
        if file_name is not None:
            file_name = file_name.strip()
        if youtube_dl_username is not None:
            youtube_dl_username = youtube_dl_username.strip()
        if youtube_dl_password is not None:
            youtube_dl_password = youtube_dl_password.strip()
        logger.info(url)
        logger.info(file_name)
    else:
        for entity in update.entities:
            if entity.type == "text_link":
                url = entity.url
            elif entity.type == "url":
                o = entity.offset
                length = entity.length
                url = url[o: o + length]
    if Config.HTTP_PROXY != "":
        command_to_exec = [
            "yt-dlp",
            "--no-warnings",
            "--allow-dynamic-mpd",
            "-j",
            url,
            "--proxy",
            Config.HTTP_PROXY,
        ]
    else:
        command_to_exec = ["yt-dlp", "--no-warnings", "--allow-dynamic-mpd", "-j", url]
    if youtube_dl_username is not None:
        command_to_exec.append("--username")
        command_to_exec.append(youtube_dl_username)
    if youtube_dl_password is not None:
        command_to_exec.append("--password")
        command_to_exec.append(youtube_dl_password)
    logger.info(command_to_exec)
    chk = await bot.send_message(
        chat_id=update.chat.id,
        text="Processing your request... ⌛",
        disable_web_page_preview=True,
        reply_to_message_id=update.id,
    )

    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    logger.info(e_response)
    t_response = stdout.decode().strip()
    if e_response and "nonnumeric port" not in e_response:
        error_message = e_response.replace(
            """
            please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version;
            see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output.
            """,
            "",
        )
        if "This video is only available for registered users." in error_message:
            error_message += KeyboardAndText.SET_CUSTOM_USERNAME_PASSWORD
        await chk.delete()

        time.sleep(40.5)
        await bot.send_message(
            chat_id=update.chat.id,
            text=KeyboardAndText.NO_VOID_FORMAT_FOUND.format(str(error_message)),
            reply_to_message_id=update.id,
            disable_web_page_preview=True,
        )
        return False
    if t_response:
        x_reponse = t_response
        if "\n" in x_reponse:
            x_reponse, _ = x_reponse.split("\n")
        response_json = json.loads(x_reponse)
        randem = random_char(5)
        save_ytdl_json_path = (
            Config.DOWNLOAD_LOCATION
            + "/"
            + str(update.from_user.id)
            + f"{randem}"
            + ".json"
        )
        with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
            json.dump(response_json, outfile, ensure_ascii=False)
        inline_keyboard = []
        duration = None
        if "duration" in response_json:
            duration = response_json["duration"]
        if "formats" in response_json:
            for formats in response_json["formats"]:
                format_id = formats.get("format_id")
                format_string = formats.get("format_note")
                if format_string is None:
                    format_string = formats.get("format")
                if "DASH" in format_string.upper():
                    continue

                format_ext = formats.get("ext")

                if formats.get("filesize"):
                    size = formats["filesize"]
                elif formats.get("filesize_approx"):
                    size = formats["filesize_approx"]
                else:
                    size = 0

                cb_string_video = f"video |{format_id}|{format_ext}|{randem}"

                if format_string is not None and not ("audio only" in format_string) and format_ext == "webm":
                    video_bottom = [
                        InlineKeyboardButton(
                            "🎬 "
                            + format_string
                            + " "
                            + format_ext
                            + " "
                            + convert_to_human_bytes(size)
                            + " ",
                            callback_data=cb_string_video.encode("UTF-8"),
                        )
                    ]
                try:
                    inline_keyboard.append(video_bottom)
                    del video_bottom
                except UnboundLocalError:
                    continue
            if duration is not None:
                cb_string_64 = "{}|{}|{}|{}".format("audio", "64k", "mp3", randem)
                cb_string_128 = "{}|{}|{}|{}".format("audio", "128k", "mp3", randem)
                cb_string = "{}|{}|{}|{}".format("audio", "320k", "mp3", randem)
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(
                            "🎼 ᴍᴘ𝟹 " + "(" + "64 ᴋʙᴘs" + ")",
                            callback_data=cb_string_64.encode("UTF-8"),
                        ),
                        InlineKeyboardButton(
                            "🎼 ᴍᴘ𝟹 " + "(" + "128 ᴋʙᴘs" + ")",
                            callback_data=cb_string_128.encode("UTF-8"),
                        ),
                    ]
                )
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(
                            "🎼 ᴍᴘ𝟹 " + "(" + "320 ᴋʙᴘs" + ")",
                            callback_data=cb_string.encode("UTF-8"),
                        )
                    ]
                )
                inline_keyboard.append(
                    [InlineKeyboardButton("⛔ ᴄʟᴏsᴇ", callback_data="close")]
                )
        else:
            format_id = response_json["format_id"]
            format_ext = response_json["ext"]
            cb_string_video = "{}|{}|{}|{}".format(
                "video", format_id, format_ext, randem
            )
            inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        "🎬 Video", callback_data=cb_string_video.encode("UTF-8")
                    )
                ]
            )
            cb_string_file = "{}={}={}".format("file", format_id, format_ext)
            inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        "📁 Document", callback_data=cb_string_file.encode("UTF-8")
                    )
                ]
            )
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await chk.delete()

        await bot.send_message(
            chat_id=update.chat.id,
            text=KeyboardAndText.FORMAT_SELECTION.format(Thumbnail)
                 + "\n"
                 + KeyboardAndText.SET_CUSTOM_USERNAME_PASSWORD,
            reply_markup=reply_markup,
            reply_to_message_id=update.id,
        )
    else:
        # fallback for nonnumeric port a.k.a seedbox.io
        inline_keyboard = []
        cb_string_video = "{}={}={}".format("video", "OFL", "ENON")
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    "🎬 ᴍᴇᴅɪᴀ", callback_data=cb_string_video.encode("UTF-8")
                )
            ]
        )
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await chk.delete(True)

        await bot.send_message(
            chat_id=update.chat.id,
            text=KeyboardAndText.FORMAT_SELECTION,
            reply_markup=reply_markup,
            reply_to_message_id=update.id,
        )
