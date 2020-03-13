"""Обработка действий обычных пользователей"""
from contextlib import suppress

from aiogram import types, exceptions

from backend import files, Broadcast
from consts import texts, others
from frontend.frontend_utils import keyboards as kb
from utils import db


async def menu(message: types.Message):
    await message.answer(texts.MENU, reply_markup=kb.START)


# region playlist

async def playlist_now(message: types.Message):
    if not (broadcast := Broadcast.now()):
        return await message.answer(texts.SONG_NO_NOW, reply_markup=kb.WHAT_PLAYING)

    playback = [i if i else r'¯\_(ツ)_/¯' for i in await broadcast.get_now()]
    await message.answer(texts.WHAT_PLAYING.format(*playback), reply_markup=kb.WHAT_PLAYING)


async def playlist_next(query: types.CallbackQuery):
    if not (broadcast := Broadcast.now()):
        return await query.message.answer(texts.CHOOSE_DAY, reply_markup=kb.playlist_choose_day())
    await query.message.answer(await _get_playlist_text(broadcast),
                               reply_markup=kb.playlist_choose_time(broadcast.day))


async def playlist_choose_day(query: types.CallbackQuery):
    with suppress(exceptions.MessageNotModified):
        await query.message.edit_text(texts.CHOOSE_DAY, reply_markup=kb.playlist_choose_day())


async def playlist_choose_time(query: types.CallbackQuery, day: int):
    with suppress(exceptions.MessageNotModified):
        await query.message.edit_text(texts.CHOOSE_TIME.format(others.WEEK_DAYS[day]),
                                      reply_markup=kb.playlist_choose_time(day))


async def playlist_show(query: types.CallbackQuery, broadcast: Broadcast):
    with suppress(exceptions.MessageNotModified):
        await query.message.edit_text(await _get_playlist_text(broadcast),
                                      reply_markup=kb.playlist_choose_time(broadcast.day))


# endregion

async def timetable(message: types.Message):
    text = 'Карантиновый режим \n'
    # for day_num, day_name in {0: 'Будни', 6: 'Воскресенье'}.items():
    #     text += f"{day_name} \n"
    day_num = 0
    for break_num, (start, stop) in others.BROADCAST_TIMES[day_num].items():
        text += f"   {start} - {stop}   {others.TIMES[break_num]} \n"

    # todo
    # text += "До ближайшего эфира ..."

    await message.answer(text)


async def help_change(query: types.CallbackQuery, key: str):
    with suppress(exceptions.MessageNotModified):
        await query.message.edit_text(texts.HELP[key], reply_markup=kb.CHOICE_HELP)


async def notify_switch(message: types.Message):
    status = await db.users.notification_get(message.from_user.id)
    await db.users.notification_set(message.from_user.id, not status)
    text = "Уведомления <b>включены</b> \n /notify - выключить" if status else \
        "Уведомления <b>выключены</b> \n /notify - включить"
    await message.answer(text)


async def add_in_db(message: types.Message):
    await db.users.add(message.chat.id)


#


async def _get_playlist_text(broadcast: Broadcast) -> str:
    if broadcast.is_now():
        playback = await broadcast.get_playlist_next()
        return '\n'.join([
            f"🕖<b>{track.time_start.strftime('%H:%M:%S')}</b> {track.title}"
            for track in playback[:10]
        ])
    else:
        name = f"<b>{broadcast.name}</b>\n"
        if not (playback := files.get_downloaded_tracks(broadcast.path)):
            return name + "❗️Еще ничего не заказали"

        text = name + '\n'.join([
            f"🕖<b>{i + 1}</b> {track.stem}"
            for i, track in enumerate(playback[:10])
        ])
        if len(playback) > 10:
            text += '\n<pre>   ...</pre>'
        return text
