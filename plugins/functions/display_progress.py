import math
import time
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


async def progress_for_pyrogram(current, total, ud_type, message, start):
    """
    Display progress for a Pyrogram file upload or download.

    Parameters:
    - current (int): Current progress value.
    - total (int): Total value (completion point).
    - ud_type (str): Type of upload/download (e.g., "Uploading", "Downloading").
    - message: The Pyrogram message to edit.
    - start: The start time of the operation.

    Returns:
    None
    """
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        estimated_total_time = time_formatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \nP: {2}%\n".format(
            "".join(["◾" for _ in range(math.floor(percentage / 5))]),
            "".join(["◽" for _ in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2),
        )

        tmp = progress + "{0} of {1}\n\nSpeed: {2}/s\n\nETA: {3}\n\n".format(
            convert_to_human_bytes(current),
            convert_to_human_bytes(total),
            convert_to_human_bytes(speed),
            estimated_total_time if estimated_total_time != "" else "0 s",
        )
        try:
            await message.edit(text=f"{ud_type}\n {tmp}")
        except Exception as e:
            logger.info("Error %s", e)
            return


SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]


def convert_to_human_bytes(size):
    """
    Convert size to human-readable format.

    Parameters:
    - size (int): Size in bytes.

    Returns:
    str: Human-readable size.
    """
    if not size:
        return ""
    power = 2**10
    n = 0
    bytes_metrics = {0: " ", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        n += 1
    return f"{str(round(size, 2))} {bytes_metrics[n]}B"


def time_formatter(milliseconds: int) -> str:
    """
    Format time in milliseconds to a human-readable string.

    Parameters:
    - milliseconds (int): Time in milliseconds.

    Returns:
    str: Formatted time string.
    """
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)}d, " if days else "")
        + (f"{str(hours)}h, " if hours else "")
        + (f"{str(minutes)}m, " if minutes else "")
        + (f"{str(seconds)}s, " if seconds else "")
        + (f"{str(milliseconds)}ms, " if milliseconds else "")
    )

    return tmp[:-2]
