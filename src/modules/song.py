import os
import requests
import yt_dlp
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch
from src import app

@app.on_message(filters.command(["song", "vsong", "video", "music"]))
async def song(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    m = await message.reply_text("🔎")

    query = " ".join(message.command[1:])
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    audio_file = None
    thumb_name = None
    try:
        results = YoutubeSearch(query, max_results=5).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb_{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as ex:
        print(ex)
        return await m.edit_text(
            f"Failed to fetch track from YouTube.\n\n**Reason : {ex}"
        )

    await m.edit_text("Downloading song, please wait...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

        rep = f"**Title : [{title[:23]}]({link})\n**Duration : `{duration}`\n**Uploaded by : {app.me.mention}"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60

        try:
            visit_butt = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="YouTube",
                            url=link,
                        )
                    ]
                ]
            )
            await app.send_audio(
                chat_id=message.chat.id,
                audio=audio_file,
                caption=rep,
                thumb=thumb_name,
                title=title,
                duration=dur,
                reply_markup=visit_butt,
            )
        except Exception as e:
            print(e)
            start_butt = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Click Here",
                            url=f"https://t.me/{app.me.username}?start",
                        )
                    ]
                ]
            )
            return await m.edit_text(
                text="Click on the button below and start me for downloading songs.",
                reply_markup=start_butt,
            )
        await m.delete()
    except Exception as e:
        print(e)
        return await m.edit_text("Failed to upload audio on Telegram servers.")

    finally:
        try:
            if audio_file and os.path.exists(audio_file):
                os.remove(audio_file)
            if thumb_name and os.path.exists(thumb_name):
                os.remove(thumb_name)
        except Exception as ex:
            print(ex)
